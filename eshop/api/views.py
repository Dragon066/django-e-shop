from django.shortcuts import render
from catalog.models import Product
from rest_framework import generics, viewsets
from .serializers import ProductSerializer, ProductEditSerializer
from rest_framework.permissions import IsAuthenticated

class ProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True).prefetch_related('category')
    serializer_class = ProductSerializer


class ProductModelEditViewSet(viewsets.ModelViewSet):
    serializer_class = ProductEditSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user).prefetch_related('category')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
