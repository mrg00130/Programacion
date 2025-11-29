from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.libreriaHabitacion import Habitacion
from libreriaDispositivos.libreriaHub import Hub


def imprimir_info(msg):
    print(f"[INFO] {msg}")


def imprimir_error(msg):
    print(f"[ERROR] {msg}")


print("=== VALIDACIÓN ENTREGA 5: ABSTRACCIÓN E INTERFACES ===\n")

salon = Habitacion("Salón Principal")
b1 = Bombilla("Lámpara Techo", intensidad=20)
a1 = AireAcondicionado("Aire Split", temperatura=22)

salon.anadir_bombilla(b1)
salon.anadir_aire(a1)

print("1. Probando métodos abstractos (sin parámetros)...")

imprimir_info(f"Bombilla antes: {b1.get_intensidad()}%")
try:
    b1.aumentarIntensidad()
    imprimir_info(f"Bombilla después (debe ser +10): {b1.get_intensidad()}%")
except ValueError as e:
    imprimir_error(e)

imprimir_info(f"Aire antes: {a1.get_temperatura()}ºC")
try:
    a1.aumentarIntensidad()
    imprimir_info(f"Aire después (debe ser +1): {a1.get_temperatura()}ºC")
except ValueError as e:
    imprimir_error(e)

print("\n2. Probando generación de Log...")
nombre_log = "historial_habitacion.txt"

try:
    salon.guardaLog(nombre_log)
    imprimir_info(f"Se ha llamado a guardaLog(). Verifique '{nombre_log}'.")

    b1.encender()
    b1.aumentarIntensidad(50)
    salon.guardaLog(nombre_log)
    imprimir_info("Se ha guardado una segunda entrada en el log tras modificar dispositivos.")

except Exception as e:
    imprimir_error(f"Fallo al guardar log: {e}")

print("\n=== FIN VALIDACIÓN ===")