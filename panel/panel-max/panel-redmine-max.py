from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk

root = tk.Tk()
root.title('Redmine - ')
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
    text='Biemvenido',
    font=("Garamond", 12))
lbl_access.pack(pady=15)

root.mainloop()
