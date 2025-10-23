from django.core.management.base import BaseCommand
from productos.models import TipoProducto, Proveedor, Producto, ProductoProveedor
from decimal import Decimal


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos de prueba...')

        # Limpiar datos existentes
        ProductoProveedor.objects.all().delete()
        Producto.objects.all().delete()
        TipoProducto.objects.all().delete()
        Proveedor.objects.all().delete()

        # Crear Tipos de Producto
        tipos = [
            TipoProducto.objects.create(
                nombre='Electrónica',
                descripcion='Productos electrónicos y dispositivos'
            ),
            TipoProducto.objects.create(
                nombre='Alimentos',
                descripcion='Productos alimenticios y bebidas'
            ),
            TipoProducto.objects.create(
                nombre='Ropa',
                descripcion='Prendas de vestir y accesorios'
            ),
            TipoProducto.objects.create(
                nombre='Hogar',
                descripcion='Artículos para el hogar'
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'✓ Creados {len(tipos)} tipos de producto'))

        # Crear Proveedores
        proveedores = [
            Proveedor.objects.create(
                nombre='TechSupply SA',
                descripcion='Proveedor de productos tecnológicos'
            ),
            Proveedor.objects.create(
                nombre='ElectroMundo',
                descripcion='Distribuidor de electrónica'
            ),
            Proveedor.objects.create(
                nombre='AlimentiCorp',
                descripcion='Mayorista de alimentos'
            ),
            Proveedor.objects.create(
                nombre='FoodDistributors',
                descripcion='Distribución de productos alimenticios'
            ),
            Proveedor.objects.create(
                nombre='ModaTotal',
                descripcion='Proveedor de ropa y accesorios'
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'✓ Creados {len(proveedores)} proveedores'))

        # Crear Productos
        productos_data = [
            {
                'clave': 'ELEC-001',
                'nombre': 'Laptop HP 15"',
                'tipo': tipos[0],
                'proveedores': [
                    {'proveedor': proveedores[0], 'clave': 'HP-LAP-001', 'costo': Decimal('8500.00')},
                    {'proveedor': proveedores[1], 'clave': 'ELEC-HP-15', 'costo': Decimal('8200.00')},
                ]
            },
            {
                'clave': 'ELEC-002',
                'nombre': 'Mouse Inalámbrico Logitech',
                'tipo': tipos[0],
                'proveedores': [
                    {'proveedor': proveedores[0], 'clave': 'LOG-M170', 'costo': Decimal('250.00')},
                ]
            },
            {
                'clave': 'ELEC-003',
                'nombre': 'Teclado Mecánico RGB',
                'tipo': tipos[0],
                'proveedores': [
                    {'proveedor': proveedores[1], 'clave': 'KB-RGB-001', 'costo': Decimal('1200.00')},
                ]
            },
            {
                'clave': 'ALI-001',
                'nombre': 'Arroz Premium 1kg',
                'tipo': tipos[1],
                'proveedores': [
                    {'proveedor': proveedores[2], 'clave': 'ARR-PREM-1K', 'costo': Decimal('45.00')},
                    {'proveedor': proveedores[3], 'clave': 'FOOD-ARR-001', 'costo': Decimal('42.00')},
                ]
            },
            {
                'clave': 'ALI-002',
                'nombre': 'Aceite de Oliva 500ml',
                'tipo': tipos[1],
                'proveedores': [
                    {'proveedor': proveedores[2], 'clave': 'ACE-OLI-500', 'costo': Decimal('85.00')},
                ]
            },
            {
                'clave': 'ALI-003',
                'nombre': 'Pasta Italiana 500g',
                'tipo': tipos[1],
                'proveedores': [
                    {'proveedor': proveedores[3], 'clave': 'PAST-IT-500', 'costo': Decimal('32.00')},
                ]
            },
            {
                'clave': 'ROP-001',
                'nombre': 'Playera Algodón Unisex',
                'tipo': tipos[2],
                'proveedores': [
                    {'proveedor': proveedores[4], 'clave': 'PLY-ALG-UNI', 'costo': Decimal('120.00')},
                ]
            },
            {
                'clave': 'ROP-002',
                'nombre': 'Jeans Mezclilla',
                'tipo': tipos[2],
                'proveedores': [
                    {'proveedor': proveedores[4], 'clave': 'JNS-MZC-001', 'costo': Decimal('450.00')},
                ]
            },
            {
                'clave': 'HOG-001',
                'nombre': 'Juego de Sábanas King Size',
                'tipo': tipos[3],
                'proveedores': [
                    {'proveedor': proveedores[4], 'clave': 'SAB-KNG-001', 'costo': Decimal('650.00')},
                ]
            },
            {
                'clave': 'HOG-002',
                'nombre': 'Toallas de Baño Set 3pz',
                'tipo': tipos[3],
                'proveedores': [
                    {'proveedor': proveedores[4], 'clave': 'TOA-SET-3', 'costo': Decimal('280.00')},
                ]
            },
        ]

        for prod_data in productos_data:
            producto = Producto.objects.create(
                clave=prod_data['clave'],
                nombre=prod_data['nombre'],
                tipo_producto=prod_data['tipo']
            )

            # Agregar proveedores
            for prov_data in prod_data['proveedores']:
                ProductoProveedor.objects.create(
                    producto=producto,
                    proveedor=prov_data['proveedor'],
                    clave_proveedor=prov_data['clave'],
                    costo=prov_data['costo']
                )

        self.stdout.write(self.style.SUCCESS(f'✓ Creados {len(productos_data)} productos'))
        self.stdout.write(self.style.SUCCESS('\n¡Datos de prueba creados exitosamente!'))