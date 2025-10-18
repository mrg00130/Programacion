from libreriaDispositivos.libreriaHabitacion import creaHabitacion, imprimeHabitacion
from libreriaDispositivos.libreriaBombilla import creaBombilla
from libreriaDispositivos.libreriaAcondicionado import creaAireAcondicionado

# Crear la estructura principal de la casa
def crearCasa():
    return []

# Crear el hub inicial con una lista de habitaciones
def creaHub(listaHabitaciones):
    hub = []
    for nombre_habitacion in listaHabitaciones:
        habitacion = creaHabitacion(descripcion=nombre_habitacion)
        hub.append(habitacion)
    return hub

# Agregar una nueva habitación al hub
def anadirHabitacion(hub, nombre_habitacion):
    nueva_habitacion = creaHabitacion(descripcion=nombre_habitacion)
    hub.append(nueva_habitacion)
    print(f"Habitación '{nombre_habitacion}' añadida al hub.")

# Quitar una habitación del hub
def quitarHabitacion(hub, nombre_habitacion):
    for habitacion in hub:
        if habitacion["descripcion"] == nombre_habitacion:
            hub.remove(habitacion)
            print(f"Habitación '{nombre_habitacion}' eliminada del hub.")
            return
    print(f"Habitación '{nombre_habitacion}' no encontrada en el hub.")

# Imprimir información sobre todas las habitaciones del hub
def listarHabitaciones(hub):
    print("Lista de habitaciones en el hub:")
    for habitacion in hub:
        imprimeHabitacion(habitacion)

# Contar el número de habitaciones en el hub
def numeroHabitaciones(hub):
    print(f"El número total de habitaciones es: {len(hub)}")
    return len(hub)

# Listar los dispositivos por habitación
def dispositivosPorHabitacion(hub):
    print("Dispositivos en cada habitación:")
    for habitacion in hub:
        print(f"Habitación: {habitacion['descripcion']}")
        print(f"- Bombillas: {len(habitacion['bombilla'])}")
        print(f"- Aires acondicionados: {len(habitacion['aire'])}")

# Agregar un dispositivo (bombilla o aire acondicionado) a una habitación
def agregarDispositivoAHabitacion(hub, nombre_habitacion, tipo_dispositivo, descripcion_dispositivo):
    for habitacion in hub:
        if habitacion["descripcion"] == nombre_habitacion:
            if tipo_dispositivo == "bombilla":
                bombilla = creaBombilla(tipo=descripcion_dispositivo)
                habitacion["bombilla"].append(bombilla)
                print(f"Bombilla '{descripcion_dispositivo}' añadida a la habitación '{nombre_habitacion}'.")
            elif tipo_dispositivo == "aire":
                aire = creaAireAcondicionado(descripcion=descripcion_dispositivo)
                habitacion["aire"].append(aire)
                print(f"Aire acondicionado '{descripcion_dispositivo}' añadido a la habitación '{nombre_habitacion}'.")
            return
    print(f"Habitación '{nombre_habitacion}' no encontrada en el hub.")

# Quitar un dispositivo (bombilla o aire acondicionado) de una habitación
def quitarDispositivoDeHabitacion(hub, nombre_habitacion, tipo_dispositivo, descripcion_dispositivo):
    for habitacion in hub:
        if habitacion["descripcion"] == nombre_habitacion:
            if tipo_dispositivo == "bombilla":
                for bombilla in habitacion["bombilla"]:
                    if bombilla["tipo"] == descripcion_dispositivo:
                        habitacion["bombilla"].remove(bombilla)
                        print(f"Bombilla '{descripcion_dispositivo}' eliminada de la habitación '{nombre_habitacion}'.")
                        return
            elif tipo_dispositivo == "aire":
                for aire in habitacion["aire"]:
                    if aire["descripcion"] == descripcion_dispositivo:
                        habitacion["aire"].remove(aire)
                        print(f"Aire acondicionado '{descripcion_dispositivo}' eliminado de la habitación '{nombre_habitacion}'.")
                        return
    print(f"Dispositivo '{descripcion_dispositivo}' no encontrado en la habitación '{nombre_habitacion}'.")

# Contar el número total de dispositivos en el hogar
def numeroDispositivosEnHogar(hub):
    total_dispositivos = 0
    for habitacion in hub:
        total_dispositivos += len(habitacion["bombilla"]) + len(habitacion["aire"])
    print(f"El número total de dispositivos en el hogar es: {total_dispositivos}")
    return total_dispositivos

# Contar el número de dispositivos en cada habitación
def numeroDispositivosPorHabitacion(hub):
    print("Número de dispositivos por habitación:")
    for habitacion in hub:
        total = len(habitacion["bombilla"]) + len(habitacion["aire"])
        print(f"Habitación '{habitacion['descripcion']}': {total} dispositivos")