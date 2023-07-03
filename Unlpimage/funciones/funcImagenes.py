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



#################################################### SELECCIONAR DE DISEnO DE COLLAGE ####################################################



def crear_collage_vertical(imagenes):

    """Esta funcion crea un collage en vertical para las imagenes
    dadas"""
    altura_total = sum(imagen.size[1] for imagen in imagenes)
    anchura_total = max(imagen.size[0] for imagen in imagenes)

    collage = Image.new('RGB', (anchura_total, altura_total))
    y_offset = 0

    for imagen in imagenes:
        collage.paste(imagen, (0, y_offset))
        y_offset += imagen.size[1]

    return collage


def crear_collage_horizontal(imagenes):

    """Esta funcion crea un collage en horizontal para las imagenes
    dadas"""
    anchura_total = sum(imagen.size[0] for imagen in imagenes)
    altura_total = max(imagen.size[1] for imagen in imagenes)

    collage = Image.new('RGB', (anchura_total, altura_total))
    x_offset = 0

    for imagen in imagenes:
        collage.paste(imagen, (x_offset, 0))
        x_offset += imagen.size[0]

    return collage


def crear_collage_triple(imagenes):

    """Esta funcion crea un collage de tres imagenes para 
    las imagenes dadas"""
    anchura_total = imagenes[0].size[0] + imagenes[1].size[0]
    altura_total = max(imagenes[0].size[1], imagenes[1].size[1])

    for imagen in imagenes[2:]:
        altura_total += imagen.size[1]
        anchura_total = max(anchura_total, imagen.size[0])

    collage = Image.new('RGB', (anchura_total, altura_total))
    x_offset = 0

    for imagen in imagenes[:2]:
        collage.paste(imagen, (x_offset, 0))
        x_offset += imagen.size[0]

    y_offset = max(imagenes[0].size[1], imagenes[1].size[1])

    for imagen in imagenes[2:]:
        new_width = anchura_total
        new_height = altura_total - y_offset
        imagen_modificada = imagen.resize((new_width, new_height))
        collage.paste(imagen_modificada, (0, y_offset))
        y_offset += new_height

    return collage


def crear_collage_cuadruple(imagenes):

    """Esta funcion crea un collage de 4 imagenes para las imagenes
    dadas"""
    anchura_total = max(imagen.size[0] for imagen in imagenes)
    altura_total = max(imagen.size[1] for imagen in imagenes)

    collage = Image.new('RGB', (anchura_total * 2, altura_total * 2))

    collage.paste(imagenes[0], (0, 0))
    collage.paste(imagenes[1], (anchura_total, 0))
    collage.paste(imagenes[2], (0, altura_total))
    collage.paste(imagenes[3], (anchura_total, altura_total))

    return collage


def seleccionador_diseno_collage(rutas_imagenes, ruta_salida, diseno, titulo_collage):
    # Carga las imágenes
    imagenes = [Image.open(io.BytesIO(fn.cargar_imagen(ruta))) for ruta in rutas_imagenes]

    # Definir diccionario de disenos y funciones correspondientes
    diccionario_disenos = {
        'Diseno 1': crear_collage_vertical,
        'Diseno 2': crear_collage_horizontal,
        'Diseno 3': crear_collage_triple,
        'Diseno 4': crear_collage_cuadruple
    }

    # Verificar si el diseno existe en el diccionario
    if diseno in diccionario_disenos:
        # Obtener la función correspondiente al diseno
        funcion_creacion_collage = diccionario_disenos[diseno]

        # Crear el collage utilizando la función correspondiente
        collage = funcion_creacion_collage(imagenes)

        # Agregar el título al collage
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(collage)
        titulo_posicion = (int(collage.width * 0.02), int(collage.height * 0.92))
        draw.text(titulo_posicion, titulo_collage, (255, 255, 255), font=font)

        # Guardar el collage con el título
        collage.save(ruta_salida)
    else:
        print("Error, hubo problemas en la seleccion de disenos")

################################################ VERIFICADOR DE ETIQUETAS ###############################################################

def verificar_etiquetas_imagenes(rutas_imagenes, evento):

    """Esta funcion verifica si una imagen pertenece al archivo de
    imagenes etiquetadas antes de permitir la creacion de un collage
    con la misma. Toma como argumentos:
    evento: El usuario que se encuentra operando"""
    
    df = pd.read_csv(pt.ruta_tags)
    etiquetas_imagenes = df['Direccion del archivo']
    imagenes_faltantes = []

    rutas_imagenes_relativas=[pt.convertir_para_guardar(ruta_imagen,pt.dir_proyecto) for ruta_imagen in rutas_imagenes]
    
    for ruta_imagen in rutas_imagenes_relativas:
        if ruta_imagen not in list(etiquetas_imagenes):
            imagenes_faltantes.append(ruta_imagen)
    
    if len(imagenes_faltantes) > 0:
        mensaje = "Las siguientes imágenes faltan etiquetar:\n" + "\n".join(imagenes_faltantes)
        sg.popup('Imágenes faltantes', mensaje)
        

        return False
    
    return True


###########################################################################################################################################


def escritor_de_imagenes(meme,fuente_de_texto,carpeta_memes,cuadros_texto_coords,*textos):

	'''Esta funcion escribe texto sobre las imagenes. Sus argumentos de entrada son:
	meme: El path a el template que estemos usando
	fuente_de_texto: El path a la fuente que estemos usando
	carpeta_memes: El path a donde guardar los memes una vez terminados
	cuadros_texto_coord: La informacion de la posicion de los textos en la imagen
	textos (lista variable): La lista de contenidos de cada cuadro de texto'''

	nombre_del_template=meme.split('/')[-1]
	
	
	# Abrir la imagen
	imagen = Image.open(meme)   ###Primero esta esto, abre la imagen. En el programa esto tendria que venir de 									afuera, porque tenemos templates predeterminados

	# Crear un objeto ImageDraw para dibujar en la imagen
	dibujo = ImageDraw.Draw(imagen)

	# Definir el texto a escribir
	
	for indice, caption in enumerate(textos):
		if len(caption) > 20:
			caption = fn.insertar_salto_de_linea(caption, 20)

		# Definir la fuente y el tamano del texto
		escala = 80
		fuente =ImageFont.truetype(fuente_de_texto, escala)  ### DEFINI UNA CARPETA DE FUENTES incluso descargue unas bonitas. 										Esa carpeta de fuentes se llama /fonts/ y esta dentro de 											grupo 18. Habria que escribir esto mas bonito, pero bue

	
		# Define las coordenadas de la posición inicial y límite
		x_inicio, y_inicio = cuadros_texto_coords[indice]['top_left_x'], cuadros_texto_coords[indice]['top_left_y']
		x_limite, y_limite = cuadros_texto_coords[indice]['bottom_right_x'], cuadros_texto_coords[indice]['bottom_right_y']
		
		ancho_max = x_limite - x_inicio
		alto_max = y_limite - y_inicio
	
		# Dibuja un rectángulo que representa el área límite
		
		while True:
	
			rectangulo = dibujo.textbbox((x_inicio, y_inicio), caption, font=fuente)
		
	
			# Calcula la posición central del área límite
			ancho = rectangulo[2] - rectangulo[0] 
			alto = rectangulo[3] - rectangulo[1]
			
			if ancho > ancho_max or alto > alto_max:
				escala-=2
				fuente =ImageFont.truetype(fuente_de_texto, escala)
			else:
				break
		
		posicion_x = rectangulo[0]
		posicion_y = rectangulo[1] 
		
			
		
		# Escribir el texto en la imagen
		dibujo.text((posicion_x, posicion_y), caption, font=fuente, fill=(0, 0, 0))  # Cambia el color del texto si lo deseas

	###Aca las posiciones deberian salir del json, texto es el texto ingresado por el usuario, la fuente tambien y fill es el color de la letra (que personalmente no creo que se pueda cambiar, pero no recuerdo)

	# Guardar la imagen con el texto agregado
	

	newsize = (600, 600)
	imagen = imagen.resize(newsize)
	imagen_bytes = io.BytesIO()
	imagen.save(imagen_bytes, format='PNG')
	imagen_bytes.seek(0)
	imagen_modificada = imagen_bytes.read()
	
	return imagen_modificada

__all__ = ['crear_collage_vertical', 'crear_collage_horizontal', 'crear_collage_triple', 'crear_collage_cuadruple', 'seleccionador_diseno_collage', 'verificar_etiquetas_imagenes', 'escritor_de_imagenes']

