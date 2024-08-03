import logging

from catalog.models import Product
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductEditSerializer, ProductSerializer


class ProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True).prefetch_related(
        "category"
    )
    serializer_class = ProductSerializer


class ProductModelEditViewSet(viewsets.ModelViewSet):
    serializer_class = ProductEditSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            owner=self.request.user
        ).prefetch_related("category")

    def perform_create(self, serializer):
        logging.info(f'User "{self.request.user}" created product via API')
        serializer.save(owner=self.request.user)
