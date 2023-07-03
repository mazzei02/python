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


#########################################################################################################################################

def insertar_salto_de_linea(texto, longitud):
    
    """Funcion que realiza un salto de linea al llegar a determinado
    numero de caracteres"""
    
    lineas = wrap(texto, longitud)
    return '\n'.join(lineas)


############################################################ Logs sistema ###############################################################

def logs_sistema(alias,operacion,valores='',texto=''):
    """Esta funcion toma por parametros "alias" correspondiente al 
    usuario que este usando la aplicacion y "operacion" que nos idica
    que accion realizo el usuario. 
    Esta funcion agrega estos datos, junton con la fecha y hora que las
    calcula, al archivo csv que lleva el registro.
    """
    
    try:
        timestamp = datetime.timestamp(datetime.now())
        #fecha_hora = datetime.fromtimestamp(timestamp)
        fecha = timestamp 
        
        lista = [alias, fecha, operacion,valores,texto]
        
        with open(pt.ruta_archivo_csv, 'a', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            if archivo.tell() == 0:  # Verificar si el archivo está vacío
                escritor_csv.writerow(["Usuario", "Fecha y hora", "Operacion","Valores","Textos"])
            escritor_csv.writerow(lista)
    
    except PermissionError:
        sg.popup('''No tienes permiso para guardar y registrar tus acciones
Es necesario para continuar''')
        sys.exit()
    except csv.Error:
         sg.popup("Un archivo vital no está en formato CSV válido.",title="Error escencial")
         sys.exit()


############################################################# CARGAR IMAGEN #############################################################

def cargar_imagen(path):

    """ Esta funcion toma por parametro "ruta" que es la ruta a la 
    imagen y retorna. Esta funcion abre la imagen seleccionada y 
    permite mostrarla en pantalla. 
    """

    image = Image.open(path)
    newsize = (200, 200)
    image = image.resize(newsize)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    image_data = image_bytes.read()
    return image_data



######################################################### FILTRAR ######################################################################

def filtrar(*listas):
    """ Esta es una funcion que dadas una serie de listas filtra los elementos y devuelve una sola lista 
    con todos los elementos sin repetir que haya en las listas ingresadas por parametro"""
    lista_filtrada = reduce(lambda x,y: x+y, listas)
    return list(set(lista_filtrada))



__all__ = ['filtrar','logs_sistema','cargar_imagen','insertar_salto_de_linea']
