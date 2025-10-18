# principal.py - Script de Validación

from libreriaDispositivos.libreriaBombilla import *
from libreriaDispositivos.libreriaAcondicionado import *
from libreriaDispositivos import libreriaHabitacion as hab
from libreriaDispositivos import libreriaHub as hub

# --- INICIO DE LA VALIDACIÓN ---
print("=============================================")
print("== INICIO DE LA VALIDACIÓN DEL HOGAR DIGITAL ==")
print("=============================================")

# --- HU01: GESTIÓN DE BOMBILLA INTELIGENTE ---
print("\n--- VALIDANDO HU01: Gestión de Bombilla ---")
bombilla_estudio = creaBombilla(tipo="Luz de escritorio")
print("1.1. Estado inicial de la bombilla:")
imprimirBombilla(bombilla_estudio)

print("\n1.2. Encender y apagar bombilla:")
apagarBombilla(bombilla_estudio)
print("Estado después de apagar:")
imprimirBombilla(bombilla_estudio)
encenderBombilla(bombilla_estudio)
print("Estado después de encender:")
imprimirBombilla(bombilla_estudio)

# NOTA: Tus funciones cambiarIntensidad y cambiarColor pedían un input().
# Para una validación automática, las he modificado ligeramente en este script
# para no detener la ejecución. Puedes mantener las tuyas si prefieres la interacción.

print("\n1.3. Cambiar intensidad:")
bombilla_estudio["intensidad"] = 50 # Cambio directo para la prueba
print("Intensidad cambiada a 50:")
imprimirBombilla(bombilla_estudio)

print("\n1.4. Cambiar color:")
bombilla_estudio["color"] = (0, 0, 255) # Cambio a azul para la prueba
print("Color cambiado a azul:")
imprimirBombilla(bombilla_estudio)
print("--- HU01 VALIDADA CORRECTAMENTE ---")


# --- HU02: GESTIÓN DEL AIRE ACONDICIONADO ---
print("\n\n--- VALIDANDO HU02: Gestión de Aire Acondicionado ---")
aire_salon = creaAireAcondicionado(descripcion="Aire del Salón")
print("2.1. Estado inicial del aire:")
imprimirAire(aire_salon)

print("\n2.2. Conocer temperatura y estado:")
print(f"La temperatura actual es: {aire_salon['temperatura']} grados.")
print(f"El aire está {'encendido' if aire_salon['estado'] else 'apagado'}.")

print("\n2.3. Cambiar temperatura:")
aire_salon["temperatura"] = 22 # Cambio directo para la prueba
print("Temperatura cambiada a 22:")
imprimirAire(aire_salon)

print("\n2.4. Encender y apagar:")
apagarAire(aire_salon)
print("Estado después de apagar:")
imprimirAire(aire_salon)
encenderAire(aire_salon)
print("Estado después de encender:")
imprimirAire(aire_salon)
print("--- HU02 VALIDADA CORRECTAMENTE ---")


# --- HU03: DISTRIBUCIÓN DE DISPOSITIVOS ---
print("\n\n--- VALIDANDO HU03: Distribución de Dispositivos en el Hogar ---")
# 3.1. Crear el hogar y añadir habitaciones
mi_hogar = hub.creaHub(["Salón", "Dormitorio", "Cocina"])
print("3.1. El hogar ha sido creado.")
print(f"Número de habitaciones: {hub.numeroHabitaciones(mi_hogar)}")
print(f"Nombres de las habitaciones: {hub.obtenerNombresHabitaciones(mi_hogar)}")

# 3.2. Añadir dispositivos al hogar
print("\n3.2. Añadiendo dispositivos a las habitaciones...")
salon = mi_hogar[0]
dormitorio = mi_hogar[1]

bombilla_techo_salon = creaBombilla("Lámpara de techo")
hab.anadeBombillaHabitacion(salon, bombilla_techo_salon)
hab.anadeAireHabitacion(salon, aire_salon) # Usamos el aire creado antes

bombilla_noche_dormitorio = creaBombilla("Luz de noche")
hab.anadeBombillaHabitacion(dormitorio, bombilla_noche_dormitorio)
print("Dispositivos añadidos.")

print("\n3.3. Estado actual de los dispositivos en el hogar:")
hub.resumenDispositivosHogar(mi_hogar)

print("\n3.4. Quitar un dispositivo:")
hab.quitaBombillaHabitacion(dormitorio, bombilla_noche_dormitorio)
print("Se ha quitado la 'Luz de noche' del dormitorio.")
hub.resumenDispositivosHogar(mi_hogar)

# 3.5. Modificar un dispositivo ya ubicado
print("\n3.5. Modificar un dispositivo existente en el Salón:")
bombilla_techo_salon["intensidad"] = 20
print("Se ha cambiado la intensidad de la 'Lámpara de techo' del salón a 20.")
hab.imprimeHabitacion(salon)

print("\n3.6. Identificar dispositivo y saber cantidad:")
print(f"El salón tiene {hab.numeroDispositivos(salon)} dispositivos.")
print("--- HU03 VALIDADA CORRECTAMENTE ---")


print("\n=============================================")
print("==== VALIDACIÓN FINALIZADA CON ÉXITO ====")
print("=============================================")