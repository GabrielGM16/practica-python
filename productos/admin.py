from django.contrib import admin
from .models import TipoProducto, Proveedor, Producto, ProductoProveedor


@admin.register(TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']


class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    fields = ['proveedor', 'clave_proveedor', 'costo', 'activo']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['clave', 'nombre', 'tipo_producto', 'activo', 'fecha_creacion']
    list_filter = ['tipo_producto', 'activo']
    search_fields = ['clave', 'nombre']
    inlines = [ProductoProveedorInline]


@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['producto', 'proveedor', 'clave_proveedor', 'costo', 'activo']
    list_filter = ['activo', 'proveedor']
    search_fields = ['producto__clave', 'producto__nombre', 'proveedor__nombre', 'clave_proveedor']