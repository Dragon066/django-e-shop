import json

from catalog.models import Product
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from user.models import User

from .serializers import ProductSerializer, UserSerializer
from .views import ProductModelEditViewSet, ProductModelViewSet


class APISerializerTest(TestCase):
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
        self.product = Product.objects.get(pk=1)

    def test_product_serializer(self):
        serializer = ProductSerializer(instance=self.product)
        self.assertEqual(serializer.data["name"], "TestProduct")
        self.assertEqual(serializer.data["description"], "Test")
        self.assertEqual(serializer.data["quantity"], 10)
        self.assertEqual(float(serializer.data["price"]), 1)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data["email"], "test1@user.com")
        self.assertEqual(serializer.data["first_name"], "test1")
        self.assertEqual(serializer.data["last_name"], "user")

    def test_user_serializer_create(self):
        data = {
            "email": "test2@user.com",
            "first_name": "test2",
            "last_name": "user",
            "password": "difficult_password_123",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(User.objects.filter(email="test2@user.com").exists())


class APUViewTest(TestCase):
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
        self.factory = APIRequestFactory()
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)

    def test_product_list_api(self):
        request = self.factory.get(reverse("api:product-list"))
        request.user = self.user
        response = ProductModelViewSet.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "TestProduct")

    def test_product_detail_api(self):
        request = self.factory.get(
            reverse("api:product-detail", kwargs={"pk": 1})
        )
        request.user = self.user
        response = ProductModelViewSet.as_view({"get": "retrieve"})(
            request, pk=1
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "TestProduct")

    def test_edit_product_login_required(self):
        request = self.factory.get(
            reverse("api:products_edit-detail", kwargs={"pk": 1})
        )
        response = ProductModelEditViewSet.as_view({"get": "retrieve"})(
            request, pk=1
        )
        self.assertEqual(response.status_code, 401)

    def test_edit_product_update(self):
        data = {
            "name": "TestProduct2",
            "description": "Test2",
            "quantity": 20,
            "price": 2,
        }

        request = self.factory.put(
            reverse("api:products_edit-detail", kwargs={"pk": 1}),
            data=json.dumps(data),
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)
        response = ProductModelEditViewSet.as_view({"put": "update"})(
            request, pk=1
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "TestProduct2")
        self.assertEqual(response.data["description"], "Test2")
        self.assertEqual(response.data["quantity"], 20)
        self.assertEqual(float(response.data["price"]), 2)

    def test_edit_product_delete(self):
        request = self.factory.delete(
            reverse("api:products_edit-detail", kwargs={"pk": 1})
        )
        force_authenticate(request, user=self.user)
        response = ProductModelEditViewSet.as_view({"delete": "destroy"})(
            request, pk=1
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=1).exists())
