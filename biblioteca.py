# ejercicio3.py
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = '',
        database = 'libreria'
    )

def crear_modelo():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id       INT          PRIMARY KEY AUTO_INCREMENT,
            nombre   VARCHAR(100) NOT NULL,
            correo   VARCHAR(100) UNIQUE NOT NULL,
            telefono VARCHAR(20),
            ciudad   VARCHAR(50)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id        INT          PRIMARY KEY AUTO_INCREMENT,
            titulo    VARCHAR(200) NOT NULL,
            autor     VARCHAR(100) NOT NULL,
            precio    FLOAT        NOT NULL,
            stock     INT          DEFAULT 0,
            categoria VARCHAR(50)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id         INT   PRIMARY KEY AUTO_INCREMENT,
            fecha      DATE  DEFAULT (CURRENT_DATE),
            cantidad   INT   NOT NULL,
            total      FLOAT NOT NULL,
            cliente_id  INT  NOT NULL,
            libro_id    INT  NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (libro_id)   REFERENCES libros(id)
        )
    ''')
    conexion.commit()
    conexion.close()
    print('Tablas creadas correctamente')

crear_modelo()

# ═══════════════════════════════════════════════════════
# DATOS DE PRUEBA
# ═══════════════════════════════════════════════════════

def insertar_datos_prueba():
    conexion = conectar()
    cursor = conexion.cursor()

    clientes = [
        ('Laura Jimenez',  'laura@mail.com',  '3001234567', 'Bogota'),
        ('Pedro Sanchez',  'pedro@mail.com',  '3119876543', 'Medellin'),
        ('Diana Morales',  'diana@mail.com',  '3204567890', 'Cali'),
        ('Andres Castro',  'andres@mail.com', '3055551234', 'Bogota'),
        ('Sofia Herrera',  'sofia@mail.com',  '3177778888', 'Barranquilla'),
    ]
    for c in clientes:
        cursor.execute('''
            INSERT IGNORE INTO clientes (nombre, correo, telefono, ciudad)
            VALUES (%s, %s, %s, %s)
        ''', c)

    libros = [
        ('Cien Anos de Soledad',       'Gabriel Garcia Marquez', 45000,  20, 'Novela'),
        ('El Principito',              'Antoine de Saint-Exupery', 25000, 30, 'Infantil'),
        ('Harry Potter T1',            'J.K. Rowling',           55000,  15, 'Fantasia'),
        ('Don Quijote de la Mancha',   'Miguel de Cervantes',    60000,  10, 'Clasico'),
        ('El Alquimista',              'Paulo Coelho',           35000,  25, 'Novela'),
        ('1984',                       'George Orwell',          40000,  18, 'Distopia'),
    ]
    for l in libros:
        cursor.execute('''
            INSERT IGNORE INTO libros (titulo, autor, precio, stock, categoria)
            VALUES (%s, %s, %s, %s, %s)
        ''', l)

    conexion.commit()

    # Ventas de prueba
    ventas = [
        (1, 1, 2),
        (1, 3, 1),
        (1, 5, 3),
        (1, 2, 1),
        (2, 2, 2),
        (2, 4, 1),
        (3, 1, 1),
        (3, 6, 2),
        (4, 3, 2),
        (4, 5, 1),
        (5, 2, 3),
        (5, 1, 1),
    ]
    for cliente_id, libro_id, cantidad in ventas:
        cursor.execute('SELECT precio, stock FROM libros WHERE id = %s', (libro_id,))
        libro = cursor.fetchone()
        if libro and libro[1] >= cantidad:
            total = libro[0] * cantidad
            cursor.execute('''
                INSERT IGNORE INTO ventas (cantidad, total, cliente_id, libro_id)
                VALUES (%s, %s, %s, %s)
            ''', (cantidad, total, cliente_id, libro_id))
            cursor.execute('''
                UPDATE libros SET stock = stock - %s WHERE id = %s
            ''', (cantidad, libro_id))

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
        print(f'✓ Cliente {nombre} registrado')
    except mysql.connector.IntegrityError:
        print('✗ Error: ese correo ya existe')

def listar_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY nombre')
    filas = cursor.fetchall()
    conexion.close()
    if not filas:
        print('No hay clientes')
        return
    print(f"\n{'ID':<4} {'Nombre':<20} {'Correo':<25} {'Telefono':<15} {'Ciudad'}")
    print('-' * 75)
    for f in filas:
        print(f'{f[0]:<4} {f[1]:<20} {f[2]:<25} {f[3]:<15} {f[4]}')

# ═══════════════════════════════════════════════════════
# LIBROS
# ═══════════════════════════════════════════════════════

def agregar_libro():
    print('\n--- NUEVO LIBRO ---')
    titulo    = input('Titulo: ').strip()
    autor     = input('Autor: ').strip()
    precio    = float(input('Precio: '))
    stock     = int(input('Stock: '))
    categoria = input('Categoria: ').strip()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO libros (titulo, autor, precio, stock, categoria)
        VALUES (%s, %s, %s, %s, %s)
    ''', (titulo, autor, precio, stock, categoria))
    conexion.commit()
    conexion.close()
    print(f'✓ Libro "{titulo}" registrado')

def listar_libros():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM libros ORDER BY titulo')
    filas = cursor.fetchall()
    conexion.close()
    if not filas:
        print('No hay libros')
        return
    print(f"\n{'ID':<4} {'Titulo':<30} {'Autor':<20} {'Precio':>12} {'Stock':>6} {'Categoria'}")
    print('-' * 80)
    for f in filas:
        print(f'{f[0]:<4} {f[1]:<30} {f[2]:<20} ${f[3]:>10,.0f} {f[4]:>6} {f[5]}')

# ═══════════════════════════════════════════════════════
# REGISTRAR VENTA CON TRANSACCIÓN
# ═══════════════════════════════════════════════════════

def registrar_venta():
    listar_clientes()
    listar_libros()
    try:
        cliente_id = int(input('\nID del cliente: '))
        libro_id   = int(input('ID del libro: '))
        cantidad   = int(input('Cantidad: '))
    except ValueError:
        print('Valor invalido')
        return

    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute('SELECT titulo, precio, stock FROM libros WHERE id = %s',
                       (libro_id,))
        libro = cursor.fetchone()
        if libro is None:
            raise ValueError('Libro no encontrado')
        titulo, precio, stock_actual = libro
        if stock_actual < cantidad:
            raise ValueError(f'Stock insuficiente. Disponible: {stock_actual}')
        total = precio * cantidad
        cursor.execute('''
            INSERT INTO ventas (cantidad, total, cliente_id, libro_id)
            VALUES (%s, %s, %s, %s)
        ''', (cantidad, total, cliente_id, libro_id))
        cursor.execute('''
            UPDATE libros SET stock = stock - %s WHERE id = %s
        ''', (cantidad, libro_id))
        conexion.commit()
        print(f'✓ Venta registrada: {cantidad}x "{titulo}" = ${total:,.0f}')
    except (ValueError, mysql.connector.Error) as e:
        conexion.rollback()
        print(f'✗ Error: {e}')
        print('Ningún cambio fue guardado (rollback)')
    finally:
        conexion.close()

# ═══════════════════════════════════════════════════════
# REPORTE VENTAS POR MES
# ═══════════════════════════════════════════════════════

def reporte_ventas_por_mes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT
            DATE_FORMAT(fecha, '%Y-%m') AS mes,
            COUNT(*) AS num_ventas,
            SUM(total) AS total_mes
        FROM ventas
        GROUP BY DATE_FORMAT(fecha, '%Y-%m')
        ORDER BY mes DESC
    ''')
    filas = cursor.fetchall()
    conexion.close()
    print(f"\n{'Mes':<10} {'Ventas':>7} {'Total':>15}")
    print('-' * 35)
    if not filas:
        print('No hay ventas registradas')
        return
    for f in filas:
        print(f'{f[0]:<10} {f[1]:>7} ${f[2]:>12,.0f}')

# ═══════════════════════════════════════════════════════
# LIBROS MÁS VENDIDOS
# ═══════════════════════════════════════════════════════

def libros_mas_vendidos(top_n=3):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT l.titulo, l.autor, SUM(v.cantidad) AS total_unidades
        FROM ventas v
        INNER JOIN libros l ON v.libro_id = l.id
        GROUP BY l.id
        ORDER BY total_unidades DESC
        LIMIT %s
    ''', (top_n,))
    filas = cursor.fetchall()
    conexion.close()
    print(f'\n--- Top {top_n} libros más vendidos ---')
    if not filas:
        print('No hay ventas registradas')
        return
    for i, f in enumerate(filas, 1):
        print(f'  {i}. {f[0]:<30} {f[1]:<20} {f[2]:>5} unidades')

# ═══════════════════════════════════════════════════════
# CLIENTES FRECUENTES
# ═══════════════════════════════════════════════════════

def clientes_frecuentes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT c.nombre, c.ciudad, COUNT(v.id) AS num_compras, SUM(v.total) AS total
        FROM ventas v
        INNER JOIN clientes c ON v.cliente_id = c.id
        GROUP BY c.id
        HAVING COUNT(v.id) > 3
        ORDER BY num_compras DESC
    ''')
    filas = cursor.fetchall()
    conexion.close()
    print('\n--- Clientes frecuentes (más de 3 compras) ---')
    if not filas:
        print('No hay clientes con más de 3 compras')
        return
    for f in filas:
        print(f'  {f[0]:<20} {f[1]:<12} {f[2]:>3} compras   ${f[3]:>10,.0f}')

# ═══════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════

def menu():
    while True:
        print('\n===== LIBRERÍA UNIVERSITARIA =====')
        print('1. Agregar cliente')
        print('2. Ver clientes')
        print('3. Agregar libro')
        print('4. Ver libros')
        print('5. Registrar venta')
        print('6. Reporte ventas por mes')
        print('7. Libros más vendidos')
        print('8. Clientes frecuentes')
        print('0. Salir')
        opcion = input('\nSeleccione: ').strip()

        if   opcion == '1': agregar_cliente()
        elif opcion == '2': listar_clientes()
        elif opcion == '3': agregar_libro()
        elif opcion == '4': listar_libros()
        elif opcion == '5': registrar_venta()
        elif opcion == '6': reporte_ventas_por_mes()
        elif opcion == '7':
            try:
                n = int(input('¿Top cuántos libros? (default 3): ') or 3)
            except ValueError:
                n = 3
            libros_mas_vendidos(n)
        elif opcion == '8': clientes_frecuentes()
        elif opcion == '0':
            print('Hasta luego')
            break
        else: print('Opcion no valida')

menu()