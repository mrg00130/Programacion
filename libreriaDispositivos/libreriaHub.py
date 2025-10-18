from libreriaDispositivos.libreriaHabitacion import *
from libreriaDispositivos.libreriaBombilla import *
from libreriaDispositivos.libreriaAcondicionado import *

def crearCasa():
    nombre =list()
    return  nombre

def creaHub(listaHabitacion):
    hub = list()
    for habitacion in listaHabitacion:
        hub.append(creaHabitacion(habitacion))
    return hub

def anadirHabitacion(hub, habitacion):
    hub.append(habitacion)
    return hub

def quitarHabitacion(hub, habitacion):
    hub.remove(habitacion)
    return hub

def imprimeHabitacionHub(hub, indexHabitacion):
    habitacion = hub[indexHabitacion]
    imprimeHabitacion(habitacion)

def numeroHabitaciones(hub):
    return len(hub)

def obtenerNombresHabitaciones(hub):
    nombres = []
    for habitacion in hub:
        nombres.append(habitacion["descripcion"])
    return nombres

# --- FUNCIÓN MEJORADA Y MÁS ROBUSTA ---
def resumenDispositivosHogar(hub):
    print("--- Resumen de Dispositivos del Hogar ---")
    total_dispositivos = 0
    for habitacion in hub:
        num_dispositivos_hab = numeroDispositivos(habitacion)
        total_dispositivos += num_dispositivos_hab
        print(f"\nHabitación: {habitacion['descripcion']} ({num_dispositivos_hab} dispositivos)")

        if not habitacion["bombilla"] and not habitacion["aire"]:
            print("  No hay dispositivos.")

        # Bucle para bombillas
        for bombilla in habitacion["bombilla"]:
            if isinstance(bombilla, dict) and 'tipo' in bombilla:
                print(f"  - Bombilla: {bombilla['tipo']}")
            else:
                print(f"  - ATENCIÓN: Dispositivo de bombilla con formato incorrecto: {bombilla}")

        # Bucle para aires acondicionados
        for aire in habitacion["aire"]:
            if isinstance(aire, dict) and 'descripcion' in aire:
                print(f"  - Aire Acondicionado: {aire['descripcion']}")
            else:
                print(f"  - ATENCIÓN: Dispositivo de aire con formato incorrecto: {aire}")

    print("\n-----------------------------------------")
    print(f"Total de dispositivos en el hogar: {total_dispositivos}")
    print("-----------------------------------------")