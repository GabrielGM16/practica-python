-- ============================================
-- Script de Creación de Base de Datos
-- Sistema de Distribución de Productos
-- ============================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS distribuidora_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE distribuidora_db;

-- ============================================
-- Tabla: tipo_producto
-- ============================================
CREATE TABLE tipo_producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME(6) NOT NULL,
    fecha_modificacion DATETIME(6) NOT NULL,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: proveedor
-- ============================================
CREATE TABLE proveedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    descripcion TEXT,
    departamento VARCHAR(100) NOT NULL COMMENT 'Departamento o categoría del proveedor (ej: Electrónicos, Alimentos, Ropa)',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME(6) NOT NULL,
    fecha_modificacion DATETIME(6) NOT NULL,
    INDEX idx_nombre (nombre),
    INDEX idx_departamento (departamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: producto
-- ============================================
CREATE TABLE producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    tipo_producto_id INT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME(6) NOT NULL,
    fecha_modificacion DATETIME(6) NOT NULL,
    INDEX idx_clave (clave),
    INDEX idx_tipo_producto (tipo_producto_id),
    CONSTRAINT fk_producto_tipo 
        FOREIGN KEY (tipo_producto_id) 
        REFERENCES tipo_producto(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: producto_proveedor (Relación Many-to-Many)
-- ============================================
CREATE TABLE producto_proveedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    proveedor_id INT NOT NULL,
    clave_proveedor VARCHAR(100) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME(6) NOT NULL,
    fecha_modificacion DATETIME(6) NOT NULL,
    UNIQUE KEY unique_producto_proveedor (producto_id, proveedor_id),
    INDEX idx_producto (producto_id),
    INDEX idx_proveedor (proveedor_id),
    CONSTRAINT fk_producto_proveedor_producto 
        FOREIGN KEY (producto_id) 
        REFERENCES producto(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_producto_proveedor_proveedor 
        FOREIGN KEY (proveedor_id) 
        REFERENCES proveedor(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_costo_positivo 
        CHECK (costo > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Datos de prueba (Opcional)
-- ============================================

-- Insertar Tipos de Producto
INSERT INTO tipo_producto (nombre, descripcion, activo, fecha_creacion, fecha_modificacion) VALUES
('Electrónica', 'Productos electrónicos y dispositivos', TRUE, NOW(), NOW()),
('Alimentos', 'Productos alimenticios y bebidas', TRUE, NOW(), NOW()),
('Ropa', 'Prendas de vestir y accesorios', TRUE, NOW(), NOW()),
('Hogar', 'Artículos para el hogar', TRUE, NOW(), NOW());

-- Insertar Proveedores
INSERT INTO proveedor (nombre, descripcion, departamento, activo, fecha_creacion, fecha_modificacion) VALUES
('TechSupply SA', 'Proveedor de productos tecnológicos', 'Electrónicos', TRUE, NOW(), NOW()),
('ElectroMundo', 'Distribuidor de electrónica', 'Electrónicos', TRUE, NOW(), NOW()),
('AlimentiCorp', 'Mayorista de alimentos', 'Alimentos', TRUE, NOW(), NOW()),
('FoodDistributors', 'Distribución de productos alimenticios', 'Alimentos', TRUE, NOW(), NOW()),
('ModaTotal', 'Proveedor de ropa y accesorios', 'Ropa', TRUE, NOW(), NOW());

-- Insertar Productos
INSERT INTO producto (clave, nombre, tipo_producto_id, activo, fecha_creacion, fecha_modificacion) VALUES
('ELEC-001', 'Laptop HP 15"', 1, TRUE, NOW(), NOW()),
('ELEC-002', 'Mouse Inalámbrico Logitech', 1, TRUE, NOW(), NOW()),
('ALI-001', 'Arroz Premium 1kg', 2, TRUE, NOW(), NOW()),
('ROP-001', 'Playera Algodón Unisex', 3, TRUE, NOW(), NOW());

-- Insertar Relaciones Producto-Proveedor
INSERT INTO producto_proveedor (producto_id, proveedor_id, clave_proveedor, costo, activo, fecha_creacion, fecha_modificacion) VALUES
(1, 1, 'HP-LAP-001', 8500.00, TRUE, NOW(), NOW()),
(1, 2, 'ELEC-HP-15', 8200.00, TRUE, NOW(), NOW()),
(2, 1, 'LOG-M170', 250.00, TRUE, NOW(), NOW()),
(3, 3, 'ARR-PREM-1K', 45.00, TRUE, NOW(), NOW()),
(3, 4, 'FOOD-ARR-001', 42.00, TRUE, NOW(), NOW()),
(4, 5, 'PLY-ALG-UNI', 120.00, TRUE, NOW(), NOW());

-- ============================================
-- Consultas útiles para verificar
-- ============================================

-- Ver todos los productos con sus tipos
-- SELECT p.clave, p.nombre, t.nombre as tipo 
-- FROM producto p 
-- INNER JOIN tipo_producto t ON p.tipo_producto_id = t.id;

-- Ver productos con sus proveedores y costos
-- SELECT 
--     p.clave, 
--     p.nombre, 
--     pr.nombre as proveedor,
--     pp.clave_proveedor,
--     pp.costo
-- FROM producto p
-- INNER JOIN producto_proveedor pp ON p.id = pp.producto_id
-- INNER JOIN proveedor pr ON pp.proveedor_id = pr.id;