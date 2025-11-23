from libreriaDispositivos.libreriaProgramador import Programador
from libreriaDispositivos.dispositivo import Dispositivo



class AireAcondicionado(Dispositivo):
    __contador = 0

    def __init__(self, descripcion="Aire Salón", estado=False, temperatura=24):
        super().__init__(nombre=descripcion, nivel_inicial=temperatura, min_val=16, max_val=30, estado=estado)

        AireAcondicionado.__contador += 1
        self.__id = f"aire{AireAcondicionado.__contador}"
        self.__programador = None

    def cambiar_temperatura(self, nueva_temp):
        diferencia = nueva_temp - self._nivelIntensidad
        if diferencia > 0:
            self.aumentarIntensidad(diferencia)
        elif diferencia < 0:
            self.disminuirIntensidad(abs(diferencia))


    def get_id(self):
        return self.__id

    def get_temperatura(self):
        return self.get_nivel()  # La intensidad es la temperatura

    def get_descripcion(self):
        return self.get_nombre()

    def set_programador(self, programador_obj):
        if isinstance(programador_obj, Programador):
            self.__programador = programador_obj

    def get_programador(self):
        return self.__programador