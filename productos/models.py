from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoProducto(models.Model):
    """Tipo o categoría de producto"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipo_producto'
        verbose_name = 'Tipo de Producto'
        verbose_name_plural = 'Tipos de Productos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    """Proveedor de productos"""
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto principal"""
    clave = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=200)
    tipo_producto = models.ForeignKey(
        TipoProducto,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    proveedores = models.ManyToManyField(
        Proveedor,
        through='ProductoProveedor',
        related_name='productos'
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['clave']
        indexes = [
            models.Index(fields=['clave']),
            models.Index(fields=['tipo_producto']),
        ]

    def __str__(self):
        return f"{self.clave} - {self.nombre}"


class ProductoProveedor(models.Model):
    """Relación entre Producto y Proveedor con información adicional"""
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='producto_proveedores'
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='proveedor_productos'
    )
    clave_proveedor = models.CharField(
        max_length=100,
        help_text='Clave del producto según el proveedor'
    )
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'producto_proveedor'
        verbose_name = 'Producto-Proveedor'
        verbose_name_plural = 'Productos-Proveedores'
        unique_together = ['producto', 'proveedor']
        ordering = ['producto', 'proveedor']

    def __str__(self):
        return f"{self.producto.clave} - {self.proveedor.nombre} (${self.costo})"