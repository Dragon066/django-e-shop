from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form for creating a new product or editing existing one.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "quantity",
            "picture",
            "available",
        ]
