from django.urls import path
from .views import CartView, CartFormView, CartDeleteView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/<int:pk>", CartFormView.as_view(), name="cart_detail"),
    path("delete/<int:pk>", CartDeleteView.as_view(), name="cart_delete"),
]
