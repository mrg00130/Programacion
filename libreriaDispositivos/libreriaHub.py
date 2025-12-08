from .libreriaHabitacion import Habitacion
import pickle


class Hub:
    def __init__(self):
        self.__lista_habitaciones = []
        self._ruta_plano = None

    def anadir_habitacion(self, h):
        if isinstance(h, Habitacion): self.__lista_habitaciones.append(h)

    def quitar_habitacion(self, h):
        if h in self.__lista_habitaciones: self.__lista_habitaciones.remove(h)

    def get_habitaciones(self):
        return self.__lista_habitaciones

    def get_numero_habitaciones(self):
        return len(self.__lista_habitaciones)

    def get_nombres_habitaciones(self):
        return [h.get_descripcion() for h in self.__lista_habitaciones]

    def get_total_dispositivos_hogar(self):
        total = 0
        for h in self.__lista_habitaciones: total += h.get_numero_dispositivos()
        return total

    def set_plano(self, r):
        self._ruta_plano = r

    def get_plano(self):
        return getattr(self, '_ruta_plano', None)  # Seguro anti-fallos

    # --- PERSISTENCIA INTELIGENTE ---
    def guardar_hogar(self, nombre_fichero="datos_casa.pkl"):
        with open(nombre_fichero, "wb") as f:
            pickle.dump(self, f)  # Guardamos SIEMPRE el objeto Hub entero

    def recuperar_hogar(self, nombre_fichero="datos_casa.pkl"):
        with open(nombre_fichero, "rb") as f:
            datos = pickle.load(f)

            # DETECTAMOS SI ES EL FORMATO VIEJO O NUEVO
            if isinstance(datos, Hub):
                # Es formato nuevo (v6)
                self.__lista_habitaciones = datos.get_habitaciones()
                self._ruta_plano = datos.get_plano()
            elif isinstance(datos, list):
                # Es formato viejo (v5 o anterior) - Solo era una lista de habitaciones
                self.__lista_habitaciones = datos
                self._ruta_plano = None  # Los viejos no tenían plano
            else:
                print("Formato de fichero desconocido.")