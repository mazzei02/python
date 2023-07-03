import sys
from datetime import datetime
import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageDraw, ImageFont
from textwrap import wrap
from PIL.ExifTags import TAGS
import io
from tkinter import Tk, font
import json as js
import pandas as pd
import os
import mimetypes
import csv 

from rutas import path as pt
from funciones import funciones as fn


def manejo_datos_usuario(datos_usuarios,alias,**values):

    """ Esta funcion toma por parametros: "datos_usuarios" que contiene los datos del archivo json que contine la informacion del usuario, "alias" es el alias del usuario, "ruta" es la ruta de la imagen elegida por el usuario y "**values" el diccionario de valores que retorna la ventana.
Esta funcion invoca a la funcion verificar_datos_en_json y si los datos son correctos se encarga de tomar y a�adir nuevos usuarios al json"""

    edad=list(values.values())[2]
    aviso = verificar_datos_en_json(datos_usuarios,alias,edad,1)#llamamos a la funcion que verifica los datos
    if aviso == "nuevo":
        error = None 
        dicc_aux= {} #usamos un diccionario auxiliar que despues vamos a agregar al json original
        for i in range(len(values.keys())):
            lista1 = list(values.keys()) #tomamos las claves que ya estan en el json original
            lista2 = list(values.values()) #tomamos los valores que ingreso el usuario
            dicc_aux[lista1[i]] = lista2[i] #armamos el diccionario nuevo
        datos_usuarios.append(dicc_aux) #metemos los datos en la variable
        sg.popup("Se ha guardado el usuario")
        fn.logs_sistema(values['Alias'],"Nuevo usuario")
    else: 
        error = "el alias ingresado ya existe, prueve con otro" 
        return error
   
    return error

###################################################### DATOS CONFIGURACION #############################################################


def manejo_json_configuracion(datos_archivo, alias, **values):
    """ Esta funcion toma por parametro: "datos_archivo" que toma los datos del json, "alias" es el alias del usuario y "**values" el diccionario de valores que retorna la ventana. 
Esta funci�n se encarga de manejar el guardado de las carpetas configuradas por el usuario."""

    # Crear un diccionario auxiliar con los valores actualizados
    dicc_aux = {'Alias': values['Alias'], 'Repositorio de imagenes': values['Repositorio de imagenes'], 
                'Repositorio de collage': values['Repositorio de collage'], 'Repositorio de memes': values['Repositorio de memes']}
    
    # Crear una nueva lista con los valores actualizados
    datos_actualizados = [dicc_aux if elem['Alias'] == alias else elem for elem in datos_archivo]
    
    # Si no se encontró el usuario en la lista, agregar un nuevo elemento
    if not any(elem['Alias'] == alias for elem in datos_archivo):
        datos_actualizados.append(dicc_aux)
        
    # Reemplazar la lista original con la lista actualizada
    datos_archivo[:] = datos_actualizados
    
    return
    
############################################################ DATOS NUEVOS USUARIOS #######################################################


def manejo_archivo_json(ventana,ruta_archivo,**values): #el ** es porque el values del layout es un diccionario

    """ esta funcion agrega los datos de los nuevos usuarios al json que contiene todos los usuarios"""
    
    try:
        with open(ruta_archivo, "x") as archivo:
           datos = []
           js.dump(datos, archivo,indent=4)
	
    except FileExistsError :
        pass
    except PermissionError:
        sg.popup("No existe el archivo de usuarios y no tienes permiso de creacion.",title="Error escencial")
        sys.exit()

    try:    
        with open(ruta_archivo,"r") as archivo: #"archivo" es la ruta al json, en el programa es ruta archivo 
    
           datos_archivo=js.load(archivo) #bajamos los datos de json a una variable datos
           alias = list(values.values())[0] #tomamos el valor del alias ingresado por el usuario
    except PermissionError:
           sg.popup("No tienes permiso de lectura en un archivo vital para la aplicacion.",title="Error escencial")
           sys.exit()
    except js.JSONDecodeError:
           sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
           sys.exit()

        
    if ventana == 1:
            
            error=manejo_datos_usuario(datos_archivo,alias,**values)
            if error != None:
                return error


    elif ventana == 4:
            manejo_json_configuracion(datos_archivo, alias, **values)
            error=None
            
    elif ventana ==7:
            manejo_json_edicion_de_perfil(datos_archivo, alias, **values)
            error =None


            
    with open(ruta_archivo,"w") as archivos: #abrimos de nuevo para meter los datos nuevos, es con w para que me escriba
                                             #los nuevo datos 
        js.dump(datos_archivo,archivos,indent=4)
        
    return error
    
#########################################################################################################################################


def verificar_datos_en_json(datos_json, dato,edad,pantalla):

    """ Esta funcion toma por parametros: "datos_json" que son los datos del archivo json, "dato" es el alias ingresado por el usuario,"edad" es la edad ingresada por el usuario y "pantalla" nos dice donde fue invocada la funcion.
Esta funcion verifica que el alias no este repetido y que la edad este entre 18 y 100 anos."""


    # Cargamos los datos JSON
    #datos = js.loads(datos_json)
    clave = "Alias"
    chequeo_edad='Edad'
    # Buscamos el dato en el diccionario
    for elem in datos_json:
        check = elem[clave] if pantalla ==1 else None
        check2= int(edad)
        if (dato == check) or (check2 not in range(18,101)): #datos.values():
            sg.popup('Los datos ingresados son incorrectos, recuerde que la edad debe ser un numero entero entre 18 y 100 y el Alias no debe estar tomado.', title='Advertencia: Datos incorrectos.')
            x='repetido'
            return x
        else:
            x = "nuevo"
            
    return x

#########################################################################################################################################
def manejo_json_edicion_de_perfil(datos_archivo, alias, **values):

    """ Esta funcion toma por parametros: "datos_archivo" que contine la informacion de un archivo json, "alias" que indica el usuario que esta usando la aplicacion y "**values" el diccionario de valores que retorna la ventana.
Esta funcion invoca la funcion "verificar_datos_en_json" para verificar que el alias no este repetido y luego spbreescribe los datos que el usuario este cambiando en json que los almacena. """
   
   
    edad=list(values.values())[2]
    aviso = verificar_datos_en_json(datos_archivo,alias,edad,7)#llamamos a la funcion que verifica los datos
    
    if aviso == "repetido":
        return

    diccionario_aux = {'Alias':values['Alias'], 'Nombre':values['Nombre'], 'Edad':values['Edad'], 
                       'Genero':values['Genero'], 'Genero_alt':values['Genero_alt'], 'Imagen':values['Imagen']}

    resultados = list(filter(lambda x: x['Alias'] == alias, datos_archivo))
    if resultados:
        list(map(lambda x: datos_archivo.__setitem__(datos_archivo.index(x), diccionario_aux), resultados))
        sg.popup('Se han guardado los cambios, vuelva a iniciar sesion para ver los cambios')
        fn.logs_sistema(values['Alias'],'Perfil modificado')
    
    return

__all__ = ['manejo_datos_usuario', 'manejo_json_configuracion', 'manejo_archivo_json', 'verificar_datos_en_json', 'manejo_json_edicion_de_perfil']

