from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, index, OrderViewSet,CounterViewSet,PaymentMethodViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'counters', CounterViewSet,basename='counter')
router.register(r'payment_methods', PaymentMethodViewSet,basename='payment_method')

urlpatterns = [
    path('', index),
    path('api/', include(router.urls)),

]
