from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.libreriaHabitacion import Habitacion
from libreriaDispositivos.libreriaHub import Hub

def mostrar_resumen(hub, titulo="ESTADO ACTUAL"):
    print(f"\n--- {titulo} ---")
    nombres = hub.get_nombres_habitaciones()
    if not nombres:
        print(" (Casa vacía)")
    else:
        for hab in hub.get_habitaciones():
            print(f"Habitación: {hab.get_descripcion()}")
            for b in hab.get_bombillas():
                print(f"  - Bombilla: {b.get_tipo()} | Intensidad: {b.get_intensidad()}%")
            for a in hab.get_aires():
                print(f"  - Aire: {a.get_descripcion()} | Temp: {a.get_temperatura()}°C")

print("=== VALIDACIÓN ENTREGA 4: REFACTORIZACIÓN Y PERSISTENCIA ===\n")

mi_hub = Hub()
salon = Habitacion("Salón Principal")
mi_hub.anadir_habitacion(salon)

print("1. Probando Herencia (Clase Dispositivo)...")
b1 = Bombilla(tipo="Lámpara LED", intensidad=50)
salon.anadir_bombilla(b1)

print(f"Intensidad inicial: {b1.get_intensidad()}%")
b1.aumentarIntensidad(20)
print(f"Intensidad tras aumentar 20: {b1.get_intensidad()}%")


print("\n2. Probando Gestión de Errores (ValueError)...")

print("  -> Intentando subir bombilla por encima de 100...")
try:
    b1.aumentarIntensidad(1000)
    print("ERROR: El programa no debería llegar aquí.")
except ValueError as e:
    print(f"  [EXCEPCIÓN CAPTURADA]: {e}")
    print("  (El programa continúa correctamente)")

a1 = AireAcondicionado(descripcion="Split Pared", temperatura=18)
salon.anadir_aire(a1)
print(f"\n  -> Intentando bajar aire por debajo de 16 (Temp actual: {a1.get_temperatura()})...")
try:
    a1.disminuirIntensidad(10)
except ValueError as e:
    print(f"  [EXCEPCIÓN CAPTURADA]: {e}")

print("\n3. Probando Persistencia (HU04)...")
mostrar_resumen(mi_hub, "Antes de Guardar")

mi_hub.guardar_hogar("test_casa.pkl")

print("\n... Reiniciando sistema (Creando Hub vacío) ...")
nuevo_hub = Hub()
mostrar_resumen(nuevo_hub, "Nuevo Hub (Vacío)")

print("\n... Cargando datos del fichero ...")
nuevo_hub.recuperar_hogar("test_casa.pkl")
mostrar_resumen(nuevo_hub, "Después de Cargar")

print("\n=== FIN DE LA VALIDACIÓN ===")