from rest_framework import serializers
from .models import TipoProducto, Proveedor, Producto, ProductoProveedor
from decimal import Decimal


class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ['id', 'nombre', 'descripcion', 'activo', 'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'descripcion', 'activo', 'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']


class ProductoProveedorSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    
    class Meta:
        model = ProductoProveedor
        fields = ['id', 'proveedor', 'proveedor_nombre', 'clave_proveedor', 'costo', 'activo']
    
    def validate_costo(self, value):
        """Valida que el costo sea mayor a 0"""
        if value <= Decimal('0'):
            raise serializers.ValidationError("El costo debe ser mayor a 0")
        return value


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer para listar productos (vista simplificada)"""
    tipo_producto_nombre = serializers.CharField(source='tipo_producto.nombre', read_only=True)
    cantidad_proveedores = serializers.SerializerMethodField()
    costo_minimo = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'clave', 'nombre', 'tipo_producto', 'tipo_producto_nombre', 
                  'cantidad_proveedores', 'costo_minimo', 'activo']
    
    def get_cantidad_proveedores(self, obj):
        return obj.producto_proveedores.filter(activo=True).count()
    
    def get_costo_minimo(self, obj):
        """Calcula el costo mínimo de todos los proveedores activos"""
        proveedores_activos = obj.producto_proveedores.filter(activo=True)
        if proveedores_activos.exists():
            return min(pp.costo for pp in proveedores_activos)
        return None


class ProductoDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle y edición de productos"""
    tipo_producto_nombre = serializers.CharField(source='tipo_producto.nombre', read_only=True)
    proveedores_detalle = ProductoProveedorSerializer(
        source='producto_proveedores', 
        many=True, 
        read_only=True
    )
    
    class Meta:
        model = Producto
        fields = ['id', 'clave', 'nombre', 'tipo_producto', 'tipo_producto_nombre',
                  'proveedores_detalle', 'activo', 'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def validate_clave(self, value):
        """Valida que la clave sea única (excepto en actualización)"""
        instance = self.instance
        if instance and instance.clave == value:
            return value
        
        if Producto.objects.filter(clave=value).exists():
            raise serializers.ValidationError("Ya existe un producto con esta clave")
        return value


class ProductoCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar productos con sus proveedores"""
    proveedores = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Producto
        fields = ['id', 'clave', 'nombre', 'tipo_producto', 'proveedores', 'activo']
    
    def validate_proveedores(self, value):
        """Valida la estructura de los proveedores"""
        if not value:
            return value
        
        for prov in value:
            if 'proveedor' not in prov:
                raise serializers.ValidationError("Cada proveedor debe tener el campo 'proveedor'")
            if 'clave_proveedor' not in prov:
                raise serializers.ValidationError("Cada proveedor debe tener 'clave_proveedor'")
            if 'costo' not in prov:
                raise serializers.ValidationError("Cada proveedor debe tener 'costo'")
            
            try:
                costo = Decimal(str(prov['costo']))
                if costo <= Decimal('0'):
                    raise serializers.ValidationError("El costo debe ser mayor a 0")
            except (ValueError, TypeError):
                raise serializers.ValidationError("El costo debe ser un número válido")
        
        return value
    
    def create(self, validated_data):
        proveedores_data = validated_data.pop('proveedores', [])
        producto = Producto.objects.create(**validated_data)
        
        # Crear relaciones con proveedores
        for prov_data in proveedores_data:
            ProductoProveedor.objects.create(
                producto=producto,
                proveedor_id=prov_data['proveedor'],
                clave_proveedor=prov_data['clave_proveedor'],
                costo=prov_data['costo'],
                activo=prov_data.get('activo', True)
            )
        
        return producto
    
    def update(self, instance, validated_data):
        proveedores_data = validated_data.pop('proveedores', None)
        
        # Actualizar campos del producto
        instance.clave = validated_data.get('clave', instance.clave)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.tipo_producto = validated_data.get('tipo_producto', instance.tipo_producto)
        instance.activo = validated_data.get('activo', instance.activo)
        instance.save()
        
        # Actualizar proveedores si se enviaron
        if proveedores_data is not None:
            # Eliminar relaciones existentes
            instance.producto_proveedores.all().delete()
            
            # Crear nuevas relaciones
            for prov_data in proveedores_data:
                ProductoProveedor.objects.create(
                    producto=instance,
                    proveedor_id=prov_data['proveedor'],
                    clave_proveedor=prov_data['clave_proveedor'],
                    costo=prov_data['costo'],
                    activo=prov_data.get('activo', True)
                )
        
        return instance