from django.shortcuts import get_object_or_404, redirect, render
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from category.models import Category
from django.db.models import Q
from django.contrib import messages,auth
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, ReviewRating, Variation
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.


def store(request,category_slug=None):
    products= None
    product_count = 0 
    if category_slug != None:
        categories= get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(is_avialable=True,category=categories)
        paginator = Paginator(products,3)
        page  = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_avialable=True).order_by('id')
        paginator = Paginator(products,3)
        page  = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    categories = Category.objects.all()
    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'categories' : categories
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    product= get_object_or_404(Product,slug=product_slug,category__slug=category_slug)
    in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product=product).exists()
    color   = Variation.objects.filter(product=product,is_active=True,variation_category='color')
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct =None
    else:
        orderproduct =None
    reviews = ReviewRating.objects.filter(product_id =product.id,status=True )

    context = {
        'product' : product,
        'in_cart' : in_cart,
        'colors'   : color,
        'reviews' : reviews,
        'orderproduct' : orderproduct
    }
    return render(request,'store/product_detail.html',context)


def search(request):
    
    if 'searchKeyword' in request.GET:
        keyword = request.GET['searchKeyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains =keyword))
            product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count
    }
    #print(context)
    return render(request,'store/store.html',context)


def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try :
            reviews = ReviewRating.objects.get(user__id = request.user.id,product__id = product_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you! Your review has been submitted.')
                return redirect(url)

