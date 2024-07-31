from django import forms
from catalog.models import Product


class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")
