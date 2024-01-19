from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem

from store.models import Product

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item= CartItem.objects.create(
            product=product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()


    return redirect('cart')



def cart(request,total=0,quantity=0,cart_items=None):
    try :

        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            cart_item.product.brand = cart_item.product.product_name.split('-')[0]
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    tax = (2*total)/100
    grand_total = total+tax
    context = {    
        'quantity' : quantity,
        'total'   : total,
        'cart_items' : cart_items,
        'tax' : tax,
       'grand_total' : grand_total
    }
    #print(context)
    return render(request,'store/cart.html',context)

def remove_item(request,product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = Product.objects.get(id=product_id) 
        cart_item = CartItem.objects.get(cart=cart,product=product)
        cart_item.delete()

    except Cart.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart(request,product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = Product.objects.get(id=product_id) 
        cart_item = CartItem.objects.get(cart=cart,product=product)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart')
        