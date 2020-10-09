from django.contrib import admin
from .models import Order, OrderItem, Address

admin.site.register(Address)

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ('product',)

# class OrderAddressInline(admin.TabularInline):
#     model = Address
#     raw_id_fields = ['address_detail']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]
    readonly_fields = ('customer', 'paid',)         
    # inlines = [OrderAddressInline]                    
