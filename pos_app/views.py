from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


def index(request):
  return render(request,  'pos_app/index.html')
class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        product_code = self.request.query_params.get('product_code', None)
        if product_code is not None:
            queryset = queryset.filter(product_code=product_code)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
