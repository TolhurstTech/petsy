from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    list_display = ('name', 'price', 'stock', 'sold', 'created_on')
    search_fields = ['name', 'content']
    list_filter = ('draft', 'created_on', 'sold',)
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('content',)

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(ShippingAddress)

