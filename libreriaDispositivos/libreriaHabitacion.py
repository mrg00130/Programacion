from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
class Habitacion:

    def __init__(self, descripcion):
        self.__descripcion = descripcion
        self.__lista_bombillas = []
        self.__lista_aires = []

    def anadir_bombilla(self, bombilla_obj):
        if isinstance(bombilla_obj, Bombilla):
            self.__lista_bombillas.append(bombilla_obj)

    def anadir_aire(self, aire_obj):
        if isinstance(aire_obj, AireAcondicionado):
            self.__lista_aires.append(aire_obj)
            
    def quitar_bombilla(self, bombilla_obj):
        if bombilla_obj in self.__lista_bombillas:
            self.__lista_bombillas.remove(bombilla_obj)

    def quitar_aire(self, aire_obj):
        if aire_obj in self.__lista_aires:
            self.__lista_aires.remove(aire_obj)

    def get_descripcion(self):
        return self.__descripcion

    def get_bombillas(self):
        return self.__lista_bombillas

    def get_aires(self):
        return self.__lista_aires

    def get_numero_dispositivos(self):
        return len(self.__lista_bombillas) + len(self.__lista_aires)