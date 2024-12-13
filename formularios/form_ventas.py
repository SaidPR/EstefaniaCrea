import sqlite3, os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from config import COLOR_PRINCIPAL
from util.db_utils.consultas_db import obtener_conexion
from fpdf import FPDF

class FormularioVentas():
    def __init__(self, panel_principal):
        
        # Función para obtener la lista de ventas desde la base de datos
        def obtener_ventas():
            conn = obtener_conexion()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas")
                ventas = cursor.fetchall()
                conn.close()
                return ventas
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
                return []

        # Actualizar la tabla con colores alternados
        def actualizar_tabla(tabla):
            for item in tabla.get_children():
                tabla.delete(item)  # Limpiar la tabla
            ventas = obtener_ventas()  # Obtener ventas de la base de datos
            for index, venta in enumerate(ventas):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                tabla.insert("", "end", values=venta, tags=(tag,))  # Agregar cada venta a la tabla

        # Función para eliminar un Venta a la base de datos
        def eliminar_venta(tabla):
            # Obtener la selección actual
            seleccion = tabla.selection()
            
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona una venta para eliminar.")
                return

            # Obtener el ID del producto desde la selección
            item = tabla.item(seleccion)
            venta_id = item['values'][0]  # El ID es el primer valor de la fila seleccionada

            # Confirmar la eliminación
            confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar la venta con ID {venta_id}?")

            if confirmacion:
                try:
                    # Conectar a la base de datos
                    conn = obtener_conexion()
                    cursor = conn.cursor()

                    # Eliminar el producto de la tabla "Inventario"
                    cursor.execute("DELETE FROM Ventas WHERE Id = ?", (venta_id,))

                    # Restablecer la secuencia del ID
                    cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='Ventas'")

                    # Confirmar cambios y cerrar conexión
                    conn.commit()
                    conn.close()

                    # Eliminar la fila de la tabla en la interfaz
                    tabla.delete(seleccion)

                    # Mostrar mensaje de éxito
                    messagebox.showinfo("Éxito", f"Venta con ID {venta_id} eliminado correctamente.")
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la venta. Error: {str(e)}")
 
        def facturar_venta(tabla):
            # Obtener la selección actual
            seleccion = tabla.selection()

            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona una venta para generar el ticket.")
                return

            # Obtener los datos de la fila seleccionada
            item = tabla.item(seleccion)
            venta_datos = item['values']  # Obtiene todos los valores de la fila seleccionada

            if not venta_datos:
                messagebox.showerror("Error", "No se pudo obtener la información de la venta seleccionada.")
                return

            # Crear la carpeta "Reportes y Tickets" en Documentos si no existe
            directorio_documentos = os.path.join(os.path.expanduser("~"), "Desktop")
            carpeta_destino = os.path.join(directorio_documentos, "Reportes y Tickets")

            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)

            # Crear el ticket en formato PDF
            try:
                pdf = FPDF()
                pdf.add_page()

                # Estilo y encabezado del ticket
                pdf.set_font("Arial", style='B', size=16)
                pdf.set_text_color(33, 37, 41)
                pdf.cell(0, 10, "ESTEFANIACREA - Ticket de Venta", ln=True, align="C")
                pdf.ln(5)
                pdf.set_font("Arial", style='I', size=12)
                pdf.cell(0, 10, "Gracias por su compra", ln=True, align="C")
                pdf.ln(10)

                # Información del cliente y venta
                pdf.set_font("Arial", size=12)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 10, f"Cliente: {venta_datos[3]}", ln=True)
                pdf.cell(0, 10, f"Fecha: {venta_datos[1]}", ln=True)
                pdf.cell(0, 10, f"Hora: {venta_datos[2]}", ln=True)
                pdf.ln(5)

                # Tabla de productos
                pdf.set_font("Arial", style='B', size=12)
                pdf.set_fill_color(200, 220, 255)
                pdf.cell(80, 10, "Producto", border=1, align="C", fill=True)
                pdf.cell(30, 10, "Cantidad", border=1, align="C", fill=True)
                pdf.cell(40, 10, "Precio", border=1, align="C", fill=True)
                pdf.cell(40, 10, "Total", border=1, align="C", fill=True)
                pdf.ln(10)

                pdf.set_font("Arial", size=12)
                pdf.cell(80, 10, venta_datos[4], border=1)
                pdf.cell(30, 10, str(venta_datos[5]), border=1, align="C")
                pdf.cell(40, 10, "-", border=1, align="C")  # Puedes agregar precio unitario si está disponible
                pdf.cell(40, 10, f"${float(venta_datos[6]):.2f}", border=1, align="C")
                pdf.ln(10)

                # Total y método de pago
                pdf.set_font("Arial", style='B', size=12)
                pdf.cell(0, 10, f"Monto Total: ${float(venta_datos[6]):.2f}", ln=True, align="R")
                pdf.cell(0, 10, f"Método de Pago: {venta_datos[7]}", ln=True, align="R")
                pdf.ln(10)

                # Información adicional
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, f"Lugar de Entrega: {venta_datos[8]}", ln=True)
                pdf.cell(0, 10, f"Estatus: {venta_datos[9]}", ln=True)

                # Mensaje final
                pdf.ln(10)
                pdf.set_font("Arial", style='I', size=10)
                pdf.cell(0, 10, "Favor de conservar este ticket como comprobante.", ln=True, align="C")

                # Guardar el archivo PDF en la carpeta
                archivo_pdf = os.path.join(carpeta_destino, f"ticket_venta_{venta_datos[0]}.pdf")
                pdf.output(archivo_pdf)

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", f"El ticket se generó correctamente: {archivo_pdf}")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el ticket. Error: {str(e)}")


        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Primer Label con texto
        self.labelTitulo = tk.Label(self.barra_superior, text="Ventas")
        self.labelTitulo.config(fg="#222d33", font=("Playfair Display", 30, "bold"), bg=COLOR_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True, anchor='w')

        # Crear el marco de la tabla dentro del contenedor
        tabla_frame = tk.Frame(panel_principal, bg="white")
        tabla_frame.place(x=10, y=150, width=1100, height=430)  # Ajustar el tamaño del marco

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
            columns=("Id", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"),
            show="headings",
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )
            # Aplicar zebra striping (colores alternos)
        tabla.tag_configure("oddrow", background="#E8E8E8")
        tabla.tag_configure("evenrow", background="#FFFFFF")

        # Encabezados y ajustes de las columnas
        tabla.heading("Id", text="ID")
        tabla.heading("Fecha", text="Fecha")
        tabla.heading("Hora", text="Hora")
        tabla.heading("Cliente", text="Cliente")
        tabla.heading("Producto", text="Producto vendido")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.heading("Monto", text="Monto total")
        tabla.heading("Pago", text="Método de pago")
        tabla.heading("Entrega", text="Lugar de entrega")
        tabla.heading("Estatus", text="Estatus")

        # Ajustar el ancho de las columnas
        tabla.column("Id", width=50, anchor="center")
        tabla.column("Fecha", width=80, anchor="center")
        tabla.column("Hora", width=70, anchor="center")
        tabla.column("Cliente", width=150, anchor="w")
        tabla.column("Producto", width=180, anchor="w")
        tabla.column("Cantidad", width=80, anchor="center")
        tabla.column("Monto", width=100, anchor="e")
        tabla.column("Pago", width=150, anchor="w")
        tabla.column("Entrega", width=180, anchor="w")
        tabla.column("Estatus", width=100, anchor="center")

        # Configurar las barras de desplazamiento
        scrollbar_x.config(command=tabla.xview)
        scrollbar_y.config(command=tabla.yview)

        tabla.pack(fill=BOTH, expand=True)

        # Creación del botón Actualizar
        def botonActualizar(text, command):
            # Crear el lienzo para el botón con las dimensiones adecuadas
            canvas = tk.Canvas(panel_principal, width=150, height=30, bg="#FFFFFF", highlightthickness=0)  
            canvas.place(x=300, y=70)  # Ajustar posición del lienzo

            # Dibuja las esquinas redondeadas (ajustadas para el tamaño del botón)
            canvas.create_oval(0, 0, 30, 30, fill="#005DE8", outline="#005DE8")  # Esquina superior izquierda
            canvas.create_oval(120, 0, 150, 30, fill="#005DE8", outline="#005DE8")  # Esquina superior derecha

            # Dibuja el cuerpo del botón
            canvas.create_rectangle(15, 0, 135, 30, fill="#005DE8", outline="#005DE8")  

            # Añade el texto al botón (centrado en el lienzo)
            canvas.create_text(75, 15, text=text, fill="white", font=("Inter", 10, "bold"), anchor="center")  

            # Vincula el evento de clic al comando proporcionado
            canvas.bind("<Button-1>", lambda e: command())

    # Creación del botón Editar
        def botonEliminar(text, command):
            # Crear el lienzo para el botón con las dimensiones adecuadas
            canvas = Canvas(panel_principal, width=150, height=30, bg="white", highlightthickness=0)  
            canvas.place(x=700, y=70)  # Ajustar posición del lienzo

            # Dibuja las esquinas redondeadas (ajustadas para el tamaño del botón)
            canvas.create_oval(0, 0, 30, 30, fill="#C83434", outline="#C83434")  # Esquina superior izquierda
            canvas.create_oval(120, 0, 150, 30, fill="#C83434", outline="#C83434")  # Esquina superior derecha

            # Dibuja el cuerpo del botón
            canvas.create_rectangle(15, 0, 135, 30, fill="#C83434", outline="#C83434")  

            # Añade el texto al botón (centrado en el lienzo)
            canvas.create_text(75, 15, text=text, fill="white", font=("Inter", 10, "bold"), anchor="center")  

            # Vincula el evento de clic al comando proporcionado
            canvas.bind("<Button-1>", lambda e: command())

    # Creación del botón Editar
        def botonFacturar(text, command):
            # Crear el lienzo para el botón con las dimensiones adecuadas
            canvas = Canvas(panel_principal, width=150, height=30, bg="white", highlightthickness=0)  
            canvas.place(x=500, y=70)  # Ajustar posición del lienzo

            # Dibuja las esquinas redondeadas (ajustadas para el tamaño del botón)
            canvas.create_oval(0, 0, 30, 30, fill="#9828E2", outline="#9828E2")  # Esquina superior izquierda
            canvas.create_oval(120, 0, 150, 30, fill="#9828E2", outline="#9828E2")  # Esquina superior derecha

            # Dibuja el cuerpo del botón
            canvas.create_rectangle(15, 0, 135, 30, fill="#9828E2", outline="#9828E2")  

            # Añade el texto al botón (centrado en el lienzo)
            canvas.create_text(75, 15, text=text, fill="white", font=("Inter", 10, "bold"), anchor="center")  

            # Vincula el evento de clic al comando proporcionado
            canvas.bind("<Button-1>", lambda e: command())

        # Crear el botón de Actualizar
        botonActualizar("Actualizar", lambda: actualizar_tabla(tabla)) 
        # Crear el botón de guardar producto
        botonEliminar("Eliminar", lambda: eliminar_venta(tabla))  # Llama a la función para eliminar la venta
        # Crear el botón de guardar producto
        botonFacturar("Ticket", lambda: facturar_venta(tabla))  # Llama a la función para eliminar la venta

        # Actualizar la tabla al cargar
        actualizar_tabla(tabla)
