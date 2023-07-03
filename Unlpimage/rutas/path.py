import os
import sys

############################################################################################################

dir_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

############################################################################################################
def convertir_para_guardar(ruta, proyecto=dir_proyecto):
    """ Esta funcion toma la ruta relativa de cada ruta absoluta
    que se le pase """
    ruta_relativa = os.path.relpath(ruta, start=proyecto)
    ruta_generica = ruta_relativa.replace(os.path.sep, "/")  
    return ruta_generica

def convertir_guardado_para_usar(ruta, proyecto=dir_proyecto):  
    """ Esta funcion devuelve la ruta absoluta para cada ruta
    relativa que se le pase"""
    ruta_del_sistema = ruta.replace("/", os.path.sep)
    ruta_absoluta = os.path.abspath(os.path.join(proyecto,ruta_del_sistema))
    return ruta_absoluta



##############################################################################################################

####################################### Rutas auxiliares #####################################################

ruta_archivo = os.path.join(dir_proyecto, "files", "usuarios.json")
ruta_configuracion = os.path.join(dir_proyecto,"files","configuracion.json")
ruta_tags = os.path.join(dir_proyecto, "files", "tagsimagen.csv")
ruta_carpeta_imagenes = os.path.join(dir_proyecto,"Imagenes")
ruta_carpeta_memes = os.path.join(ruta_carpeta_imagenes,"Memes")
ruta_carpeta_collages = os.path.join(ruta_carpeta_imagenes,"Collages")
templates = os.path.join(ruta_carpeta_imagenes,"Templates")
configuracion_de_templates = os.path.join(templates,'templates.json')
ruta_fuentes_de_texto = os.path.join(dir_proyecto,'fonts')
ruta_archivo_csv =os.path.join(dir_proyecto,'files',"LogSistema.csv")
ruta_imagenes = os.path.join(ruta_carpeta_imagenes,'ProfilePictures')

#########################################################################
ruta_fuente_predeterminado = os.path.join(ruta_fuentes_de_texto,'28 Days Later.ttf')
ruta_imagenes_defecto = os.path.join(ruta_imagenes,'abeja2.png')
ruta_templates = os.path.join(ruta_carpeta_collages, "Templates")
ruta_previsualizacion_collage = os.path.join(ruta_carpeta_collages, 'previa.jpg')



