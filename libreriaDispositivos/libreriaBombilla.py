from libreriaDispositivos.libreriaProgramador import Programador
from libreriaDispositivos.dispositivo import Dispositivo


class Bombilla(Dispositivo):
    __contador = 0

    def __init__(self, tipo="Lámpara", estado=False, intensidad=100, color=(255, 255, 255)):
        super().__init__(nombre=tipo, nivel_inicial=intensidad, min_val=0, max_val=100, estado=estado)

        Bombilla.__contador += 1
        self.__id = f"bombilla{Bombilla.__contador}"
        self.__color = color
        self.__programador = None

    def cambiar_color(self, nuevo_color):
        self.__color = nuevo_color

    def cambiar_intensidad(self, valor_absoluto):

        diferencia = valor_absoluto - self._nivelIntensidad
        if diferencia > 0:
            self.aumentarIntensidad(diferencia)
        elif diferencia < 0:
            self.disminuirIntensidad(abs(diferencia))

    def get_id(self):
        return self.__id

    def get_intensidad(self):
        return self.get_nivel()

    def get_color(self):
        return self.__color

    def get_tipo(self):
        return self.get_nombre()

    def set_programador(self, programador_obj):
        if isinstance(programador_obj, Programador):
            self.__programador = programador_obj

    def get_programador(self):
        return self.__programador