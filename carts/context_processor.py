from carts.views import _cart_id
from .models import CartItem,Cart


def cart_count(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_items = CartItem.objects.filter(cart__cart_id = _cart_id(request))
            for items in cart_items:
                count += items.quantity
        except Cart.DoesNotExist:
            count = 0
    
        #print(count)
        return dict(cart_count = count)