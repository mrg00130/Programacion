
from libreriaDispositivos.libreriaProgramador import Programador
class AireAcondicionado:
    __contador = 0

    def __init__(self, descripcion="Aire Salón", estado=False, temperatura=24):
        AireAcondicionado.__contador += 1
        self.__id = f"aire{AireAcondicionado.__contador}"
        self.__descripcion = descripcion
        self.__estado = estado
        self.__temperatura = temperatura
        self.__programador = None

    def encender(self):
        self.__estado = True

    def apagar(self):
        self.__estado = False

    def cambiar_temperatura(self, nueva_temp):
        self.__temperatura = nueva_temp

    def set_programador(self, programador_obj):
        if isinstance(programador_obj, Programador):
            self.__programador = programador_obj
        else:
            print("Error: El objeto no es un Programador válido.")

    def get_programador(self):
        return self.__programador

    def get_id(self):
        return self.__id

    def get_estado(self):
        return self.__estado

    def get_temperatura(self):
        return self.__temperatura

    def get_descripcion(self):
        return self.__descripcion