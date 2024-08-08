from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_title = self.request.query_params.get('search', None)
        if product_title:
            queryset = queryset.filter(positions__product__title__icontains=product_title)
        return queryset

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['address']
