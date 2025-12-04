from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.libreriaHabitacion import Habitacion
from libreriaDispositivos.libreriaHub import Hub

def imprimir_info(msg):
    print(f"[INFO] {msg}")

def imprimir_error(msg):
    print(f"[ERROR] {msg}")

def imprimir_exito(msg):
    print(f"[ÉXITO] {msg}")

print("=== VALIDACIÓN ENTREGA 5: ABSTRACCIÓN, INTERFACES Y CORRECCIONES ===\n")

hub = Hub()
salon = Habitacion("Salón Principal")
hub.anadir_habitacion(salon)

b1 = Bombilla("Lámpara Techo", intensidad=80) # Empezamos cerca del límite (100)
a1 = AireAcondicionado("Aire Split", temperatura=22)

salon.anadir_bombilla(b1)
salon.anadir_aire(a1)

print("1. Probando Gestión de Errores y Recuperación...")

imprimir_info(f"Intensidad actual Bombilla: {b1.get_intensidad()}%")
valor_excesivo = 50  # 80 + 50 = 130 (Falla)
valor_correcto = 10  # 80 + 10 = 90 (Funciona)

try:
    imprimir_info(f"Intentando subir intensidad en {valor_excesivo}...")
    b1.aumentarIntensidad(valor_excesivo)
except ValueError as e:
    imprimir_error(f"Capturado error: {e}")
    print("      >>> Simulando reintento del usuario con valor válido...")
    try:
        b1.aumentarIntensidad(valor_correcto)
        imprimir_exito(f"Recuperado. Nueva intensidad: {b1.get_intensidad()}%")
    except ValueError as e2:
        imprimir_error(f"Falló también el reintento: {e2}")



print("\n2. Probando Persistencia (Hub sin prints internos)...")
nombre_fichero = "datos_casa_v5.pkl"

#
try:
    hub.guardar_hogar(nombre_fichero)
    imprimir_exito(f"Hogar guardado en '{nombre_fichero}'")
except Exception as e:
    imprimir_error(f"No se pudo guardar: {e}")

print("   ... Borrando datos de memoria y recuperando ...")
hub_nuevo = Hub() # Hub vacío
try:
    hub_nuevo.recuperar_hogar(nombre_fichero)
    num_habs = hub_nuevo.get_numero_habitaciones()
    imprimir_exito(f"Hogar recuperado. Habitaciones cargadas: {num_habs}")
    desc_hab = hub_nuevo.get_habitaciones()[0].get_descripcion()
    print(f"      -> Habitación recuperada: {desc_hab}")
except FileNotFoundError:
    imprimir_error("El fichero no existe.")
except Exception as e:
    imprimir_error(f"Error crítico al cargar: {e}")


print("\n3. Probando Log Histórico (Interfaz)...")
nombre_log = "historial_habitacion.txt"

try:
    salon.guardaLog(nombre_log)
    imprimir_exito(f"Log generado en '{nombre_log}'")
except Exception as e:
    imprimir_error(f"Fallo al guardar log: {e}")

print("\n=== FIN VALIDACIÓN ===")