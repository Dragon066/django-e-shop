from django.test import RequestFactory, TestCase
from django.urls import reverse
from user.jwt import get_access_token
from user.models import User

from .forms import ProductForm
from .models import Product


class CatalogLoginRequiredTest(TestCase):
    def test_login_required_product_form_view(self):
        response = self.client.get(reverse("catalog:product_form"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/catalog/my_products/create"
        )

    def test_login_required_product_update_view(self):
        response = self.client.get(
            reverse("catalog:product_update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/catalog/my_products/1/"
        )

    def test_login_required_catalog_delete(self):
        response = self.client.get(reverse("catalog:my_products"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/catalog/my_products/"
        )


class CatalogViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="test1@user.com",
            first_name="test1",
            last_name="user",
            password="difficult_password_123",
        )

        Product.objects.create(
            name="TestProduct",
            description="Test",
            quantity=10,
            price=1,
            owner=User.objects.get(pk=1),
        )

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(pk=1)
        self.client.cookies["jwt-access"] = get_access_token(self.user)
        self.product = Product.objects.get(pk=1)

    def test_product_list(self):
        response = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog_list.html")
        self.assertContains(response, "TestProduct")

    def test_product_detail(self):
        response = self.client.get(
            reverse("catalog:product_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_detail.html")
        self.assertContains(response, "TestProduct")

    def test_contacts_view(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts.html")

    def test_my_products_view(self):
        response = self.client.get(reverse("catalog:my_products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_products.html")
        self.assertContains(response, "TestProduct")

    def test_product_create(self):
        data = {
            "name": "TestProduct2",
            "description": "Test2",
            "quantity": 10,
            "price": 1,
        }
        response = self.client.post(reverse("catalog:product_form"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/catalog/my_products/")
        self.assertTrue(Product.objects.filter(name="TestProduct2").exists())

    def test_product_update(self):
        data = {
            "name": "TestProduct2",
            "description": "Test2",
            "quantity": 10,
            "price": 1,
            "available": False,
        }
        response = self.client.post(
            reverse("catalog:product_update", kwargs={"pk": 1}), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:my_products"))
        self.assertEqual(Product.objects.get(pk=1).name, "TestProduct2")
        self.assertEqual(Product.objects.get(pk=1).available, False)


class CatalogFormTest(TestCase):
    def test_product_form_valid(self):
        data = {
            "name": "TestProduct",
            "description": "Test",
            "quantity": 10,
            "price": 10,
            "available": True,
        }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid(self):
        data = {
            "name": "TestProduct",
            "description": "Test",
            "quantity": -1,
            "price": 10,
            "available": False,
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
