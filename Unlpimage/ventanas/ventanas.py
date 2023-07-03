import sys
from datetime import datetime
import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageDraw, ImageFont
import textwrap
from PIL.ExifTags import TAGS
import io
from tkinter import Tk, font
import pandas as pd
import json as js
import os
import mimetypes
import csv

from funciones import funciones as fn
from funciones import funcJson as fj
from funciones import funcImagenes as fim
from funciones import funcCSV as fcsv
from ventanas import ventUsuario as vtu
from rutas import path as pt





################################################ AYUDA #################################################################################

def ayuda():
    


    """Esta funcion abre la pantalla de ayuda, una pantalla con consejos para el usuario"""
    
    
    layout = [
        [sg.Text("""Para anadir etiquetas a su imagén presione el boton etiquetar imagen.

Si desea generar un collage presione generar collage.

Si desea generar un meme presione generar meme.

Presione configuración para seleccionar las carpetas en donde se leeran los archivos. 

Si desea editar su usuario, presione su imagen de perfil.

Si desea cerrar su sesión presione Salir""", 
                 font=("Courtier", 10, "bold italic"), justification="left", size=(40, 20)),
                 sg.Text('', size=(30,1)),sg.Button("Cancelar", font=("Arial", 12), size=(10, 1), 
                 border_width=0, pad=(20, 5), key="-CANCELAR-")]
    ]



# Creamos la ventana con el layout definido
    window = sg.Window("Ayuda", layout)

# Bucle para leer los eventos de la ventana
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-CANCELAR-"):
            break

# Cerramos la ventana y finalizamos la aplicación
    window.close()



    

########################################################### VENTANA PRINCIPAL ############################################################

def layout_principal(datos):

	""" Pantalla que aparece al momento de abrir el programa."""
	layout = [ [ sg.Text('UNLPImage!!', size=(10,1), font=('Courier', 30, 'bold italic'), pad=((0,0), (0,0))), sg.Text('', size=(30,1))]]
         
	if len(datos) >= 8:
	    datos_dividido = [datos[i:i+9] for i in range(0, len(datos), 9)]
	else:
	    datos_dividido = [datos]


	listas_de_botones = []
	for sublista in datos_dividido:
	    linea_de_botones = [sg.Button(key=diccionario['Alias'], tooltip=diccionario["Alias"], image_filename=pt.convertir_guardado_para_usar(diccionario['Imagen'], pt.dir_proyecto), pad=((0, 0), (20, 0))) for diccionario in sublista]
	    listas_de_botones.append(linea_de_botones)

	layout.append(listas_de_botones[0])

	layout.append([sg.Button("Anadir Usuario", pad=((0,5),(20,5))),sg.Button('Mas usuarios', pad=((0,240),(20,5))),sg.Button('Cerrar programa',button_color=('white', 'red'), pad=((0,0),(20,5)),key = 'Cerrar')])
	
	return layout
	
######################################################################################################################################   


def mas_usuarios(datos):

	""" Pantalla que muestra mas usuarios """

	layout = [ [ sg.Text('Mas usuarios', size=(14,1), font=('Courier', 30, 'bold italic'), pad=((0,0), (0,0))), sg.Text('', size=(30,1))]]
         
	if len(datos) >= 8:
	    datos_dividido = [datos[i:i+9] for i in range(0, len(datos), 9)]
	else:
	    datos_dividido = [datos]


	listas_de_botones = []
	for sublista in datos_dividido:
	    linea_de_botones = [sg.Button(key=diccionario['Alias'], tooltip=diccionario["Alias"], image_filename=pt.convertir_guardado_para_usar(diccionario['Imagen'], pt.dir_proyecto), pad=((0, 0), (20, 0))) for diccionario in sublista]
	    listas_de_botones.append(linea_de_botones)

	layout.append(listas_de_botones)
	
	window = sg.Window('UNLP IMAGE', layout)
	
	while True:
		event, values = window.read()
		
		if event == sg.WIN_CLOSED: # if user closes window
		
		        break
		else:
			window.hide()
			vtu.interfaz_usuario(event,datos)
			window.close()
			
    ######################################################  CONFIGURACION ################################################################




def configuracion(evento):

    """ Esta es la funcion que abre la ventana de configuracion """



    

    
    layout = [
        [sg.Text("Configuración", font=("Courtier", 30, "bold italic"), justification="left", size=(15, 1)),sg.Text('', size=(30,1)),sg.Button("Cancelar", font=("Arial", 12), size=(10, 1), border_width=0, pad=(20, 5), key="-CANCELAR-")],
        [sg.Text("Repositorio de imágenes", font=("Arial", 14), justification="left", pad=((200, 5),(100,5)))],
        [sg.InputText(font=("Arial", 12), size=(40, 1), disabled=True, key="Carpeta_Imagenes", pad=(100, 0)), sg.FolderBrowse(font=("Arial", 12), button_text="Browse", initial_folder=pt.ruta_carpeta_imagenes, size=(10, 1))],
        [sg.Text("Repositorio de collage", font=("Arial", 14), justification="left",  pad=((200, 5),(10,5)))],
        [sg.InputText(font=("Arial", 12), size=(40, 1), disabled=True, key="Collage", pad=(100, 0)), sg.FolderBrowse(font=("Arial", 12), button_text="Browse", initial_folder=pt.ruta_carpeta_collages, size=(10, 1))],
        [sg.Text("Repositorio de memes", font=("Arial", 14), justification="left",  pad=((200, 5),(10,5)))],
        [sg.InputText(font=("Arial", 12), size=(40, 1), disabled=True, key="Memes", pad=(100, 0)), sg.FolderBrowse(font=("Arial", 12), button_text="Browse", initial_folder=pt.ruta_carpeta_memes, size=(10, 1))],
        [sg.Button("Guardar", font=("Arial", 12), size=(10, 1), border_width=0, pad=((660, 20),(100,0)), key="-GUARDAR-")],
    ]

# Creamos la ventana con el layout definido
    window = sg.Window("Configuración", layout)

    

# Bucle para leer los eventos de la ventana
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-CANCELAR-"):
            break
        elif event == "-GUARDAR-":      
            try:    
                # Mas adelante vemos en donde guardamos las direcciones de donde se guardan las imagenes
                Diccionario_de_direcciones={"Alias":evento,"Repositorio de imagenes":pt.convertir_para_guardar(values["Carpeta_Imagenes"]),"Repositorio de collage":pt.convertir_para_guardar(values["Collage"]),"Repositorio de memes":pt.convertir_para_guardar(values["Memes"])}

                fj.manejo_archivo_json(4,pt.ruta_configuracion,**Diccionario_de_direcciones)
                fn.logs_sistema(evento,'Cambio_configuración')
            
                sg.popup("Se ha guardado la configuracion")
            except ValueError:
                sg.popup("Por favor, no olvide aclarar todas las rutas de configuracion", title= "Todas las rutas son necesarias")


            

            

# Cerramos la ventana y finalizamos la aplicación
    window.close()
        

__all__ = ['ayuda', 'layout_principal', 'mas_usuarios', 'configuracion']

