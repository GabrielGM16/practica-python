from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoProductoViewSet,
    ProveedorViewSet,
    ProductoViewSet,
    ProductoProveedorViewSet,
    producto_list,
    producto_create,
    producto_edit,
)

# API Router
router = DefaultRouter()
router.register(r'tipos-producto', TipoProductoViewSet, basename='tipoproducto')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'productos-proveedores', ProductoProveedorViewSet, basename='productoproveedor')

urlpatterns = [
    # Frontend URLs
    path('', producto_list, name='producto_list'),
    path('crear/', producto_create, name='producto_create'),
    path('editar/<int:pk>/', producto_edit, name='producto_edit'),
    
    # API URLs
    path('api/', include(router.urls)),
]