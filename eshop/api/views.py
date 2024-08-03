import logging

from catalog.models import Product
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductEditSerializer, ProductSerializer


class ProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing products.

    This view only available in read mode.
    """

    queryset = Product.objects.filter(available=True).prefetch_related(
        "category"
    )
    serializer_class = ProductSerializer


class ProductModelEditViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.

    Login with DRF JWT tokens required.
    """

    serializer_class = ProductEditSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            owner=self.request.user
        ).prefetch_related("category")

    def perform_create(self, serializer):
        logging.info(f'User "{self.request.user}" created product via API')
        serializer.save(owner=self.request.user)
