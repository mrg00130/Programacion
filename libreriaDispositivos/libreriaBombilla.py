class Bombilla:

    def __init__(self, tipo="lámpara", estado=False, intensidad=100, color=(255, 255, 255)):
        self.__tipo = tipo
        self.__estado = estado  # False = apagada, True = encendida
        self.__intensidad = intensidad
        self.__color = color

    def encender(self):
        self.__estado = True

    def apagar(self):

        self.__estado = False

    def cambiar_intensidad(self, nueva_intensidad):
        if 0 <= nueva_intensidad <= 100:
            self.__intensidad = nueva_intensidad

    def cambiar_color(self, nuevo_color):
        self.__color = nuevo_color


    def get_estado(self):
        return self.__estado

    def get_intensidad(self):
        return self.__intensidad

    def get_color(self):
        return self.__color

    def get_tipo(self):
        return self.__tipo