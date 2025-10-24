# Sistema de Distribución de Productos

Sistema web desarrollado en Django para la gestión de productos y sus relaciones con proveedores.

##  Características

-  Gestión completa de productos (CRUD)
-  Relación many-to-many entre productos y proveedores
-  Categorización de proveedores por departamentos (Electrónicos, Alimentos, Ropa, etc.)
-  API REST completa con Django REST Framework
-  Interfaz web responsiva con Tailwind CSS
-  Búsqueda y filtrado de productos y proveedores
-  Validaciones de datos
-  Manejo de errores

##  Requisitos

- Python 3.9 o superior
- MySQL 5.7 o superior (o PostgreSQL)
- pip (gestor de paquetes de Python)

##  Instalación

### 1. Clonar o descargar el proyecto
```bash
cd practica-python
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

**Opción A: Usar el script SQL**
```bash
# Ejecutar el script database_schema.sql en MySQL
mysql -u root -p < database_schema.sql
```

**Opción B: Usar migraciones de Django**
```bash
# Crear la base de datos manualmente
mysql -u root -p
CREATE DATABASE distribuidora_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Ejecutar migraciones
python manage.py migrate

# Nota: La migración 0003_auto_20251023_1702.py incluye:
# - Asignación automática de departamentos a proveedores existentes
# - Conversión del campo 'departamento' de opcional a obligatorio
```

### 5. Configurar credenciales de BD

Editar `distribuidora/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'distribuidora_db',
        'USER': 'tu_usuario',      # Cambiar
        'PASSWORD': 'tu_password',  # Cambiar
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Cargar datos de prueba (Opcional)
```bash
python manage.py poblar_datos
```

### 8. Iniciar servidor
```bash
python manage.py runserver
```

Abrir navegador en: `http://127.0.0.1:8000/`

##  Estructura del Proyecto
```
distribuidora-app/
│
├── distribuidora/           # Configuración del proyecto
│   ├── settings.py         # Configuraciones
│   ├── urls.py             # URLs principales
│   └── wsgi.py
│
├── productos/              # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y API ViewSets
│   ├── serializers.py      # Serializadores DRF
│   ├── urls.py             # URLs de la app
│   ├── admin.py            # Configuración del admin
│   ├── templates/          # Templates HTML
│   └── management/         # Comandos personalizados
│
├── database_schema.sql     # Script SQL
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

##  Endpoints de la API

### Productos
- `GET /api/productos/` - Listar productos
- `POST /api/productos/` - Crear producto
- `GET /api/productos/{id}/` - Detalle de producto
- `PUT /api/productos/{id}/` - Actualizar producto
- `DELETE /api/productos/{id}/` - Eliminar producto
- `GET /api/productos/{id}/proveedores/` - Proveedores del producto

### Proveedores
- `GET /api/proveedores/` - Listar proveedores
- `POST /api/proveedores/` - Crear proveedor
- `GET /api/proveedores/{id}/` - Detalle de proveedor
- `PUT /api/proveedores/{id}/` - Actualizar proveedor
- `DELETE /api/proveedores/{id}/` - Eliminar proveedor
- `GET /api/proveedores/departamentos/` - Listar departamentos únicos

### Tipos de Producto
- `GET /api/tipos-producto/` - Listar tipos
- `POST /api/tipos-producto/` - Crear tipo
- `GET /api/tipos-producto/{id}/` - Detalle de tipo
- `PUT /api/tipos-producto/{id}/` - Actualizar tipo
- `DELETE /api/tipos-producto/{id}/` - Eliminar tipo

##  Interfaces Disponibles

- **Frontend**: `http://127.0.0.1:8000/productos/`
- **API REST**: `http://127.0.0.1:8000/api/`
- **Admin Django**: `http://127.0.0.1:8000/admin/`

##  Modelos de Datos

### TipoProducto
- Nombre
- Descripción
- Activo

### Proveedor
- Nombre
- Descripción
- Departamento (Electrónicos, Alimentos, Ropa, etc.)
- Activo

### Producto
- Clave (única)
- Nombre
- Tipo de Producto (FK)
- Activo
- Proveedores (M2M)

### ProductoProveedor (Tabla intermedia)
- Producto (FK)
- Proveedor (FK)
- Clave del Proveedor
- Costo

##  Búsqueda y Filtros

La API soporta los siguientes parámetros de búsqueda:

### Productos
```
GET /api/productos/?clave=ELEC
GET /api/productos/?tipo_producto=1
GET /api/productos/?activo=true
```

### Proveedores
```
GET /api/proveedores/?departamento=Electrónicos
GET /api/proveedores/?nombre=TechSupply
GET /api/proveedores/?activo=true
```

##  Tecnologías Utilizadas

- **Backend**: Python 3.9+, Django 4.x
- **API**: Django REST Framework
- **Base de Datos**: MySQL
- **Frontend**: Tailwind CSS, JavaScript (Vanilla)
- **Estilos**: Tailwind CSS, Bootstrap Icons

##  Notas Adicionales

- Todos los endpoints de la API usan formato JSON
- Las relaciones producto-proveedor se manejan automáticamente
- El sistema incluye validaciones tanto en backend como frontend
- Los costos deben ser valores positivos
