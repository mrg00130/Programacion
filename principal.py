from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.libreriaHabitacion import Habitacion
from libreriaDispositivos.libreriaHub import Hub

print("=== VALIDACIÓN ENTREGA 5: ABSTRACCIÓN E INTERFACES ===\n")

# 1.  Inicial
salon = Habitacion("Salón Principal")
b1 = Bombilla("Lámpara Techo", intensidad=20)
a1 = AireAcondicionado("Aire Split", temperatura=22)
salon.anadir_bombilla(b1)
salon.anadir_aire(a1)

print("1. Probando métodos abstractos con valor por defecto...")
print(f"Bombilla intensidad inicial: {b1.get_intensidad()}%")
b1.aumentarIntensidad()
print(f"Bombilla tras aumentar (default): {b1.get_intensidad()}% (Esperado: 30)")

print(f"Aire temp inicial: {a1.get_temperatura()}ºC")
a1.aumentarIntensidad()
print(f"Aire tras aumentar (default): {a1.get_temperatura()}ºC (Esperado: 23)")

print("\n2. Probando generación de Log (Interfaz LogHistorico)...")
nombre_log = "historial_habitacion.txt"

salon.guardaLog(nombre_log)

b1.encender()
b1.aumentarIntensidad(50) # Subimos a 80
a1.apagar()

salon.guardaLog(nombre_log)

print(f"\n--> Verifica el archivo '{nombre_log}' para ver el resultado.")
print("=== FIN VALIDACIÓN ===")