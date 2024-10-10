from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import CustomUser
from ecommerce.models import Product, Category, CartItem, ProductVariation, Cart
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.

def _get_or_create_session_id(request):
    session = request.session.session_key

    if not session:
        session = request.session.create()

    return session


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
    in_cart = CartItem.objects.filter(user__username='dario', product=product).exists()
    # in_cart = Cart.objects.filter(user__username='dario', product=product).count()

    context = {
        'product': product,
        'in_cart': in_cart
    }

    return render(request, 'store/product_detail.html', context)


def cart(request, total_price=0, total_quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_get_or_create_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total_price += cart_item.sub_total()
            total_quantity += cart_item.quantity

        tax = (total_price * 0.02)
        grand_total = total_price + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total
    }

    # print(context['cart_products'])

    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    if current_user.is_authenticated:
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

        is_cart_product_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_product_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_items:
                existing_variations = item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                user=current_user,
                product=product,
                quantity=1
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

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

    # User not authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id=_get_or_create_session_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_get_or_create_session_id(request)
            )
            cart.save()

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

        is_cart_product_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_product_exists:
            # cart = Cart.objects.filter(product=product, user=user)
            # cart.quantity += 1
            cart_items = CartItem.objects.filter(product=product, cart=cart)
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
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                print(item)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()


        else:
            cart = CartItem.objects.create(
                cart=cart,
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


def remove_cartItem_from_cart(request, product_id, cart_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id, id=cart_id)
        else:
            cart = Cart.objects.get(cart_id=_get_or_create_session_id(request))
            cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id, id=cart_id)
        cart_item.delete()
    except:
        pass

    return redirect('cart')


def decrese_quantity_from_cart_product(request, product_id, cart_id):
    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id, id=cart_id)
        else:
            cart = Cart.objects.get(cart_id=_get_or_create_session_id(request))
            cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id, id=cart_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
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


@login_required(login_url='login')
def checkout(request, tax=0, grand_total=0, cart_items=None):
    total_price = 0
    total_quantity = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_get_or_create_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            total_price += cart_item.sub_total()
            total_quantity += cart_item.quantity

        tax = (total_price * 0.02)
        grand_total = total_price + tax
    except:
        pass

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)
