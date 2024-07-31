from django.urls import path
from .views import ProductModelViewSet, ProductModelEditViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api"

router = DefaultRouter()
router.register("products", ProductModelViewSet, basename="product")
router.register(
    "my_products", ProductModelEditViewSet, basename="products_edit"
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns += router.urls
