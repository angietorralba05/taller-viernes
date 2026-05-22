import mysql.connector

# ═══════════════════════════════════════════════════════
# CONEXIÓN
# ═══════════════════════════════════════════════════════

def conectar():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'universidad'
    )

# ═══════════════════════════════════════════════════════
# MÓDULO 1 — Conectar y crear tabla
# ═══════════════════════════════════════════════════════

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            correo VARCHAR(100) UNIQUE NOT NULL,
            edad INT,
            promedio FLOAT DEFAULT 0.0
        )
    ''')
    conexion.commit()
    print('Tabla estudiantes creada exitosamente')
    conexion.close()

crear_tabla()

# ═══════════════════════════════════════════════════════
# MÓDULO 1 — Insertar datos
# ═══════════════════════════════════════════════════════

def insertar_estudiante(nombre, apellido, correo, edad, promedio):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO estudiantes (nombre, apellido, correo, edad, promedio)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nombre, apellido, correo, edad, promedio))
    conexion.commit()
    print(f'Estudiante {nombre} {apellido} insertado correctamente')
    conexion.close()

insertar_estudiante('Maria', 'Lopez', 'maria@uni.edu', 19, 4.2)
insertar_estudiante('Carlos', 'Ramirez', 'carlos@uni.edu', 20, 3.8)
insertar_estudiante('Ana', 'Torres', 'ana@uni.edu', 18, 4.7)

# ═══════════════════════════════════════════════════════
# MÓDULO 2 — Leer datos
# ═══════════════════════════════════════════════════════

def obtener_todos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM estudiantes')
    estudiantes = cursor.fetchall()
    conexion.close()
    return estudiantes

def obtener_por_id(id_estudiante):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM estudiantes WHERE id = %s', (id_estudiante,))
    estudiante = cursor.fetchone()
    conexion.close()
    return estudiante

def mostrar_estudiantes():
    print('=' * 65)
    print(f'{"ID":<5} {"NOMBRE":<15} {"APELLIDO":<15} {"CORREO":<20} {"PROMEDIO"}')
    print('=' * 65)
    for e in obtener_todos():
        print(f'{e[0]:<5} {e[1]:<15} {e[2]:<15} {e[3]:<20} {e[5]:.1f}')
    print('=' * 65)
    print(f'Total: {len(obtener_todos())} estudiantes')

mostrar_estudiantes()

# ═══════════════════════════════════════════════════════
# MÓDULO 2 — Actualizar datos
# ═══════════════════════════════════════════════════════

def actualizar_promedio(id_estudiante, nuevo_promedio):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE estudiantes
        SET promedio = %s
        WHERE id = %s
    ''', (nuevo_promedio, id_estudiante))
    if cursor.rowcount > 0:
        print(f'Promedio actualizado para el estudiante ID {id_estudiante}')
    else:
        print(f'No se encontro estudiante con ID {id_estudiante}')
    conexion.commit()
    conexion.close()

def actualizar_datos_completos(id_est, nombre, apellido, edad):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE estudiantes
        SET nombre = %s, apellido = %s, edad = %s
        WHERE id = %s
    ''', (nombre, apellido, edad, id_est))
    conexion.commit()
    print('Datos actualizados correctamente')
    conexion.close()

actualizar_promedio(1, 4.5)
actualizar_datos_completos(2, 'Carlos Alberto', 'Ramirez', 21)

# ═══════════════════════════════════════════════════════
# MÓDULO 2 — Eliminar datos
# ═══════════════════════════════════════════════════════

def eliminar_estudiante(id_estudiante):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT nombre FROM estudiantes WHERE id = %s', (id_estudiante,))
    resultado = cursor.fetchone()
    if resultado is None:
        print(f'Error: no existe estudiante con ID {id_estudiante}')
        conexion.close()
        return
    confirmacion = input(f'Eliminar a {resultado[0]}? (s/n): ')
    if confirmacion.lower() == 's':
        cursor.execute('DELETE FROM estudiantes WHERE id = %s', (id_estudiante,))
        conexion.commit()
        print(f'Estudiante {resultado[0]} eliminado')
    else:
        print('Operacion cancelada')
    conexion.close()

eliminar_estudiante(3)

# ═══════════════════════════════════════════════════════
# TALLER 2.1 — Sistema CRUD con menú
# ═══════════════════════════════════════════════════════

def crear_estudiante():
    print('\n--- NUEVO ESTUDIANTE ---')
    nombre = input('Nombre: ').strip()
    apellido = input('Apellido: ').strip()
    correo = input('Correo: ').strip()
    edad = int(input('Edad: '))
    promedio = float(input('Promedio (0.0 - 5.0): '))
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            'INSERT INTO estudiantes (nombre, apellido, correo, edad, promedio) VALUES (%s, %s, %s, %s, %s)',
            (nombre, apellido, correo, edad, promedio))
        conexion.commit()
        conexion.close()
        print(f'Estudiante {nombre} registrado exitosamente')
    except mysql.connector.IntegrityError:
        print('Error: ese correo ya esta registrado')

def listar_estudiantes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM estudiantes ORDER BY apellido')
    filas = cursor.fetchall()
    conexion.close()
    if not filas:
        print('No hay estudiantes registrados')
        return
    print(f"\n{'ID':<4} {'Nombre':<15} {'Apellido':<15} {'Correo':<22} {'Edad':>4} {'Prom':>5}")
    print('-' * 70)
    for f in filas:
        print(f'{f[0]:<4} {f[1]:<15} {f[2]:<15} {f[3]:<22} {f[4]:>4} {f[5]:>5.1f}')
    print(f'Total: {len(filas)} estudiantes')

def menu():
    while True:
        print('\n===== SISTEMA DE ESTUDIANTES =====')
        print('1. Agregar estudiante')
        print('2. Ver todos los estudiantes')
        print('3. Salir')
        opcion = input('Seleccione: ')
        if opcion == '1': crear_estudiante()
        elif opcion == '2': listar_estudiantes()
        elif opcion == '3':
            print('Hasta luego')
            break
        else: print('Opcion no valida')

menu()
