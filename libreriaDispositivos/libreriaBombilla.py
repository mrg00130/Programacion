from libreriaDispositivos.libreriaProgramador import Programador

class Bombilla:
    __contador = 0

    def __init__(self, tipo="lámpara", estado=False, intensidad=100, color=(255, 255, 255)):
        Bombilla.__contador += 1
        self.__id = f"bombilla{Bombilla.__contador}"
        self.__tipo = tipo
        self.__estado = estado
        self.__intensidad = intensidad
        self.__color = color
        self.__programador = None

    def encender(self):
        self.__estado = True

    def apagar(self):
        self.__estado = False

    def cambiar_intensidad(self, nueva_intensidad):
        if 0 <= nueva_intensidad <= 100:
            self.__intensidad = nueva_intensidad

    def cambiar_color(self, nuevo_color):
        self.__color = nuevo_color

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
        
    def get_tipo(self):
        return self.__tipo

    
    def get_intensidad(self):
        """Devuelve la intensidad actual."""
        return self.__intensidad
        
    def get_color(self):
        """Devuelve el color actual."""
        return self.__color