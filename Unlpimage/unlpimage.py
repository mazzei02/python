import sys
from datetime import datetime
import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageDraw, ImageFont
import textwrap
from PIL.ExifTags import TAGS
import io
from tkinter import Tk, font
import json as js
import os
import mimetypes
import csv




from rutas import path as pt
from ventanas import ventanas as vt 
from ventanas import ventUsuario as vtu




##########################################3




###########################################3

try:
	with open(pt.ruta_archivo, 'x') as archivo:
		datos=[{"Alias": "Invitado", "Nombre": "Invitado", "Edad": '99', "Genero": "Otro", 'Genero_alt': 'No especificado', "Imagen": pt.convertir_para_guardar(pt.ruta_imagenes_defecto,pt.dir_proyecto)}]
		js.dump(datos,archivo)
except FileExistsError :
	pass
except PermissionError:
	sg.popup("No existe el archivo de usuarios y no tienes permiso de creacion.",title="Error escencial")
	sys.exit()
	
try:
    with open(pt.ruta_archivo, "r") as archivo:
        datos = js.load(archivo)
except PermissionError:
    sg.popup("No tienes permiso de lectura en un archivo vital para la aplicacion.",title="Error escencial")
    sys.exit()
except js.JSONDecodeError:
    sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
    sys.exit()

sg.theme('DarkGreen')




window = sg.Window('UNLP IMAGE', vt.layout_principal(datos))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window
        sys.exit()
        break
        
    elif event == "Anadir Usuario":
        window.hide()
        vtu.nuevo_usuario()
        window.close()                                                  ##Una vez añadido el nuevo usuario volvemos a abrir la ventana
                								  ## para poder ingresar a la nueva sesion
        
        
        with open(pt.ruta_archivo, "r") as archivo:
        	datos=js.load(archivo)
	
        window = sg.Window('UNLP IMAGE', vt.layout_principal(datos))

    elif event == "Mas usuarios":
    	window.hide()
    	
    	with open(pt.ruta_archivo, "r") as archivo:
        	datos=js.load(archivo)
    	vt.mas_usuarios(datos)
    	window.un_hide()
    
    elif event == "Cerrar":
          break

    else:
        window.hide()
        vtu.interfaz_usuario(event,datos)
        window.close()
        
        with open(pt.ruta_archivo, "r") as archivo:
        	datos=js.load(archivo)
	
        window = sg.Window('UNLP IMAGE', vt.layout_principal(datos))
        

window.close()                                         ##Si cualquier usuario inicia sesion, abrimos su interfaz


