def creaBombilla(estado =True, nivelIntensidad = 100, color = (255,255,255)):
    bombilla = {"estado": estado, "nivelIntensidad": nivelIntensidad, "color": color}
    return bombilla

def imprimirBombilla(bombilla):
    print("---------------------------------------")
    if (bombilla["estado"]):
        print("Bombilla encendida")
    else:
        print("Bombilla apagada")
    print("Nivel de intensidad:", bombilla["nivelIntensidad"])
    print("Color:", bombilla["color"])
    print("---------------------------------------")
