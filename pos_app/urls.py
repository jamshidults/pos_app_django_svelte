from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, index, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', index),
    path('api/', include(router.urls)),

]
