from django.contrib import admin

from shop.models import Cart, CartItem, Category, Product

admin.site.register([Product, Category, Cart, CartItem])
