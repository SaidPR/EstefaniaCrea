from tkcalendar import Calendar
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.util_window as util_win
from util.db_utils.consultas_db import obtener_conexion

class AnadirPedido(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.contruirWidget()

    def config_window(self):
        self.title('Añadir Pedido')
        self.resizable(False, False)
        self.config(bg="white")
        w, h = 700, 800
        util_win.centrar_ventana(self, w, h)

    def contruirWidget(self):
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
                cantidad = int(entry_cantidad.get())
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
            fecha_entrega = calendario.get_date()
            hora_entrega = combo_hora.get() + ":" + combo_minuto.get() + " " + combo_am_pm.get()
            tipo_entrega = combo_tipo_entrega.get()
            domicilio = entry_domicilio.get() if tipo_entrega == "Envío a domicilio" else "Recoger en Tienda"
            notas = entry_notas.get()
            estado = combo_estado.get()

            if not (cliente and contacto and metodo_pago and fecha_entrega and tipo_entrega and estado):
                messagebox.showwarning("Campos Incompletos", "Por favor, llena todos los campos obligatorios.")
                return

            if not lista_productos:
                messagebox.showwarning("Sin productos", "Debes agregar al menos un producto al pedido.")
                return

            try:
                conn = obtener_conexion()
                cursor = conn.cursor()

                # Concatenar los productos en un solo string
                productos_str = ", ".join([f"{producto} (x{cantidad})" for producto, cantidad, _, _ in lista_productos])

                # Calcular el monto total sumando los precios de todos los productos
                monto_total = sum([precio_total for _, _, _, precio_total in lista_productos])

                # Insertar el pedido con todos los productos y el monto total
                cursor.execute(
                    """
                    INSERT INTO Pedidos (Cliente, Contacto, Producto, Cantidad, Monto_total, Metodo_de_pago, Fecha, Hora, Lugar_de_entrega, Notas, Estatus)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (cliente, contacto, productos_str, len(lista_productos), monto_total, metodo_pago, fecha_entrega, hora_entrega, domicilio, notas, estado)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Pedido guardado correctamente.")
                limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al guardar el pedido: {e}")

        def limpiar_campos():
            entry_cliente.delete(0, tk.END)
            entry_contacto.delete(0, tk.END)
            combo_metodo_pago.set("")
            combo_hora.set("")
            combo_minuto.set("")
            combo_am_pm.set("")
            combo_tipo_entrega.set("")
            entry_domicilio.delete(0, tk.END)
            entry_domicilio.config(state="disabled")
            entry_notas.delete(0, tk.END)
            combo_estado.set("")
            lista_productos.clear()
            actualizar_lista_productos()

        def habilitar_domicilio(event):
            if combo_tipo_entrega.get() == "Envío a domicilio":
                entry_domicilio.config(state="normal")
            else:
                entry_domicilio.delete(0, tk.END)
                entry_domicilio.config(state="disabled")

        # Elementos de la interfaz
        tk.Label(self, text="Cliente:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_cliente = tk.Entry(self, width=40)
        entry_cliente.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Contacto:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_contacto = tk.Entry(self, width=40)
        entry_contacto.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Producto:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        combo_productos = ttk.Combobox(self, values=list(productos.keys()), state="readonly", width=37)
        combo_productos.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Cantidad:").grid(row=2, column=2, padx=10, pady=10, sticky="w")
        entry_cantidad = tk.Entry(self, width=10)
        entry_cantidad.grid(row=2, column=3, padx=10, pady=10)

        btn_agregar_producto = tk.Button(self, text="Agregar Producto", command=agregar_producto, bg="blue", fg="white")
        btn_agregar_producto.grid(row=2, column=4, padx=10, pady=10)

        frame_productos = tk.Frame(self, bg="white")
        frame_productos.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="w")

        label_total = tk.Label(self, text="Total: $0.00", bg="white", font=("Arial", 14, "bold"))
        label_total.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="w")

        tk.Label(self, text="Método de pago:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        combo_metodo_pago = ttk.Combobox(self, values=["Efectivo", "Tarjeta/Transferencia"], state="readonly", width=37)
        combo_metodo_pago.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(self, text="Fecha de entrega:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        calendario = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        calendario.grid(row=6, column=1, padx=10, pady=10)

        tk.Label(self, text="Hora de entrega:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        frame_hora = tk.Frame(self)
        frame_hora.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        combo_hora = ttk.Combobox(frame_hora, values=[f"{i:02d}" for i in range(1, 13)], width=5, state="readonly")
        combo_hora.grid(row=0, column=0, padx=2)
        tk.Label(frame_hora, text=":").grid(row=0, column=1)
        combo_minuto = ttk.Combobox(frame_hora, values=[f"{i:02d}" for i in range(0, 60)], width=5, state="readonly")
        combo_minuto.grid(row=0, column=2, padx=2)
        combo_am_pm = ttk.Combobox(frame_hora, values=["AM", "PM"], width=5, state="readonly")
        combo_am_pm.grid(row=0, column=3, padx=2)

        tk.Label(self, text="Tipo de entrega:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
        combo_tipo_entrega = ttk.Combobox(self, values=["Envío a domicilio", "Recoger en tienda"], state="readonly", width=37)
        combo_tipo_entrega.grid(row=8, column=1, padx=10, pady=10)
        combo_tipo_entrega.bind("<<ComboboxSelected>>", habilitar_domicilio)

        tk.Label(self, text="Domicilio:").grid(row=9, column=0, padx=10, pady=10, sticky="w")
        entry_domicilio = tk.Entry(self, width=40, state="disabled")
        entry_domicilio.grid(row=9, column=1, padx=10, pady=10)

        tk.Label(self, text="Notas:").grid(row=10, column=0, padx=10, pady=10, sticky="w")
        entry_notas = tk.Entry(self, width=40)
        entry_notas.grid(row=10, column=1, padx=10, pady=10)

        tk.Label(self, text="Estado:").grid(row=11, column=0, padx=10, pady=10, sticky="w")
        combo_estado = ttk.Combobox(self, values=["Anotado", "Confirmado", "Pendiente", "Cancelado"], state="readonly", width=37)
        combo_estado.grid(row=11, column=1, padx=10, pady=10)

        btn_guardar = tk.Button(self, text="Guardar Pedido", command=guardar_pedido, bg="green", fg="white", width=15)
        btn_guardar.grid(row=12, column=0, padx=10, pady=20)

        btn_limpiar = tk.Button(self, text="Limpiar", command=limpiar_campos, bg="gray", fg="white", width=15)
        btn_limpiar.grid(row=12, column=1, padx=10, pady=20)
