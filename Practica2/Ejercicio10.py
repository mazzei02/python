#10. Dada una lista de nombres de estudiantes y dos listas con sus notas en un curso, escriba un programa que manipule dichas estructuras de datos para poder resolver los siguientes puntos:
#    1. Generar una estructura con todas las notas relacionando el nombre del estudiante con las notas. Utilizar esta estructura para la resolución de los siguientes items.
#    2. Calcular el promedio de notas de cada estudiante.
#    3. Calcular el promedio general del curso.
#    4. Identificar al estudiante con la nota promedio más alta.
#    5. Identificar al estudiante con la nota más baja.


#**Nota**:
#- Las 3 estructuras están ordenadas de forma que los elementos en la misma posición corresponden a un mismo alumno.
#- Realizar funciones con cada item

##########################################################################################################

##########################################################################################################

nombres = ''' 'Agustin', 'Alan', 'Andrés', 'Ariadna', 'Bautista', 'CAROLINA', 'CESAR',
'David','Diego', 'Dolores', 'DYLAN', 'ELIANA', 'Emanuel', 'Fabián', 'Facundo',
'Francsica', 'FEDERICO', 'Fernanda', 'GONZALO', 'Gregorio', 'Ignacio', 'Jonathan',
'Joaquina', 'Jorge', 'JOSE', 'Javier', 'Joaquín' , 'Julian', 'Julieta', 'Luciana',
'LAUTARO', 'Leonel', 'Luisa', 'Luis', 'Marcos', 'María', 'MATEO', 'Matias',
'Nicolás', 'Nancy', 'Noelia', 'Pablo', 'Priscila', 'Sabrina', 'Tomás', 'Ulises',
'Yanina' '''
notas_1 = [81,  60, 72, 24, 15, 91, 12, 70, 29, 42, 16, 3, 35, 67, 10, 57, 11, 69, 12, 77, 
           13, 86, 48, 65, 51, 41, 87, 43, 10, 87, 91, 15, 44, 85, 73, 37, 42, 95, 18, 7, 
           74, 60, 9, 65, 93, 63, 74]
notas_2 = [30, 95, 28, 84, 84, 43, 66, 51, 4, 11, 58, 10, 13, 34, 96, 71, 86, 37, 64, 13, 8,
           87, 14, 14, 49, 27, 55, 69, 77, 59, 57, 40, 96, 24, 30, 73, 95, 19, 47, 15, 31,
           39, 15, 74, 33, 57, 10]

###########################################################################################################


#CONVERTIMOS EL ARCHIVO DE NOMBRES EN UNA LISTA PARA OPERAR CON FACILIDAD

ID=nombres.replace('\n',' ').replace('\'', '').split(',') 


#CONVERTIMOS LAS TRES LISTAS EN UN DICCIONARIO, DONDE LAS CLAVES SON LOS NOMBRES Y LOS VALUES SON LAS LISTAS
#DE NOTAS
registro={}
for i in range(len(ID)):
    registro[ID[i]]=[notas_1[i],notas_2[i]]

###########################################################################################################
def promedio(**kwargs):
           
        """ Esta funcion calcula el promedio de cada alumno """
    
    
    for clave, valor in kwargs.items():    #recorremos los items del diccionario
        
        a=0                                # a sera la variable donde sumaremos las notas para el promedio
        cont=0                         # En un principio supondremos la cantidad de notas desconocidas para ello 
                                       # cont contabilizara las notas y dividira "a" para el promedio 
        
        for i in valor:
            a+=i
            cont+=1
        
        a/=cont
        
        print(f"El promedio de{clave} es {a}")

###########################################################################################################

def promediogral(**kwargs):
    
    """ Esta funcion imprime el promedio gral del curso"""
    
    PROM_GRAL=0
    
    
    for clave, valor in kwargs.items():    #recorremos los items del diccionario
        
        a=0                                # a sera la variable donde sumaremos las notas para el promedio
        cont=0                         # En un principio supondremos la cantidad de notas desconocidas para ello 
                                       # cont contabilizara las notas y dividira "a" para el promedio 
        
        for i in valor:
            a+=i
            cont+=1
        
        a/=cont
        
        PROM_GRAL+=a                   # en cada iteracion del for sumamos la nota del alumno al promedio gral
        
        
    PROM_GRAL/=len(kwargs)             # Finalmente, una vez recorridos todos los alumnos dividimos la suma de
                                       #  promedio gral por la cantidad de alumnos para el promedio de la clase.
    print()
    print(f"""
    ---------------------------------------------------
    
    El promedio general de la clase es {PROM_GRAL}
        
    ---------------------------------------------------""")
    
    
###########################################################################################################

def registropromedio(**kwargs):
    
     """ Esta funcion se usa para añadir los promedios al diccionario """
    

    
    for clave, valor in kwargs.items():    #recorremos los items del diccionario
        
        a=0                                # a sera la variable donde sumaremos las notas para el promedio
        cont=0                         # En un principio supondremos la cantidad de notas desconocidas para ello 
                                       # cont contabilizara las notas y dividira "a" para el promedio 
        
        for i in valor:
            a+=i
            cont+=1
        
        a/=cont
        
        
        
        kwargs[clave].append(a)  # ...y la añadimos a un diccionario que contiene solo {nombre: promedio}
        
    print()




promedio(**registro)  #Llamamos a nuestra función sobre el diccionario que creamos
promediogral(**registro)  #Llamamos a nuestra función sobre el diccionario que creamos
registropromedio(**registro)  #Llamamos a nuestra función sobre el diccionario que creamos


###########################################################################################################

print()
print()


#TOMAMOS EL DICCIONARIO DE SALIDA DE NUESTRA FUNCION Y LO SORTEAMOS SEGUN LA COLUMNA DE VALORES

#TOMAMOS EL DICCIONARIO DE SALIDA DE NUESTRA FUNCION Y LO SORTEAMOS SEGUN LA COLUMNA DE VALORES

high_value= max(registro.items(), key=lambda item: item[1][2]) #Sorteado de mayor a menor

print(f"El mejor promedio es {high_value[0]} con {high_value[1][2]}.")
print()
print()


###########################################################################################################

min1=min(registro.items(), key=lambda item: item[1][0])
min2=min(registro.items(), key=lambda item: item[1][1])

for name in registro.keys():
    if min1 <= min2:
        if registro[name][0]==min1[1][0]:
            print(f"La menor nota es {name} con {registro[name][0]} en el primer examen")
    elif min2 < min1:
        if registro[name][1]==min2[1][1]:
            print(f"La menor nota es {name} con {registro[name][1]} en el segundo examen")
        
        
