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

    # --- IMPLEMENTACIÓN (Sin prints, solo lógica y excepciones) ---

    def aumentarIntensidad(self, cantidad=0):
        incremento = 10 if cantidad == 0 else cantidad
        nuevo_valor = self._nivelIntensidad + incremento

        if nuevo_valor > self._maxIntensidad:
            raise ValueError(f"La bombilla no puede superar {self._maxIntensidad} (intentado: {nuevo_valor})")
        self._nivelIntensidad = nuevo_valor

    def disminuirIntensidad(self, cantidad=0):
        decremento = 10 if cantidad == 0 else cantidad
        nuevo_valor = self._nivelIntensidad - decremento

        if nuevo_valor < self._minIntensidad:
            raise ValueError(f"La bombilla no puede bajar de {self._minIntensidad} (intentado: {nuevo_valor})")
        self._nivelIntensidad = nuevo_valor

    # --- MÉTODOS ESPECÍFICOS ---

    def cambiar_color(self, nuevo_color):
        self.__color = nuevo_color

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