from django.contrib import admin
from user.admin import admin_site

from .models import Order, OrderDetails

admin_site.register(Order)
admin_site.register(OrderDetails)
