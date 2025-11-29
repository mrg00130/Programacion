from abc import ABC, abstractmethod


class Dispositivo(ABC):

    def __init__(self, nombre, nivel_inicial=0, min_val=0, max_val=100, estado=False):
        self._nombre = nombre
        self._nivelIntensidad = nivel_inicial
        self._minIntensidad = min_val
        self._maxIntensidad = max_val
        self._estado = estado
        self._id = "genérico"

    def encender(self):
        self._estado = True

    def apagar(self):
        self._estado = False


    @abstractmethod
    def aumentarIntensidad(self, cantidad=0):
        pass

    @abstractmethod
    def disminuirIntensidad(self, cantidad=0):
        pass

    def get_estado(self):
        return self._estado

    def get_nivel(self):
        return self._nivelIntensidad

    def get_nombre(self):
        return self._nombre