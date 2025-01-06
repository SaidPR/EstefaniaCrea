import sqlite3
import tkinter as tk
from tkinter import BOTH, END, ttk, messagebox, Canvas, Entry, Label
from util.db_utils.consultas_db import obtener_conexion  
from config import COLOR_PRINCIPAL

class FormularioProv:
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
   
        # Crear barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Etiqueta Proveedores
        etTitulo = Label(panel_principal, text="Proveedores", fg="black", bg="white", font=("Playfair Display", 30, "bold"))
        etTitulo.place(x=30, y=40)

        # Campos de entrada
        self.etNom_entry = self.crear_campo(panel_principal, "Nombre:", 550, 10)
        self.etContacto_entry = self.crear_campo(panel_principal, "Teléfono:", 550, 70)
        self.etDireccion = self.crear_campo(panel_principal, "Dirección:", 850, 10)

        # Botones
        self.crear_boton("Añadir", self.add_prov, 350, 170, "#2DD22D")
        self.crear_boton("Actualizar", lambda: self.actualizar_tabla(tabla), 550, 170, "#005DE8")
        self.crear_boton("Editar", lambda: self.editar_prov(tabla), 750, 170, "#E2A128")
        self.crear_boton("Eliminar", lambda: self.eliminar_prov(tabla), 950, 170, "#C83434")

        # Crear el marco de la tabla dentro del contenedor
        tabla_frame = tk.Frame(panel_principal, bg="white")
        tabla_frame.place(x=10, y=220, width=560, height=430)  # Ajustar el tamaño del marco
        
        # Crear las barras de desplazamiento
        scrollbar_x = tk.Scrollbar(tabla_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y = tk.Scrollbar(tabla_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        
        # Crear y personalizar el estilo de la tabla
        style = ttk.Style()
        style.theme_use("default")  # Usa el tema base
        style.configure("Treeview", 
                        background="#F2F2F2", 
                        foreground="black", 
                        rowheight=25, 
                        fieldbackground="#FFFFFF", 
                        font=("Inter", 10))
        style.configure("Treeview.Heading", 
                        background=COLOR_PRINCIPAL, 
                        foreground="black", 
                        font=("Inter", 11, "bold"))
        # Alternar colores en las filas
        style.map("Treeview", 
                background=[("selected", "#005DE8")], 
                foreground=[("selected", "white")])
        
        # Crear la tabla para mostrar productos
        tabla = ttk.Treeview(
            tabla_frame,
            columns=("Id_Proveedor", "Nombre_Proveedor", "Telefono", "Direccion"),
            show="headings",
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )

        # Aplicar zebra striping (colores alternos)
        tabla.tag_configure("oddrow", background="#E8E8E8")
        tabla.tag_configure("evenrow", background="#FFFFFF")

        # Encabezados y ajustes de las columnas
        tabla.heading("Id_Proveedor", text="ID")
        tabla.heading("Nombre_Proveedor", text="Nombre")
        tabla.heading("Telefono", text="Teléfono")
        tabla.heading("Direccion", text="Dirección")

        # Ajustar el ancho de las columnas
        tabla.column("Id_Proveedor", width=50, anchor="center")
        tabla.column("Nombre_Proveedor", width=80, anchor="center")
        tabla.column("Telefono", width=70, anchor="center")
        tabla.column("Direccion", width=150, anchor="w")
        
        # Configurar las barras de desplazamiento
        scrollbar_x.config(command=tabla.xview)
        scrollbar_y.config(command=tabla.yview)

        tabla.pack(fill=BOTH, expand=True)  

        # Actualizar la tabla al iniciar
        self.actualizar_tabla(tabla)

    # Campo de entrada de datos
    def crear_campo(self, panel, texto, x, y):
        """Crea una etiqueta y un campo de entrada."""
        etiqueta = Label(panel, text=texto, fg="black", bg="white", font=("Playfair Display", 16, "italic"))
        etiqueta.place(x=x, y=y)
        entrada = Entry(panel, width=20, fg="black", bg="#D9D9D9", border=0, font=("Playfair Display", 14))
        entrada.place(x=x, y=y + 30)
        return entrada
    
    def crear_boton(self, texto, command, x, y, color):
        """Crea un botón con esquinas redondeadas."""
        canvas = Canvas(self.panel_principal, width=150, height=30, bg="white", highlightthickness=0)
        canvas.place(x=x, y=y)

        # Esquinas redondeadas
        canvas.create_oval(0, 0, 30, 30, fill=color, outline=color)
        canvas.create_oval(120, 0, 150, 30, fill=color, outline=color)
        canvas.create_rectangle(15, 0, 135, 30, fill=color, outline=color)

        # Texto del botón
        canvas.create_text(75, 15, text=texto, fill="white", font=("Inter", 10, "bold"), anchor="center")

        # Vincula el clic al comando
        canvas.bind("<Button-1>", lambda e: command())
        
    def obtener_provs(self):
        """Obtiene la lista de proveedores desde la base de datos."""
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id_Proveedor, Nombre_Proveedor, Telefono, Direccion FROM Proveedores")
            proveedores = cursor.fetchall()
            conn.close()
            return proveedores
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return []

    def actualizar_tabla(self, tabla):
        """Actualiza la tabla con los datos de los proveedores."""
        for item in tabla.get_children():
            tabla.delete(item)  # Limpiar la tabla
        proveedores = self.obtener_provs()  # Obtener productos de la base de datos
        for index, proveedor in enumerate(proveedores):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tabla.insert('', 'end', values=proveedor, tags=(tag,))  # Agregar cada proveedor a la tabla
        
    # Función para agregar un proveedor a la base de datos
    def add_prov(self):
        """Añade un proveedor a la base de datos."""
        # Obtener los datos de los campos de entrada
        nombre = self.etNom_entry.get().strip()
        contacto = self.etContacto_entry.get().strip()
        direccion = self.etDireccion.get().strip()

        # Validar que los campos obligatorios no estén vacíos
        if not nombre or not contacto or not direccion:
            messagebox.showwarning("Advertencia", "Por favor, llena todos los campos obligatorios.")
            return

        try:
            # Conectar a la base de datos
            conn = obtener_conexion()  # Implementa esta función para tu base de datos
            if conn:
                cursor = conn.cursor()

                # Insertar datos en la tabla `Proveedores`
                cursor.execute('''
                    INSERT INTO Proveedores (Nombre_Proveedor, Telefono, Direccion)
                    VALUES (?, ?, ?)
                ''', (nombre, contacto, direccion))

                # Confirmar los cambios
                conn.commit()
                conn.close()

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", "Proveedor agregado con éxito")

                # Limpiar campos y restablecer la interfaz
                self.etNom_entry.delete(0, tk.END)
                self.etContacto_entry.delete(0, tk.END)
                self.etDireccion.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        except ValueError:
            # Manejar errores de conversión
            messagebox.showerror("Error de entrada", "Por favor, ingresa un valor válido para el precio.")
        except Exception as e:
            # Manejar otros errores
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
            
    # Función para eliminar un proveedor a la base de datos
    def eliminar_prov(self, tabla):
        # Obtener la selección actual
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un proveedor para eliminar.")
            return
        
        # Obtener el ID del proveedor desde la selección
        item = tabla.item(seleccion)
        prov_id = item['values'][0]
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar eliminación.", f"¿Estás seguro de que deseas eliminar el proveedor con ID {prov_id}?")
    
        if confirmacion:
            try:
                # Conectar a la BD
                conn = obtener_conexion()
                cursor = conn.cursor()
                # Eliminar el producto de la tabla "Inventario"
                cursor.execute("DELETE FROM Proveedores WHERE Id_Proveedor = ?", (prov_id,))

                # Restablecer la secuencia del ID
                cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='Proveedores'")

                # Confirmar cambios y cerrar conexión
                conn.commit()
                conn.close()

                # Eliminar la fila de la tabla en la interfaz
                tabla.delete(seleccion)

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", f"Proveedor con ID {prov_id} eliminado correctamente.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar la venta. Error: {str(e)}")
 
    def editar_prov(self, tabla):
        """Edita un proveedor seleccionado."""
        # Obtener la selección actual
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un proveedor para editar.")
            return
        
        # Obtener los datos del proveedor seleccionado
        item = tabla.item(seleccion)
        self.proveedor_id = item['values'][0]  # ID del proveedor seleccionado
        nombre_prov = item['values'][1]
        telefono_prov = item['values'][2]
        direccion_prov = item['values'][3]

        # Rellenar los campos de entrada con los datos del proveedor seleccionado
        self.etNom_entry.delete(0, END)
        self.etNom_entry.insert(0, nombre_prov)
        self.etContacto_entry.delete(0, END)
        self.etContacto_entry.insert(0, telefono_prov)
        self.etDireccion.delete(0, END)
        self.etDireccion.insert(0, direccion_prov)

        # Crear o actualizar el botón "Modificar"
        if hasattr(self, "btn_modificar"):
            self.btn_modificar.destroy()  # Elimina el botón si ya existe
        
        # Crear el botón con el mismo diseño
        self.btn_modificar = Canvas(self.panel_principal, width=150, height=30, bg="white", highlightthickness=0)
        self.btn_modificar.place(x=850, y=100)

        # Esquinas redondeadas
        self.btn_modificar.create_oval(0, 0, 30, 30, fill="#25A925", outline="#25A925")
        self.btn_modificar.create_oval(120, 0, 150, 30, fill="#25A925", outline="#25A925")
        self.btn_modificar.create_rectangle(15, 0, 135, 30, fill="#25A925", outline="#25A925")

        # Texto del botón
        self.btn_modificar.create_text(75, 15, text="Modificar", fill="white", font=("Inter", 10, "bold"), anchor="center")

        # Vincular el clic al comando
        self.btn_modificar.bind("<Button-1>", lambda e: self.guardar_edicion(tabla))

    def guardar_edicion(self, tabla):
        """Guarda los cambios realizados en el proveedor editado."""
        # Validar que haya un proveedor en edición
        if self.proveedor_id is None:
            messagebox.showerror("Error", "No hay proveedor seleccionado para guardar.")
            return

        # Obtener los valores de los campos de entrada
        nombre = self.etNom_entry.get().strip()
        telefono = self.etContacto_entry.get().strip()
        direccion = self.etDireccion.get().strip()

        if not nombre or not telefono or not direccion:
            messagebox.showwarning("Advertencia", "Por favor, llena todos los campos.")
            return

        try:
            # Conectar a la base de datos y actualizar los datos
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Proveedores
                SET Nombre_Proveedor = ?, Telefono = ?, Direccion = ?
                WHERE Id_Proveedor = ?
            ''', (nombre, telefono, direccion, self.proveedor_id))
            conn.commit()
            conn.close()

            # Mostrar mensaje de éxito y actualizar la tabla
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            self.actualizar_tabla(tabla)

            # Limpiar los campos y restablecer el estado
            self.etNom_entry.delete(0, END)
            self.etContacto_entry.delete(0, END)
            self.etDireccion.delete(0, END)
            self.proveedor_id = None

            # Eliminar el botón "Modificar"
            if hasattr(self, "btn_modificar"):
                self.btn_modificar.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {e}")

