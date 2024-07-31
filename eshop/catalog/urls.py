from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductFormView,
    ProductUserListView,
    ProductUpdateView,
)

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("my_products/create", ProductFormView.as_view(), name="product_form"),
    path(
        "my_products/<int:pk>/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path("my_products/", ProductUserListView.as_view(), name="my_products"),
]
