from django.contrib import admin
from user.admin import admin_site

from .models import Cart

admin_site.register(Cart)
