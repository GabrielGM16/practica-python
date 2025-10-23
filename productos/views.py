from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import TipoProducto, Proveedor, Producto, ProductoProveedor
from .serializers import (
    TipoProductoSerializer,
    ProveedorSerializer,
    ProductoListSerializer,
    ProductoDetailSerializer,
    ProductoCreateUpdateSerializer,
    ProductoProveedorSerializer
)


class TipoProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Tipos de Producto
    """
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['nombre']

    def destroy(self, request, *args, **kwargs):
        """Elimina un tipo de producto si no tiene productos asociados"""
        instance = self.get_object()
        
        if instance.productos.exists():
            return Response(
                {'error': 'No se puede eliminar el tipo de producto porque tiene productos asociados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProveedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Proveedores
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['nombre']

    def destroy(self, request, *args, **kwargs):
        """Elimina un proveedor si no tiene productos asociados"""
        instance = self.get_object()
        
        if instance.proveedor_productos.exists():
            return Response(
                {'error': 'No se puede eliminar el proveedor porque tiene productos asociados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Productos
    """
    queryset = Producto.objects.select_related('tipo_producto').prefetch_related(
        'producto_proveedores__proveedor'
    )
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['clave', 'nombre']
    ordering_fields = ['clave', 'nombre', 'fecha_creacion']
    ordering = ['clave']

    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateUpdateSerializer
        return ProductoDetailSerializer

    def get_queryset(self):
        """
        Filtra productos por clave o tipo de producto
        """
        queryset = super().get_queryset()
        
        # Filtro por clave
        clave = self.request.query_params.get('clave', None)
        if clave:
            queryset = queryset.filter(clave__icontains=clave)
        
        # Filtro por tipo de producto
        tipo_producto = self.request.query_params.get('tipo_producto', None)
        if tipo_producto:
            queryset = queryset.filter(tipo_producto_id=tipo_producto)
        
        # Filtro por activo
        activo = self.request.query_params.get('activo', None)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset

    @action(detail=True, methods=['get'])
    def proveedores(self, request, pk=None):
        """
        Endpoint para obtener todos los proveedores de un producto
        GET /api/productos/{id}/proveedores/
        """
        producto = self.get_object()
        proveedores = producto.producto_proveedores.filter(activo=True)
        serializer = ProductoProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def agregar_proveedor(self, request, pk=None):
        """
        Endpoint para agregar un proveedor a un producto
        POST /api/productos/{id}/agregar_proveedor/
        Body: {
            "proveedor": 1,
            "clave_proveedor": "ABC123",
            "costo": 100.50
        }
        """
        producto = self.get_object()
        serializer = ProductoProveedorSerializer(data=request.data)
        
        if serializer.is_valid():
            # Verificar si ya existe la relación
            if ProductoProveedor.objects.filter(
                producto=producto,
                proveedor=serializer.validated_data['proveedor']
            ).exists():
                return Response(
                    {'error': 'Este proveedor ya está asociado al producto'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(producto=producto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='eliminar_proveedor/(?P<proveedor_id>[^/.]+)')
    def eliminar_proveedor(self, request, pk=None, proveedor_id=None):
        """
        Endpoint para eliminar un proveedor de un producto
        DELETE /api/productos/{id}/eliminar_proveedor/{proveedor_id}/
        """
        producto = self.get_object()
        
        try:
            producto_proveedor = ProductoProveedor.objects.get(
                producto=producto,
                proveedor_id=proveedor_id
            )
            producto_proveedor.delete()
            return Response(
                {'message': 'Proveedor eliminado del producto correctamente'},
                status=status.HTTP_204_NO_CONTENT
            )
        except ProductoProveedor.DoesNotExist:
            return Response(
                {'error': 'Relación producto-proveedor no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """Elimina un producto y sus relaciones"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Producto eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )


class ProductoProveedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar la relación Producto-Proveedor
    """
    queryset = ProductoProveedor.objects.select_related('producto', 'proveedor').all()
    serializer_class = ProductoProveedorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['costo', 'fecha_creacion']
    ordering = ['producto__clave']

    def get_queryset(self):
        """Filtra por producto o proveedor si se especifica"""
        queryset = super().get_queryset()
        
        producto_id = self.request.query_params.get('producto', None)
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        
        proveedor_id = self.request.query_params.get('proveedor', None)
        if proveedor_id:
            queryset = queryset.filter(proveedor_id=proveedor_id)
        
        return queryset

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def producto_list(request):
    """Vista para listar productos"""
    return render(request, 'productos/producto_list.html')


def producto_create(request):
    """Vista para crear un producto"""
    return render(request, 'productos/producto_form.html', {
        'modo': 'crear'
    })


def producto_edit(request, pk):
    """Vista para editar un producto"""
    # Verificar que el producto existe
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_form.html', {
        'modo': 'editar',
        'producto_id': pk
    })