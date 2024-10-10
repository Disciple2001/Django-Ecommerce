from ecommerce.models import Category, CartItem, Cart
from ecommerce.views import _get_or_create_session_id


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def get_cart_products_quantity(request):
    total_quantity = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_get_or_create_session_id(request))

            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                total_quantity += cart_item.quantity

        except Cart.DoesNotExist:
            total_quantity = 0

        return dict(total_quantity=total_quantity)
