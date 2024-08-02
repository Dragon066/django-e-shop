from catalog.models import Product
from django.test import RequestFactory, TestCase
from django.urls import reverse
from user.jwt import get_access_token
from user.models import User

from .forms import CartForm
from .models import Cart
from .views import CartFormView


class CartLoginRequiredTest(TestCase):
    def test_login_required_cart(self):
        response = self.client.get(reverse("cart:cart"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/cart/")

    def test_login_required_cart_detail(self):
        response = self.client.get(
            reverse("cart:cart_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/cart/add/1")

    def test_login_required_cart_delete(self):
        response = self.client.post(
            reverse("cart:cart_delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/cart/delete/1")


class CartViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email="test1@user.com",
            first_name="test1",
            last_name="user",
            password="123",
        )

        product = Product.objects.create(
            name="TestProduct",
            description="Test",
            quantity=10,
            price=1,
            owner=User.objects.get(pk=1),
        )

        Cart.objects.create(
            user=user,
            product=product,
            quantity=1,
        )

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)
        self.client.cookies["jwt-access"] = get_access_token(self.user)

    def test_cart_get(self):
        response = self.client.get(reverse("cart:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина")

    def test_cart_detail_get(self):
        response = self.client.get(
            reverse("cart:cart_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestProduct")

    def test_cart_delete(self):
        response = self.client.post(
            reverse("cart:cart_delete", kwargs={"pk": 1})
        )

        self.assertFalse(Cart.objects.all())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cart:cart"))

    def test_cart_add(self):
        factory = RequestFactory()
        data = {"product_id": 1, "quantity": 5}

        request = factory.post(reverse("cart:cart"), data=data)
        request.user = self.user

        response = CartFormView.as_view()(request)

        self.assertEqual(
            Cart.objects.get(user=self.user, product=self.product).quantity, 5
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:product_list"))


class CartFormTest(TestCase):
    def test_valid_form(self):
        form = CartForm(data={"quantity": 1})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CartForm(data={"quantity": 0})
        self.assertFalse(form.is_valid())
