import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from config import COLOR_PRINCIPAL
from util.db_utils.consultas_db import obtener_conexion
from formularios.subForms.formAñadirPedido import AnadirPedido

class FormularioPedidos:
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal

        # Crear barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        etTitulo = Label(panel_principal, text="Pedidos", fg="black", bg="white", font=("Playfair Display", 30, "bold"))
        etTitulo.place(x=500, y=30)

        # Botones
        self.crear_boton("Añadir", self.openForm, 100, 130, "#2DD22D")
        self.crear_boton("Actualizar", lambda: self.actualizar_tabla(tabla), 300, 130, "#005DE8")
        self.crear_boton("Liberar", lambda: self.liberar_pedido(tabla), 500, 130, "#9828E2")
        #self.crear_boton("Editar", lambda: self.editar_pedido(tabla), 700, 130, "#E2A128")
        self.crear_boton("Eliminar", lambda: self.eliminar_pedido(tabla), 700, 130, "#C83434")

         # Crear el marco de la tabla dentro del contenedor
        tabla_frame = tk.Frame(panel_principal, bg="white")
        tabla_frame.place(x=10, y=180, width=1100, height=430)  # Ajustar el tamaño del marco

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
            columns=("Id_Pedido", "Cliente", "Contacto", "Producto", "Cantidad", "Monto_total", "Metodo_de_pago", "Fecha", "Hora", "Lugar_de_entrega", "Notas", "Estatus"),
            show="headings",
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )
            # Aplicar zebra striping (colores alternos)
        tabla.tag_configure("oddrow", background="#E8E8E8")
        tabla.tag_configure("evenrow", background="#FFFFFF")

        # Encabezados y ajustes de las columnas
        tabla.heading("Id_Pedido", text="ID")
        tabla.heading("Cliente", text="Cliente")
        tabla.heading("Contacto", text="Contacto")
        tabla.heading("Producto", text="Producto")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.heading("Monto_total", text="Monto total")
        tabla.heading("Metodo_de_pago", text="Método de pago")
        tabla.heading("Fecha", text="Fecha")
        tabla.heading("Hora", text="Hora")
        tabla.heading("Lugar_de_entrega", text="Entrega")
        tabla.heading("Notas", text="Notas")
        tabla.heading("Estatus", text="Estatus")

        # Ajustar el ancho de las columnas
        tabla.column("Id_Pedido", width=50, anchor="center")
        tabla.column("Cliente", width=80, anchor="center")
        tabla.column("Contacto", width=70, anchor="center")
        tabla.column("Producto", width=150, anchor="w")
        tabla.column("Cantidad", width=180, anchor="w")
        tabla.column("Monto_total", width=80, anchor="center")
        tabla.column("Metodo_de_pago", width=100, anchor="e")
        tabla.column("Fecha", width=150, anchor="w")
        tabla.column("Notas", width=180, anchor="w")
        tabla.column("Estatus", width=100, anchor="center")

        # Configurar las barras de desplazamiento
        scrollbar_x.config(command=tabla.xview)
        scrollbar_y.config(command=tabla.yview)

        tabla.pack(fill=BOTH, expand=True)

        # Actualizar la tabla al cargar
        self.actualizar_tabla(tabla)

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
                    
    # Función para obtener la lista de pedidos desde la base de datos
    def obtener_pedidos(self):
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id_Pedido, Cliente, Contacto, Producto, Cantidad, Monto_total, Metodo_de_pago, Fecha, Hora, Lugar_de_entrega, Notas, Estatus FROM Pedidos")
            pedidos = cursor.fetchall()
            conn.close()
            return pedidos
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return []

    # Actualizar la tabla con colores alternados
    def actualizar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)  # Limpiar la tabla
        pedidos = self.obtener_pedidos()  # Obtener pedidos de la base de datos
        for index, pedido in enumerate(pedidos):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tabla.insert("", "end", values=pedido, tags=(tag,))  # Agregar cada pedido a la tabla

    # Función para eliminar un pedido a la base de datos
    def eliminar_pedido(self, tabla):
        # Obtener la selección actual
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una pedido para eliminar.")
            return

        # Obtener el ID del producto desde la selección
        item = tabla.item(seleccion)
        pedido_id = item['values'][0]  # El ID es el primer valor de la fila seleccionada

        # Confirmar la eliminación
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar la pedido con ID {pedido_id}?")

        if confirmacion:
            try:
                # Conectar a la base de datos
                conn = obtener_conexion()
                cursor = conn.cursor()

                # Eliminar el producto de la tabla "Inpedidorio"
                cursor.execute("DELETE FROM Pedidos WHERE Id_Pedido = ?", (pedido_id,))

                # Restablecer la secuencia del ID
                cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='Pedidos'")

                # Confirmar cambios y cerrar conexión
                conn.commit()
                conn.close()

                # Eliminar la fila de la tabla en la interfaz
                tabla.delete(seleccion)

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", f"Pedido con ID {pedido_id} eliminado correctamente.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar la pedido. Error: {str(e)}")

    # Función para liberar un pedido
    def liberar_pedido(self, tabla):
        # Obtener la selección actual
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para liberar.")
            return

        # Obtener el ID del pedido desde la selección
        item = tabla.item(seleccion)
        pedido_id = item['values'][0]  # El ID es el primer valor de la fila seleccionada

        # Obtener los detalles del pedido
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pedidos WHERE Id_Pedido = ?", (pedido_id,))
            pedido = cursor.fetchone()

            if pedido:
                # Confirmar la acción
                confirmacion = messagebox.askyesno("Confirmar Liberación", f"¿Estás seguro de que deseas liberar el pedido con ID {pedido_id}?")

                if confirmacion:
                    try:
                        # Insertar el pedido en la tabla "Ventas"
                        cursor.execute("""
                            INSERT INTO Ventas (Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            pedido[7],  # Fecha
                            pedido[8],  # Hora
                            pedido[1],  # Cliente
                            pedido[3],  # Producto
                            pedido[4],  # Cantidad
                            pedido[5],  # Monto_total
                            pedido[6],  # Metodo_de_pago
                            pedido[9],  # Lugar_de_entrega
                            "Vendido"   # Estatus
                        ))

                        # Actualizar el estatus en la tabla "Pedidos" a "Vendido"
                        cursor.execute("UPDATE Pedidos SET Estatus = 'Vendido' WHERE Id_Pedido = ?", (pedido_id,))

                        # Eliminar el pedido de la tabla "Pedidos"
                        cursor.execute("DELETE FROM Pedidos WHERE Id_Pedido = ?", (pedido_id,))

                        # Confirmar cambios y cerrar conexión
                        conn.commit()
                        conn.close()

                        # Eliminar la fila de la tabla en la interfaz
                        tabla.delete(seleccion)

                        # Mostrar mensaje de éxito
                        messagebox.showinfo("Éxito", f"Pedido con ID {pedido_id} liberado y registrado como venta correctamente.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"No se pudo liberar el pedido. Error: {str(e)}")
            else:
                messagebox.showerror("Error", "No se encontró el pedido.")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    # Función para editar un pedido
    def editar_pedido(self, tabla):
        # Obtener la selección actual
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para editar.")
            return

        # Obtener el ID del pedido desde la selección
        item = tabla.item(seleccion)
        pedido_id = item['values'][0]  # El ID es el primer valor de la fila seleccionada

        # Obtener los detalles del pedido
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pedidos WHERE Id_Pedido = ?", (pedido_id,))
            pedido = cursor.fetchone()

            if pedido:
                # Abrir el formulario de "Añadir" con los datos del pedido
                AnadirPedido(pedido, es_editar=True)
            else:
                messagebox.showerror("Error", "No se encontró el pedido.")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")


    def openForm(self):
        AnadirPedido()

        

