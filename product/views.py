from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductListSerializer, ProductDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductCategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        name = self.request.query_params.get("name")
        if name:
            queryset = Product.objects.filter(name__icontains=name)

        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        
        return queryset