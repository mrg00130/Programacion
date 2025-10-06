def creaBombilla(tipo = "lampara", estado = True, intensidad = 100, color = (255,255,255)):
    bombilla = { "tipo": tipo, "estado": estado, "intensidad": intensidad, "color": color}
    return bombilla


def imprimirBombilla(bombilla):
    print("---------------------------------------")
    if (bombilla["estado"]):
        print("Bombilla encendida")
    else:
        print("Bombilla apagada")
    print("Nivel de intensidad:", bombilla["intensidad"])
    print("Color:", bombilla["color"])
    print("---------------------------------------")
def encenderBombilla(bombilla):
    bombilla["estado"] = True

def apagarBombilla(bombilla):
    bombilla["estado"] = False
def cambiarIntensidad(bombilla):
    print("La intensidad es de ", bombilla ["lumens"])
    i2 = input("A que intensidad quieres ")
    bombilla["intensidad"] = i2
    print("La intensidad es de  --->", bombilla["intensidad"])

def cambiarColor(bombilla):

    color2 = input("elige un color de los siguientes: blanco, rojo, verde, azul, amarillo, cian, magenta. ")
    color_minusculas = color2.lower()
    if color_minusculas == "blanco":
        print("El color cambiado a --->", bombilla["color"])

    elif color_minusculas == "rojo":
        bombilla["color"] = (255, 0, 0)
        print("El color cambiado a --->", bombilla["color"])

    elif color_minusculas == "verde":
        bombilla["color"] = (0, 255, 0)
        print("El color cambiado a --->", bombilla["color"])

    elif color_minusculas == "azul":
        bombilla["color"] = (0, 0, 255)
        print("El color cambiado a --->", bombilla["color"])

    elif color_minusculas == "amarillo":
        bombilla["color"] = (255, 255, 0)
        print("El color cambiado a --->", bombilla["color"])

    elif color_minusculas == "cian":
        bombilla["color"] = (0, 255, 255)
        print("El color cambiado a --->", bombilla["color"])

    elif color_minusculas == "magenta":
        bombilla["color"] = (255, 0, 255)
        print("El color cambiado a --->", bombilla["color"])

    else:

        print(f"El color '{color_minusculas}' no es una opción válida.")
        cambiarColor(bombilla)







