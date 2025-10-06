import time
from libreriaDispositivos.libreriaAcondicionado import *
from libreriaDispositivos.libreriaBombilla import *


def temporizadorAireApagar (aire,tiempo):
    time.sleep(tiempo)
    print("el ", aire["descripcion"], "se ha apagado")
    apagarAire(aire)


def temporizadorAireEncender (aire,tiempo):
    time.sleep(tiempo)
    print("el ", aire["descripcion"], "se ha Encendido")
    encenderAire(aire)


def temporizadorBombillaApagar (bombilla,tiempo):
    time.sleep(tiempo)
    print("el ", bombilla["descripcion"], "se ha apagado")
    apagarBombilla(bombilla)


def temporizadorBombillaEncender (bombilla,tiempo):
    time.sleep(tiempo)
    print("el ", bombilla["descripcion"], "se ha apagado")
    encenderBombilla(bombilla)
