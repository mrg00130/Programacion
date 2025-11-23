from libreriaDispositivos.libreriaHabitacion import Habitacion
import pickle


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


    def guardar_hogar(self, nombre_fichero="datos_casa.pkl"):
        try:
            with open(nombre_fichero, "wb") as f:
                pickle.dump(self.__lista_habitaciones, f)
            print(f"--> Datos guardados correctamente en '{nombre_fichero}'.")
        except Exception as e:
            print(f"Error al guardar: {e}")

    def recuperar_hogar(self, nombre_fichero="datos_casa.pkl"):
        try:
            with open(nombre_fichero, "rb") as f:
                self.__lista_habitaciones = pickle.load(f)
            print(f"--> Datos recuperados correctamente de '{nombre_fichero}'.")
        except FileNotFoundError:
            print("No se encontró el fichero de datos. Se inicia vacío.")
        except Exception as e:
            print(f"Error al cargar: {e}")