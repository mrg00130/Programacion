class AireAcondicionado:

    def __init__(self, descripcion="Aire Salón", estado=False, temperatura=24):
        self.__descripcion = descripcion
        self.__estado = estado
        self.__temperatura = temperatura

    def encender(self):
        self.__estado = True

    def apagar(self):
        self.__estado = False

    def cambiar_temperatura(self, nueva_temp):
        self.__temperatura = nueva_temp


    def get_estado(self):
        return self.__estado

    def get_temperatura(self):
        return self.__temperatura

    def get_descripcion(self):
        return self.__descripcion