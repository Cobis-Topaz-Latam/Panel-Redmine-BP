from tkinter import *
from PIL import ImageTk, Image
from redminelib import Redmine as Rm
import tkinter as tk
import pyperclip as clipboard
import config as const
from redminelib.exceptions import AuthError, ServerError, ResourceNotFoundError

def login_ventana():
    root = tk.Tk()
    root.title('Redmine')
    #root.iconbitmap('../static/icon/cobis-icon.ico')
    root.resizable(width=False, height=False)
    #  Obtenemos el largo y  ancho de la pantalla

    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    #  Guardamos el largo y alto de la ventana
    wventana = 450
    hventana = 180
    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    #  Se lo aplicamos a la geometría de la ventana
    root.geometry(f'{wventana}x{hventana}+{pwidth}+{pheight}')

    # Label de inicio
    lbl_access = tk.Label(
        root,
        text='Ingrese la clave de acceso de la API',
        font=("Garamond", 12))
    lbl_access.pack(pady=15)

    # Cuando se llame a la función, recibirá 3 argumentos a los que no les daremos uso
    def btn_state(*args):
        if var_api_key.get():
            btn_login.configure(state="normal")
        else:
            btn_login.configure(state="disabled")

    var_api_key = tk.StringVar()

    # Entry para la clave de acceso de la API
    txt_api_key = tk.Entry(
        root,
        textvariable=var_api_key)
    txt_api_key.pack(pady=10, ipadx=100, ipady=5)

    var_api_key.trace_add('write',btn_state)

    def paste_clipboard():
        var_api_key.set(clipboard.paste())

    img_paste = Image.open('./static/icon/paste-icon.png')
    img_paste = img_paste.resize((30,30), Image.Resampling.LANCZOS)

    img_paste_clipboard = ImageTk.PhotoImage(img_paste)

    # Button para pegar portapapeles
    btn_paste = tk.Button(
        root,
        image=img_paste_clipboard,
        text="Pegar",
        compound=LEFT,
        command=paste_clipboard)
    btn_paste.pack(side=LEFT, padx=70, ipadx=20)

    img_login = Image.open('./static/icon/login-icon.png')
    img_login = img_login.resize((30,30), Image.Resampling.LANCZOS)

    img_login_validate = ImageTk.PhotoImage(img_login)

    def redmine_login():
        try:
            # Intenta crear una instancia de Redmine
            #print(var_api_key.get())
            redmine = Rm(const.REDMINE_URL, key=var_api_key.get())

            # Si llegamos aquí, la conexión se ha establecido exitosamente
            print("Conexión exitosa a Redmine")

            # Ahora puedes realizar acciones en la instancia de Redmine
            # Por ejemplo, obtener información de proyectos
            proyectos = redmine.project.all()

            # Iterar a través de los proyectos y mostrar sus nombres
            for proyecto in proyectos:
                print(proyecto.name)
        except AuthError:
            print("Error de autenticación. Verifica tu clave de acceso a la API.")
        except ServerError:
            print("Error del servidor. Comprueba la URL de Redmine.")
        except ResourceNotFoundError:
            print("No se pudo encontrar el recurso en Redmine.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {str(e)}")

    # Button para ingresar
    btn_login = tk.Button(
        root,
        image=img_login_validate,
        text="Ingresar",
        compound=LEFT,
        state=DISABLED,
        command=redmine_login)
    btn_login.pack(side=LEFT, padx=0, ipadx=20)

    root.mainloop()

if __name__ == '__main__':
    login_ventana()