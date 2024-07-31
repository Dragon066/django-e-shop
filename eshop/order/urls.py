from django.urls import path, include
from .views import (
    MyOrdersView,
    OrderCreateView,
    OrderDetailView,
    OrderProcessView,
    OrderProcessDetailView,
)

app_name = "order"

urlpatterns = [
    path("my_orders/", MyOrdersView.as_view(), name="my_orders"),
    path(
        "my_orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"
    ),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("client_orders/", OrderProcessView.as_view(), name="order_process"),
    path(
        "client_orders/<int:pk>/",
        OrderProcessDetailView.as_view(),
        name="order_process_detail",
    ),
]
