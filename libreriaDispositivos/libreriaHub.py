from libreriaDispositivos.libreriaHabitacion import *
from libreriaDispositivos.libreriaBombilla import *
from libreriaDispositivos.libreriaAcondicionado import *

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
    masHabitacion = hub.append(habitacion)
    print(masHabitacion)
    return masHabitacion

def quitarHabitacion(hub, habitacion):
    listaHabitaciones(habitacion)
    hub = list()
    menosHabitacion = hub.remove(habitacion)
    print(menosHabitacion)
    return menosHabitacion


def imprimeHabitacionHub(hub, indexHabitacion):
    habitacion = hub[indexHabitacion]
    imprimeHabitacion(habitacion)

def numeroHabitaciones(hub):
    numeroHabitaciones= len(hub)
    print(numeroHabitaciones)

