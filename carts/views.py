from django.http import HttpResponse
from django.shortcuts import  redirect, render
from .models import Cart, CartItem

from store.models import Product, Variation
from django.contrib.auth.decorators import login_required
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart

 
def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for each in request.POST:
                key = each
                value = request.POST[key]
                try :
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except :
                    pass
        #print(product_variation)
    

        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product,user=current_user)

            existing_variations_list = []
            id = []
            for cart_item in cart_items:

                existing_variations_list.append(list(cart_item.variations.all()))
                id.append(cart_item.id)
            #print(existing_variations_list)
        
            if product_variation in existing_variations_list:
                #increase cart item quantity
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                
                item.save()
            else:
                #create new combination of size and color
                item = CartItem.objects.create(
                    product=product,quantity=1,user=current_user
                )
                if len(product_variation) > 0 :
                        item.variations.clear()
                        item.variations.add(*product_variation)
                
                item.save()

                
        else:
            cart_item= CartItem.objects.create(
                product=product,
                quantity = 1,
                user = current_user
            )
            if len(product_variation) > 0 :
                for item in product_variation:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
        
            cart_item.save()


        return redirect('cart')
    else:
            
        product_variation = []
        if request.method == 'POST':
            for each in request.POST:
                key = each
                value = request.POST[key]
                try :
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except :
                    pass
        #print(product_variation)
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            

            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product,cart=cart)

            existing_variations_list = []
            id = []
            for cart_item in cart_items:

                existing_variations_list.append(list(cart_item.variations.all()))
                id.append(cart_item.id)
            #print(existing_variations_list)
        
            if product_variation in existing_variations_list:
                #increase cart item quantity
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                
                item.save()
            else:
                #create new combination of size and color
                item = CartItem.objects.create(
                    product=product,quantity=1,cart=cart
                )
                if len(product_variation) > 0 :
                        item.variations.clear()
                        item.variations.add(*product_variation)
                
                item.save()

                
        else:
            cart_item= CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0 :
                for item in product_variation:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
        
            cart_item.save()


        return redirect('cart')



def cart(request,total=0,quantity=0,cart_items=None):
    try :
      
        
        if request.user.is_authenticated:
            
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
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

def remove_item(request,product_id,cart_item_id):

    try:
       
        product = Product.objects.get(id=product_id) 
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user,product=product,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        cart_item.delete()

    except Cart.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    product = Product.objects.get(id=product_id) 
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user,product=product,id=cart_item_id)
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            
            cart_item = CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart')

@login_required(login_url='login')     
def checkout(request,total=0,quantity=0,cart_items=None):
    try :
        if request.user.is_authenticated:
            
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:

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
    return render(request,'store/checkout.html',context)