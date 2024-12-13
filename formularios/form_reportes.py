import os
from tkinter import messagebox
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from util.db_utils.consultas_db import obtener_conexion
import tkinter as tk
from datetime import datetime, timedelta

class FormularioReportes():
    
    def __init__(self, panel_principal):
        def obtener_ruta_carpeta():
            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            carpeta_destino = os.path.join(escritorio, "Reportes y Tickets")
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            return carpeta_destino
        
        def generar_reporte_ventas():
            carpeta_destino = obtener_ruta_carpeta()
            nombre_pdf = os.path.join(carpeta_destino, "reporte_ventas.pdf")
            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Configuración de la fuente
            c.setFont("Helvetica-Bold", 12)

            # Título del reporte
            c.drawString(400, 550, "Reporte de Ventas")  # Ajustar la posición del título para la orientación horizontal

            # Encabezados de la tabla
            encabezados = ["ID", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"]

            # Definir las posiciones de las columnas y el tamaño de las celdas
            column_widths = [60, 90, 60, 120, 150, 90, 100, 100, 120, 100]  # Tamaño de las columnas
            y_position = 500  # Iniciar desde la parte superior

            # Dibujar los encabezados de la tabla
            c.setFont("Helvetica-Bold", 10)
            x_position = 30  # Posición inicial para las columnas
            for i, header in enumerate(encabezados):
                c.drawString(x_position + 5, y_position + 3, header)  # Dibujar los encabezados dentro de cada columna
                x_position += column_widths[i]  # Ajustar la posición para la siguiente columna

            # Dibujar una línea horizontal debajo del encabezado
            c.setStrokeColor(colors.black)
            c.line(30, y_position - 5, 1300, y_position - 5)

            y_position -= 20  # Ajustar la posición para las filas de datos

            # Obtener las ventas de la base de datos
            conn = obtener_conexion()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas")
                ventas = cursor.fetchall()
                conn.close()

                # Datos de ventas
                for venta in ventas:
                    # Convertir cada venta en una lista de cadenas
                    venta_str = [
                        f"{venta[0]}", f"{venta[1]}", f"{venta[2]}", f"{venta[3]}", 
                        f"{venta[4]}", f"{venta[5]}", f"{venta[6]}", f"{venta[7]}", 
                        f"{venta[8]}", f"{venta[9]}"
                    ]

                    # Dibujar cada fila de datos
                    x_position = 30  # Posición inicial para las columnas
                    for i, data in enumerate(venta_str):
                        c.drawString(x_position + 5, y_position + 3, data)  # Dibujar los datos de cada venta
                        x_position += column_widths[i]  # Ajustar la posición para la siguiente columna
                    
                    # Ajustar el espacio entre filas
                    y_position -= 20
                    if y_position < 100:  # Si se acerca al final de la página, crear una nueva página
                        c.showPage()  # Nueva página cuando no hay espacio suficiente
                        y_position = 550  # Reiniciar posición vertical
                        # Redibujar los encabezados
                        x_position = 30
                        for i, header in enumerate(encabezados):
                            c.drawString(x_position + 5, y_position + 3, header)
                            x_position += column_widths[i]
                        # Redibujar la línea horizontal del encabezado
                        c.setStrokeColor(colors.black)
                        c.line(30, y_position - 5, 1300, y_position - 5)
                        y_position -= 20  # Ajustar la posición para las siguientes filas

                # Guardar el archivo PDF
                c.save()
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente: {nombre_pdf}")
            else:
                messagebox.showerror("Error", "Error al conectar con la base de datos.")
        
        # Función para generar el reporte de ventas semanal
        def generar_reporte_semanal():
            carpeta_destino = obtener_ruta_carpeta()
            nombre_pdf = os.path.join(carpeta_destino, "reporte_semanal.pdf")
            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Configuración de la fuente
            c.setFont("Helvetica-Bold", 12)

            # Título del reporte
            c.drawString(400, 550, "Reporte de Ventas Semanal")

            # Encabezados de la tabla
            encabezados = ["ID", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"]

            # Definir las posiciones de las columnas y el tamaño de las celdas
            column_widths = [60, 90, 60, 120, 150, 90, 100, 100, 120, 100]
            y_position = 500  # Iniciar desde la parte superior

            # Dibujar los encabezados de la tabla
            c.setFont("Helvetica-Bold", 10)
            x_position = 30
            for i, header in enumerate(encabezados):
                c.drawString(x_position + 5, y_position + 3, header)
                x_position += column_widths[i]

            # Dibujar una línea horizontal debajo del encabezado
            c.setStrokeColor(colors.black)
            c.line(30, y_position - 5, 1300, y_position - 5)

            y_position -= 20

            # Obtener las ventas de la base de datos de la última semana
            conn = obtener_conexion()
            if conn:
                cursor = conn.cursor()

                # Fecha de inicio de la semana (7 días atrás)
                fecha_inicio = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas WHERE Fecha >= ?", (fecha_inicio,))
                ventas = cursor.fetchall()
                conn.close()

                # Datos de ventas
                for venta in ventas:
                    venta_str = [f"{venta[0]}", f"{venta[1]}", f"{venta[2]}", f"{venta[3]}", 
                                 f"{venta[4]}", f"{venta[5]}", f"{venta[6]}", f"{venta[7]}", 
                                 f"{venta[8]}", f"{venta[9]}"]

                    x_position = 30
                    for i, data in enumerate(venta_str):
                        c.drawString(x_position + 5, y_position + 3, data)
                        x_position += column_widths[i]

                    y_position -= 20
                    if y_position < 100:
                        c.showPage()
                        y_position = 550
                        x_position = 30
                        for i, header in enumerate(encabezados):
                            c.drawString(x_position + 5, y_position + 3, header)
                            x_position += column_widths[i]
                        c.setStrokeColor(colors.black)
                        c.line(30, y_position - 5, 1300, y_position - 5)
                        y_position -= 20

                c.save()
                messagebox.showinfo("Éxito", f"Reporte semanal generado: {nombre_pdf}")
            else:
                messagebox.showerror("Error", "Error al conectar con la base de datos.")

        # Función para generar el reporte de ventas mensual
        def generar_reporte_mensual():
            carpeta_destino = obtener_ruta_carpeta()
            nombre_pdf = os.path.join(carpeta_destino, "reporte_mensual.pdf")
            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Configuración de la fuente
            c.setFont("Helvetica-Bold", 12)

            # Título del reporte
            c.drawString(400, 550, "Reporte de Ventas Mensual")

            # Encabezados de la tabla
            encabezados = ["ID", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"]

            # Definir las posiciones de las columnas y el tamaño de las celdas
            column_widths = [60, 90, 60, 120, 150, 90, 100, 100, 120, 100]
            y_position = 500  # Iniciar desde la parte superior

            # Dibujar los encabezados de la tabla
            c.setFont("Helvetica-Bold", 10)
            x_position = 30
            for i, header in enumerate(encabezados):
                c.drawString(x_position + 5, y_position + 3, header)
                x_position += column_widths[i]

            # Dibujar una línea horizontal debajo del encabezado
            c.setStrokeColor(colors.black)
            c.line(30, y_position - 5, 1300, y_position - 5)

            y_position -= 20

            # Obtener las ventas de la base de datos del mes actual
            conn = obtener_conexion()
            if conn:
                cursor = conn.cursor()

                # Fecha de inicio del mes (primer día del mes)
                fecha_inicio = datetime.now().replace(day=1).strftime("%Y-%m-%d")

                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas WHERE Fecha >= ?", (fecha_inicio,))
                ventas = cursor.fetchall()
                conn.close()

                # Datos de ventas
                for venta in ventas:
                    venta_str = [f"{venta[0]}", f"{venta[1]}", f"{venta[2]}", f"{venta[3]}", 
                                 f"{venta[4]}", f"{venta[5]}", f"{venta[6]}", f"{venta[7]}", 
                                 f"{venta[8]}", f"{venta[9]}"]

                    x_position = 30
                    for i, data in enumerate(venta_str):
                        c.drawString(x_position + 5, y_position + 3, data)
                        x_position += column_widths[i]

                    y_position -= 20
                    if y_position < 100:
                        c.showPage()
                        y_position = 550
                        x_position = 30
                        for i, header in enumerate(encabezados):
                            c.drawString(x_position + 5, y_position + 3, header)
                            x_position += column_widths[i]
                        c.setStrokeColor(colors.black)
                        c.line(30, y_position - 5, 1300, y_position - 5)
                        y_position -= 20

                c.save()
                messagebox.showinfo("Éxito", f"Reporte mensual generado: {nombre_pdf}")
            else:
                messagebox.showerror("Error", "Error al conectar con la base de datos.")

         # Función para generar el reporte de productos vendidos
        
        def generar_reporte_productos_vendidos():
            carpeta_destino = obtener_ruta_carpeta()
            nombre_pdf = os.path.join(carpeta_destino, "reporte_productos_vendidos.pdf")
            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Configuración de la fuente
            c.setFont("Helvetica-Bold", 12)

            # Título del reporte
            c.drawString(400, 550, "Reporte de Productos Vendidos")

            # Encabezados de la tabla
            encabezados = ["Producto", "Cantidad Vendida", "Monto Total"]

            # Definir las posiciones de las columnas y el tamaño de las celdas
            column_widths = [300, 150, 150]  # Ajuste del tamaño de las columnas
            y_position = 500  # Iniciar desde la parte superior

            # Dibujar los encabezados de la tabla
            c.setFont("Helvetica-Bold", 10)
            x_position = 30
            for i, header in enumerate(encabezados):
                c.drawString(x_position + 5, y_position + 3, header)
                x_position += column_widths[i]

            # Dibujar una línea horizontal debajo del encabezado
            c.setStrokeColor(colors.black)
            c.line(30, y_position - 5, 1300, y_position - 5)

            y_position -= 20

            # Obtener los productos vendidos de la base de datos
            conn = obtener_conexion()
            if conn:
                cursor = conn.cursor()

                # Consulta para obtener productos, cantidad total y monto total
                cursor.execute("""
                    SELECT Producto_vendido, SUM(Cantidad), SUM(Monto_total) 
                    FROM Ventas 
                    GROUP BY Producto_vendido
                    ORDER BY SUM(Cantidad) DESC
                """)
                productos = cursor.fetchall()
                conn.close()

                # Datos de productos vendidos
                for producto in productos:
                    producto_str = [f"{producto[0]}", f"{producto[1]}", f"${producto[2]:.2f}"]

                    x_position = 30
                    for i, data in enumerate(producto_str):
                        c.drawString(x_position + 5, y_position + 3, data)
                        x_position += column_widths[i]

                    y_position -= 20
                    if y_position < 100:
                        c.showPage()
                        y_position = 550
                        x_position = 30
                        for i, header in enumerate(encabezados):
                            c.drawString(x_position + 5, y_position + 3, header)
                            x_position += column_widths[i]
                        c.setStrokeColor(colors.black)
                        c.line(30, y_position - 5, 1300, y_position - 5)
                        y_position -= 20

                c.save()
                messagebox.showinfo("Éxito", f"Reporte de productos vendidos generado: {nombre_pdf}")
            else:
                messagebox.showerror("Error", "Error al conectar con la base de datos.")

        # Crear barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Título
        etTitulo = tk.Label(panel_principal, text="Administración de Reportes", fg="black", bg="white", font=("Playfair Display", 28, "bold"))
        etTitulo.place(x=300, y=40)

        # Botones para generar los reportes
        boton_generar = tk.Button(panel_principal, text="Exportar Ventas", command=generar_reporte_ventas)
        boton_generar.config(bg="#9828E2", fg="white", font=("Inter", 12, "bold"), width=20)
        boton_generar.place(x=450, y=150)

        boton_generar_semanal = tk.Button(panel_principal, text="Generar Reporte Semanal", command=generar_reporte_semanal)
        boton_generar_semanal.config(bg="#9828E2", fg="white", font=("Inter", 12, "bold"), width=20)
        boton_generar_semanal.place(x=450, y=220)

        boton_generar_mensual = tk.Button(panel_principal, text="Generar Reporte Mensual", command=generar_reporte_mensual)
        boton_generar_mensual.config(bg="#9828E2", fg="white", font=("Inter", 12, "bold"), width=20)
        boton_generar_mensual.place(x=450, y=290)

        # Botón para generar el reporte de productos vendidos
        boton_generar_productos = tk.Button(panel_principal, text="Generar Reporte de Productos Vendidos", command=generar_reporte_productos_vendidos)
        boton_generar_productos.config(bg="#9828E2", fg="white", font=("Inter", 12, "bold"), width=35)
        boton_generar_productos.place(x=380, y=360)
