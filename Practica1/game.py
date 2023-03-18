from random import choice, randrange
from datetime import datetime
# Operadores posibles
operators = ["+", "-","*","/"]


# Cantidad de cuentas a resolver
times = 5


# Contador inicial de tiempo.
# Esto toma la fecha y hora actual.
init_time = datetime.now()


print(f"¡Veremos cuanto tardas en responder estas {times} operaciones!")


acertados=0  ##ESTO VA A CONTAR LAS CUENTAS ACERTADAS
errados=0    ##Y ESTO LAS ERRADAS


for i in range(0, times):
    
    # Se eligen números y operador al azar
    
    number_1 = randrange(10)
    
    operator = choice(operators)
    
    if operator == "/" :                       ##UTILIZAMOS ESTE IF PARA ASEGURARNOS DE QUE LA OPERACION NO IMPLIQUE DIVISION POR CERO
        number_2 = randrange(1,10) 
    else:
         number_2 = randrange(10)

         
    # Se imprime la cuenta.
    print(f"{i+1}- ¿Cuánto es {number_1} {operator} {number_2}?")
    
    # Le pedimos al usuario el resultado
    result = float(input("Resultado: "))

    if operator == "+":
        value= number_1+number_2
    elif operator == "-":
        value= number_1-number_2
    elif operator == "*":
        value=number_1*number_2
    else:
        value=number_1/number_2
    
    if result ==  value:
        print ()
        print ("El resultado es correcto.")
        print ()
        acertados += 1                                            ##CADA VEZ QUE ACIERTE LE SUMA UNO
    else:
        print()
        print ("El resultado es incorrecto.")
        print ()
        errados += 1                                              ##CADA VEZ QUE ERRE LE SUMA UNO

        
print("RESULTADOS:")
print("Aciertos:", acertados)
print("Errados:", errados)


# Al terminar toda la cantidad de cuentas por resolver.
# Se vuelve a tomar la fecha y la hora.
end_time = datetime.now()

# Restando las fechas obtenemos el tiempo transcurrido.
total_time = end_time - init_time

# Mostramos ese tiempo en segundos.
print(f"\n Tardaste {total_time.seconds} segundos.")




