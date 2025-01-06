import sqlite3
import tkinter as tk
from tkinter import BOTH, END, filedialog, messagebox, Canvas, Entry, Label, ttk, font
from PIL import Image, ImageTk
from util.db_utils.consultas_db import obtener_conexion  
from config import COLOR_PRINCIPAL

class FormularioCatalogo:
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal

        # Crear barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        etTitulo = Label(panel_principal, text="Inventario", fg="black", bg="white", font=("Playfair Display", 28, "bold"))
        etTitulo.place(x=30, y=40)

        # Campos de entrada
        self.etNom_entry = self.crear_campo(panel_principal, "Nombre:", 550, 10)
        self.etDescripcion_entry = self.crear_campo(panel_principal, "Descripción:", 550, 70)
        self.etPrecio_entry = self.crear_campo(panel_principal, "Precio unitario:", 850, 10)

        # Cuadro para la imagen
        self.imagen_label = tk.Label(panel_principal, text="Imagen", bg="#D9D9D9", width=20, height=10, relief="ridge")
        self.imagen_label.place(x=350, y=40)
        self.imagen_label.bind("<Button-1>", self.seleccionar_imagen)

        # Botones
        self.crear_boton("Añadir", self.add_producto, 570, 230, "#2DD22D")
        self.crear_boton("Actualizar", lambda: self.actualizar_tabla(tabla), 760, 230, "#005DE8")
        self.crear_boton("Editar", lambda: self.editar_prod(tabla), 760, 290, "#E2A128")
        self.crear_boton("Eliminar", lambda: self.eliminar_prod(tabla), 960, 230, "#C83434")
        self.crear_boton("Visualizar", lambda: self.ver_prod(tabla), 960, 290, "#9828E2") 

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
            columns=("Id_Prod", "Nombre", "Descripcion", "Precio"),
            show="headings",
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )

        # Aplicar zebra striping (colores alternos)
        tabla.tag_configure("oddrow", background="#E8E8E8")
        tabla.tag_configure("evenrow", background="#FFFFFF")

        # Encabezados y ajustes de las columnas
        tabla.heading("Id_Prod", text="ID")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Descripcion", text="Descripcion")
        tabla.heading("Precio", text="Precio")

        # Ajustar el ancho de las columnas
        tabla.column("Id_Prod", width=50, anchor="center")
        tabla.column("Nombre", width=80, anchor="center")
        tabla.column("Descripcion", width=70, anchor="center")
        tabla.column("Precio", width=150, anchor="w")
        
        # Configurar las barras de desplazamiento
        scrollbar_x.config(command=tabla.xview)
        scrollbar_y.config(command=tabla.yview)

        tabla.pack(fill=BOTH, expand=True)  

        # Actualizar la tabla al iniciar
        self.actualizar_tabla(tabla)

    def crear_campo(self, panel, texto, x, y):
        """Crea una etiqueta y un campo de entrada."""
        etiqueta = Label(panel, text=texto, fg="black", bg="white", font=("Playfair Display", 16, "italic"))
        etiqueta.place(x=x, y=y)
        entrada = Entry(panel, width=20, fg="black", bg="#D9D9D9", border=0, font=("Playfair Display", 14))
        entrada.place(x=x, y=y + 30)
        return entrada

    def seleccionar_imagen(self, event):
        """Abre el cuadro de diálogo para seleccionar una imagen."""
        ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif")]
        )
        if ruta_imagen:
            self.imagen_ruta = ruta_imagen
            self.mostrar_imagen(ruta_imagen)

    def mostrar_imagen(self, ruta):
        """Carga y muestra la imagen seleccionada."""
        try:
            img = Image.open(ruta)
            img = img.resize((150, 140), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.imagen_label.config(width=150, height=140, bg="gray", image=img_tk, text="")
            self.imagen_label.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
            
    def visualizar_imagen(self, ruta):
        """Carga y muestra la imagen seleccionada, reescalándola proporcionalmente a un tamaño máximo."""
        try:
            # Cargar la imagen desde la ruta
            img = Image.open(ruta)

            # Definir el tamaño máximo para la imagen (ajustar según lo que necesites)
            max_width = 250
            max_height = 250

            # Obtener las dimensiones originales de la imagen
            original_width, original_height = img.size

            # Calcular las nuevas dimensiones de la imagen proporcionalmente
            if original_width > original_height:
                ratio = max_width / original_width
                new_width = max_width
                new_height = int(original_height * ratio)
            else:
                ratio = max_height / original_height
                new_height = max_height
                new_width = int(original_width * ratio)

            # Redimensionar la imagen manteniendo las proporciones
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            # Si la imagen ya fue mostrada previamente, la actualizamos
            if hasattr(self, 'imagen_producto_label'):
                self.imagen_producto_label.config(image=img_tk)
                self.imagen_producto_label.image = img_tk
            else:
                # Si no existe, creamos el Label para mostrar la imagen
                self.imagen_producto_label = tk.Label(self.panel_principal, bg="gray", image=img_tk)
                # Posicionar la imagen debajo del botón Editar
                self.imagen_producto_label.place(x=760, y=330)  # Ajusta la Y según la posición deseada
                self.imagen_producto_label.image = img_tk  # Referencia para evitar que la imagen sea recolectada por el garbage collector
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

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

    def obtener_prods(self):
        """Obtiene la lista de proveedores desde la base de datos."""
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id_Prod, Nombre, Descripcion, Precio FROM Catalogo")
            proveedores = cursor.fetchall()
            conn.close()
            return proveedores
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return []

    # Función para agregar un producto a la base de datos
    def add_producto(self):
        """Añade un producto a la base de datos."""
        # Obtener los datos de los campos de entrada
        nombre = self.etNom_entry.get().strip()
        descripcion = self.etDescripcion_entry.get().strip()
        precio = self.etPrecio_entry.get().strip()
        ruta = getattr(self, 'imagen_ruta', None)  # Ruta de la imagen seleccionada

        # Validar que los campos obligatorios no estén vacíos
        if not nombre or not descripcion or not precio:
            messagebox.showwarning("Advertencia", "Por favor, llena todos los campos obligatorios.")
            return

        try:
            # Validar y convertir el precio
            precio = float(precio)

            # Conectar a la base de datos
            conn = obtener_conexion()  # Implementa esta función para tu base de datos
            if conn:
                cursor = conn.cursor()

                # Insertar datos en la tabla `Catalogo`
                cursor.execute('''
                    INSERT INTO Catalogo (Nombre, Descripcion, Precio, RutaImg)
                    VALUES (?, ?, ?, ?)
                ''', (nombre, descripcion, precio, ruta))

                # Confirmar los cambios
                conn.commit()
                conn.close()

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", "Producto agregado con éxito")

                # Limpiar campos y restablecer la interfaz
                self.etNom_entry.delete(0, tk.END)
                self.etDescripcion_entry.delete(0, tk.END)
                self.etPrecio_entry.delete(0, tk.END)
                # Restablecer el cuadro de imagen a su estado original
                self.imagen_label.config(
                    image='',  # Eliminar imagen
                    text="Imagen",  # Texto por defecto
                    bg="#D9D9D9",  # Color de fondo original
                    width=20,  # Ancho original en caracteres
                    height=10,  # Alto original en caracteres
                    relief="ridge"  # Estilo del borde original
                )
                delattr(self, 'imagen_ruta')  # Eliminar atributo de ruta de imagen si existe
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        except ValueError:
            # Manejar errores de conversión
            messagebox.showerror("Error de entrada", "Por favor, ingresa un valor válido para el precio.")
        except Exception as e:
            # Manejar otros errores
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
  
    def actualizar_tabla(self, tabla):
        """Actualiza la tabla con los datos de los proveedores."""
        for item in tabla.get_children():
            tabla.delete(item)  # Limpiar la tabla
        proveedores = self.obtener_prods()  # Obtener productos de la base de datos
        for index, proveedor in enumerate(proveedores):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tabla.insert('', 'end', values=proveedor, tags=(tag,))  # Agregar cada proveedor a la tabla
     
    # Función para eliminar un proveedor a la base de datos
    def eliminar_prod(self, tabla):
        # Obtener la selección actual
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")
            return
        
        # Obtener el ID del proveedor desde la selección
        item = tabla.item(seleccion)
        prov_id = item['values'][0]
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar eliminación.", f"¿Estás seguro de que deseas eliminar el producto con ID {prov_id}?")
    
        if confirmacion:
            try:
                # Conectar a la BD
                conn = obtener_conexion()
                cursor = conn.cursor()
                # Eliminar el producto de la tabla "Inventario"
                cursor.execute("DELETE FROM Catalogo WHERE Id_Prod = ?", (prov_id,))

                # Restablecer la secuencia del ID
                cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='Catalogo'")

                # Confirmar cambios y cerrar conexión
                conn.commit()
                conn.close()

                # Eliminar la fila de la tabla en la interfaz
                tabla.delete(seleccion)

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", f"Producto con ID {prov_id} eliminado correctamente.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar la venta. Error: {str(e)}")
   
    def editar_prod(self, tabla):
        """Edita un proveedor seleccionado."""
        # Obtener la selección actual
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un proveedor para editar.")
            return
        
        # Obtener los datos del proveedor seleccionado
        item = tabla.item(seleccion)
        self.producto_id = item['values'][0]  # ID del proveedor seleccionado
        nombre_prod = item['values'][1]
        desc_prod = item['values'][2]
        precio_prod = item['values'][3]

        # Rellenar los campos de entrada con los datos del proveedor seleccionado
        self.etNom_entry.delete(0, END)
        self.etNom_entry.insert(0, nombre_prod)
        self.etDescripcion_entry.delete(0, END)
        self.etDescripcion_entry.insert(0, desc_prod)
        self.etPrecio_entry.delete(0, END)
        self.etPrecio_entry.insert(0, precio_prod)

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
        # Validar que haya un producto en edición
        if self.producto_id is None:
            messagebox.showerror("Error", "No hay producto seleccionado para guardar.")
            return

        # Obtener los valores de los campos de entrada
        nombre = self.etNom_entry.get().strip()
        desc = self.etDescripcion_entry.get().strip()
        precio = self.etPrecio_entry.get().strip()

        if not nombre or not desc or not precio:
            messagebox.showwarning("Advertencia", "Por favor, llena todos los campos.")
            return

        try:
            # Conectar a la base de datos y actualizar los datos
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Catalogo
                SET Nombre = ?, Descripcion = ?, Precio = ?
                WHERE Id_Prod = ?
            ''', (nombre, desc, precio, self.producto_id))
            conn.commit()
            conn.close()

            # Mostrar mensaje de éxito y actualizar la tabla
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self.actualizar_tabla(tabla)

            # Limpiar los campos y restablecer el estado
            self.etNom_entry.delete(0, END)
            self.etDescripcion_entry.delete(0, END)
            self.etPrecio_entry.delete(0, END)
            self.producto_id = None

            # Eliminar el botón "Modificar"
            if hasattr(self, "btn_modificar"):
                self.btn_modificar.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")
           
    def ver_prod(self, tabla):
        """Muestra la imagen del producto seleccionado debajo del botón."""
        # Obtener la selección actual
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para visualizar.")
            return

        # Obtener el ID del producto desde la selección
        item = tabla.item(seleccion)
        prod_id = item['values'][0]  # ID del producto seleccionado

        # Conectar a la base de datos para obtener la ruta de la imagen
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT RutaImg FROM Catalogo WHERE Id_Prod = ?", (prod_id,))
            resultado = cursor.fetchone()

            if resultado:
                ruta_imagen = resultado[0]
                self.visualizar_imagen(ruta_imagen)
            else:
                messagebox.showwarning("Advertencia", "No se encontró la imagen del producto.")
            conn.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
