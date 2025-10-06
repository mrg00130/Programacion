from libreriaDispositivos.libreriaHabitacion import *

def crearCasa():
    nombre =list()
    return  nombre
def creaHub(listaHabitacion): # lista con cadenas de caracteres con la descripción de las habitaciones
    hub = list()
    for habitacion in listaHabitacion:
        hub.append(creaHabitacion(habitacion))

    return hub
def anadirHabitacion(hub, habitacion):
    listaHabitaciones(habitacion)
    hub = list()
    nuevaHabitacion = hub.append(habitacion)
    print(nuevaHabitacion)
    return nuevaHabitacion

def anadeBombillaHub(hub, indexHabitacion, bombilla):

    habitacion = hub[indexHabitacion]
    anadeBombillaHabitacion(habitacion,bombilla)

def imprimeHabitacionHub(hub, indexHabitacion):
    habitacion = hub[indexHabitacion]
    imprimeHabitacion(habitacion)

def numeroHabitaciones(hub):
    numeroHabitaciones= len(hub)
    print(numeroHabitaciones)