def creaHabitacion(descripcion = "Habitación ad hoc", listaBombillas = list(), listaAire =list()):
    resultado = {
        "descripcion" : descripcion,
        "bombillas" : listaBombillas,
        "aires": listaAire
    }
    return resultado

def listaHabitaciones (lista, habitacion):

    lista.append(habitacion)
    return lista


def anadeBombillaHabitacion(habitacion, bombilla):
    habitacion["bombillas"].append(bombilla)

def quitaBombillaHabitacion(habitacion, bombilla):
    habitacion["bombillas"].remove(bombilla)

def imprimeHabitacion(habitacion):
    print("Habitación:", habitacion)







