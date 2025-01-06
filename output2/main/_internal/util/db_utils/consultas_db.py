import os
import sys
import sqlite3


def obtener_conexion():
    # Verificar si estamos ejecutando el archivo como ejecutable (frozen) o en modo desarrollo
    if getattr(sys, 'frozen', False):  # Si estamos ejecutando el ejecutable
        base_path = sys._MEIPASS  # PyInstaller extrae los archivos en una carpeta temporal
    else:
        base_path = os.path.abspath('.')  # Ruta del directorio actual en modo desarrollo

    # Ruta de la base de datos
    db_path = os.path.join(base_path, 'database', 'Floristeria.db')
    
    # Conectar a la base de datos
    return sqlite3.connect(db_path)

def agregar_usuario(nombre, apellido, correo, contrasena):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        # Insertar el nuevo usuario en la tabla Usuarios
        cursor.execute("INSERT INTO Usuario (Nombre, Apellido, Correo, Contrasena) VALUES (?, ?, ?, ?)", 
                       (nombre, apellido, correo, contrasena))
        conn.commit()
        print("Usuario agregado exitosamente.")
    except sqlite3.IntegrityError:
        print("Error: El correo ya está registrado.")
    finally:
        conn.close()

def agregar_ventasP(fecha, hora, cliente, producto_vendido, cantidad, monto_total, metodo_de_pago, lugar_de_entrega, estatus):
    try:
        # Conectar a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Insertar datos en la tabla VentasP
        cursor.execute("""
            INSERT INTO Ventas (
                Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (fecha, hora, cliente, producto_vendido, cantidad, monto_total, metodo_de_pago, lugar_de_entrega, estatus))

        # Confirmar los cambios
        conn.commit()
        print("Registro agregado exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")
    finally:
        # Cerrar la conexión
        conn.close()    

def alterDB():
    # Conexión a la base de datos
    conn = obtener_conexion()
    cursor = conn.cursor()  # Crear un cursor para ejecutar comandos SQL

    # Crear la tabla Pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pedidos (
        Id_Pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente TEXT NOT NULL,
        Contacto TEXT NOT NULL,
        Producto TEXT NOT NULL,
        Cantidad INTEGER NOT NULL,
        Monto_total REAL NOT NULL,
        Metodo_de_pago TEXT NOT NULL,
        Fecha TEXT NOT NULL,
        Hora TEXT NOT NULL,
        Lugar_de_entrega TEXT,
        Notas TEXT NOT NULL,
        Estatus TEXT NOT NULL
    );
    """)

    # Confirmar cambios en la base de datos (usar el objeto de conexión)
    conn.commit()

    # Cerrar la conexión
    conn.close()

    print("La tabla 'VentasP' ha sido creada exitosamente.")

def mostrar_tablas():
    """Muestra todas las tablas existentes en la base de datos.

    Esta función consulta el catálogo de la base de datos para obtener una lista de todas las tablas
    y las imprime en la consola.
    """

    conn = obtener_conexion()
    cursor = conn.cursor()

    # Consulta para obtener los nombres de las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Obtener los resultados de la consulta
    tablas = cursor.fetchall()

    # Imprimir las tablas
    if tablas:
        print("Tablas en la base de datos:")
        for tabla in tablas:
            print(tabla[0])
    else:
        print("No se encontraron tablas en la base de datos.")

    conn.close()

def eliminar():
    try:
        # Conexión a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor()  # Crear un cursor para ejecutar comandos SQL
        
        # Paso 1: Crear la nueva tabla sin la columna 'Notas'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pedidos_nueva (
            Id_Pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            Cliente TEXT NOT NULL,
            Contacto TEXT NOT NULL,
            Producto TEXT NOT NULL,
            Cantidad INTEGER NOT NULL,
            Monto_total REAL NOT NULL,
            Metodo_de_pago TEXT NOT NULL,
            Fecha TEXT NOT NULL,
            Hora TEXT NOT NULL,
            Lugar_de_entrega TEXT,
            Estatus TEXT NOT NULL
        );
        """)
        
        # Paso 2: Copiar los datos de la tabla original a la nueva tabla
        cursor.execute("""
        INSERT INTO Pedidos_nueva (Id_Pedido, Cliente, Contacto, Producto, Cantidad, Monto_total, Metodo_de_pago, Fecha, Hora, Lugar_de_entrega, Estatus)
        SELECT Id_Pedido, Cliente, Contacto, Producto, Cantidad, Monto_total, Metodo_de_pago, Fecha, Hora, Lugar_de_entrega, Estatus
        FROM Pedidos;
        """)

        # Paso 3: Eliminar la tabla original
        cursor.execute("DROP TABLE Pedidos;")

        # Paso 4: Renombrar la nueva tabla a 'Pedidos'
        cursor.execute("ALTER TABLE Pedidos_nueva RENAME TO Pedidos;")
        
        # Confirmar los cambios
        conn.commit()
        print("Columna 'Notas' eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar la columna: {e}")
    finally:
        # Cerrar la conexión
        conn.close()

def xd():
    try:
        # Conexión a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor()  # Crear un cursor para ejecutar comandos SQL
        
        cursor.execute("""
        ALTER TABLE Pedidos ADD COLUMN Anticipo REAL;
        """)
    except Exception as e:
        print(f"Error al eliminar la columna: {e}")
    finally:
        # Cerrar la conexión
        conn.close()

# Ejemplo de cómo agregar un primer usuario
if __name__ == '__main__':
    #agregar_usuario("Estefania", "Gamiño Nuñez", "admin@admin.com", "1234")
    #mostrar_tablas()
    #xd()
    obtener_conexion()