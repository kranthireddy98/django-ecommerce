from django.shortcuts import get_object_or_404, render
from carts.models import CartItem
from carts.views import _cart_id

from category.models import Category

from .models import Product

# Create your views here.


def store(request,category_slug=None):
    products= None
    product_count = 0 
    if category_slug != None:
        categories= get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(is_avialable=True,category=categories)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_avialable=True).order_by('id')
        product_count = products.count()
    categories = Category.objects.all()
    context = {
        'products' : products,
        'product_count' : product_count,
        'categories' : categories
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    product= get_object_or_404(Product,slug=product_slug,category__slug=category_slug)
    in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product=product).exists()
    
    context = {
        'product' : product,
        'in_cart' : in_cart,
    }
    return render(request,'store/product_detail.html',context)