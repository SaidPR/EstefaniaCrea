from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Canvas, ttk
from util.db_utils.consultas_db import obtener_conexion  

class FormularioCaja:
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        # Consulta a la base de datos para obtener los nombres de los productos
        def obtener_productos():
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, precio FROM Catalogo")
            productos = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()
            return productos

        productos = obtener_productos()
        lista_productos = []  # Lista para almacenar los productos añadidos

        # Función para agregar un nuevo producto
        def agregar_producto():
            producto_seleccionado = combo_productos.get()
            try:
                cantidad = int(entry_cant.get())
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero.")
                return

            if producto_seleccionado not in productos:
                messagebox.showerror("Error", "Selecciona un producto válido.")
                return

            precio_unitario = productos[producto_seleccionado]
            precio_total = cantidad * precio_unitario
            lista_productos.append((producto_seleccionado, cantidad, precio_unitario, precio_total))
            actualizar_lista_productos()

        # Función para actualizar la lista de productos en la interfaz
        def actualizar_lista_productos():
            for widget in frame_productos.winfo_children():
                widget.destroy()

            total = 0
            for i, (producto, cantidad, precio_unitario, precio_total) in enumerate(lista_productos):
                tk.Label(frame_productos, text=f"{producto} (x{cantidad}) - ${precio_total:.2f}", bg="white").grid(row=i, column=0, sticky="w")
                tk.Button(frame_productos, text="Eliminar", command=lambda idx=i: eliminar_producto(idx), bg="red", fg="white").grid(row=i, column=1, padx=5)
                total += precio_total

            label_total.config(text=f"Total: ${total:.2f}")

        # Función para eliminar un producto de la lista
        def eliminar_producto(idx):
            del lista_productos[idx]
            actualizar_lista_productos()

        # Función para guardar el pedido
        def guardar_pedido():
            cliente = entry_cliente.get()
            contacto = entry_contacto.get()
            metodo_pago = combo_metodo_pago.get()
            fecha_entrega = datetime.today().strftime('%Y-%m-%d')
            hora_entrega = datetime.now().strftime('%H:%M:%S')
            domicilio = "Tienda"
            estado = "Vendido"

            if not (cliente and contacto):
                messagebox.showwarning("Campos Incompletos", "Por favor, llena todos los campos obligatorios.")
                return

            if not lista_productos:
                messagebox.showwarning("Sin productos", "Debes agregar al menos un producto al pedido.")
                return

            # Calcular el monto total y la cantidad total
            monto_total = sum([precio_total for _, _, _, precio_total in lista_productos])
            cantidad_total = sum([cantidad for _, cantidad, _, _ in lista_productos])

            try:
                # Convertir ingreso a float
                ingreso = float(entry_ingr.get())
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un valor válido para el ingreso.")
                return

            if ingreso < monto_total:
                messagebox.showerror("Error", "El ingreso debe ser mayor o igual al monto total.")
                return

            cambio = ingreso - monto_total

            try:
                conn = obtener_conexion()
                cursor = conn.cursor()

                # Concatenar los productos en un solo string
                productos_str = ", ".join([f"{producto} (x{cantidad})" for producto, cantidad, _, _ in lista_productos])

                # Insertar el pedido en la base de datos
                cursor.execute(
                    """
                    INSERT INTO Ventas (Fecha, Hora, Cliente, Producto_vendido, Cantidad, Monto_total, Metodo_de_pago, Lugar_de_entrega, Estatus, Ingreso, Cambio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (fecha_entrega, hora_entrega, cliente, productos_str, cantidad_total, monto_total, metodo_pago, domicilio, estado, ingreso, cambio)
                )

                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Venta guardada correctamente.")
                limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al guardar la venta: {e}")



        def limpiar_campos():
            entry_cliente.delete(0, tk.END)
            entry_contacto.delete(0, tk.END)
            entry_cant.delete(0, tk.END)
            entry_ingr.delete(0, tk.END)
            lista_productos.clear()
            actualizar_lista_productos()

        def calcular_cambio():
            try:
                ingreso = float(entry_ingr.get())  # Obtener el ingreso del cliente
                total = float(label_total.cget("text").split("$")[1])  # Obtener el total desde el texto del label
                if ingreso < total:
                    messagebox.showerror("Error", "El ingreso no puede ser menor al total.")
                    return
                elif ingreso == total:
                    cambio = ingreso 
                    label_cambio.config(text=f"Cambio: $0.00")  # Actualizar el label del cambio
                    return
                cambio = ingreso - total
                label_cambio.config(text=f"Cambio: ${cambio:.2f}")  # Actualizar el label del cambio
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un valor válido para el ingreso.")

        # Título
        etTitulo = tk.Label(panel_principal, text="Caja", fg="black", bg="white", font=("Playfair Display", 30, "bold"))
        etTitulo.place(x=500, y=25)

        # Etiqueta Tit
        etTitulo = tk.Label(panel_principal, text="DATOS DEL CLIENTE", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etTitulo.place(x=15, y=110)

        # Datos Cliente
        etNom = tk.Label(panel_principal, text="Nombre:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etNom.place(x=30, y=160)
        entry_cliente = tk.Entry(panel_principal, width=30, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_cliente.place(x=110, y=160)

        # Datos Contacto
        etNom = tk.Label(panel_principal, text="Teléfono:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etNom.place(x=30, y=210)
        entry_contacto = tk.Entry(panel_principal, width=13, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_contacto.place(x=111, y=210)

        # Productos
        etProd = tk.Label(panel_principal, text="PRODUCTOS", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etProd.place(x=15, y=260)

        # Et Prod
        etProd2 = tk.Label(panel_principal, text="Productos:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etProd2.place(x=30, y=310)
        combo_productos = ttk.Combobox(panel_principal, values=list(productos.keys()), state="readonly", width=37)
        combo_productos.place(x=130, y=315)

        # Et Cantidad
        etCantidad = tk.Label(panel_principal, text="Cantidad:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etCantidad.place(x=30, y=360)
        entry_cant = tk.Entry(panel_principal, width=10, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_cant.place(x=130, y=360)

        # Et MetodoP
        etMetodoP = tk.Label(panel_principal, text="Método de pago:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etMetodoP.place(x=30, y=460)
        combo_metodo_pago = ttk.Combobox(panel_principal, values=["Efectivo", "Transferencia"], state="readonly", width=27)
        combo_metodo_pago.place(x=180, y=465)

        # Frame prods
        etLista = tk.Label(panel_principal, text="LISTADO:", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etLista.place(x=750, y=110)
        frame_productos = tk.Frame(panel_principal, bg="white")
        frame_productos.place(x=750, y=150)
        
        label_total = tk.Label(panel_principal, text="Total: $0.00", bg="white", font=("Playfair Display", 16, "bold"))
        label_total.place(x=750, y=360)

        # Et Ingreso
        etIngreso = tk.Label(panel_principal, text="Ingreso:", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etIngreso.place(x=750, y=410)
        entry_ingr = tk.Entry(panel_principal, width=8, fg="black", bg="#D9D9D9", border=0, font=("Playfair Display", 16, "bold"), justify="center")
        entry_ingr.place(x=840, y=410)
        entry_ingr.bind("<Return>", lambda e: calcular_cambio())

        label_cambio = tk.Label(panel_principal, text="Cambio: $0.00", bg="white", font=("Playfair Display", 16, "bold"))
        label_cambio.place(x=750, y=460)

        # Botones
        self.crear_boton("Añadir", agregar_producto, 130, 410, "#005DE8")
        self.crear_boton("Guardar Venta", guardar_pedido, 750, 510, "#2DD22D")
        self.crear_boton("Limpiar", limpiar_campos, 960, 510, "#E2A128")

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