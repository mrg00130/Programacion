from libreriaDispositivos.libreriaHabitacion import *

def creaHub(listaHabitaciones): # lista con cadenas de caracteres con la descripción de las habitaciones
    resultado = list()
    for habitacion in listaHabitaciones:
        resultado.append(creaHabitacion(habitacion))

    return resultado

def anadeBombillaHub(hub, indexHabitacion, bombilla):

    habitacion = hub[indexHabitacion]
    anadeBombillaHabitacion(habitacion,bombilla)

def imprimeHabitacionHub(hub, indexHabitacion):
    habitacion = hub[indexHabitacion]
    imprimeHabitacion(habitacion)