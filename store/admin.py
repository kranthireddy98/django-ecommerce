from django.contrib import admin

from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}#to populate a field automatically based on previous field
    list_display = ('product_name','price','stock','category')
admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)#to make field editable in the table view directly
    list_filter = ('product','variation_category','variation_value')# to make table view to filter based on the given values in the tuple
admin.site.register(Variation,VariationAdmin)