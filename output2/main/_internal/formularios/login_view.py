import os
import sys
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from util.db_utils.consultas_db import obtener_conexion
from formularios.form_master import FormularioMaster

root = tk.Tk()
root.title('ESTEFANIA CREA')
root.state('zoomed')  # Maximiza la ventana al iniciarse
root.resizable(False, False)  # Evita que la ventana sea ajustable

font_name = "Inter"

# Verificar si estamos ejecutando el archivo como ejecutable (frozen) o en modo desarrollo
if getattr(sys, 'frozen', False):  # Si estamos ejecutando el ejecutable
    base_path = sys._MEIPASS  # PyInstaller extrae los archivos en una carpeta temporal
else:
    base_path = os.path.abspath('.')  # Ruta del directorio actual en modo desarrollo

def singin():
    username = email_entry.get()
    password = pass_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Por favor ingresa el correo y la contraseña.")
        return

    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE correo = ? AND contrasena = ?", (username, password))
        usuario = cursor.fetchone()

        if usuario:
            root.destroy()  
            FormularioMaster()  # Abre la nueva ventana de formulario
        else:
            messagebox.showerror("Incorrecto", "Usuario o contraseña incorrectos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al intentar iniciar sesión: {e}")
    finally:
        conn.close()

# Funciones para manejar la entrada de email
def on_enter_email(e):
    email_entry.delete(0, "end")  # Borra el texto de entrada al hacer clic

def on_leave_email(e):
    if email_entry.get() == "":
        email_entry.insert(0, "")  # Vuelve a mostrar el texto de marcador si está vacío    

# Funciones para manejar la entrada de contraseña
def on_enter_password(e):
    pass_entry.delete(0, "●")  # Borra el texto de entrada al hacer clic

def on_leave_password(e):
    if pass_entry.get() == "":
        pass_entry.insert(0, "")  # Vuelve a mostrar el texto de marcador si está vacío

# Cargar la imagen de fondo
bg_image_path = os.path.join(base_path, 'imgs', 'Fondo.jpg')
bg_img = Image.open(bg_image_path).resize((1366, 768), Image.LANCZOS)

# Crear una capa blanca semitransparente
white_overlay = Image.new("RGBA", bg_img.size, (255, 255, 255, int(255 * 0.25)))  # 75% blanco

# Combinar la imagen de fondo con la capa blanca
bg_img = Image.alpha_composite(bg_img.convert("RGBA"), white_overlay)

# Convertir la imagen para tkinter
bg_photo = ImageTk.PhotoImage(bg_img)

# Añadir la imagen de fondo al fondo de la ventana
bg_label = Label(root, image=bg_photo, bd=0, highlightthickness=0)
bg_label.place(x=0, y=0)

# Creación del marco superior
head = Frame(root, width=1366, height=150, bg="white")
head.place(x=0, y=0)

# Cargar imagen logo empresa
bg_logo_emp_path = os.path.join(base_path, 'imgs', 'logoEmp.jpg')
bg_logo_emp = Image.open(bg_logo_emp_path)
bg_logo_emp = bg_logo_emp.resize((140, 140), Image.LANCZOS)
bg_photo3 = ImageTk.PhotoImage(bg_logo_emp)

# Añadir logo empresa
Label(root, image=bg_photo3, bd=0, highlightthickness=0).place(x=10, y=0)

# Cargar imagen logo Jynxcode
bg_logo_path = os.path.join(base_path, 'imgs', 'JynxcodeLogo.png')
bg_logo = Image.open(bg_logo_path)
bg_logo = bg_logo.resize((140, 113), Image.LANCZOS)
bg_photo2 = ImageTk.PhotoImage(bg_logo)

# Añadir logo empresa
Label(root, image=bg_photo2, bd=0).place(x=1240, y=20)

# Título y subtítulo
title = Label(head, text="Bienvenida", fg="black", bg="white", font=(font_name, 22, "bold"))
title.place(x=600, y=30)
subtitle = Label(head, text="Inicia sesión para continuar", fg="black", bg="white", font=(font_name, 22))
subtitle.place(x=500, y=80)

# Creación marco Login
login = Frame(root, width=400, height=385, bg="white")
login.place(x=483, y=233)

# Email y contraseña
emailTitle = Label(login, text="E-mail", fg="black", bg="white", font=(font_name, 14, "bold"))
emailTitle.place(x=165, y=33)

email_entry = Entry(login, width=30, fg="black", bg="#D9D9D9", border=0, font=(font_name, 14), justify="center")
email_entry.place(x=18, y=90)
email_entry.bind("<FocusIn>", on_enter_email)
email_entry.bind("<FocusOut>", on_leave_email)

passTitle = Label(login, text="Contraseña", fg="black", bg="white", font=(font_name, 14, "bold"))
passTitle.place(x=140, y=140)

pass_entry = Entry(login, width=30, fg="black", bg="#D9D9D9", border=0, font=(font_name, 14), justify="center", show="●")
pass_entry.place(x=18, y=197)
pass_entry.bind("<FocusIn>", on_enter_password)
pass_entry.bind("<FocusOut>", on_enter_password)

# Crear un botón redondeado
def botonLogin(frame, text, command):
    canvas = Canvas(frame, width=150, height=30, bg="white", highlightthickness=0)
    canvas.place(x=125, y=250)
    canvas.create_oval(0, 0, 30, 30, fill="#005DE8", outline="#005DE8")
    canvas.create_oval(120, 0, 150, 30, fill="#005DE8", outline="#005DE8")
    canvas.create_rectangle(15, 0, 135, 30, fill="#005DE8", outline="#005DE8")
    canvas.create_text(75, 15, text=text, fill="white", font=(font_name, 10, "bold"), anchor="center")
    canvas.bind("<Button-1>", lambda e: command())

botonLogin(login, "Iniciar sesión", singin)

root.mainloop()
