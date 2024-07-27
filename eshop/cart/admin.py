from django.contrib import admin
from .models import Cart
from user.admin import admin_site

admin_site.register(Cart)
