from ecommerce.models import Category, Cart


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def get_cart_products_quantity(request):
    if 'admin' in request.path:
        return {}
    else:
        cart_products = Cart.objects.filter(user__username='dario')
        total_quantity = 0

        for cart_product in cart_products:
            total_quantity += cart_product.product.quantity

        return dict(total_quantity=total_quantity)

