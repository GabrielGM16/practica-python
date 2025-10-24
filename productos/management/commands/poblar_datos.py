from django.core.management.base import BaseCommand
from productos.models import TipoProducto, Proveedor, Producto, ProductoProveedor
from decimal import Decimal


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todos los datos antes de crear nuevos',
        )

    def handle(self, *args, **kwargs):
        limpiar = kwargs.get('limpiar', False)
        
        # Verificar si ya hay datos
        if Producto.objects.exists() and not limpiar:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  Ya existen {Producto.objects.count()} productos en la base de datos.'
                )
            )
            self.stdout.write(
                self.style.NOTICE(
                    '💡 Los datos se actualizarán/complementarán sin eliminar lo existente.'
                )
            )
            self.stdout.write(
                self.style.NOTICE(
                    '   Si deseas eliminar TODO y empezar de cero, usa: python manage.py poblar_datos --limpiar\n'
                )
            )

        if limpiar:
            self.stdout.write(self.style.WARNING('\n🗑️  Limpiando datos existentes...'))
            ProductoProveedor.objects.all().delete()
            Producto.objects.all().delete()
            TipoProducto.objects.all().delete()
            Proveedor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('   ✓ Datos eliminados'))

        self.stdout.write('\n📦 Creando/Actualizando datos de prueba...\n')

        # Crear/Actualizar Tipos de Producto
        tipos = []
        tipos_data = [
            ('Electrónica', 'Productos electrónicos y dispositivos'),
            ('Alimentos', 'Productos alimenticios y bebidas'),
            ('Ropa', 'Prendas de vestir y accesorios'),
            ('Hogar', 'Artículos para el hogar'),
        ]
        
        for nombre, descripcion in tipos_data:
            tipo, created = TipoProducto.objects.update_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion}
            )
            tipos.append(tipo)
            status = '✨ creado' if created else '🔄 actualizado'
            self.stdout.write(f'   {status}: Tipo "{nombre}"')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(tipos)} tipos de producto procesados'))

        # Crear/Actualizar Proveedores
        proveedores = []
        proveedores_data = [
            ('TechSupply SA', 'Proveedor de productos tecnológicos', 'Electrónicos'),
            ('ElectroMundo', 'Distribuidor de electrónica', 'Electrónicos'),
            ('AlimentiCorp', 'Mayorista de alimentos', 'Alimentos'),
            ('FoodDistributors', 'Distribución de productos alimenticios', 'Alimentos'),
            ('ModaTotal', 'Proveedor de ropa y accesorios', 'Ropa'),
        ]
        
        for nombre, descripcion, departamento in proveedores_data:
            proveedor, created = Proveedor.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'departamento': departamento
                }
            )
            proveedores.append(proveedor)
            status = '✨ creado' if created else '🔄 actualizado'
            self.stdout.write(f'   {status}: {nombre} (Depto: {departamento})')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(proveedores)} proveedores procesados'))

        # Crear/Actualizar Productos
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

        productos_creados = 0
        productos_actualizados = 0
        relaciones_creadas = 0
        relaciones_actualizadas = 0

        for prod_data in productos_data:
            producto, created = Producto.objects.update_or_create(
                clave=prod_data['clave'],
                defaults={
                    'nombre': prod_data['nombre'],
                    'tipo_producto': prod_data['tipo']
                }
            )
            
            if created:
                productos_creados += 1
                self.stdout.write(f'   ✨ Producto creado: {prod_data["clave"]} - {prod_data["nombre"]}')
            else:
                productos_actualizados += 1
                self.stdout.write(f'   🔄 Producto actualizado: {prod_data["clave"]} - {prod_data["nombre"]}')

            # Agregar/Actualizar proveedores
            for prov_data in prod_data['proveedores']:
                relacion, created = ProductoProveedor.objects.update_or_create(
                    producto=producto,
                    proveedor=prov_data['proveedor'],
                    defaults={
                        'clave_proveedor': prov_data['clave'],
                        'costo': prov_data['costo']
                    }
                )
                if created:
                    relaciones_creadas += 1
                else:
                    relaciones_actualizadas += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ Productos: {productos_creados} creados, {productos_actualizados} actualizados'))
        self.stdout.write(self.style.SUCCESS(f'✅ Relaciones: {relaciones_creadas} creadas, {relaciones_actualizadas} actualizadas'))
        self.stdout.write(self.style.SUCCESS('\n🎉 ¡Proceso completado exitosamente!\n'))