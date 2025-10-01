from libreriaDispositivos.libreriaBombilla import creaBombilla
from libreriaDispositivos.libreriaBombilla import imprimirBombilla
from libreriaDispositivos.libreriaBombilla import cambiarColor

from libreriaDispositivos import  libreriaAcondicionado as liba
bomb1 = creaBombilla(2)
aire1= liba.aireAcondicionado()
liba.imprimirAire(aire1)
liba.apagarAire(aire1)
liba.imprimirAire(aire1)
liba.cambiarTemperatura(aire1)
imprimirBombilla(bomb1)
cambiarColor(bomb1)


