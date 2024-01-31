from carts.views import _cart_id
from .models import CartItem,Cart


def cart_count(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            #cart = CartItem.objects.get(cart__cart_id = _cart_id(request))
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for items in cart_items:
                count += items.quantity
        except Cart.DoesNotExist:
            count = 0
    
        #print(count)
        return dict(cart_count = count)