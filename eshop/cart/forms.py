from django import forms


class CartForm(forms.Form):
    """
    Create form for adding products to the cart.

    Requires only quantity field.
    """

    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")
