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
from rutas import path as pt


############################################################## ETIQUETADO ###############################################################


def etiquetado(evento):

    """ Funcion que abre y maneja la pantalla de etiquetado de imagenes"""
    
    

    try:
      with open(pt.ruta_configuracion) as archivo:
            Datos_de_configuracion = js.load(archivo) 	# Utilizamos filter para obtener los elementos del diccionario que contienen el alias que se pasó como parámetro
            
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion) 	# Utilizamos map para obtener una lista con todos los repositorios de imágenes de los elementos filtrados
            
            repositorios = list(map(lambda d: d["Repositorio de imagenes"], configuracion_filtrada))        # Si no encontramos ninguna configuración que contenga el alias, utilizamos la ruta por defecto
            Repositorio_de_imagenes = repositorios[0] if repositorios else pt.ruta_carpeta_imagenes
        
        
    except FileNotFoundError:
        sg.popup("No ha fijado su configuracion. Se usaran los valores predeterminados", title='Advertencia: No existe la configuracion')
        Repositorio_de_imagenes=pt.ruta_carpeta_imagenes
    except PermissionError:
        sg.popup("No tienes permiso para leer este archivo.",title="Error escencial")
        sys.exit()
    except js.JSONDecodeError:
        sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
        sys.exit()
    
    
    image_files = [filename for filename in os.listdir(pt.convertir_guardado_para_usar(Repositorio_de_imagenes)) if filename.endswith(('.png', '.jpg', '.jpeg'))]
        
    izquierda = [[sg.Frame('Tags y descripcion:',[
                              [sg.Text('Tags y Descripción',size=(20, 1), font=('courier',30, "bold italic"), justification='left')],
                              [sg.Text('Selecciona una imagen:', justification="center", pad = ((5,0),(50,0))), sg.Listbox(values=image_files, size=(30, 5), key='Imagen', enable_events=True)],
                              [sg.Text('Tag           ', pad = ((5,0),(15,0))), sg.InputText(key='Tag', pad = ((5,0),(15,0)))],
                              [sg.Text('Descripción', pad = ((5,0),(15,0))), sg.InputText( key='Descripcion', pad = ((5,0),(15,5)))]
                              ])]]


    derecha = [[sg.Frame('',[
        [sg.Text(key='Key_Nombre_Imagen', font=('courier',15, "bold italic"))],
        [sg.Image(key='display', pad = ((100,0),(15,0)))],
        [sg.Text("Tamano"),sg.Text(key='Key_tamano_en_bytes', font=('courier',15, "bold italic"))],
        [sg.Text("Resolucion"),sg.Text(key='Key_ancho_alto', font=('courier',15, "bold italic"))],
        [sg.Text("Mimetype"),sg.Text(key='Key_formato', font=('courier',15, "bold italic"))],
        [sg.Text("Tags"),sg.Text(key='Key_tags', font=('courier',15, "bold italic"))],
        [sg.Text("Descripcion"),sg.Text(key='Key_descripcion', font=('courier',15, "bold italic"))]
    ])]]


    layout = [
        [sg.Column(izquierda),
        sg.VSeperator(),
        sg.Column(derecha),],
        [sg.Button('Guardar', pad=((700,0),(20,20)))],
        [sg.Button('Volver', key='volver')]] 

    

    window = sg.Window('Tags', layout, margins=(200, 150))




    while True:
        try:
            event, values = window.read()
            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            elif event == 'Imagen':
                path_de_imagenes = os.path.join(Repositorio_de_imagenes, values['Imagen'][0]) if values['Imagen'] else ""
                path_de_imagenes=pt.convertir_guardado_para_usar(path_de_imagenes)
                Nombre_de_la_imagen = values['Imagen'][0].split('/')[-1] if values['Imagen'] else ""

                if path_de_imagenes:
                    metadatos = fcsv.verificar_imagen(values['Imagen'][0])

                    imagen = Image.open(path_de_imagenes)
                    ancho_alto = str(imagen.size)
                    tamano = (100, 100)
                    imagen = imagen.resize(tamano)
                    imagen_bytes = io.BytesIO()

                    ################## Datos de la imagen ############################

                    tamano_en_bytes = str(os.path.getsize(path_de_imagenes) / 1e6)
                    mimetype = mimetypes.guess_type(Nombre_de_la_imagen)[0]

                    #################################################################

                    imagen.save(imagen_bytes, format='PNG')
                    imagen_bytes.seek(0)
                    imagen_data = imagen_bytes.read()

                    if metadatos is not None:
                        viejos_tags = metadatos[5].strip('[]')
                        viejos_tags = viejos_tags.strip("'")
                        window['Key_Nombre_Imagen'].update(Nombre_de_la_imagen)
                        window['Key_tamano_en_bytes'].update(metadatos[2] + " MB")
                        window['Key_ancho_alto'].update(metadatos[1] + " px")
                        window['Key_formato'].update(metadatos[3])
                        window['Key_tags'].update(metadatos[5])
                        window['Key_descripcion'].update(metadatos[4])
                        window['Descripcion'].update(metadatos[4])
                        window['Tag'].update(viejos_tags)
                        window['display'].update(data=imagen_data)
                    elif imagen_data is not None:
                        window['Key_Nombre_Imagen'].update(Nombre_de_la_imagen)
                        window['Key_tamano_en_bytes'].update(tamano_en_bytes + " MB")
                        window['Key_ancho_alto'].update(ancho_alto + " px")
                        window['Key_formato'].update(mimetype)
                        window['Key_tags'].update('None')
                        window['Key_descripcion'].update('None')
                        window['display'].update(data=imagen_data)

                    # Obtenemos la fecha actual
                    timestamp = datetime.timestamp(datetime.now())
                    fecha_hora = datetime.fromtimestamp(timestamp)
                    fecha_actual = fecha_hora.strftime("%d/%m/%Y, %H:%M:%S")

            elif event == 'Guardar':
                ult_act = evento
                Repositorio_de_imagenes=pt.convertir_guardado_para_usar(Repositorio_de_imagenes)
                metadata = [pt.convertir_para_guardar(path_de_imagenes,Repositorio_de_imagenes), ancho_alto, tamano_en_bytes, mimetype,
                            values['Descripcion'], values['Tag'], ult_act, timestamp]
                fcsv.manejo_archivo_csv(metadata, evento)

                sg.popup("Se han guardado los cambios")
                
                metadatos = fcsv.verificar_imagen(metadata[0])
                window['Key_tags'].update(metadatos[5])
                window['Key_descripcion'].update(metadatos[4])
                

            elif event == 'volver':
                break
        except UnboundLocalError:
            sg.popup("Asegurate de seleccionar una imagen antes de guardar.", title="Atención")

    window.close()
    return 



############################################### MEMES ############################################################################


def Meme(evento):
    """Esta función abre la ventana inicial de memes, que permite elegir el template para iniciar la creación del meme.
    Toma como argumento:
    - evento: nombre del usuario que se encuentra operando"""

    try:
        with open(pt.ruta_configuracion) as archivo:
            Datos_de_configuracion = js.load(archivo)
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion)
            repositorios = list(map(lambda d: pt.convertir_guardado_para_usar(d["Repositorio de imagenes"]), configuracion_filtrada))
            Repositorio_de_imagenes = repositorios[0] if repositorios else pt.ruta_carpeta_imagenes
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion)
            repositorio_memes = list(map(lambda d: pt.convertir_guardado_para_usar(d["Repositorio de memes"]), configuracion_filtrada))
            Repositorio_de_memes = repositorio_memes[0] if repositorio_memes else pt.ruta_carpeta_memes
    except FileNotFoundError:
        sg.popup("No ha fijado su configuración. Se usarán los valores predeterminados", title='Advertencia: No existe la configuración')
        Repositorio_de_imagenes = pt.ruta_carpeta_imagenes
        Repositorio_de_memes = pt.ruta_carpeta_memes
    except PermissionError:
        sg.popup("No tienes permiso para leer este archivo.", title="Error esencial")
        sys.exit()
    except js.JSONDecodeError:
        sg.popup("Un archivo vital no está en formato JSON válido.", title="Error esencial")
        sys.exit()

    image_files = [filename for filename in os.listdir(pt.templates) if filename.endswith(('.png', '.jpg', '.jpeg'))]

    # Definir el diseno de la ventana
    layout = [
        [sg.Text('Seleccione un template:', size=(25, 1), font=('courier', 15, "bold italic"), justification='left')],
        [sg.Listbox(values=image_files, size=(30, 20), key='Lista de templates', enable_events=True),
         sg.VSeperator(),
         sg.Image(key='Template', size=(300, 300))
         ],
        [sg.Button('Seleccionar', pad=((400, 0), (20, 5)))],
        [sg.Button('Volver', key='volver')]
    ]

    # Crear la ventana
    window = sg.Window('Selección de templates', layout)

    # Bucle principal del programa
    while True:
        try:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Lista de templates':
                template = values['Lista de templates'][0]
                image_path = os.path.join(pt.templates, template)
                image_data = fn.cargar_imagen(image_path)
                window['Template'].update(data=image_data)
            elif event == "Seleccionar" and image_data is not None:
                window.hide()
                Generador_de_memes(image_data, image_path, Repositorio_de_memes, evento)
                window.un_hide()
            elif event == "volver":
                break
        except UnboundLocalError:
            sg.popup("Aseguresé de seleccionar un template.", title="Atención")


    # Cerrar la ventana al salir
    window.close()

#########################################################################################################################################


def Generador_de_memes(datos_de_la_imagen,path_de_la_imagen, carpeta_memes,evento):

    '''Esta funcion abre la pantalla donde se escriben los textos que van en la imagen.
    datos_de_la_imagen: Es la data de la imagen, extraida directamente de la pantalla
    anterior, abre la imagen ni bien se inicia la pantalla
    path_de_la_imagen: El path de donde sale la imagen
    carpeta_memes: Es la carpeta donde se guardan los memes una vez escritos'''
    
    
    # Definir layout principal
    derecha = [
        [sg.Button('Volver')],
        [sg.Image(key='Meme', data=datos_de_la_imagen)],
        [sg.Button('Guardar')]
    ]

    #Aqui separamos el nombre de la imagen del path
    nombre_del_template=path_de_la_imagen.split('/')[-1]
    
    #Separamos el path del nombre de la imagen
    path_sin_imagen=path_de_la_imagen.replace("/"+nombre_del_template,"")
    
   
    
    #Filtro en el archivo para quedarme con la configuracion de las coordenadas de cada texto
    try:
    	with open(pt.configuracion_de_templates, 'r') as archivo:
    		coord_template = js.load(archivo)
    		mi_template = filter(lambda d: nombre_del_template in d["imagen"], [diccionario for diccionario in coord_template])
    		coordenadas = list(map(lambda d: d["coordenadas"], mi_template))
    except PermissionError:
    	sg.popup("Error de permisos al abrir el archivo de configuración.")
    	return
    except js.JSONDecodeError:
    	sg.popup("Error al decodificar el archivo JSON de configuración.")
    	return
    
    #El siguiente if se encarga de tomar el numero de cuadros correcto,
    #Si la imagen no esta aclarada en el json coord=[] y levantamos un popup
    if coordenadas != []:
    # Obtengo el numero de cuadros de texto a partir de la cantidad de coordenadas brindadas en el json
        num_cuadros = len(coordenadas[0])
    else:
        sg.popup('La imagen no esta configurada para template',title="Error")
        return

    # Generar el layout dinámico con los cuadros de texto
    izquierda = [
        [sg.FileBrowse("Seleccionar fuente",initial_folder=pt.ruta_fuentes_de_texto,file_types=(('TTF (*ttf)',"*ttf"),))],
    ]

    for i in range(num_cuadros):
        izquierda.append([sg.Multiline(f"Texto {i+1}", key=f'{i+1}',pad=((1,1),(5,10)), size=(30, 5))])

    izquierda.append([sg.Button('Aplicar')])
    # Crear una ventana con el layout
    layout = [[sg.Column(izquierda), sg.VSeparator(), sg.Column(derecha)]]

    window = sg.Window("Generador de memes", layout)

    while True:
        event, values = window.read()

        if event == 'Volver' or event == sg.WINDOW_CLOSED:
            break
        if event == 'Guardar':
            # Realizar la acción de guardar la imagen aquí
            ruta_salida = sg.popup_get_file('Guardar meme como', save_as=True, initial_folder = carpeta_memes, file_types=(('JPEG', '*.jpg'), ('PNG', '*.png')))
            if ruta_salida == None or carpeta_memes not in ruta_salida:
                sg.popup("""Por favor, verifique que la ruta del archivo sea la que está guardada en configuración.
Puede utilizar SAVE AS para guardar la imagen en su carpeta configurada""")
                continue
            else:
                try:
                    imagen = Image.open(io.BytesIO(imagen_con_texto))
                    imagen.save(ruta_salida)
                    nombre_meme=ruta_salida.split('/')[-1]
                    fn.logs_sistema(evento,'Meme guardado',nombre_del_template,textos)
                    sg.popup('Imagen guardada exitosamente!')
                except UnboundLocalError:
                    sg.popup('Por favor chequee que el texto este en orden, oprimiendo "Aplicar"',title='Chequee la imagen')
        if event == 'Aplicar':
            textos=[values[f'{i+1}'] for i in range(num_cuadros)]
            # Abrir ventana emergente para editar la imagen
            if values['Seleccionar fuente'] != '':
                imagen_con_texto=fim.escritor_de_imagenes(path_de_la_imagen,values['Seleccionar fuente'],carpeta_memes,coordenadas[0],*textos)
            else:
                imagen_con_texto=fim.escritor_de_imagenes(path_de_la_imagen,pt.ruta_fuente_predeterminado,carpeta_memes,coordenadas[0],*textos)
            window['Meme'].update(data=imagen_con_texto)
            
    window.close()
    
 ############################################### COLLAGE ################################################################################
def collage(evento):

    """Esta funcion abre la ventana que permite seleccionar un template
    para crear un collage. Toma como argumento:
    evento= El usuario que se encuentra operando"""

    try:
      with open(pt.ruta_configuracion) as archivo:
            Datos_de_configuracion = js.load(archivo) 	# Utilizamos filter para obtener los elementos del diccionario que contienen el alias que se pasó como parámetro
            
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion) 	# Utilizamos map para obtener una lista con todos los repositorios de imágenes de los elementos filtrados
            
            repositorios = list(map(lambda d: pt.convertir_guardado_para_usar(d["Repositorio de imagenes"]), configuracion_filtrada))        # Si no encontramos ninguna configuración que contenga el alias, utilizamos la ruta por defecto
            Repositorio_de_imagenes = repositorios[0] if repositorios else pt.ruta_carpeta_imagenes
            
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion)
            repositorio_collages = list(map(lambda d: pt.convertir_guardado_para_usar(d["Repositorio de collage"]), configuracion_filtrada))
            Repositorio_de_collages = repositorio_collages[0] if repositorio_collages else pt.ruta_carpeta_collages
        
        
    except FileNotFoundError:
        sg.popup("No ha fijado su configuracion. Se usaran los valores predeterminados", title='Advertencia: No existe la configuracion')
        Repositorio_de_imagenes=pt.ruta_carpeta_imagenes
        Repositorio_de_collages=pt.ruta_carpeta_collages
    except PermissionError:
        sg.popup("No tienes permiso para leer este archivo.",title="Error escencial")
        sys.exit()
    except js.JSONDecodeError:
        sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
        sys.exit()


# Define la interfaz gráfica de la primera ventana utilizando PySimpleGUI
    layout_diseno = [
        [sg.Text('Selecciona el diseno de collage')],
        [
        sg.Listbox(['Diseno 1', 'Diseno 2', 'Diseno 3', 'Diseno 4'], size=(20, 4), key='lista_disenos',enable_events=True), sg.VSeperator(),  
        sg.Image(key='-IMAGEN-', size=(300, 300))
        ],
        [sg.Button('Seleccionar', key='seleccionar')],
        [sg.Button('Volver', key = 'volver')]
    ]

    # Crea la primera ventana
    ventana_diseno = sg.Window('Seleccionar diseno de collage', layout_diseno)

    # Bucle de eventos de la primera ventana
    while True:
        try:
            event, values = ventana_diseno.read()

            if event == sg.WINDOW_CLOSED:
                break

            elif event == 'volver':
                break

            elif event == 'seleccionar':
                ventana_diseno.hide()  # Oculta la primera ventana
                generador_de_collage(num_imagenes, diseno_seleccionado, Repositorio_de_collages, Repositorio_de_imagenes, evento)
                ventana_diseno.un_hide()

            diseno_seleccionado = values['lista_disenos'][0]

            num_imagenes = 0
            disenos = {
                       'Diseno 1': ['1.jpg',2],
                       'Diseno 2': ['2.jpg',2],
                       'Diseno 3': ['3.jpg',3],
                       'Diseno 4': ['4.jpg',4]
                       }

            if diseno_seleccionado in disenos:
                nombre_imagen = disenos[diseno_seleccionado][0]
                path_imagen = os.path.join(pt.ruta_templates, nombre_imagen)
                image_data = fn.cargar_imagen(path_imagen)
                ventana_diseno['-IMAGEN-'].update(data=image_data)
                num_imagenes = disenos[diseno_seleccionado][1]

        except UnboundLocalError:
            sg.popup("Por favor seleccione un diseno antes de continuar", title="Atención")
            break

    ventana_diseno.close()



#################################################### GENERADOR DE COLLAGE ##########################################################################

def generador_de_collage(num_imagenes, diseno_seleccionado, ruta_collages, carpeta_de_imagenes, evento):

    '''Esta funcion abre la ventana que permite elegir las imagenes y
    crear el collage. Toma como argumentos:
    num_imagenes: Envia cuantas imagenes se utilizan en el collage
    diseno_seleccionado: Especifica cual es el diseno seleccionado
    evento: El usuario que se encuentra operando en la aplicacion'''

    previsualizacion=pt.ruta_previsualizacion_collage
    # Define la interfaz gráfica de la segunda ventana utilizando PySimpleGUI
    layout = [
        [sg.Text('Título del collage:'), sg.Input(key='titulo_collage', enable_events=True)],
        [sg.Text('Selecciona las imágenes para el collage')],
    ]

    for i in range(num_imagenes):
        layout.append([sg.Input(key=f'imagen{i}', enable_events=True, disabled=True, visible=True),
                       sg.FileBrowse(f'Imagen {i+1}', file_types=([("JPG (*.jpg)", "*.jpg"),("JPEG (*.jpeg)", "*.jpeg"), ("PNG (*.png)", "*.png")]), initial_folder=carpeta_de_imagenes)])

    layout.append([sg.Button('Crear collage', key='crear'), sg.Button('Volver', key='volver')])
    layout.append([sg.Image(key='previa', size=(300, 300))])  # Elemento de imagen para la vista previa del collage

    window = sg.Window('Creador de collages - {}'.format(diseno_seleccionado), layout)

    rutas_imagenes = [None] * num_imagenes
    titulo_collage = ''

    # Bucle de eventos de la segunda ventana
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'titulo_collage':
            titulo_collage = values['titulo_collage']
            if all(rutas_imagenes):
                fim.seleccionador_diseno_collage(rutas_imagenes, previsualizacion, diseno_seleccionado, titulo_collage)
                vista_previa = Image.open(previsualizacion)
                vista_previa.thumbnail((300, 300))
                window['previa'].update(data=ImageTk.PhotoImage(vista_previa))
        elif event.startswith('imagen'):
            index = int(event[len('imagen'):])
            rutas_imagenes[index] = values[event]
            # Actualiza la vista previa si todas las imágenes son seleccionadas
            if all(rutas_imagenes):
                fim.seleccionador_diseno_collage(rutas_imagenes, previsualizacion, diseno_seleccionado, titulo_collage)
                vista_previa = Image.open(previsualizacion)
                vista_previa.thumbnail((300, 300))
                window['previa'].update(data=ImageTk.PhotoImage(vista_previa))
        elif event == 'crear':
            try:
                if all(rutas_imagenes):
                    if fim.verificar_etiquetas_imagenes(rutas_imagenes, evento):
                        ruta_salida = sg.popup_get_file('Guardar collage como', initial_folder=ruta_collages, save_as=True,
                                                        file_types=(('JPEG', '*.jpg'), ('PNG', '*.png')))


                        if ruta_salida == None or ruta_collages not in ruta_salida:
                            sg.popup("Por favor, verifique que la ruta del archivo sea la que está guardada en configuración")
                            continue
                        else:
                            fim.seleccionador_diseno_collage(rutas_imagenes, ruta_salida, diseno_seleccionado, titulo_collage)
                            sg.popup('Collage creado exitosamente!', 'Archivo guardado en: {}'.format(ruta_salida))
                            nombres_imagenes=[nombre.split('/')[-1] for nombre in rutas_imagenes]
                            fn.logs_sistema(evento,'Collage guardado',nombres_imagenes, titulo_collage)

            except ValueError:
                sg.popup("Por favor, ingrese una extensión al archivo (.jpg o .png)")
                continue

        elif event == 'volver':
            window.close()

    window.close()


__all__ = ['etiquetado', 'Meme', 'Generador_de_memes']

