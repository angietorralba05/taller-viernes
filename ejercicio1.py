
# ejercicio1.py
import mysql.connector

# ═══════════════════════════════════════════════════════
# CONEXIÓN
# ═══════════════════════════════════════════════════════

def conectar():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'tienda'
    )

# ═══════════════════════════════════════════════════════
# TALLER 1.1 — Crear tabla productos
# ═══════════════════════════════════════════════════════

def crear_bd_tienda():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            precio FLOAT NOT NULL,
            stock INT DEFAULT 0,
            categoria VARCHAR(50)
        )
    ''')
    conexion.commit()
    print('Base de datos lista')
    print('Tabla productos creada')
    conexion.close()

crear_bd_tienda()

# ═══════════════════════════════════════════════════════
# TALLER 1.2 — Insertar productos
# ═══════════════════════════════════════════════════════

def insertar_producto(nombre, precio, stock, categoria):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, precio, stock, categoria)
        VALUES (%s, %s, %s, %s)
    ''', (nombre, precio, stock, categoria))
    conexion.commit()
    print(f'Producto {nombre} insertado correctamente')
    conexion.close()

insertar_producto('Laptop HP', 2500000, 10, 'Tecnologia')
insertar_producto('Mouse inalambrico', 85000, 50, 'Accesorios')
insertar_producto('Cuaderno universitario', 12000, 200, 'Papeleria')
insertar_producto('Audifonos Bluetooth', 320000, 25, 'Tecnologia')
insertar_producto('Mochila', 150000, 30, 'Accesorios')
