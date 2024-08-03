from catalog.models import Product
from django.core.validators import RegexValidator
from django.db import models
from user.models import User


class Order(models.Model):
    """
    Model representing an order instance.
    Doesn't contain a list of products.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая сумма"
    )

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message='Введите телефон в виде "+1234567890", не более 15 цифр.',
    )

    phone = models.CharField(
        max_length=15, validators=[phone_regex], verbose_name="Телефон"
    )
    address = models.CharField(max_length=255, verbose_name="Адрес")

    class Meta:
        ordering = ["-created_at"]


class OrderDetails(models.Model):
    """
    Model representing a product in some order.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Заказ #"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("Ordered", "Заказан"),
            ("InProcess", "В обработке"),
            ("InDelivery", "Доставляется"),
            ("Completed", "Завершён"),
        ],
        default="Ordered",
        verbose_name="Статус",
    )
