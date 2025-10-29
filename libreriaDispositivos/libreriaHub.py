from libreriaDispositivos.libreriaHabitacion import Habitacion


class Hub:
    def __init__(self, lista_nombres_habitaciones=None):
        self._habitaciones = list()
        if lista_nombres_habitaciones:
            for nombre in lista_nombres_habitaciones:
                self.anadir_habitacion(Habitacion(nombre))

    def get_habitaciones(self):
        return self._habitaciones

    def get_habitacion_por_nombre(self, nombre):
        for h in self._habitaciones:
            if h.get_descripcion() == nombre:
                return h
        return None  # No se encontró

    def anadir_habitacion(self, habitacion: Habitacion):
        if isinstance(habitacion, Habitacion):
            self._habitaciones.append(habitacion)

    def quitar_habitacion(self, habitacion: Habitacion):
        if habitacion in self._habitaciones:
            self._habitaciones.remove(habitacion)

    def get_numero_habitaciones(self):
        return len(self._habitaciones)

    def get_nombres_habitaciones(self):
        return [h.get_descripcion() for h in self._habitaciones]

    def get_total_dispositivos(self):
        total = 0
        for h in self._habitaciones:
            total += h.get_numero_dispositivos()
        return total

    def __str__(self):
        info = "--- Resumen de Dispositivos del Hogar ---"
        for h in self._habitaciones:
            info += str(h)  # Llama al __str__ de cada Habitacion

        info += "\n\n-----------------------------------------"
        info += f"\nTotal de dispositivos en el hogar: {self.get_total_dispositivos()}"
        info += "\n-----------------------------------------"
        return info