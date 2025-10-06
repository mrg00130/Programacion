from libreriaDispositivos.libreriaBombilla import *
from libreriaDispositivos.libreriaAcondicionado import *
from libreriaDispositivos.libreriaTemporizadores import *
from libreriaDispositivos import  libreriaHub as hub
from libreriaDispositivos import  libreriaHabitacion as hab


hogar = hub.crearCasa()

listaHab = list()
aire1=creaAireAcondicionado("Aire del salon")
salon = hab.creaHabitacion("salon")
candelabro = creaBombilla("candelabro")
bomb2 = creaBombilla()
hab.anadeBombillaHabitacion(salon, candelabro)
hab.anadeAireHabitacion(salon, aire1)
hab.imprimeHabitacion(salon)


temporizadorAireEncender(aire1,1)
hab.imprimeHabitacion(salon)
temporizadorAireApagar(aire1,1)
hab.imprimeHabitacion(salon)
