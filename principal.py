from libreriaDispositivos.libreriaHub import *
from libreriaDispositivos.libreriaHabitacion import *
from libreriaDispositivos.libreriaBombilla import *
from libreriaDispositivos.libreriaAcondicionado import *


def menu():
    print("---------------------------------------")
    print("----------------MENÚ-------------------")
    print("1. Gestionar habitaciones")
    print("2. Gestionar dispositivos")
    print("3. Listar información del hogar")
    print("4. Salir")
    print("---------------------------------------")


def menu_habitaciones():
    print("1. Agregar habitación")
    print("2. Quitar habitación")
    print("3. Listar habitaciones")
    print("4. Contar habitaciones")
    print("5. Volver")


def menu_dispositivos():
    print("1. Agregar dispositivo a habitación")
    print("2. Quitar dispositivo de habitación")
    print("3. Listar dispositivos por habitación")
    print("4. Contar dispositivos en el hogar")
    print("5. Contar dispositivos por habitación")
    print("6. Volver")


# Crear el hogar como una lista vacía
hogar = crearCasa()

while True:
    menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":  # Gestionar habitaciones
        while True:
            menu_habitaciones()
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":  # Agregar habitación
                nombre_habitacion = input("Ingrese el nombre de la habitación: ")
                anadirHabitacion(hogar, nombre_habitacion)

            elif sub_opcion == "2":  # Quitar habitación
                nombre_habitacion = input("Ingrese el nombre de la habitación a quitar: ")
                quitarHabitacion(hogar, nombre_habitacion)

            elif sub_opcion == "3":  # Listar habitaciones
                listarHabitaciones(hogar)

            elif sub_opcion == "4":  # Contar habitaciones
                numeroHabitaciones(hogar)

            elif sub_opcion == "5":  # Volver
                break

            else:
                print("Opción no válida. Intente de nuevo.")

    elif opcion == "2":  # Gestionar dispositivos
        while True:
            menu_dispositivos()
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":  # Agregar dispositivo
                nombre_habitacion = input("Ingrese el nombre de la habitación: ")
                tipo_dispositivo = input("Ingrese el tipo de dispositivo (bombilla/aire): ").lower()
                descripcion_dispositivo = input("Ingrese la descripción del dispositivo: ")
                agregarDispositivoAHabitacion(hogar, nombre_habitacion, tipo_dispositivo, descripcion_dispositivo)

            elif sub_opcion == "2":  # Quitar dispositivo
                nombre_habitacion = input("Ingrese el nombre de la habitación: ")
                tipo_dispositivo = input("Ingrese el tipo de dispositivo (bombilla/aire): ").lower()
                descripcion_dispositivo = input("Ingrese la descripción del dispositivo: ")
                quitarDispositivoDeHabitacion(hogar, nombre_habitacion, tipo_dispositivo, descripcion_dispositivo)

            elif sub_opcion == "3":  # Listar dispositivos por habitación
                dispositivosPorHabitacion(hogar)

            elif sub_opcion == "4":  # Contar dispositivos en el hogar
                numeroDispositivosEnHogar(hogar)

            elif sub_opcion == "5":  # Contar dispositivos por habitación
                numeroDispositivosPorHabitacion(hogar)

            elif sub_opcion == "6":  # Volver
                break

            else:
                print("Opción no válida. Intente de nuevo.")

    elif opcion == "3":  # Listar información del hogar
        print("Información del hogar:")
        listarHabitaciones(hogar)
        dispositivosPorHabitacion(hogar)

    elif opcion == "4":  # Salir
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")