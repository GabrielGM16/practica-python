from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoProductoViewSet,
    ProveedorViewSet,
    ProductoViewSet,
    ProductoProveedorViewSet
)

router = DefaultRouter()
router.register(r'tipos-producto', TipoProductoViewSet, basename='tipoproducto')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'productos-proveedores', ProductoProveedorViewSet, basename='productoproveedor')

urlpatterns = [
    path('', include(router.urls)),
]