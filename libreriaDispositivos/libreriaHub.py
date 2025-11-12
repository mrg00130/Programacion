from libreriaDispositivos.libreriaHabitacion import Habitacion

class Hub:

    def __init__(self):
        self.__lista_habitaciones = []

    def anadir_habitacion(self, habitacion_obj):
        if isinstance(habitacion_obj, Habitacion):
            self.__lista_habitaciones.append(habitacion_obj)
            
    def quitar_habitacion(self, habitacion_obj):
        if habitacion_obj in self.__lista_habitaciones:
            self.__lista_habitaciones.remove(habitacion_obj)

    def get_habitaciones(self):
        return self.__lista_habitaciones

    def get_numero_habitaciones(self):
        return len(self.__lista_habitaciones)

    def get_nombres_habitaciones(self):
        return [h.get_descripcion() for h in self.__lista_habitaciones]

    def get_total_dispositivos_hogar(self):
        total = 0
        for hab in self.__lista_habitaciones:
            total += hab.get_numero_dispositivos()
        return total