import os
import tempfile
from tkinter import messagebox
import webbrowser
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from util.db_utils.consultas_db import obtener_conexion
import tkinter as tk
from datetime import datetime, timedelta

class FormularioReportes():
    
    def __init__(self, panel_principal):
        # Función para generar el reporte de ventas 
        def generar_reporte_ventas():
            # Crear archivo temporal para vista previa
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            nombre_pdf = temp_file.name

            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Encabezado con logotipo
            logotipo_path = "imgs/logoEmp.jpg"
            if os.path.exists(logotipo_path):
                try:
                    c.drawImage(logotipo_path, 30, 530, width=80, height=80)
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"No se pudo cargar el logotipo: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "No se encontró el archivo del logotipo.")

            # Título y subtítulo del reporte
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkblue)
            c.drawString(300, 550, "Reporte de Ventas")

            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            c.drawString(300, 530, "Resumen de ventas con detalles por cliente y totales.")

            # Dibujar línea debajo del encabezado
            c.setStrokeColor(colors.black)
            c.setLineWidth(2)
            c.line(30, 520, 800, 520)

            # Encabezados de la tabla
            encabezados = ["ID", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"]
            column_widths = [50, 80, 50, 120, 140, 60, 80, 90, 100, 90]
            y_position = 480

            # Dibujar encabezado de la tabla
            def dibujar_encabezados():
                x_position = 30
                c.setFont("Helvetica-Bold", 10)
                for i, header in enumerate(encabezados):
                    c.setFillColor(colors.whitesmoke)
                    c.rect(x_position, y_position, column_widths[i], 20, fill=True, stroke=False)
                    c.setFillColor(colors.black)
                    c.drawString(x_position + 5, y_position + 5, header)
                    x_position += column_widths[i]
                c.line(30, y_position - 5, 800, y_position - 5)

            dibujar_encabezados()
            y_position -= 25

            # Conexión a la base de datos y consulta
            conn = obtener_conexion()
            total_ventas = 0

            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas")
                ventas = cursor.fetchall()
                conn.close()

                # Dibujar datos de las ventas
                for venta in ventas:
                    venta_str = [str(dato) for dato in venta]
                    x_position = 30
                    for i, data in enumerate(venta_str):
                        c.drawString(x_position + 5, y_position + 5, data)
                        x_position += column_widths[i]
                    total_ventas += float(venta[6])
                    y_position -= 20

                    # Verificar si se necesita una nueva página
                    if y_position < 100:
                        c.showPage()
                        y_position = 480
                        dibujar_encabezados()

                # Mostrar el total de las ventas
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.darkblue)
                c.drawString(600, y_position - 30, "Total de Ventas:")
                c.setFillColor(colors.black)
                c.drawString(700, y_position - 30, f"${total_ventas:.2f}")
                c.line(600, y_position - 35, 800, y_position - 35)

                # Pie de página con fecha
                c.setFont("Helvetica", 8)
                c.setFillColor(colors.grey)
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M")


                c.drawString(30, 40, f"Generado el {fecha} - Página 1")  # Se podría calcular el número de página dinámicamente

                # Guardar el archivo PDF
                c.save()

                # Mostrar vista previa del PDF
                webbrowser.open_new(temp_file.name)

            else:
                os.remove(temp_file.name)
                messagebox.showerror("Error", "Error al conectar con la base de datos.")
        
        # Función para generar el reporte de ventas semanal
        def generar_reporte_semanal():
            # Crear archivo temporal para vista previa
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            nombre_pdf = temp_file.name

            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Encabezado con logotipo
            logotipo_path = "imgs/logoEmp.jpg"
            if os.path.exists(logotipo_path):
                try:
                    c.drawImage(logotipo_path, 30, 530, width=80, height=80)  # Ajustar posición y tamaño del logotipo
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"No se pudo cargar el logotipo: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "No se encontró el archivo del logotipo.")

            # Título del reporte
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkblue)
            c.drawString(300, 550, "Reporte de Ventas Semanal")  # Ajustar posición del título

            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            c.drawString(300, 530, "Ventas realizadas durante la última semana.")  # Subtítulo

            # Dibujar una línea debajo del encabezado
            c.setStrokeColor(colors.black)
            c.setLineWidth(2)
            c.line(30, 520, 800, 520)

            # Encabezados de la tabla
            c.setFont("Helvetica-Bold", 10)
            encabezados = ["ID", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"]
            column_widths = [60, 90, 60, 120, 150, 90, 100, 100, 120, 100]
            y_position = 480
            x_position = 30

            for i, header in enumerate(encabezados):
                c.setFillColor(colors.whitesmoke)
                c.rect(x_position, y_position, column_widths[i], 20, fill=True, stroke=False)
                c.setFillColor(colors.black)
                c.drawString(x_position + 5, y_position + 5, header)
                x_position += column_widths[i]

            # Dibujar línea debajo de los encabezados
            c.setStrokeColor(colors.black)
            c.line(30, y_position - 5, 800, y_position - 5)
            y_position -= 25

            # Conexión a la base de datos
            conn = obtener_conexion()
            total_ventas = 0  # Variable para la sumatoria total

            if conn:
                cursor = conn.cursor()

                # Fecha de inicio de la semana (7 días atrás)
                fecha_inicio = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas WHERE Fecha >= ?", (fecha_inicio,))
                ventas = cursor.fetchall()
                conn.close()

                for venta in ventas:
                    venta_str = [str(dato) for dato in venta]
                    x_position = 30
                    for i, data in enumerate(venta_str):
                        c.drawString(x_position + 5, y_position + 5, data)
                        x_position += column_widths[i]

                    total_ventas += float(venta[6])  # Sumar el monto total de la venta
                    y_position -= 20

                    # Verificar si se necesita una nueva página
                    if y_position < 100:
                        c.showPage()
                        y_position = 480
                        x_position = 30

                        # Dibujar encabezados nuevamente
                        for i, header in enumerate(encabezados):
                            c.setFillColor(colors.whitesmoke)
                            c.rect(x_position, y_position, column_widths[i], 20, fill=True, stroke=False)
                            c.setFillColor(colors.black)
                            c.drawString(x_position + 5, y_position + 5, header)
                            x_position += column_widths[i]

                        c.line(30, y_position - 5, 800, y_position - 5)
                        y_position -= 25

                # Mostrar el total de las ventas al final del reporte
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.darkblue)
                c.drawString(600, y_position - 30, "Total de Ventas:")
                c.setFillColor(colors.black)
                c.drawString(700, y_position - 30, f"${total_ventas:.2f}")
                c.line(600, y_position - 35, 800, y_position - 35)

                # Guardar el archivo PDF
                c.save()

                # Mostrar vista previa del PDF
                webbrowser.open_new(temp_file.name)
            else:
                os.remove(temp_file.name)
                messagebox.showerror("Error", "Error al conectar con la base de datos.")

        # Función para generar el reporte de ventas mensual
        def generar_reporte_mensual():
            # Crear archivo temporal para vista previa
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            nombre_pdf = temp_file.name

            c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

            # Encabezado con logotipo
            logotipo_path = "imgs/logoEmp.jpg"
            if os.path.exists(logotipo_path):
                try:
                    c.drawImage(logotipo_path, 30, 530, width=80, height=80)  # Ajustar posición y tamaño del logotipo
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"No se pudo cargar el logotipo: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "No se encontró el archivo del logotipo.")

            # Título del reporte
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkblue)
            c.drawString(300, 550, "Reporte de Ventas Mensual")  # Ajustar posición del título

            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            c.drawString(300, 530, "Ventas realizadas durante el último mes.")  # Subtítulo

            # Dibujar una línea debajo del encabezado
            c.setStrokeColor(colors.black)
            c.setLineWidth(2)
            c.line(30, 520, 800, 520)

            # Encabezados de la tabla
            c.setFont("Helvetica-Bold", 10)
            encabezados = ["ID", "Fecha", "Hora", "Cliente", "Producto", "Cantidad", "Monto", "Pago", "Entrega", "Estatus"]
            column_widths = [60, 90, 60, 120, 150, 90, 100, 100, 120, 100]
            y_position = 480
            x_position = 30

            for i, header in enumerate(encabezados):
                c.setFillColor(colors.whitesmoke)
                c.rect(x_position, y_position, column_widths[i], 20, fill=True, stroke=False)
                c.setFillColor(colors.black)
                c.drawString(x_position + 5, y_position + 5, header)
                x_position += column_widths[i]

            # Dibujar una línea horizontal debajo del encabezado
            c.setStrokeColor(colors.black)
            c.line(30, y_position - 5, 800, y_position - 5)
            y_position -= 25

            # Obtener las ventas de la base de datos del mes actual
            conn = obtener_conexion()
            total_ventas = 0  # Variable para la sumatoria total
            if conn:
                cursor = conn.cursor()

                # Fecha de inicio del mes (primer día del mes)
                fecha_inicio = datetime.now().replace(day=1).strftime("%Y-%m-%d")

                cursor.execute("SELECT Id, Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus FROM Ventas WHERE Fecha >= ?", (fecha_inicio,))
                ventas = cursor.fetchall()
                conn.close()

                # Datos de ventas
                for venta in ventas:
                    venta_str = [str(dato) for dato in venta]
                    x_position = 30
                    for i, data in enumerate(venta_str):
                        c.drawString(x_position + 5, y_position + 5, data)
                        x_position += column_widths[i]

                    total_ventas += float(venta[6])  # Sumar el monto total de la venta
                    y_position -= 20

                    # Verificar si se necesita una nueva página
                    if y_position < 100:
                        c.showPage()
                        y_position = 480
                        x_position = 30

                        # Dibujar encabezados nuevamente
                        for i, header in enumerate(encabezados):
                            c.setFillColor(colors.whitesmoke)
                            c.rect(x_position, y_position, column_widths[i], 20, fill=True, stroke=False)
                            c.setFillColor(colors.black)
                            c.drawString(x_position + 5, y_position + 5, header)
                            x_position += column_widths[i]

                        c.line(30, y_position - 5, 800, y_position - 5)
                        y_position -= 25

                # Mostrar el total de las ventas al final del reporte
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.darkblue)
                c.drawString(600, y_position - 30, "Total de Ventas:")
                c.setFillColor(colors.black)
                c.drawString(700, y_position - 30, f"${total_ventas:.2f}")
                c.line(600, y_position - 35, 800, y_position - 35)

                # Guardar el archivo PDF
                c.save()

                # Mostrar vista previa del PDF
                webbrowser.open_new(temp_file.name)
            else:
                os.remove(temp_file.name)
                messagebox.showerror("Error", "Error al conectar con la base de datos.")

         # Función para generar el reporte de productos vendidos
        
        # Crear barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Título
        etTitulo = tk.Label(panel_principal, text="Administración de Reportes", fg="black", bg="white", font=("Playfair Display", 28, "bold"))
        etTitulo.place(x=300, y=30)

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