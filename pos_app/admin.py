from django.contrib import admin
from .models import Product, Order, OrderDetail,Counter,PaymentMethod

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'product_name', 'unit_qty', 'qty_in_ltr', 'price')
    search_fields = ('product_code', 'product_name')

admin.site.register(Product, ProductAdmin)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline]

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_code', 'product_name', 'qty', 'price')


admin.site.register(Counter)
admin.site.register(PaymentMethod)
