import sqlite3
import os

def crear_base_de_datos():
    # Ruta para la base de datos
    db_path = os.path.join('database', 'Floristeria.db')
    
    # Crear directorio si no existe
    if not os.path.exists('database'):
        os.makedirs('database')
    
    # Conexión a la base de datos (se crea el archivo .db si no existe)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Script de creación de tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        Id_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,          
        Apellido TEXT NOT NULL,   
        Correo TEXT NOT NULL UNIQUE,
        Contrasena TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Proveedores (
        Id_Proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Proveedor TEXT NOT NULL,
        Telefono TEXT NOT NULL,
        Direccion TEXT NOT NULL
    )
    ''')
    # Confirmar cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print("Base de datos creada exitosamente en", db_path)

# Ejecutar la función para crear la base de datos
if __name__ == '__main__':
    crear_base_de_datos()
