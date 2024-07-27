from django import forms
from .models import Order, OrderDetails


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'address']
