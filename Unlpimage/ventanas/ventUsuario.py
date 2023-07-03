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
from rutas import path as pt
from ventanas import ventAcc as vta
from ventanas import ventanas as vt



############################################################## NUEVO USUARIO ############################################################

def nuevo_usuario():

    """ Esta es la pantalla para un perfil de nuevo usuario, aqui se puede crear un nuevo usuario """


    
    
    izquierda = [[sg.Frame('Nuevo Usuario:',[
                          [sg.Text('Nuevo Perfil',size=(20, 1), font=('courier',30, "bold italic"), justification='left')],
                          [sg.Text('Alias'), sg.InputText(key='Alias')],
                          [sg.Text('Nombre'), sg.InputText( key='Nombre')],
                          [sg.Text('Edad'),sg.InputText( key='Edad') ],
                          [sg.Text('Genero autopercibido'), sg.Combo(values=['Masculino', 'Femenino', 'Otro'],default_value="Masculino", key='Genero', size=(30, 6))],
                          [sg.Text('''En caso de otro 
(SI NO CORRESPONDE ´-´):'''), sg.InputText(key='Genero_alt')]])]]

    derecha = [
        [sg.Text('Selecciona una imagen:', justification="center"), sg.InputText(default_text=pt.ruta_imagenes_defecto,disabled = True, key='Imagen'), sg.FileBrowse(initial_folder=pt.ruta_imagenes)],
        [sg.Image(key='image_display')],
        [sg.Button('Previsualizar', pad=((300,0),(50,0)), key='show_image')],
        [sg.Button('Volver', pad=((300,0),(50,0)), key='Volver')]
    ]

    layout = [
        [sg.Column(izquierda), sg.VSeperator(), sg.Column(derecha)],
        [sg.Button('Guardar', pad=((850,0),(20,20)))],
    ] 

    window = sg.Window('CREACION DE PERFIL', layout, margins=(200, 150))

    while True:
      try:
        event, values = window.read()
        if event == 'show_image':
            image_path = values['Imagen']
            if image_path:
                image_data = fn.cargar_imagen(image_path)
                window['image_display'].update(data=image_data)
        
                window['image_display'].update(data=image_data)
        elif event == 'Guardar':
            values['Imagen'] = pt.convertir_para_guardar(values['Imagen'],pt.dir_proyecto)
            values.pop('Browse')
            fj.manejo_archivo_json(1, pt.ruta_archivo, **values)
        elif event == sg.WIN_CLOSED or event == 'Volver': # if user closes window or clicks back button
            break
        else:
            print(event)
      except ValueError:
         sg.Popup("Por favor, vuelva a crear el usuario escribiendo un número entero como edad",title="Atención")

    window.close()

#################################################### INTERFAZ USUARIO ####################################################################

def interfaz_usuario(evento,datos):

    """ Pantalla que maneja la interfaz principal del usuario """
    
    
    
    
    #print(event)
    for dictionary in datos:
        if evento == dictionary["Alias"]:
             imagen2 = sg.Button(key='Editar',image_filename=pt.convertir_guardado_para_usar(dictionary['Imagen'],pt.dir_proyecto)) 
             #print(event)
             #print(dictionary["Imagen"])
             #print(imagen2)
               

    layout = [
        [imagen2,sg.Text('', size=(30,1)), sg.Button('Configuración', size=(10,1), pad=((0,0), (0,0)), key='Configuracion'), sg.Button('Ayuda', size=(10,1), pad=((0,0), (0,0)), key='Ayuda')],
        [sg.Text(evento,size=(60,1))],
        [sg.Button('Etiquetar Imagenes', size=(15,2), pad=((200,0), (100,0)), key='Etiquetar')],
        [sg.Button('Generar Meme', size=(15,2), pad=((200,0), (10,0)), key='Meme')],
        [sg.Button('Generar Collage', size=(15,2), pad=((200,0), (10,0)), key='Collage')],
        [sg.Button('Salir', size=(15,2), pad=((200,0), (10,0)), button_color=('white', 'red'), key='Salir')],
        [] 
    ]

    # Crear la ventana
    window = sg.Window('Menu principal', layout)

    # Bucle principal del programa
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Salir":
            break

        elif event == 'Configuracion':
            window.hide()          
            vt.configuracion(evento)
            window.un_hide()

        elif event == 'Ayuda':
            window.hide()
            vt.ayuda()
            window.un_hide()
            
        elif event == 'Editar':
            window.hide()
            editar_usuario(evento)
            
            try:
            	with open(pt.ruta_archivo, "r") as archivo:
            		datos = js.load(archivo)
            except PermissionError:
            	sg.popup("Error de permisos al abrir el archivo.")
            except js.JSONDecodeError:
            	sg.popup("Error al decodificar el archivo JSON.")
        	
            for dictionary in datos:
                 if evento == dictionary["Alias"]:
                     imagen_nueva=pt.convertir_guardado_para_usar(dictionary['Imagen'],pt.dir_proyecto)
                     window['Editar'].Update(image_filename=imagen_nueva)
            window.un_hide()


        elif event == "Etiquetar":
            window.hide()
            vta.etiquetado(evento)
            window.un_hide()

        elif event == "Meme":
            window.hide()
            vta.Meme(evento)
            window.un_hide()

        elif event == "Collage":
            window.hide()
            vta.collage(evento)    
            window.un_hide()    
    


    # Cerrar la ventana
    window.close()



########################################################## EDITAR USUARIOS #############################################################

def editar_usuario(evento):

    """ Esta es la pantalla para un perfil de editar usuario, aqui se puede manipular los datos de un usuario """
    
    try:
	    with open(pt.ruta_archivo) as archivo:
         
        	 usuarios=js.load(archivo)
    except PermissionError:
    	    sg.popup('No tienes permiso para leer un archivo escencial')
    	    return
    except js.JSONDecodeError:
    	    sg.popup("Error al decodificar el archivo JSON.")
    	    return
         
    usuario_actual = None
    for dicc in usuarios:
        if evento in dicc["Alias"]:
            usuario_actual = dicc
            break

    if usuario_actual is None:
        return

    Nombre_original = usuario_actual['Nombre']
    Edad_original = usuario_actual['Edad']
    Genero_original = usuario_actual['Genero']
    Genero_alt_original = usuario_actual['Genero_alt']
    Imagen_original = usuario_actual['Imagen']

    image_data = fn.cargar_imagen(pt.convertir_guardado_para_usar(Imagen_original,pt.dir_proyecto))

    izquierda = [
        [sg.Frame('Editar Usuario:',[
            [sg.Text('Editar Perfil',size=(20, 1), font=('courier',30, "bold italic"), justification='left')],
            [sg.Text('Alias'), sg.InputText(key='Alias', default_text=evento)],
            [sg.Text('Nombre'), sg.InputText(key='Nombre', default_text=Nombre_original)],
            [sg.Text('Edad'), sg.InputText(key='Edad', default_text=Edad_original)],
            [sg.Text('Genero autopercibido'), sg.Combo(values=['Masculino', 'Femenino', 'Otro'], key='Genero',default_value=Genero_original, size=(30, 6))],
            [sg.Text('''En caso de otro 
            (SI NO CORRESPONDE ´-´):'''), sg.InputText(key='Genero_alt', default_text=Genero_alt_original)]
        ])]
    ]

    derecha = [
        [sg.Text('Selecciona una imagen:', justification="center"), sg.FileBrowse(initial_folder=pt.ruta_imagenes, key='Imagen')],
        [sg.Image(key='image_display', data=image_data)],
        [sg.Button('Previsualizar', pad=((300,0),(50,0)), key='show_image')],
        [sg.Button('Volver', pad=((300,0),(50,0)), key='Volver')]
    ]

    layout = [
        [sg.Column(izquierda), sg.VSeperator(), sg.Column(derecha)],
        [sg.Button('Guardar', pad=((850,0),(20,20)))],
    ]

    window = sg.Window('EDICION DE PERFIL', layout, margins=(200, 150))

    image_path = None
    while True:
      try:
        event, values = window.read()
        if values['Alias'] != evento:
            sg.popup('No se puede cambiar el alias de usuario', title='Error: Cambio de alias de usuario')
        
        if event == 'show_image':
            image_path = values['Imagen']
            if image_path:
                image_data = fn.cargar_imagen(image_path)
                window['image_display'].update(data=image_data)
        
        elif event == 'Guardar':
            if image_path is None:
                values['Imagen'] = Imagen_original
            else:
                values['Imagen']=pt.convertir_para_guardar(values['Imagen'],pt.dir_proyecto)
            
            fj.manejo_archivo_json(7, pt.ruta_archivo, **values)
            
        
        elif event == sg.WIN_CLOSED or event == 'Volver':
            break
      except ValueError:
        sg.Popup("Por favor, vuelva a editar el usuario escribiendo un número entero como edad",title="Atención")

    window.close()


__all__ = ['nuevo_usuario', 'interfaz_usuario', 'editar_usuario']

