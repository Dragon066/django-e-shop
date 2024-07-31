from catalog.models import Product
from django import forms


class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")
