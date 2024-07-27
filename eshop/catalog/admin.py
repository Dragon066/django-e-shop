from django.contrib import admin
from .models import Product, ProductCategory
from user.admin import admin_site

admin_site.register(ProductCategory)
admin_site.register(Product)
