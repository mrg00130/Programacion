def creaHabitacion(descripcion = "Habitación ad hoc", listaBombillas = list(), listaAire =list()):
    resultado = {
        "descripcion" : descripcion,
        "bombilla" : listaBombillas,
        "aire": listaAire
    }
    return resultado

def listaHabitaciones (lista, habitacion):
    lista.append(habitacion)
    return lista


def anadeBombillaHabitacion(habitacion, bombilla):
    habitacion["bombilla"].append(bombilla)
    numeroB = len(habitacion["bombilla"])
    return bombilla

def quitaBombillaHabitacion(habitacion, bombilla):
    habitacion["bombilla"].remove(bombilla)

def anadeAireHabitacion(habitacion, aire):
    habitacion["aire"].append(aire)

def quitaAireHabitacion(habitacion, aire):
    habitacion["aire"].remove(aire)


def imprimeHabitacion(habitacion):
    print("\n--- Información de la Habitación ---")
    print("Nombre:", habitacion["descripcion"])
    print("Dispositivos:")

    if not habitacion["bombilla"] and not habitacion["aire"]:
        print("  No hay dispositivos en esta habitación.")

    # Bucle seguro para bombillas
    for bombilla in habitacion["bombilla"]:
        if isinstance(bombilla, dict) and 'tipo' in bombilla:
            print(f"  - Bombilla: {bombilla['tipo']}")
        else:
            print(f"  - ATENCIÓN: Dispositivo de bombilla con formato incorrecto: {bombilla}")

    # Bucle seguro para aires acondicionados
    for aire in habitacion["aire"]:
        if isinstance(aire, dict) and 'descripcion' in aire:
            print(f"  - Aire Acondicionado: {aire['descripcion']}")
        else:
            print(f"  - ATENCIÓN: Dispositivo de aire con formato incorrecto: {aire}")

    print("------------------------------------")


def numeroBombillas(habitacion):
    return len(habitacion["bombilla"])

def numeroAires(habitacion):
    return len(habitacion["aire"])

def numeroDispositivos(habitacion):
    return numeroBombillas(habitacion) + numeroAires(habitacion)