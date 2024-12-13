#CODIGO PARA MOSTRAR CONTENIDO DE LAS TABLAS
import sqlite3
from util.db_utils.consultas_db import obtener_conexion

def cargar_usuarios():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Cambiar consulta para seleccionar todos los campos de la tabla Usuario
        cursor.execute("SELECT * FROM Usuario")
        usuarios = cursor.fetchall()

        # Imprimir encabezados
        print(f"{'ID Usuario':<10} {'Nombre':<20} {'Apellido':<20} {'Correo':<30} {'Contraseña':<30}")
        print("="*110)  # Línea separadora

        # Iterar sobre los registros y mostrarlos
        for usuario in usuarios:
            id_usuario, nombre, apellido, correo, contrasena = usuario  # Desempaquetar cada registro
            print(f"{id_usuario:<10} {nombre:<20} {apellido:<20} {correo:<30} {contrasena:<30}")  # Imprimir cada usuario

    except Exception as e:
        print(f"Ocurrió un error al cargar los usuarios: {e}")

    finally:
        conn.close()  # Asegurarse de que la conexión se cierra correctamente

def cargar_proveedores():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Cambiar consulta para seleccionar todos los campos de la tabla Usuario
        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()

        # Imprimir encabezados
        print(f"{'ID Proveedor':<10} {'Nombre':<20} {'Telefono':<20} {'Direccion':<30}")
        print("="*110)  # Línea separadora

        # Iterar sobre los registros y mostrarlos
        for proveedor in proveedores:
            id_proveedor, nombre, telefono, direccion = proveedor  # Desempaquetar cada registro
            print(f"{id_proveedor:<10} {nombre:<20} {telefono:<20} {direccion:<30}")  # Imprimir cada proveedor

    except Exception as e:
        print(f"Ocurrió un error al cargar los proveedores: {e}")

    finally:
        conn.close()  # Asegurarse de que la conexión se cierra correctamente

def cargar_inv():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Cambiar la consulta para seleccionar solo las columnas necesarias
        cursor.execute("SELECT Id_Proveedor, Nombre_Proveedor, Telefono, Direccion FROM Proveedores")
        productos = cursor.fetchall()

        # Imprimir encabezados
        print(f"{'Id_Prov':<10} {'Nombre':<20} {'Telefono':<20} {'Direccion':<30} ")
        print("="*110)  # Línea separadora

        # Iterar sobre los registros y mostrarlos
        for producto in productos:
            id_producto, nombre, telefono, direccion = producto  # Desempaquetar cada registro
            print(f"{id_producto:<10} {nombre:<20} {telefono:<20} {direccion:<30}")  # Imprimir cada producto

    except Exception as e:
        print(f"Ocurrió un error al cargar el catalogo: {e}")

    finally:
        conn.close()  # Asegurarse de que la conexión se cierra correctamente

def agregar_proveedor(nombre, descripcion, precio, ruta):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        #Insertar el nuevo proveedor en la tabla Proveedores
        cursor.execute(''' 
                    INSERT INTO Catalogo (Nombre, Descripcion, Precio, RutaImg)
                    VALUES (?, ?, ?, ?)
                ''', (nombre, descripcion, precio, ruta))
        conn.commit()
        print("Proveedor agregado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: El proveedor ya está registrado.")
    finally:
        conn.close()

def cargar_pedidos():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Cambiar consulta para seleccionar todos los campos de la tabla Pedidos
        cursor.execute("SELECT * FROM Pedidos")
        pedidos = cursor.fetchall()

        # Imprimir encabezados
        print(f"{'ID Pedido':<10} {'Cliente':<20} {'Contacto':<20} {'Producto(s)':<40} {'Cantidad':<10} {'Monto Total':<15} {'Método de Pago':<20} {'Fecha':<15} {'Hora':<10} {'Lugar de Entrega':<25} {'Notas':<30} {'Estatus':<10}")
        print("="*155)  # Línea separadora

        # Iterar sobre los registros y mostrarlos
        for pedido in pedidos:
            id_pedido, cliente, contacto, productos, cantidad, monto_total, metodo_pago, fecha, hora, lugar_entrega, notas, estado = pedido  # Desempaquetar cada registro
            print(f"{id_pedido:<10} {cliente:<20} {contacto:<20} {productos:<40} {cantidad:<10} {monto_total:<15.2f} {metodo_pago:<20} {fecha:<15} {hora:<10} {lugar_entrega:<25} {notas:<30} {estado:<10}")  # Imprimir cada pedido

    except Exception as e:
        print(f"Ocurrió un error al cargar los pedidos: {e}")

    finally:
        conn.close()  # Asegurarse de que la conexión se cierra correctamente


if __name__ == "__main__":
    #agregar_proveedor("Hola", "Hola", 12.0, "C:/Users/ramos/OneDrive/Imágenes/SQLite.jpg")
    #cargar_usuarios()
    #cargar_inv()
    #cargar_proveedores()
    cargar_pedidos()