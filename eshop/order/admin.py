from django.contrib import admin
from .models import Order, OrderDetails
from user.admin import admin_site

admin_site.register(Order)
admin_site.register(OrderDetails)
