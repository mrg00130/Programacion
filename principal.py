
# Importamos las CLASES
from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.libreriaHabitacion import Habitacion
from libreriaDispositivos.libreriaHub import Hub

print("=============================================")
print("== INICIO DE LA VALIDACIÓN DEL HOGAR DIGITAL (POO) ==")
print("=============================================")

# HU01: GESTIÓN DE BOMBILLA
print("\n--- VALIDANDO HU01: Gestión de Bombilla ---")
# 1. Creamos un OBJETO Bombilla
bombilla_estudio = Bombilla(tipo="Luz de escritorio", estado=False, intensidad=75, color=(255, 255, 0))
print("1.1. Estado inicial de la bombilla:")
print(bombilla_estudio) # Llama a __str__

print("\n1.2. Encender y apagar bombilla:")
bombilla_estudio.encender()
print("Estado después de encender:")
print(f"  El estado es: {'Encendido' if bombilla_estudio.get_estado() else 'Apagado'}")
bombilla_estudio.apagar()
print("Estado después de apagar:")
print(f"  El estado es: {'Encendido' if bombilla_estudio.get_estado() else 'Apagado'}")

print("\n1.3. Cambiar intensidad:")
bombilla_estudio.set_intensidad(50)
print("Intensidad cambiada a 50:")
print(f"  Intensidad actual: {bombilla_estudio.get_intensidad()}%")

print("\n1.4. Cambiar color:")
bombilla_estudio.set_color(0, 0, 255) # Azul
print("Color cambiado a azul:")
print(f"  Color actual (RGB): {bombilla_estudio.get_color()}")
print("--- HU01 VALIDADA CORRECTAMENTE ---")


# HU02: GESTIÓN DEL AIRE ACONDICIONADO
print("\n\n--- VALIDANDO HU02: Gestión de Aire Acondicionado ---")
aire_salon = AireAcondicionado(descripcion="Aire del Salón", estado=False, temperatura=25)
print("2.1. Estado inicial del aire:")
print(aire_salon)

print("\n2.2. Conocer temperatura y estado:")
print(f"La temperatura actual es: {aire_salon.get_temperatura()} grados.")
print(f"El aire está {'encendido' if aire_salon.get_estado() else 'apagado'}.")

print("\n2.3. Cambiar temperatura:")
aire_salon.set_temperatura(22)
print("Temperatura cambiada a 22:")
print(aire_salon)

print("\n2.4. Encender y apagar:")
aire_salon.encender()
print("Estado después de encender:")
print(aire_salon)
aire_salon.apagar()
print("Estado después de apagar:")
print(aire_salon)
print("--- HU02 VALIDADA CORRECTAMENTE ---")


# HU03: DISTRIBUCIÓN DE DISPOSITIVOS
print("\n\n--- VALIDANDO HU03: Distribución de Dispositivos en el Hogar ---")

mi_hogar = Hub(["Salón", "Dormitorio", "Cocina"])
print("3.1. El hogar ha sido creado.")
print(f"Número de habitaciones: {mi_hogar.get_numero_habitaciones()}")
print(f"Nombres de las habitaciones: {mi_hogar.get_nombres_habitaciones()}")

print("\n3.2. Añadiendo dispositivos a las habitaciones...")
# Obtenemos los OBJETOS habitacion
salon = mi_hogar.get_habitacion_por_nombre("Salón")
dormitorio = mi_hogar.get_habitacion_por_nombre("Dormitorio")

bombilla_techo_salon = Bombilla("Lámpara de techo")
salon.anadir_bombilla(bombilla_techo_salon)
salon.anadir_aire(aire_salon)
bombilla_noche_dormitorio = Bombilla("Luz de noche")
dormitorio.anadir_bombilla(bombilla_noche_dormitorio)
print("Dispositivos añadidos.")

print("\n3.3. Estado actual de los dispositivos en el hogar:")
print(mi_hogar)

print("\n3.4. Quitar un dispositivo:")
dormitorio.quitar_bombilla(bombilla_noche_dormitorio)
print("Se ha quitado la 'Luz de noche' del dormitorio.")
print(mi_hogar)

print("\n3.5. Modificar un dispositivo existente en el Salón:")
bombilla_techo_salon.set_intensidad(20)
print("Se ha cambiado la intensidad de la 'Lámpara de techo' del salón a 20.")
print(salon)

print("\n3.6. Identificar dispositivo y saber cantidad:")
print(f"El salón tiene {salon.get_numero_dispositivos()} dispositivos.")
print("--- HU03 VALIDADA CORRECTAMENTE ---")


print("\n=============================================")
print("==== VALIDACIÓN POO FINALIZADA CON ÉXITO ====")
print("=============================================")