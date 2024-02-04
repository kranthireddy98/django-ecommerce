import datetime
from django.core.mail import EmailMessage
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import CartItem
from orders.forms import OrderForm
from store.models import Product
from .models import Order, OrderProduct, Payment

def place_order(request):
    current_user = request.user

    #If the cart count is less than or equal to 0 , then redirect bck to shop
    cart_item = CartItem.objects.filter(user=current_user)
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect('store')
    
    if request.method == 'POST' :
        form = OrderForm(request.POST)

        grand_total = 0
        total = 0
        quantity = 0
        tax = 0
        for item in cart_item:
            total+=(item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2*total)/100
        grand_total = total+tax  
        
        if form.is_valid():
            
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.adress_line_1 = form.cleaned_data['adress_line_1']
            data.adress_line_2 = form.cleaned_data['adress_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)

            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order' : order,
                'cart_items' : cart_item,
                'total':total,
                'tax':tax,
                'grand_total':grand_total
            }
            print(order)
            return render(request,'orders/payments.html',context)
        else:
          
            return redirect('checkout')

def payments(request):
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],


    )

    payment.save()

    order.payment=payment
    order.is_ordered=True
    order.save()

    #move the cart items to orderproduct table
    cart_items = CartItem.objects.filter(user=request.user)
    

    for item in cart_items:
        orderproduct = OrderProduct()

        orderproduct.order_id = order.id
        orderproduct.Payment  = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)

        product_variation = cart_item.variations.all()

        orderproduct = OrderProduct.objects.get(id=orderproduct.id)

        orderproduct.variation.set(product_variation)

        orderproduct.save()




    #reduce the quantitiy of the sold products

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear cart
    CartItem.objects.filter(user=request.user).delete()
    
    #order Recieved mail to customer

    mail_subject = 'Thank you for your order!'
    message      = render_to_string('orders/order_recieved_email.html',{
                'user': request.user
            })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()


    data = {
        'order_number' : order.order_number,
        'transID'   : payment.payment_id,


    }

    return JsonResponse(data)

    return render(request,'orders/payments.html')
                         
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id = transID)
        subtotal = 0

        for i in ordered_products:
            subtotal+= i.product_price * i.quantity
        context = {
            'order' : order,
            'ordered_products' : ordered_products,
            'transID' : payment.payment_id,
            'payment' : payment,
            'subtotal' : subtotal
        }
        return render(request,'orders/order_complete.html',context)
    except (Order.DoesNotExist,Payment.DoesNotExist):
        return redirect('home')