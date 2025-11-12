from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.libreriaHabitacion import Habitacion
from libreriaDispositivos.libreriaHub import Hub
from libreriaDispositivos.libreriaProgramador import Programador
def imprimir_estado_bombilla(b):
    print(f"  > Bombilla [{b.get_id()}]: {b.get_tipo()}")
    print(f"    Estado: {'Encendida' if b.get_estado() else 'Apagada'}")
    print(f"    Intensidad: {b.get_intensidad()}%")
    print(f"    Color: {b.get_color()}")

def imprimir_estado_aire(a):
    print(f"  > Aire [{a.get_id()}]: {a.get_descripcion()}")
    print(f"    Estado: {'Encendido' if a.get_estado() else 'Apagado'}")
    print(f"    Temperatura: {a.get_temperatura()}°C")

def imprimir_resumen_hogar(hub):
    print("===========================================")
    print("== RESUMEN DEL HOGAR DIGITAL ==")
    print(f"Total de Habitaciones: {hub.get_numero_habitaciones()}")
    
    for hab in hub.get_habitaciones():
        print(f"\n--- HABITACIÓN: {hab.get_descripcion()} ({hab.get_numero_dispositivos()} dispositivos) ---")
        if hab.get_numero_dispositivos() == 0:
            print("  (Esta habitación está vacía)")
            
        for b in hab.get_bombillas():
            imprimir_estado_bombilla(b)
        for a in hab.get_aires():
            imprimir_estado_aire(a)
            
    print("\n-------------------------------------------")
    print(f"Total de dispositivos en el hogar: {hub.get_total_dispositivos_hogar()}")
    print("===========================================")

print("\n[Validando HU01 y HU02: Creación de Dispositivos con IDs]...")
b1 = Bombilla(tipo="Lámpara de techo Salón")
a1 = AireAcondicionado(descripcion="Aire del Salón")
b2_noche = Bombilla(tipo="Luz de noche Dormitorio", estado=True, intensidad=20)

imprimir_estado_bombilla(b1)
imprimir_estado_aire(a1)
imprimir_estado_bombilla(b2_noche)

print("\n[Validando HU03: Hogar...]")
mi_casa = Hub()
salon = Habitacion(descripcion="Salón")
dormitorio = Habitacion(descripcion="Dormitorio")
mi_casa.anadir_habitacion(salon)
mi_casa.anadir_habitacion(dormitorio)
salon.anadir_bombilla(b1)
salon.anadir_aire(a1)
dormitorio.anadir_bombilla(b2_noche)

imprimir_resumen_hogar(mi_casa)

print("\n\n--- VALIDANDO MEJORAS (ENTREGA 3): Programador Polimórfico ---")

print("\n1. Probando métodos de clase:")
print(f"  Hora actual del sistema: {Programador.get_hora_actual()}")

print("\n2. Probando programación de BOMBILLA (Luz Entrada):")
b3_programada = Bombilla(tipo="Luz Entrada", estado=False)
p_bombilla = Programador(b3_programada)
b3_programada.set_programador(p_bombilla)
p_bombilla.comienzo("Lunes", "08:00")
print(p_bombilla.get_horario())

print("\n3. Probando programación de AIRE ACONDICIONADO (Aire Salón):")
print("   Estado inicial del Aire del Salón:")
imprimir_estado_aire(a1) 

p_aire = Programador(a1)
a1.set_programador(p_aire)

p_aire.comienzo("Viernes", "17:00")
p_aire.fin("Viernes", "23:00") 

print("\n   Horario programado para 'Aire del Salón':")
print(p_aire.get_horario())
print("\n--- VALIDACIÓN DE MEJORAS FINALIZADA ---")