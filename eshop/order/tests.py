from cart.models import Cart
from catalog.models import Product
from django.test import RequestFactory, TestCase
from django.urls import reverse
from user.jwt import get_access_token
from user.models import User

from .models import Order


class OrderLoginRequiredTest(TestCase):
    def test_login_required_my_orders(self):
        response = self.client.get(reverse("order:my_orders"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/order/my_orders/"
        )

    def test_login_required_order_detail(self):
        response = self.client.get(
            reverse("order:order_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/order/my_orders/1/"
        )

    def test_login_required_order_delete(self):
        response = self.client.get(reverse("order:order_create"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/order/create/")

    def test_login_required_order_process(self):
        response = self.client.get(reverse("order:order_process"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/order/client_orders/"
        )

    def test_login_required_order_process_detail(self):
        response = self.client.get(
            reverse("order:order_process_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/order/client_orders/1/"
        )


class OrderViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email="test1@user.com",
            first_name="test1",
            last_name="user",
            password="difficult_password_123",
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
        self.factory = RequestFactory()
        self.user = User.objects.get(pk=1)
        self.client.cookies["jwt-access"] = get_access_token(self.user)
        self.product = Product.objects.get(pk=1)

    def test_order_create_view(self):
        data = {"phone": "+79998887766", "address": "some address"}

        response = self.client.post(reverse("order:order_create"), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("order:my_orders"))
        self.assertTrue(Order.objects.get(pk=1))

    def test_order_fail_create_view(self):
        data = {"phone": "+79998887766", "address": "some address"}

        self.product.available = False
        self.product.save()

        response = self.client.post(reverse("order:order_create"), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Order.objects.count())

    def test_order_my_orders_view(self):
        data = {"phone": "+79998887766", "address": "some address"}

        self.client.post(reverse("order:order_create"), data=data)

        response = self.client.get(reverse("order:my_orders"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "#1")

    def test_order_detail_view(self):
        data = {"phone": "+79998887766", "address": "some address"}

        self.client.post(reverse("order:order_create"), data=data)

        response = self.client.get(
            reverse("order:order_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["order"].pk, 1)
        self.assertEqual(response.context["products"].count(), 1)

    def test_order_process_view(self):
        data = {"phone": "+79998887766", "address": "some address"}

        self.client.post(reverse("order:order_create"), data=data)

        response = self.client.get(reverse("order:order_process"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestProduct")

    def test_order_process_detail_view(self):
        data = {"phone": "+79998887766", "address": "some address"}

        self.client.post(reverse("order:order_create"), data=data)

        response = self.client.get(
            reverse("order:order_process_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestProduct")

        self.client.post(
            reverse("order:order_process_detail", kwargs={"pk": 1}),
            data={"status": "InDelivery"},
        )

        response = self.client.get(
            reverse("order:order_process_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"].status, "InDelivery")
