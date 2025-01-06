from tkcalendar import Calendar
from datetime import datetime
import tkinter as tk
from tkinter import Canvas, ttk
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
        w, h = 900, 700
        util_win.centrar_ventana(self, w, h)

    def contruirWidget(self):
        # Obtener la fecha actual
        fecha_actual = datetime.today().strftime('%Y-%m-%d')
        
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
            fecha_entrega = calendario.get_date()
            hora_entrega = combo_hora.get() + ":" + combo_minuto.get() + " " + combo_am_pm.get()
            tipo_entrega = combo_tipo_entrega.get()
            if tipo_entrega == "Envío a domicilio":
                domicilio = (entry_domicilio.get() + " " + 
                            str(entry_NumEx.get()) + " " + 
                            str(entry_NumIn.get()) + " " + 
                            entry_Calle.get() + " " + 
                            entry_Calle2.get() + " " + 
                            entry_Ref.get())
            else: 
                domicilio = "Recoger en Tienda"
            estado = combo_estado.get()
            abono = entry_Ant.get()

            if not (cliente and contacto and metodo_pago and fecha_entrega and tipo_entrega and estado and abono):
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
                    INSERT INTO Pedidos (Cliente, Contacto, Producto, Cantidad, Monto_total, Metodo_de_pago, Fecha, Hora, Lugar_de_entrega, Estatus, Anticipo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (cliente, contacto, productos_str, len(lista_productos), monto_total, metodo_pago, fecha_entrega, hora_entrega, domicilio, estado, abono)
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
            entry_Ant.delete(0, tk.END)
            combo_metodo_pago.set("")
            combo_hora.set("")
            combo_minuto.set("")
            combo_am_pm.set("")
            combo_tipo_entrega.set("")
            entry_domicilio.delete(0, tk.END)
            entry_domicilio.config(state="disabled")
            combo_estado.set("")
            lista_productos.clear()
            actualizar_lista_productos()

        def habilitar_domicilio(event):
            if combo_tipo_entrega.get() == "Envío a domicilio":
                entry_domicilio.config(state="normal")
                entry_NumEx.config(state="normal")
                entry_NumIn.config(state="normal")
                entry_Calle.config(state="normal")
                entry_Calle2.config(state="normal")
                entry_Ref.config(state="normal")
            else:
                entry_domicilio.delete(0, tk.END)
                entry_domicilio.config(state="disabled")
                entry_NumEx.delete(0, tk.END)
                entry_NumEx.config(state="disabled")
                entry_NumIn.delete(0, tk.END)
                entry_NumIn.config(state="disabled")
                entry_Calle.delete(0, tk.END)
                entry_Calle.config(state="disabled")
                entry_Calle2.delete(0, tk.END)
                entry_Calle2.config(state="disabled")
                entry_Ref.delete(0, tk.END)
                entry_Ref.config(state="disabled")

        # Etiqueta Tit
        etTitulo = tk.Label(self, text="DATOS DEL CLIENTE", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etTitulo.place(x=15, y=10)

        # Datos Cliente
        etNom = tk.Label(self, text="Nombre:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etNom.place(x=30, y=60)
        entry_cliente = tk.Entry(self, width=30, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_cliente.place(x=110, y=60)

        # Datos Contacto
        etNom = tk.Label(self, text="Teléfono:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etNom.place(x=30, y=110)
        entry_contacto = tk.Entry(self, width=13, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_contacto.place(x=111, y=110)

        # Etiqueta Entrega  
        etEntrega = tk.Label(self, text="DATOS DE ENTREGA", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etEntrega.place(x=15, y=160)

        # Obtener la fecha actual
        fecha_actual = datetime.today()

        # Calendario
        etFecha = tk.Label(self, text="Fecha de entrega:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etFecha.place(x=30, y=210)
        calendario = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        calendario.place(x=50, y= 260)

        # Configurar la fecha mínima seleccionable
        calendario.config(mindate=fecha_actual)

        # Función para actualizar las opciones de hora según AM/PM
        def actualizar_hora():
            if combo_am_pm.get() == "AM":
                # Restringir horas entre 8 y 11 AM
                combo_hora['values'] = [f"{i:02d}" for i in range(8, 12)]
            elif combo_am_pm.get() == "PM":
                # Restringir horas entre 12 y 10 PM
                combo_hora['values'] = [f"{i:02d}" for i in range(1, 11)]  # De 12 a 10
            else:
                # Si no se selecciona AM o PM, vaciar el combobox
                combo_hora['values'] = []

        # Hora
        etHora = tk.Label(self, text="Hora de entrega:", fg="black", bg="white", font=("Inter", 12, "bold"))   
        etHora.place(x=250, y=210)
        frame_hora = tk.Frame(self)
        frame_hora.place(x=300, y=260)

        combo_hora = ttk.Combobox(frame_hora, values=[], width=5, state="readonly")
        combo_hora.grid(row=0, column=0, padx=2)
        tk.Label(frame_hora, text=":").grid(row=0, column=1)
        combo_minuto = ttk.Combobox(frame_hora, values=[f"{i:02d}" for i in range(0, 60, 10)], width=5, state="readonly")
        combo_minuto.grid(row=0, column=2, padx=2)
        combo_am_pm = ttk.Combobox(frame_hora, values=["AM", "PM"], width=5, state="readonly")
        combo_am_pm.grid(row=0, column=3, padx=2)

        # Llamar a la función de actualización de hora cuando se cambie AM/PM
        combo_am_pm.bind("<<ComboboxSelected>>", lambda event: actualizar_hora())

        # Etiqueta Lugar
        etUbi = tk.Label(self, text="LUGAR DE ENTREGA", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etUbi.place(x=15, y=430)

        # Datos Lugar
        etTipo = tk.Label(self, text="Tipo de entrega:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etTipo.place(x=30, y=480)
        combo_tipo_entrega = ttk.Combobox(self, values=["Envío a domicilio", "Recoger en tienda"], state="readonly", width=37)
        combo_tipo_entrega.place(x=180, y=485)
        combo_tipo_entrega.bind("<<ComboboxSelected>>", habilitar_domicilio)

        # Datos Domicilio
        etDom = tk.Label(self, text="Colonia / Calle:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etDom.place(x=30, y=530)
        entry_domicilio = tk.Entry(self, width=30, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_domicilio.place(x=90, y=530)
        entry_domicilio.config(state="disabled")

        etNumEx = tk.Label(self, text="Núm. Ext:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etNumEx.place(x=30, y=580)
        entry_NumEx = tk.Entry(self, width=8, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_NumEx.place(x=108, y=580)
        entry_NumEx.config(state="disabled")

        etNumIn = tk.Label(self, text="Núm. Int:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etNumIn.place(x=230, y=580)
        entry_NumIn = tk.Entry(self, width=8, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_NumIn.place(x=305, y=580)
        entry_NumIn.config(state="disabled")

        etCalle = tk.Label(self, text="Entre calle:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etCalle.place(x=30, y=630)
        entry_Calle = tk.Entry(self, width=15, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_Calle.place(x=120, y=630)
        entry_Calle.config(state="disabled")

        etCalle2 = tk.Label(self, text="Y calle:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etCalle2.place(x=250, y=630)
        entry_Calle2 = tk.Entry(self, width=15, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_Calle2.place(x=325, y=630)
        entry_Calle2.config(state="disabled")

        etRef = tk.Label(self, text="Referencia:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etRef.place(x=30, y=670)
        entry_Ref = tk.Entry(self, width=30, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_Ref.place(x=130, y=670)
        entry_Ref.config(state="disabled")

        # Productos
        etProd = tk.Label(self, text="PRODUCTOS", fg="black", bg="white", font=("Playfair Display", 16, "bold"))
        etProd.place(x=535, y=10)

        # Et Prod
        etProd2 = tk.Label(self, text="Productos:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etProd2.place(x=550, y=60)
        combo_productos = ttk.Combobox(self, values=list(productos.keys()), state="readonly", width=37)
        combo_productos.place(x=650, y=65)

        # Et Cantidad
        etCantidad = tk.Label(self, text="Cantidad:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etCantidad.place(x=550, y=110)
        entry_cant = tk.Entry(self, width=10, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_cant.place(x=650, y=110)

        # Frame prods
        etLista = tk.Label(self, text="Listado:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etLista.place(x=550, y=210)
        frame_productos = tk.Frame(self, bg="white")
        frame_productos.place(x=550, y=250)
        
        label_total = tk.Label(self, text="Total: $0.00", bg="white", font=("Playfair Display", 16, "bold"))
        label_total.place(x=550, y=430)

        #Et Anticipo
        etAnt = tk.Label(self, text="Anticipo:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etAnt.place(x=550, y=480)
        entry_Ant = tk.Entry(self, width=10, fg="black", bg="#D9D9D9", border=0, font=("Inter", 12), justify="center")
        entry_Ant.place(x=650, y=480)

        # Et MetodoP
        etMetodoP = tk.Label(self, text="Método de pago:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etMetodoP.place(x=550, y=530)
        combo_metodo_pago = ttk.Combobox(self, values=["Efectivo", "Tarjeta/Transferencia"], state="readonly", width=27)
        combo_metodo_pago.place(x=700, y=535)

        # Et Estado
        etEstado = tk.Label(self, text="Estado:", fg="black", bg="white", font=("Inter", 12, "bold"))
        etEstado.place(x=550, y=580)
        combo_estado = ttk.Combobox(self, values=["Confirmado", "Pendiente"], state="readonly", width=37)
        combo_estado.place(x=630, y=585)
        
        self.crear_boton("Añadir", agregar_producto, 650, 160, "#005DE8")
        self.crear_boton("Guardar Pedido", guardar_pedido, 740, 610, "#2DD22D")
        self.crear_boton("Limpiar", limpiar_campos, 550, 610, "#E2A128")

    def crear_boton(self, texto, command, x, y, color):
        """Crea un botón con esquinas redondeadas."""
        canvas = Canvas(self, width=150, height=30, bg="white", highlightthickness=0)
        canvas.place(x=x, y=y)

        # Esquinas redondeadas
        canvas.create_oval(0, 0, 30, 30, fill=color, outline=color)
        canvas.create_oval(120, 0, 150, 30, fill=color, outline=color)
        canvas.create_rectangle(15, 0, 135, 30, fill=color, outline=color)

        # Texto del botón
        canvas.create_text(75, 15, text=texto, fill="white", font=("Inter", 10, "bold"), anchor="center")

        # Vincula el clic al comando
        canvas.bind("<Button-1>", lambda e: command())