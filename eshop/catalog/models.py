from django.db import models
from django.urls import reverse
from user.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Наименование")
    description = models.TextField(default=None, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    available = models.BooleanField(default=True, verbose_name="Статус")
    picture = models.ImageField(default="no-photo.jpg", verbose_name="Фото")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец"
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.id])

    def __str__(self):
        return self.name
