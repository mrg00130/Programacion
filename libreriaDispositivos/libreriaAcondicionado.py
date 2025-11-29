from libreriaDispositivos.libreriaProgramador import Programador
from libreriaDispositivos.dispositivo import Dispositivo


class AireAcondicionado(Dispositivo):
    __contador = 0

    def __init__(self, descripcion="Aire Salón", estado=False, temperatura=24):
        super().__init__(nombre=descripcion, nivel_inicial=temperatura, min_val=16, max_val=30, estado=estado)

        AireAcondicionado.__contador += 1
        self.__id = f"aire{AireAcondicionado.__contador}"
        self.__programador = None


    def aumentarIntensidad(self, cantidad=0):
        incremento = 1 if cantidad == 0 else cantidad
        nuevo_valor = self._nivelIntensidad + incremento

        if nuevo_valor > self._maxIntensidad:
            raise ValueError(f"El aire no puede superar {self._maxIntensidad}º (intentado: {nuevo_valor})")
        self._nivelIntensidad = nuevo_valor

    def disminuirIntensidad(self, cantidad=0):
        decremento = 1 if cantidad == 0 else cantidad
        nuevo_valor = self._nivelIntensidad - decremento

        if nuevo_valor < self._minIntensidad:
            raise ValueError(f"El aire no puede bajar de {self._minIntensidad}º (intentado: {nuevo_valor})")
        self._nivelIntensidad = nuevo_valor

    def cambiar_temperatura(self, nueva_temp):
        diferencia = nueva_temp - self._nivelIntensidad
        if diferencia > 0:
            self.aumentarIntensidad(diferencia)
        elif diferencia < 0:
            self.disminuirIntensidad(abs(diferencia))

    def get_temperatura(self):
        return self.get_nivel()

    def get_descripcion(self):
        return self.get_nombre()

    def set_programador(self, programador_obj):
        if isinstance(programador_obj, Programador):
            self.__programador = programador_obj

    def get_programador(self):
        return self.__programador