def creaAireAcondicionado(estado = True, temperatura = 27):
    aire = {"estado" : estado, "temperatura" : temperatura }
    return aire

def imprimirAire(aire):
    print("---------------------------------------")
    if (aire["estado"]):
        print("El aire acondicionado esta encendido")
    else:
        print("El aire acondicionado esta apagado")
    print("La temperatura es de ", aire["temperatura"])

    print("---------------------------------------")
#un temporizador es buena idea o hasta que tenga la temperatura de la sala a un valor
def encenderAire(aire):
    aire["estado"] = True

def apagarAire(aire):
    aire["estado"] = False
def cambiarTemperatura(aire):
    print("La temperatura es de ", aire["temperatura"])
    t2 = input("A que temperatura lo quieres ")
    aire["temperatura"] = t2
    print("La temperatura es de  --->", aire["temperatura"])

