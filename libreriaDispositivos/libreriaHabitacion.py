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
    print(habitacion["descripcion"], habitacion)


def numeroBomb(habitacion):
    numerB = 0
    for bombilla in habitacion["bombilla"]:
        numerB +=1






