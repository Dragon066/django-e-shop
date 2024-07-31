from django.contrib import admin
from user.admin import admin_site

from .models import Product, ProductCategory

admin_site.register(ProductCategory)
admin_site.register(Product)
