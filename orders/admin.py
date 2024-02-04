from django.contrib import admin

# Register your models here.
from .models import Payment,Order,OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['Payment','user','product','quantity','product_price','order']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','city','order_total','tax','status','is_ordered']

    list_filter = ['status','is_ordered']

    search_fields = ['order_number','full_name','phone','email']

    list_per_page = 20

    inlines = [OrderProductInline]
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)

admin.site.register(OrderProduct)
