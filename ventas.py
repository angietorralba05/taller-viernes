# ventas.py
import mysql.connector

# ═══════════════════════════════════════════════════════
# CONEXIÓN
# ═══════════════════════════════════════════════════════

def conectar():
    return mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = '',
        database = 'ventas'
    )

# ═══════════════════════════════════════════════════════
# CREAR TABLAS
# ═══════════════════════════════════════════════════════

def crear_modelo_ventas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id        INT          PRIMARY KEY AUTO_INCREMENT,
            nombre    VARCHAR(100) NOT NULL,
            correo    VARCHAR(100) UNIQUE NOT NULL,
            telefono  VARCHAR(20),
            ciudad    VARCHAR(50)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id        INT          PRIMARY KEY AUTO_INCREMENT,
            nombre    VARCHAR(100) NOT NULL,
            precio    FLOAT        NOT NULL,
            stock     INT          DEFAULT 0,
            categoria VARCHAR(50)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id          INT   PRIMARY KEY AUTO_INCREMENT,
            fecha       DATE  DEFAULT (CURRENT_DATE),
            cantidad    INT   NOT NULL,
            total       FLOAT NOT NULL,
            cliente_id  INT   NOT NULL,
            producto_id INT   NOT NULL,
            FOREIGN KEY (cliente_id)  REFERENCES clientes(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    conexion.commit()
    conexion.close()
    print('Modelo de ventas creado correctamente')

crear_modelo_ventas()

# ═══════════════════════════════════════════════════════
# INSERTAR DATOS DE PRUEBA
# ═══════════════════════════════════════════════════════

def insertar_datos_prueba():
    conexion = conectar()
    cursor = conexion.cursor()

    clientes = [
        ('Laura Jimenez',  'laura@mail.com',  '3001234567', 'Bogota'),
        ('Pedro Sanchez',  'pedro@mail.com',  '3119876543', 'Medellin'),
        ('Diana Morales',  'diana@mail.com',  '3204567890', 'Cali'),
    ]
    for c in clientes:
        cursor.execute('''
            INSERT IGNORE INTO clientes (nombre, correo, telefono, ciudad)
            VALUES (%s, %s, %s, %s)
        ''', c)

    productos = [
        ('Laptop HP',          2500000, 20, 'Tecnologia'),
        ('Mouse inalambrico',    85000, 50, 'Accesorios'),
        ('Audifonos Bluetooth', 320000, 30, 'Tecnologia'),
        ('Mochila',             150000, 40, 'Accesorios'),
    ]
    for p in productos:
        cursor.execute('''
            INSERT IGNORE INTO productos (nombre, precio, stock, categoria)
            VALUES (%s, %s, %s, %s)
        ''', p)

    conexion.commit()
    conexion.close()
    print('Datos de prueba insertados')

insertar_datos_prueba()

# ═══════════════════════════════════════════════════════
# CLIENTES
# ═══════════════════════════════════════════════════════

def agregar_cliente():
    print('\n--- NUEVO CLIENTE ---')
    nombre   = input('Nombre: ').strip()
    correo   = input('Correo: ').strip()
    telefono = input('Telefono: ').strip()
    ciudad   = input('Ciudad: ').strip()
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, correo, telefono, ciudad)
            VALUES (%s, %s, %s, %s)
        ''', (nombre, correo, telefono, ciudad))
        conexion.commit()
        conexion.close()
        print(f'✓ Cliente {nombre} registrado correctamente')
    except mysql.connector.IntegrityError:
        print('✗ Error: ese correo ya esta registrado')

def listar_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY nombre')
    filas = cursor.fetchall()
    conexion.close()
    if not filas:
        print('No hay clientes registrados')
        return
    print(f"\n{'ID':<4} {'Nombre':<20} {'Correo':<25} {'Telefono':<15} {'Ciudad'}")
    print('-' * 75)
    for f in filas:
        print(f'{f[0]:<4} {f[1]:<20} {f[2]:<25} {f[3]:<15} {f[4]}')

# ═══════════════════════════════════════════════════════
# PRODUCTOS
# ═══════════════════════════════════════════════════════

def agregar_producto():
    print('\n--- NUEVO PRODUCTO ---')
    nombre    = input('Nombre: ').strip()
    precio    = float(input('Precio: '))
    stock     = int(input('Stock: '))
    categoria = input('Categoria: ').strip()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, precio, stock, categoria)
        VALUES (%s, %s, %s, %s)
    ''', (nombre, precio, stock, categoria))
    conexion.commit()
    conexion.close()
    print(f'✓ Producto {nombre} registrado correctamente')

def listar_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM productos ORDER BY nombre')
    filas = cursor.fetchall()
    conexion.close()
    if not filas:
        print('No hay productos registrados')
        return
    print(f"\n{'ID':<4} {'Nombre':<25} {'Precio':>12} {'Stock':>6} {'Categoria'}")
    print('-' * 60)
    for f in filas:
        print(f'{f[0]:<4} {f[1]:<25} ${f[2]:>10,.0f} {f[3]:>6} {f[4]}')

# ═══════════════════════════════════════════════════════
# VENTAS
# ═══════════════════════════════════════════════════════

def registrar_venta():
    listar_clientes()
    listar_productos()
    try:
        cliente_id  = int(input('\nID del cliente: '))
        producto_id = int(input('ID del producto: '))
        cantidad    = int(input('Cantidad: '))
    except ValueError:
        print('Valor invalido')
        return

    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute('SELECT nombre, precio, stock FROM productos WHERE id = %s',
                       (producto_id,))
        producto = cursor.fetchone()
        if producto is None:
            raise ValueError('Producto no encontrado')
        nombre_prod, precio, stock_actual = producto
        if stock_actual < cantidad:
            raise ValueError(f'Stock insuficiente. Disponible: {stock_actual}')
        total = precio * cantidad
        cursor.execute('''
            INSERT INTO ventas (cantidad, total, cliente_id, producto_id)
            VALUES (%s, %s, %s, %s)
        ''', (cantidad, total, cliente_id, producto_id))
        cursor.execute('''
            UPDATE productos SET stock = stock - %s WHERE id = %s
        ''', (cantidad, producto_id))
        conexion.commit()
        print(f'✓ Venta registrada: {cantidad}x {nombre_prod} = ${total:,.0f}')
    except (ValueError, mysql.connector.Error) as e:
        conexion.rollback()
        print(f'✗ Error: {e}')
    finally:
        conexion.close()

# ═══════════════════════════════════════════════════════
# REPORTES
# ═══════════════════════════════════════════════════════

def reporte_ventas_detallado():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT v.id, v.fecha, c.nombre, c.ciudad,
               p.nombre, v.cantidad, p.precio, v.total
        FROM ventas v
        INNER JOIN clientes  c ON v.cliente_id  = c.id
        INNER JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
    ''')
    ventas = cursor.fetchall()
    conexion.close()
    if not ventas:
        print('No hay ventas registradas')
        return
    print(f"\n{'ID':>3} {'Fecha':<12} {'Cliente':<18} {'Producto':<18} {'Cant':>4} {'Total':>12}")
    print('-' * 72)
    total_general = 0
    for v in ventas:
        print(f'{v[0]:>3} {str(v[1]):<12} {v[2]:<18} {v[4]:<18} {v[5]:>4} ${v[7]:>10,.0f}')
        total_general += v[7]
    print('=' * 72)
    print(f'{"TOTAL GENERAL":>55} ${total_general:>10,.0f}')

def reportes_estadisticos():
    conexion = conectar()
    cursor = conexion.cursor()
    print('\n===== ESTADÍSTICAS DE VENTAS =====')
    cursor.execute('SELECT SUM(total) FROM ventas')
    total = cursor.fetchone()[0] or 0
    cursor.execute('SELECT AVG(total) FROM ventas')
    promedio = cursor.fetchone()[0] or 0
    cursor.execute('SELECT MAX(total) FROM ventas')
    maxima = cursor.fetchone()[0] or 0
    cursor.execute('SELECT MIN(total) FROM ventas')
    minima = cursor.fetchone()[0] or 0
    print(f'Total vendido:       ${total:>12,.0f}')
    print(f'Promedio por venta:  ${promedio:>12,.0f}')
    print(f'Venta más alta:      ${maxima:>12,.0f}')
    print(f'Venta más baja:      ${minima:>12,.0f}')
    print('\n--- Ventas por ciudad ---')
    cursor.execute('''
        SELECT c.ciudad, COUNT(v.id), SUM(v.total)
        FROM ventas v
        INNER JOIN clientes c ON v.cliente_id = c.id
        GROUP BY c.ciudad
        ORDER BY SUM(v.total) DESC
    ''')
    for fila in cursor.fetchall():
        print(f'  {fila[0]:<15} {fila[1]:>3} ventas   ${fila[2]:>10,.0f}')
    print('\n--- Top 3 productos ---')
    cursor.execute('''
        SELECT p.nombre, SUM(v.cantidad)
        FROM ventas v
        INNER JOIN productos p ON v.producto_id = p.id
        GROUP BY p.id
        ORDER BY SUM(v.cantidad) DESC
        LIMIT 3
    ''')
    for i, fila in enumerate(cursor.fetchall(), 1):
        print(f'  {i}. {fila[0]:<20} {fila[1]:>5} unidades')
    conexion.close()

# ═══════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════

def menu():
    while True:
        print('\n===== SISTEMA DE VENTAS =====')
        print('1. Agregar cliente')
        print('2. Ver clientes')
        print('3. Agregar producto')
        print('4. Ver productos')
        print('5. Registrar venta')
        print('6. Ver reporte de ventas')
        print('7. Ver estadisticas')
        print('0. Salir')
        opcion = input('\nSeleccione: ').strip()

        if   opcion == '1': agregar_cliente()
        elif opcion == '2': listar_clientes()
        elif opcion == '3': agregar_producto()
        elif opcion == '4': listar_productos()
        elif opcion == '5': registrar_venta()
        elif opcion == '6': reporte_ventas_detallado()
        elif opcion == '7': reportes_estadisticos()
        elif opcion == '0':
            print('Hasta luego')
            break
        else: print('Opcion no valida')

menu()