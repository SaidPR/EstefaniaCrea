import tkinter as tk
import os
import sys
from tkinter import font
from config import COLOR_ONBUTTON, COLOR_PRINCIPAL, COLOR_SIDEBAR, COLOR_TOP
import util.util_imgs as util_img
import util.util_window as util_win
from formularios.form_proveedores import FormularioProv
from formularios.form_catalogo import FormularioCatalogo
from formularios.form_pedidos import FormularioPedidos
from formularios.form_ventas import FormularioVentas
from formularios.form_reportes import FormularioReportes

class FormularioMaster(tk.Tk):
    def __init__(self):
        super().__init__()
        # Función para obtener la ruta correcta de las imágenes
        def obtener_ruta_imagen(imagen):
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS  # Ruta temporal cuando el archivo está empaquetado
            else:
                base_path = os.path.abspath(os.path.dirname(__file__))  # Ruta del archivo fuente
            return os.path.join(base_path, imagen)

        # Cargar imágenes con la ruta correcta
        ruta_logo = obtener_ruta_imagen("imgs/logoEmp.jpg")
        ruta_perfil = obtener_ruta_imagen("imgs/user.png")# Establecer el icono de la ventana
        
        # Aquí asumo que util_img.read_image es una función que carga la imagen
        self.logo = util_img.read_image(ruta_logo, (560, 560))
        self.perfil = util_img.read_image(ruta_perfil, (100, 100))
        
        # Configuración de la ventana principal
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.control_sidebar()
        self.controles_cuerpo()

    def config_window(self):
        self.title("Estefania Crea")
        self.state("zoomed")
        self.resizable(False, False)
        w, h = 1366, 768
        util_win.centrar_ventana(self, w, h)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def paneles(self):        
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=COLOR_TOP, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_SIDEBAR, width=200)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(self, bg=COLOR_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configurar la fuente Playfair Display
        fuente_playfair = font.Font(family="Playfair Display", size=22, weight="bold")

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="ESTEFANIACREA")
        self.labelTitulo.config(fg="#DD940C", font=fuente_playfair, bg=COLOR_TOP, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT, padx=20)

        # Etiqueta de información
        self.labelInformacion = tk.Label(self.barra_superior, text="", font=("Roboto", 10), bg=COLOR_TOP, padx=20)
        self.labelInformacion.pack(side=tk.RIGHT, padx=10)

    def control_sidebar(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family="Playfair Display", size=16, slant="italic", weight="bold")

        # Etiqueta de perfil con borde redondeado
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_SIDEBAR)
        self.labelPerfil.pack(side=tk.TOP, pady=10, padx=5)

        # Botones del menú lateral
        self.buttonCatalogo = tk.Button(self.menu_lateral)
        self.buttonPedidos = tk.Button(self.menu_lateral)
        self.buttonVentas = tk.Button(self.menu_lateral)
        self.buttonReportes = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)

        buttons_info = [
            ("          Inventario", self.buttonCatalogo, self.openCatalogo),
            ("          Pedidos", self.buttonPedidos, self.openPedidos),
            ("          Ventas", self.buttonVentas, self.openVentas),
            ("          Reportes", self.buttonReportes, self.openReportes),
            ("          Proveedores", self.buttonInfo, self.openProv)
        ]

        for text, button, comando in buttons_info:
            self.configurar_boton_menu(button, text, font_awesome, ancho_menu, alto_menu, comando)

    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, font_awesome, ancho_menu, alto_menu, comando):
        button.config(
            text=f"  {text}", anchor="w", font=font_awesome,
            bd=0, bg=COLOR_SIDEBAR, fg="black", width=ancho_menu, height=alto_menu,
            relief="flat",  # Borde plano
            activebackground=COLOR_ONBUTTON,  # Fondo al hacer clic
            command=comando
        )
        # Aplicar bordes redondeados a los botones
        button.config(highlightbackground=COLOR_SIDEBAR, highlightcolor=COLOR_ONBUTTON, highlightthickness=1)
        button.pack(side=tk.TOP, padx=5, pady=5)  # Espaciado entre los botones
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_ONBUTTON, fg='black')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_SIDEBAR, fg='black')

    def openProv(self):
        self.limpiar_panel(self.cuerpo_principal)   
        FormularioProv(self.cuerpo_principal)

    def openCatalogo(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioCatalogo(self.cuerpo_principal) 

    def openPedidos(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioPedidos(self.cuerpo_principal)

    def openVentas(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioVentas(self.cuerpo_principal)

    def openReportes(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioReportes(self.cuerpo_principal)

    def limpiar_panel(self, panel):
        # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def on_close(self):
        # Realiza cualquier limpieza necesaria antes de cerrar
        print("Cerrando la aplicación...")
        self.destroy()  # Asegúrate de destruir correctamente la ventana
