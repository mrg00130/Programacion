from libreriaDispositivos.libreriaBombilla import *
from libreriaDispositivos.libreriaAcondicionado import *
from libreriaDispositivos import  libreriaHub as hub
from libreriaDispositivos import  libreriaHabitacion as hab


hogar = hub.crearCasa()

listaHab = list()

salon = hab.creaHabitacion("salon")
cocina = hab.creaHabitacion("cocina")
hab.listaHabitaciones(hogar,cocina)
hab.listaHabitaciones(hogar,salon)
hub.numeroHabitaciones(hogar)