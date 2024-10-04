from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import CustomUser
from ecommerce.models import Product, Category, Cart, ProductVariation
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.


def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
        # categories = Category.objects.all()

    context = {
        'products': paged_products,
        'products_count': products_count,
        # 'categories': categories
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = Cart.objects.filter(user__username='dario', product=product).exists()
    # in_cart = Cart.objects.filter(user__username='dario', product=product).count()

    context = {
        'product': product,
        'in_cart': in_cart
    }

    return render(request, 'store/product_detail.html', context)


def cart(request):
    cart_products = Cart.objects.filter(user__username='dario')
    total_price = 0
    total_quantity = 0

    for cart_product in cart_products:
        total_price += cart_product.sub_total()
        total_quantity += cart_product.quantity

    tax = (total_price * 0.02)
    grand_total = total_price + tax

    context = {
        'cart_products': cart_products,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total
    }

    # print(context['cart_products'])

    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = get_object_or_404(CustomUser, username='dario')

    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = ProductVariation.objects.get(product=product, variation_category__iexact=key,
                                                         variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    is_cart_product_exist = Cart.objects.filter(product=product, user=user).exists()

    if is_cart_product_exist:
        # cart = Cart.objects.filter(product=product, user=user)
        # cart.quantity += 1
        cart_items = Cart.objects.filter(product=product, user=user)
        # print(cart_items)

        ex_var_list = []
        id = []

        for item in cart_items:
            existing_variations = item.variations.all()
            # print(existing_variations)
            ex_var_list.append(list(existing_variations))
            id.append(item.id)

        # print(ex_var_list)
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = Cart.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = Cart.objects.create(product=product, quantity=1, user=user)
            print(item)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()


    else:
        cart = Cart.objects.create(
            user=user,
            product=product,
            quantity=1
        )
        if len(product_variation) > 0:
            cart.variations.clear()
            cart.variations.add(*product_variation)
        cart.save()

    # user = get_object_or_404(CustomUser, username='dario')
    #
    # cart, created = Cart.objects.get_or_create(
    #     user=user,
    #     product=product,
    # )
    #
    # if not created:
    #     cart.quantity += 1
    #     cart.save()

    return redirect('cart')


def remove_product_from_cart(request, product_id, cart_id):
    cart_product = get_object_or_404(Cart, user__username='dario', product__id=product_id, id=cart_id)
    cart_product.delete()
    return redirect('cart')


def decrese_quantity_from_cart_product(request, product_id, cart_id):
    try:
        cart_product = get_object_or_404(Cart, user__username='dario', product__id=product_id, id=cart_id)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        else:
            cart_product.delete()
    except:
        pass
    return redirect('cart')


def search(request):
    products = None
    products_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_at')
            products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count,
    }

    return render(request, 'store/store.html', context)
