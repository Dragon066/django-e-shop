from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Order form for user to fill in their details.
    """

    class Meta:
        model = Order
        fields = ["phone", "address"]
