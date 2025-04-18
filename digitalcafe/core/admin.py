from django.contrib import admin
from .models import Product, CartItem, Transaction, LineItem

# Register your models here.
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Transaction)
admin.site.register(LineItem)