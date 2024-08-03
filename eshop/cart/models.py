from catalog.models import Product
from django.db import models
from user.models import User


class Cart(models.Model):
    """
    Model with a list of products in each user's carts.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return self.product.name
