from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from redminelib import Redmine as Rm
import tkinter as tk
import threading
import time
import config as const
from redminelib.exceptions import AuthError, ServerError, ResourceNotFoundError

def panel_redmine():

    def redmine_login():
        try:
            # Intenta crear una instancia de Redmine
            redmine = Rm(const.REDMINE_URL, key=const.REDMINE_KEY)
            # Obtener información sobre el usuario actual (el usuario autenticado)
            usr_actual = redmine.user.get('current')
            # Imprimir el nombre del usuario
            const.REDMINE_USR_NAME = usr_actual.firstname + ' ' + usr_actual.lastname
        except AuthError:
            print("Error de autenticación. Verifica tu clave de acceso a la API.")
        except ServerError:
            print("Error del servidor. Comprueba la URL de Redmine.")
        except ResourceNotFoundError:
            print("No se pudo encontrar el recurso en Redmine.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {str(e)}")
        return redmine

    def issues_total(redmine):
        open_issues='o'
        pending_issues="1"
        try:
            # Utilizar el método filter() para obtener todas las issues para la bandeja de Producción
            issues = redmine.issue.filter(status_id=open_issues,assigned_to_id="347")
            #Issues Important
            i_issues = redmine.issue.filter(status_id=[open_issues,pending_issues],assigned_to_id="347")

            # Filtrar casos excluyendo el estado específico por su ID
            #c_issues = redmine.issue.filter(status_id=[open_issues, f'!{pending_issues}'],assigned_to_id="347")
            
            #Issues Asigned
            # Obtener información sobre el usuario actual (el usuario autenticado)
            usuario_actual = redmine.user.get('current')
            # Obtener el ID del usuario actual
            assigned_to_id = usuario_actual.id
            # Filtrar casos asignados al usuario actual
            a_issues = redmine.issue.filter(assigned_to_id=assigned_to_id)
            
            # Obtener el total de casos (issues)
            total_issues = len(issues)
            print('Total de casos en Redmine:', total_issues)

            const.REDMINE_ISSUE_IMPORTANT = i_issues
            const.REDMINE_ISSUE_CAUTION = issues
            const.REDMINE_ISSUE_ASSIGNED = a_issues
        except Exception as e:
            print('Error al obtener el total de casos:', str(e))

    """def set_values_entry(var_import, var_caution, var_assigned):
        # Simula un proceso que toma tiempo
        time.sleep(3)

        # Actualiza la interfaz gráfica en el hilo principal
        root.after(0, update_gui, var_import, var_caution, var_assigned)"""
    
    redmine=redmine_login()

    def update_gui(var_import, var_caution, var_assigned):
        issues_total(redmine)
        
        count_import = len(const.REDMINE_ISSUE_IMPORTANT)
        #txt_import.delete(0,END)
        var_import.set(count_import)

        count_caution = len(const.REDMINE_ISSUE_CAUTION)
        #txt_caution.delete(0,END)
        var_caution.set(count_caution-count_import)

        count_assigned = len(const.REDMINE_ISSUE_ASSIGNED)
        #txt_assigned.delete(0,END)
        var_assigned.set(count_assigned)

        print(count_import,count_caution,count_assigned)
        #time.sleep(15)

    root = tk.Tk()
    root.title(f'Redmine - {const.REDMINE_USR_NAME}')
    #root.iconbitmap('../static/icon/cobis-icon.ico')
    root.resizable(width=False, height=False)
    root.configure(background='#fff')
    # Obtenemos el largo y  ancho de la pantalla

    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    # Guardamos el largo y alto de la ventana
    wventana = 325
    hventana = 65
    # Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    # Se lo aplicamos a la geometría de la ventana
    root.geometry(f'{wventana}x{hventana}+{pwidth}+{pheight}')

    """# Label de inicio
    lbl_access = tk.Label(
        root,
        text='Indicadores',
        font=("Garamond", 12),
        justify=CENTER)
    #lbl_access.pack(pady=15)
    lbl_access.grid(row=0,column=0,columnspan=5)"""

    img_import = Image.open('./static/icon/import-ticket-icon.png')
    img_import = img_import.resize((30,30), Image.Resampling.LANCZOS)

    img_import_ticket = ImageTk.PhotoImage(img_import)

    # Button para tickets importante
    btn_import = tk.Button(
        root,
        background='#fff',
        image=img_import_ticket,
        relief="flat")
    #btn_import.pack(side=LEFT, padx=70, ipadx=20)
    btn_import.grid(row=1,column=0,padx=10,pady=15)

    # Crear una variable StringVar para almacenar el valor del Entry
    var_import = tk.StringVar()

    # Entry para tickets importante
    txt_import = tk.Entry(
        root,
        width=3,
        textvariable=var_import,
        readonlybackground='#fff',
        font=("Lato", 20),
        justify=CENTER,
        state='readonly')
    #txt_import.pack(pady=10, ipadx=100, ipady=5)
    txt_import.grid(row=1,column=1)

    img_caution = Image.open('./static/icon/caution-ticket-icon.png')
    img_caution = img_caution.resize((30,30), Image.Resampling.LANCZOS)

    img_caution_ticket = ImageTk.PhotoImage(img_caution)

    # Button para tickets menos importante
    btn_caution = tk.Button(
        root,
        background='#fff',
        image=img_caution_ticket,
        relief="flat")
    #btn_caution.pack(side=LEFT, padx=70, ipadx=20)
    btn_caution.grid(row=1,column=2,padx=10)

    # Crear una variable StringVar para almacenar el valor del Entry
    var_caution = tk.StringVar()

    # Entry para tickets menos importantes
    txt_caution = tk.Entry(
        root,
        width=3,
        textvariable=var_caution,
        readonlybackground='#fff',
        font=("Lato", 20),
        justify=CENTER,
        state='readonly')
    #txt_caution.pack(pady=10, ipadx=100, ipady=5)
    txt_caution.grid(row=1,column=3)

    img_assigned = Image.open('./static/icon/assigned-ticket-icon.png')
    img_assigned = img_assigned.resize((30,30), Image.Resampling.LANCZOS)

    img_assigned_ticket = ImageTk.PhotoImage(img_assigned)

    # Button para tickets asignados
    btn_assigned = tk.Button(
        root,
        background='#fff',
        image=img_assigned_ticket,
        relief="flat")
    #btn_assigned.pack(side=LEFT, padx=70, ipadx=20)
    btn_assigned.grid(row=1,column=4,padx=10)

    # Crear una variable StringVar para almacenar el valor del Entry
    var_assigned = tk.StringVar()

    # Entry para tickets asignados
    txt_assigned = tk.Entry(
        root,
        width=3,
        textvariable=var_assigned,
        readonlybackground='#fff',
        font=("Lato", 20),
        justify=CENTER,
        state='readonly')
    #txt_assigned.pack(pady=10, ipadx=100, ipady=5)
    txt_assigned.grid(row=1,column=5)

    """# Iniciar la función en segundo plano
    thread = threading.Thread(target=set_values_entry, args=(var_import, var_caution, var_assigned))
    thread.daemon = True  # Establece el hilo como demonio para que se cierre cuando se cierre el programa principal
    thread.start()"""

    # Función para actualizar periódicamente los valores
    def update_periodically():
        update_gui(var_import, var_caution, var_assigned)
        # Programa la próxima actualización en 60 segundos (60000 milisegundos)
        root.after(5000, update_periodically)

    # Iniciar la función de actualización periódica
    update_periodically()

    root.wm_attributes("-topmost", True) # Esta es la línea importante para superponer ventana a todos
    root.mainloop()

if __name__ == '__main__':
    panel_redmine()