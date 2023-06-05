import sys
sys.path.append('/home/luciano/.local/lib/python3.10/site-packages')
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

import funciones as fn


############################################################## NUEVO USUARIO ############################################################

def nuevo_usuario(ruta_archivo,ruta_imagenes,ruta):

    """ Esta es la pantalla para un perfil de nuevo usuario, aqui se puede crear un nuevo usuario """

    ruta_imagenes_defecto=os.path.join(ruta_imagenes,'abeja2.png')

    
    
    izquierda = [[sg.Frame('Nuevo Usuario:',[
                          [sg.Text('Nuevo Perfil',size=(20, 1), font=('courier',30, "bold italic"), justification='left')],
                          [sg.Text('Alias'), sg.InputText(key='Alias')],
                          [sg.Text('Nombre'), sg.InputText( key='Nombre')],
                          [sg.Text('Edad'),sg.InputText( key='Edad') ],
                          [sg.Text('Genero autopercibido'), sg.Combo(values=['Masculino', 'Femenino', 'Otro'], key='Genero', size=(30, 6))],
                          [sg.Text('''En caso de otro 
(SI NO CORRESPONDE ´-´):'''), sg.InputText(key='Genero_alt')]])]]

    derecha = [
        [sg.Text('Selecciona una imagen:', justification="center"), sg.InputText(default_text=ruta_imagenes_defecto,disabled = True,key = "Imagen"), sg.FileBrowse(initial_folder=ruta_imagenes)],
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
        event, values = window.read()
        if event == 'show_image':
            image_path = values['Imagen']
            if image_path:
                image_data = fn.cargar_imagen(image_path)
                window['image_display'].update(data=image_data)
        
                window['image_display'].update(data=image_data)
        elif event == 'Guardar':
            fn.manejo_archivo_json(1, ruta_archivo,ruta, **values)
        elif event == sg.WIN_CLOSED or event == 'Volver': # if user closes window or clicks back button
            break
        else:
            print(event)

    window.close()


############################################################## ETIQUETADO ###############################################################


def etiquetado(evento,ruta_tags,ruta_configuracion,ruta):

    """ Funcion que abre y maneja la pantalla de etiquetado de imagenes"""
    
    ruta_carpeta_imagenes = os.path.join(ruta, "Imagenes")

    try:
      with open(ruta_configuracion) as archivo:
            Datos_de_configuracion = js.load(archivo) 	# Utilizamos filter para obtener los elementos del diccionario que contienen el alias que se pasó como parámetro
            
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion) 	# Utilizamos map para obtener una lista con todos los repositorios de imágenes de los elementos filtrados
            
            repositorios = list(map(lambda d: d["Repositorio de imagenes"], configuracion_filtrada))        # Si no encontramos ninguna configuración que contenga el alias, utilizamos la ruta por defecto
            Repositorio_de_imagenes = repositorios[0] if repositorios else ruta_carpeta_imagenes
        
        
    except FileNotFoundError:
        sg.popup("No ha fijado su configuracion. Se usaran los valores predeterminados", title='Advertencia: No existe la configuracion')
        Repositorio_de_imagenes=ruta_carpeta_imagenes
    except PermissionError:
        sg.popup("No tienes permiso para leer este archivo.",title="Error escencial")
        sys.exit()
    except js.JSONDecodeError:
        sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
        sys.exit()
    

        
        
    izquierda = [[sg.Frame('Tags y descripcion:',[
                              [sg.Text('Tags y Descripción',size=(20, 1), font=('courier',30, "bold italic"), justification='left')],
                              [sg.Text('Selecciona una imagen:', justification="center", pad = ((5,0),(50,0))), sg.FileBrowse(key="Imagen", file_types=([("JPEG (*.jpg)", "*.jpg"), ("PNG (*.png)", "*.png")]), initial_folder = Repositorio_de_imagenes,  pad = ((5,0),(50,0)))],
                              [sg.Text('Tag           ', pad = ((5,0),(15,0))), sg.InputText(key='Tag', pad = ((5,0),(15,0)))],
                              [sg.Text('Descripción', pad = ((5,0),(15,0))), sg.InputText( key='Descripcion', pad = ((5,0),(15,5)))]
                              ])]]


    derecha = [[sg.Frame('',[
        [sg.Text(key='Key_Nombre_Imagen', font=('courier',15, "bold italic"))],
        [sg.Image(key='display', pad = ((100,0),(15,0)))],
        [sg.Text("Tamaño"),sg.Text(key='Key_tamaño_en_bytes', font=('courier',15, "bold italic"))],
        [sg.Text("Resolucion"),sg.Text(key='Key_ancho_alto', font=('courier',15, "bold italic"))],
        [sg.Text("Mimetype"),sg.Text(key='Key_formato', font=('courier',15, "bold italic"))],
        [sg.Text("Tags"),sg.Text(key='Key_tags', font=('courier',15, "bold italic"))],
        [sg.Text("Descripcion"),sg.Text(key='Key_descripcion', font=('courier',15, "bold italic"))],
        [sg.Button('Previsualizar', pad=((300,0),(50,0)), key='mostrar_imagen')]
    ])]]


    layout = [
        [sg.Column(izquierda),
        sg.VSeperator(),
        sg.Column(derecha),],
        [sg.Button('Guardar', pad=((850,0),(20,20)))]] 

    

    window = sg.Window('Tags', layout, margins=(200, 150))




    while True:
      try:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        elif event == 'mostrar_imagen':
            path_de_imagenes = values['Imagen']
            Nombre_de_la_imagen = values['Imagen'].split('/')[-1]
            
            if os.path.join(Repositorio_de_imagenes, Nombre_de_la_imagen) != values['Imagen']:
                sg.popup("La imagen que seleccionaste no está en tu carpeta de imágenes, recomiendo que la muevas antes de continuar",
                         title='Advertencia: Imagen no válida')
                break

            if path_de_imagenes:
                metadatos = fn.verificar_imagen(path_de_imagenes, ruta_tags)

                imagen = Image.open(path_de_imagenes)
                ancho_alto = str(imagen.size)
                tamaño = (100, 100)
                imagen = imagen.resize(tamaño)
                imagen_bytes = io.BytesIO()

                ################## Datos de la imagen ############################

                tamaño_en_bytes = str(os.path.getsize(path_de_imagenes) / 1e6)
                mimetype = mimetypes.guess_type(Nombre_de_la_imagen)[0]

                #################################################################

                imagen.save(imagen_bytes, format='PNG')
                imagen_bytes.seek(0)
                imagen_data = imagen_bytes.read()

                if metadatos is not None:
                    viejos_tags=metadatos[5].strip('[')
                    viejos_tags=viejos_tags.strip(']')
                    viejos_tags=viejos_tags.strip("'")
                    window['Key_Nombre_Imagen'].update(Nombre_de_la_imagen)
                    window['Key_tamaño_en_bytes'].update(metadatos[2] + " MB")
                    window['Key_ancho_alto'].update(metadatos[1] + " px")
                    window['Key_formato'].update(metadatos[3])
                    window['Key_tags'].update(metadatos[5])
                    window['Key_descripcion'].update(metadatos[4])
                    window['Descripcion'].update(metadatos[4])
                    window['Tag'].update(viejos_tags)
                    window['display'].update(data=imagen_data)
                elif imagen_data is not None:
                    window['Key_Nombre_Imagen'].update(Nombre_de_la_imagen)
                    window['Key_tamaño_en_bytes'].update(tamaño_en_bytes + " MB")
                    window['Key_ancho_alto'].update(ancho_alto + " px")
                    window['Key_formato'].update(mimetype)
                    window['Key_tags'].update('None')
                    window['Key_descripcion'].update('None')
                    window['display'].update(data=imagen_data)

                # Obtenemos la fecha actual
                timestamp = datetime.timestamp(datetime.now())
                fecha_hora = datetime.fromtimestamp(timestamp)
                fecha_actual = fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
        elif event == 'Guardar':
            ultact = evento
            metadata = [path_de_imagenes, ancho_alto, tamaño_en_bytes, mimetype, values['Descripcion'], values['Tag'],
                        ultact, str(fecha_actual)]
            fn.manejo_archivo_csv(metadata, ruta_tags, evento)

            sg.popup("Se han guardado los cambios")
            # print('hasta aca si llegue')

      except UnboundLocalError:
            sg.popup("Recuerde presionar previsualizar para continuar")
            pass


	
    window.close()
    return 


################################################ AYUDA #################################################################################

def ayuda():
    


    """Esta funcion abre la pantalla de ayuda, una pantalla con consejos para el usuario"""
    
    
    layout = [
        [sg.Text("""Para añadir etiquetas a su imagén presione el boton etiquetar imagen.

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
    window = sg.Window("Configuración", layout)

# Bucle para leer los eventos de la ventana
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-CANCELAR-"):
            break

# Cerramos la ventana y finalizamos la aplicación
    window.close()


    ######################################################  CONFIGURACION ################################################################




def configuracion(ruta,evento):

    """ Esta es la funcion que abre la ventana de configuracion """



    
    ruta_carpeta_imagenes=os.path.join(ruta,"Imagenes")
    ruta_carpeta_memes=os.path.join(ruta,"Memes")
    ruta_carpeta_collages=os.path.join(ruta,"Collages")
    ruta_json_configuracion=os.path.join(ruta,"Configuracion","configuracion.json")

    
    layout = [
        [sg.Text("Configuración", font=("Courtier", 30, "bold italic"), justification="left", size=(15, 1)),sg.Text('', size=(30,1)),sg.Button("Cancelar", font=("Arial", 12), size=(10, 1), border_width=0, pad=(20, 5), key="-CANCELAR-")],
        [sg.Text("Repositorio de imágenes", font=("Arial", 14), justification="left", pad=((200, 5),(100,5)))],
        [sg.InputText(font=("Arial", 12), size=(40, 1), key="Carpeta_Imagenes", pad=(100, 0)), sg.FolderBrowse(font=("Arial", 12), button_text="Browse", initial_folder=ruta_carpeta_imagenes, size=(10, 1))],
        [sg.Text("Repositorio de collage", font=("Arial", 14), justification="left",  pad=((200, 5),(10,5)))],
        [sg.InputText(font=("Arial", 12), size=(40, 1), key="Collage", pad=(100, 0)), sg.FolderBrowse(font=("Arial", 12), button_text="Browse", initial_folder=ruta_carpeta_collages, size=(10, 1))],
        [sg.Text("Repositorio de memes", font=("Arial", 14), justification="left",  pad=((200, 5),(10,5)))],
        [sg.InputText(font=("Arial", 12), size=(40, 1), key="Memes", pad=(100, 0)), sg.FolderBrowse(font=("Arial", 12), button_text="Browse", initial_folder=ruta_carpeta_memes, size=(10, 1))],
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
        # Mas adelante vemos en donde guardamos las direcciones de donde se guardan las imagenes
            Diccionario_de_direcciones={"Alias":evento,"Repositorio de imagenes":values["Carpeta_Imagenes"],"Repositorio de collage":values["Collage"],"Repositorio de memes":values["Memes"]}

            fn.manejo_archivo_json(4,ruta_json_configuracion,ruta,**Diccionario_de_direcciones)
            fn.logs_sistema(evento,'Cambio configuración del sistema.')
            
            sg.popup("Se ha guardado la configuracion")


            

            

# Cerramos la ventana y finalizamos la aplicación
    window.close()

############################################### MEMES ############################################################################


def Meme(ruta,ruta_configuracion,evento):


    ruta_carpeta_imagenes = os.path.join(ruta, "Imagenes")
    ruta_carpeta_memes = os.path.join(ruta, "Memes")

    try:
      with open(ruta_configuracion) as archivo:
            Datos_de_configuracion = js.load(archivo) 	# Utilizamos filter para obtener los elementos del diccionario que contienen el alias que se pasó como parámetro
            
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion) 	# Utilizamos map para obtener una lista con todos los repositorios de imágenes de los elementos filtrados
            
            repositorios = list(map(lambda d: d["Repositorio de imagenes"], configuracion_filtrada))        # Si no encontramos ninguna configuración que contenga el alias, utilizamos la ruta por defecto
            Repositorio_de_imagenes = repositorios[0] if repositorios else ruta_carpeta_imagenes
            
            repositorio_memes = list(map(lambda d: d["Repositorio de memes"], configuracion_filtrada))
            Repositorio_de_memes = repositorios_memes[0] if repositorio_memes else ruta_carpeta_memes
        
        
    except FileNotFoundError:
        sg.popup("No ha fijado su configuracion. Se usaran los valores predeterminados", title='Advertencia: No existe la configuracion')
        Repositorio_de_imagenes=ruta_carpeta_imagenes
        Repositorio_de_memes=ruta_carpeta_memes
    except PermissionError:
        sg.popup("No tienes permiso para leer este archivo.",title="Error escencial")
        sys.exit()
    except js.JSONDecodeError:
        sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
        sys.exit()
    
    Repositorio_de_imagenes=os.path.join(Repositorio_de_imagenes,'Templates')

    image_files = [filename for filename in os.listdir(Repositorio_de_imagenes) if filename.endswith(('.png', '.jpg', '.jpeg'))]

# Definir el diseño de la ventana
    layout = [[sg.Text('Seleccione un template:',size=(25, 1), font=('courier',15, "bold italic"), justification='left')],
        [sg.Listbox(values=image_files, size=(30, 20), key='Lista de templates', enable_events=True), sg.VSeperator(),  ###ACA APARECEN LAS IMAG EN LISTA
        sg.Image(key='Template', size=(300, 300))                                                 ###Este es donde aparece la imag
        ],
        [sg.Button('Seleccionar', pad=((400,0),(20,5)))]                                          ###Y el botoncito para arrancar a hacer memes
        ]

# Crear la ventana
    window = sg.Window('Selección de templates', layout)

# Bucle principal del programa
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Lista de templates':
            template = values['Lista de templates'][0]
            image_path = os.path.join(Repositorio_de_imagenes, template)
            image_data=fn.cargar_imagen(image_path)                                ###ACA LLAMO A LA FUNCION CARGAR IMAGEN PARA SACAR LOS DATOS
            window['Template'].update(data=image_data)                           ### y hago que aparezca la imagen en la ventana
        elif event == "Seleccionar" and image_data != None:
            Generador_de_memes(image_data,image_path, Repositorio_de_memes,ruta,evento)
        

# Cerrar la ventana al salir
    window.close()
    
#########################################################################################################################################


def Generador_de_memes(datos_de_la_imagen,path_de_la_imagen, carpeta_memes,ruta,evento):

    '''Esta funcion abre la pantalla donde se escriben los textos que van en la imagen.
    datos_de_la_imagen: Es la data de la imagen, extraida directamente de la pantalla
    anterior, abre la imagen ni bien se inicia la pantalla
    path_de_la_imagen: El path de donde sale la imagen
    carpeta_memes: Es la carpeta donde se guardan los memes una vez escritos'''
    
    ruta_fuentes_de_texto=os.path.join(ruta,'fonts')
    
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
    
    #Creo la direccion del archivo json que contiene la informacion de las coordenadas de cada imagen
    configuracion_de_templates=os.path.join(path_sin_imagen,'templates.json')
    
    #Filtro en el archivo para quedarme con la configuracion de las coordenadas de cada texto
    with open(configuracion_de_templates,'r') as archivo:
    	coord_template=js.load(archivo)
    	mi_template = filter(lambda d: nombre_del_template in d["imagen"], [diccionario for diccionario in coord_template])
    	coordenadas = list(map(lambda d: d["coordenadas"], mi_template))
    
    # Obtengo el numero de cuadros de texto a partir de la cantidad de coordenadas brindadas en el json
    num_cuadros = len(coordenadas[0])

    # Generar el layout dinámico con los cuadros de texto
    izquierda = [
        [sg.FileBrowse("Seleccionar fuente",initial_folder=ruta_fuentes_de_texto,file_types=(('TTF (*ttf)',"*ttf"),))],
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
            ruta_salida = sg.popup_get_file('Guardar collage como', save_as=True, initial_folder = carpeta_memes, file_types=(('JPEG', '*.jpg'), ('PNG', '*.png')))
            if ruta_salida == None:
                continue
            elif  carpeta_memes not in ruta_salida:
                sg.popup('No inserto un nombre valido, utilice la opcion SAVE AS para guardar la imagen')
            else:
                imagen = Image.open(io.BytesIO(imagen_con_texto))
                imagen.save(ruta_salida)
                nombre_meme=ruta_salida.split('/')[-1]
                fn.logs_sistema(evento,'Meme guardado',nombre_meme,textos)
                sg.popup('Imagen guardada exitosamente!')
        if event == 'Aplicar':
            textos=[values[f'{i+1}'] for i in range(num_cuadros)]
            # Abrir ventana emergente para editar la imagen
            if values['Seleccionar fuente'] != '':
                imagen_con_texto=fn.escritor_de_imagenes(path_de_la_imagen,values['Seleccionar fuente'],carpeta_memes,coordenadas[0],*textos)
            else:
                imagen_con_texto=fn.escritor_de_imagenes(path_de_la_imagen,os.path.join(ruta_fuentes_de_texto,'28 Days Later.ttf'),carpeta_memes,coordenadas[0],*textos)
            window['Meme'].update(data=imagen_con_texto)
            
    window.close()
    

 ############################################### COLLAGE ################################################################################
def collage(ruta, ruta_configuracion):

    ruta_carpeta_imagenes = os.path.join(ruta, "Imagenes")
    ruta_carpeta_collages = os.path.join(ruta, "Collages")
    ruta_templates = os.path.join(ruta_carpeta_collages, "Templates")

    try:
      with open(ruta_configuracion) as archivo:
            Datos_de_configuracion = js.load(archivo) 	# Utilizamos filter para obtener los elementos del diccionario que contienen el alias que se pasó como parámetro
            
            configuracion_filtrada = filter(lambda d: evento in d["Alias"], Datos_de_configuracion) 	# Utilizamos map para obtener una lista con todos los repositorios de imágenes de los elementos filtrados
            
            repositorios = list(map(lambda d: d["Repositorio de imagenes"], configuracion_filtrada))        # Si no encontramos ninguna configuración que contenga el alias, utilizamos la ruta por defecto
            Repositorio_de_imagenes = repositorios[0] if repositorios else ruta_carpeta_imagenes
            
            repositorio_collages = list(map(lambda d: d["Repositorio de collage"], configuracion_filtrada))
            Repositorio_de_collages = repositorios_collages[0] if repositorio_collages else ruta_carpeta_collages
        
        
    except FileNotFoundError:
        sg.popup("No ha fijado su configuracion. Se usaran los valores predeterminados", title='Advertencia: No existe la configuracion')
        Repositorio_de_imagenes=ruta_carpeta_imagenes
        Repositorio_de_collages=ruta_carpeta_collages
    except PermissionError:
        sg.popup("No tienes permiso para leer este archivo.",title="Error escencial")
        sys.exit()
    except js.JSONDecodeError:
        sg.popup("Un archivo vital no está en formato JSON válido.",title="Error escencial")
        sys.exit()


# Define la interfaz gráfica de la primera ventana utilizando PySimpleGUI
    layout_diseño = [
        [sg.Text('Selecciona el diseño de collage')],
        [
        sg.Listbox(['Diseño 1', 'Diseño 2', 'Diseño 3', 'Diseño 4'], size=(20, 4), key='lista_diseños',enable_events=True), sg.VSeperator(),  
        sg.Image(key='-IMAGEN-', size=(300, 300))
        ],
        [sg.Button('Seleccionar', key='seleccionar')]
    ]

    # Crea la primera ventana
    ventana_diseño = sg.Window('Seleccionar diseño de collage', layout_diseño)

    # Bucle de eventos de la primera ventana
    while True:
        event, values = ventana_diseño.read()
    
        diseño_seleccionado = values['lista_diseños'][0]

        num_imagenes = 0
        if diseño_seleccionado == 'Diseño 1':
            path_imagen=os.path.join(ruta_templates,"1.jpg")
            image_data=fn.cargar_imagen(path_imagen)                                
            ventana_diseño['-IMAGEN-'].update(data=image_data)
            num_imagenes = 2
        elif diseño_seleccionado == 'Diseño 2':
            path_imagen=os.path.join(ruta_templates,"2.jpg")
            image_data=fn.cargar_imagen(path_imagen)                                
            ventana_diseño['-IMAGEN-'].update(data=image_data)
            num_imagenes = 2
        elif diseño_seleccionado == 'Diseño 3':
            path_imagen=os.path.join(ruta_templates,"3.jpg")
            image_data =fn.cargar_imagen(path_imagen)                                
            ventana_diseño['-IMAGEN-'].update(data=image_data)
            num_imagenes = 3
        elif diseño_seleccionado == 'Diseño 4':
            path_imagen=os.path.join(ruta_templates,"4.jpg")
            image_data=fn.cargar_imagen(path_imagen)                                
            ventana_diseño['-IMAGEN-'].update(data=image_data)
            num_imagenes = 4

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'seleccionar':
        
            ventana_diseño.hide()  # Oculta la primera ventana
            generador_de_collage(ruta, num_imagenes, diseño_seleccionado, ruta_carpeta_collages)
            ventana_diseño.un_hide()

        

    ventana_diseño.close()

#################################################### SELECCIONAR DE DISEÑO DE COLLAGE ###########################################################

def seleccionador_diseño_collage(rutas_imagenes, ruta_salida, diseño):

    # Carga las imágenes
    imagenes = [Image.open(io.BytesIO(fn.cargar_imagen(ruta))) for ruta in rutas_imagenes]

    if diseño == 'Diseño 1':
        # Crea el collage en posición vertical
        altura_total = sum(imagen.size[1] for imagen in imagenes)
        ancho_maximo = max(imagen.size[0] for imagen in imagenes)

        collage = Image.new('RGB', (ancho_maximo, altura_total))
        y_offset = 0

        for imagen in imagenes:
            collage.paste(imagen, (0, y_offset))
            y_offset += imagen.size[1]

    elif diseño == 'Diseño 2':
        # Crea el collage en posición horizontal
        anchura_total = sum(imagen.size[0] for imagen in imagenes)
        altura_maxima = max(imagen.size[1] for imagen in imagenes)

        collage = Image.new('RGB', (anchura_total, altura_maxima))
        x_offset = 0

        for imagen in imagenes:
            collage.paste(imagen, (x_offset, 0))
            x_offset += imagen.size[0]

    elif diseño == 'Diseño 3':
        # Crea el collage con dos imágenes en posición horizontal y la tercera llena el resto del espacio
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

    elif diseño == 'Diseño 4':
        # Crea el collage con cuatro imágenes en las esquinas
        anchura_total = max(imagen.size[0] for imagen in imagenes)
        altura_total = max(imagen.size[1] for imagen in imagenes)

        collage = Image.new('RGB', (anchura_total * 2, altura_total * 2))

        # Esquina superior izquierda
        collage.paste(imagenes[0], (0, 0))

        # Esquina superior derecha
        collage.paste(imagenes[1], (anchura_total, 0))

        # Esquina inferior izquierda
        collage.paste(imagenes[2], (0, altura_total))

        # Esquina inferior derecha
        collage.paste(imagenes[3], (anchura_total, altura_total))

    # Guarda el collage en el archivo de salida
    collage.save(os.path.join('Collages',ruta_salida))

#################################################### GENERADOR DE COLLAGE ##########################################################################

def generador_de_collage(ruta, num_imagenes, diseño_seleccionado, ruta_collages):
        
        ruta_imagenes=os.path.join(ruta,'Collages','previa.jpg')

        # Define la interfaz gráfica de la segunda ventana utilizando PySimpleGUI
        layout = [
            [sg.Text('Selecciona las imágenes para el collage')],
        ]

    
        for i in range(num_imagenes):
            layout.append([sg.Input(key=f'imagen{i}', enable_events=True,disabled=True, visible=True), sg.FileBrowse(f'Imagen {i+1}')])

        layout.append([sg.Button('Crear collage', key='crear'), sg.Button('Volver', key='volver')])
        layout.append([sg.Image(key='previa', size=(300, 300))])  # Elemento de imagen para la vista previa del collage

        window = sg.Window('Creador de collages - {}'.format(diseño_seleccionado), layout)

        rutas_imagenes = [None] * num_imagenes

        # Bucle de eventos de la segunda ventana
        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event.startswith('imagen'):
                index = int(event[len('imagen'):])
                rutas_imagenes[index] = values[event]
                # Actualiza la vista previa si todas las imágenes son seleccionadas
                if all(rutas_imagenes):
                    seleccionador_diseño_collage(rutas_imagenes, 'previa.jpg', diseño_seleccionado)
                    vista_previa = Image.open(ruta_imagenes)
                    vista_previa.thumbnail((300, 300))
                    window['previa'].update(data=ImageTk.PhotoImage(vista_previa))
            elif event == 'crear':
                try:
                    if all(rutas_imagenes):
                        ruta_salida = sg.popup_get_file('Guardar collage como',initial_folder=ruta_collages, save_as=True, file_types=(('JPEG', '*.jpg'), ('PNG', '*.png')))

                        if ruta_salida == None or ruta_collages not in ruta_salida:
                            sg.popup("Por favor, verifique que la ruta del archivo sea la que está guardada en configuración")
                            continue
                        else:
                            seleccionador_diseño_collage(rutas_imagenes, ruta_salida, diseño_seleccionado)
                            sg.popup('Collage creado exitosamente!', 'Archivo guardado en: {}'.format(ruta_salida))

                except ValueError:
                    sg.popup("Por favor, ingrese una extensión al archivo (.jpg o .png)")
                    continue
            
            elif event == 'volver':
                window.close()

        window.close()

#################################################### INTERFAZ USUARIO ####################################################################

def interfaz_usuario(evento,datos,ruta,ruta_configuracion,ruta_archivo,ruta_imagenes):

    """ Pantalla que maneja la interfaz principal del usuario """
    
    
    ruta_tags = os.path.join(ruta, "tags", "tagsimagen.csv")
    
    
    #print(event)
    for dictionary in datos:
        if evento == dictionary["Alias"]:
             imagen2 = sg.Button(key='Editar',image_filename=dictionary['Imagen'],) 
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
            configuracion(ruta,evento)

        elif event == 'Ayuda':
            ayuda()
            
        elif event == 'Editar':
            editar_usuario(ruta_archivo,ruta_imagenes,ruta,evento)


        elif event == "Etiquetar":
            etiquetado(evento,ruta_tags,ruta_configuracion,ruta)

        elif event == "Meme":
            Meme(ruta,ruta_configuracion,evento)

        elif event == "Collage":
            collage(ruta, ruta_configuracion)    
    


    # Cerrar la ventana
    window.close()



########################################################## EDITAR USUARIOS #############################################################

def editar_usuario(ruta_archivo,ruta_imagenes,ruta,evento):

    """ Esta es la pantalla para un perfil de editar usuario, aqui se puede manipular los datos de un usuario """
    
    with open(ruta_archivo) as archivo:
         
         usuarios=js.load(archivo)
         
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

    image_data = fn.cargar_imagen(Imagen_original)

    izquierda = [
        [sg.Frame('Editar Usuario:',[
            [sg.Text('Editar Perfil',size=(20, 1), font=('courier',30, "bold italic"), justification='left')],
            [sg.Text('Alias'), sg.InputText(key='Alias', default_text=evento)],
            [sg.Text('Nombre'), sg.InputText(key='Nombre', default_text=Nombre_original)],
            [sg.Text('Edad'), sg.InputText(key='Edad', default_text=Edad_original)],
            [sg.Text('Genero autopercibido'), sg.Combo(values=['Masculino', 'Femenino', 'Otro'], key='Genero', size=(30, 6))],
            [sg.Text('''En caso de otro 
            (SI NO CORRESPONDE ´-´):'''), sg.InputText(key='Genero_alt', default_text=Genero_alt_original)]
        ])]
    ]

    derecha = [
        [sg.Text('Selecciona una imagen:', justification="center"), sg.FileBrowse(initial_folder=ruta_imagenes, key='Imagen')],
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
            
            fn.manejo_archivo_json(7, ruta_archivo, ruta, **values)
            
        
        elif event == sg.WIN_CLOSED or event == 'Volver':
            break

    window.close()


########################################################### VENTANA PRINCIPAL ############################################################

def layout_principal(datos):

	""" Pantalla que aparece al momento de abrir el programa."""
	layout = [ [ sg.Text('UNLPImage!!', size=(10,1), font=('Courier', 30, 'bold italic'), pad=((0,0), (0,0))), sg.Text('', size=(30,1))]]
         
	layout2=[[sg.Button(key=dictionary['Alias'],tooltip=dictionary["Alias"],image_filename=dictionary['Imagen'],  pad=((0,0), (20,0))) for dictionary in datos]]

	layout.append(layout2)

	layout.append([sg.Button("Añadir Usuario", pad=((0,0),(20,0)))])
	
	return layout
    


_all__ = ['ayuda','etiquetado','configuracion','nuevo_usuario','interfaz_usuario','layout_principal','editar_usuario','Generador_de_memes']
