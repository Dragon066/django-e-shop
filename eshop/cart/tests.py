from catalog.models import Product
from django.test import TestCase
from django.urls import reverse
from user.jwt import get_access_token
from user.models import User

from .models import Cart


class CartLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="test1@user.com",
            first_name="test1",
            last_name="user",
            password="123",
        )

        Product.objects.create(
            name="TestProduct",
            description="Test",
            quantity=10,
            price=1,
            owner=User.objects.get(pk=1),
        )

    def test_login_required(self):
        response = self.client.get(reverse("cart:cart"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/cart/")

        response = self.client.get(
            reverse("cart:cart_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/cart/add/1")

        response = self.client.post(
            reverse("cart:cart_delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/cart/delete/1")

    def test_cart(self):
        user = User.objects.get(pk=1)
        product = Product.objects.get(pk=1)

        self.client.cookies["jwt-access"] = get_access_token(user)

        response = self.client.get(reverse("cart:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина")

        response = self.client.get(
            reverse("cart:cart_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestProduct")

        Cart.objects.create(
            user=user,
            product=product,
            quantity=1,
        )

        response = self.client.post(
            reverse("cart:cart_delete", kwargs={"pk": 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cart:cart"))
