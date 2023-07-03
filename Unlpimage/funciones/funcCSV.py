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

################################################### SOBREESCRIBIR CSV ###################################################################

def sobreescribir_csv(contenido_csv,posicion,datos_imagen_original,lista):
    """ Esta funcion toma por parametros: "contenido_csv" que tiene el contenido del archivo csv, "posicion" que marca cual es la linea del csv  modificar, "datos_imagen_original" que son los datos originales a sobrescribir y "lista" que contiene los nuevos datos.
Esta funcion sobreescribe los datos ingresados por el usuario para una imagen que ya este usada, sobreescribiendo todos menos las etiquetas que simplemente agrega las que sean nuevas sin repetirlas."""
  
    datos_imagen_mod = datos_imagen_original[:] #copiamos la lista
    datos_imagen_mod[1:7] = lista[1:7] #reecribimos todos los datos despues de la ruta
        
    
    fila_a_modificar = posicion #decimos en donde queremos poner esto
    contenido_csv[fila_a_modificar] = datos_imagen_mod #metemos la linea modificada (elemento de lista) en el lugar correcto
        
    return contenido_csv
    
#################################################### MANEJO CSV ##########################################################################

def manejo_archivo_csv(lista,evento): #lista (son 4 cosas), text(string), tags(lista, un elemento lista), ultact(string) y fecha(int) 
    """Esta funcion toma por parametros: "lista" tiene los datos ingresados por pantalla (ruta, resolucion, tama�o, tipo, texto descriptivo, ultima actualizacion y fecha), "ruta_tags" es la ruta al archivo csv que contiene la informacion y "evento" que nos dice cual fue el evento. 
Esta funcion sobreescribe los datos si ya excisten y sino los agrega al csv"""
    
    try :
        
       archivo_csv = open(pt.ruta_tags,"x")
       escritor_csv = csv.writer(archivo_csv, delimiter = ",")
       escritor_csv.writerow(["Direccion del archivo", "Resolucion", "Tamano en MB", "Mimetype", "Descripcion", "Tags",  "Ultima actualizacion", "Fecha"])
       archivo_csv.close()

    except FileExistsError :
       pass
    except PermissionError:
       sg.popup("No existe el archivo de tags y no tienes permiso de creacion.",title="Error escencial")
       sys.exit()

    try:     
       archivo_csv= open(pt.ruta_tags, 'r+') #abrimo con lectoescritura
       lector_csv = csv.reader(archivo_csv) #hacemos el lector
    #leemos el encabezado
    
    except PermissionError:
         sg.popup("No tienes permiso de lectura en un archivo vital para la aplicacion.",title="Error escencial")
         sys.exit()
    except csv.Error:
         sg.popup("Un archivo vital no está en formato CSV válido.",title="Error escencial")
         sys.exit()
 
    encabezado = next(lector_csv)
    contenido_csv = []
    for linea in lector_csv:
	    contenido_csv.append(linea) #bajamos los datos a una lista con la que vamos a trabajar
    
    posicion = 0 #iniciamos la posicion
    
    for i, sublist in enumerate(contenido_csv): #leemos cada elemento de la lista (que son sub listas) y guardamos su posicion
    	if lista[0] in sublist: #buscamos el elemento de la lista  con la ruta repetida
            posicion = i+1 #marcamos la posicion
            datos_imagen_original = sublist #variable auxiliar con los dato de esa sublista donde se repite la ruta
            break
    	else: #este es lo que va a hacer su si la ruta no esta repatida 
            datos_imagen_original = lista #en este caso escribimos la lista de manera comun 
    
    if posicion != 0:
        sobreescribir_csv(contenido_csv,posicion-1,datos_imagen_original,lista)
        fn.logs_sistema(evento,'Modificación de imagen.')

    else: 
        contenido_csv.append(lista)
        fn.logs_sistema(evento,'Nueva imagen clasificada.')
    

    #aca escribimos todo en el csv de nuevo con encabezado y todo
    try:
	    with open(pt.ruta_tags, 'w',newline='') as archivo_csv: #abrimos en escritura y pisamos todo
        	escritor_csv = csv.writer(archivo_csv) #hacememos el lector
        	escritor_csv.writerow(encabezado) #escribimos el encabezado en la primer linea
        	escritor_csv.writerows(contenido_csv) #reescribimos el csv con los nuevos datos
    except PermissionError:
    	    sg.popup('No tienes permiso para escribir este archivo, no se guardaran los cambios')
    	    
    	    
############################################## VERIFICAR IMAGEN ######################################################################

def verificar_imagen(ruta_imagen): #"ruta_imagen" es la ruta a la imagen que estamos viendo si esta en el csv
    """Esta funcion toma por parametros: "ruta_imagen" que es la ruta de la imagen que esta verificando.
Esta funcion va a verificar si la imagen ya esta en el csv y de ser asi va a extraer la metadata."""
      

    try :
    
       archivo_csv = open(pt.ruta_tags,"x")
       escritor_csv = csv.writer(archivo_csv, delimiter = ",")
       escritor_csv.writerow(["Direccion del archivo", "Resolucion", "Tamano en MB", "Mimetype", "Descripcion", "Tags",  "Ultima actualizacion", "Fecha"])
       archivo_csv.close()

    except FileExistsError :
       pass
       
    except PermissionError:
         sg.popup("No existe el archivo de usuarios y no tienes permiso de creacion.",title="Error escencial")
         sys.exit()
       
    try:

       with open(pt.ruta_tags, "r") as archivo_csv:
           lector_csv = csv.DictReader(archivo_csv) #hacemos el lector
           contenido_csv = list(lector_csv) #leemos el contenido
        
       #veamos si la ruta de la imagen ya esta en el csv
    except PermissionError:
         sg.popup("No tienes permiso de lectura en un archivo vital para la aplicacion.",title="Error escencial")
         sys.exit()
    except csv.Error:
         sg.popup("Un archivo vital no está en formato CSV válido.",title="Error escencial")
         sys.exit()


    
    filtro=filter(lambda x: x["Direccion del archivo"] == ruta_imagen, contenido_csv)
    imagen_filtro=dict([(linea["Direccion del archivo"],list(linea.values())[0:6]) for linea in filtro])   


    if len(imagen_filtro) != 0: #esto significa que el filtro encontro algo
        metadata=imagen_filtro[ruta_imagen]#[1:5] #corresponde a las columnas de la metadata 
        return metadata
    else:
        
        return 

__all__ = ['sobreescribir_csv', 'manejo_archivo_csv', 'verificar_imagen']

