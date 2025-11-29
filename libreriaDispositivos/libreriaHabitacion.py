from datetime import datetime
from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado
from libreriaDispositivos.logHistorico import LogHistorico


class Habitacion(LogHistorico):

    def __init__(self, descripcion):
        self.__descripcion = descripcion
        self.__lista_bombillas = []
        self.__lista_aires = []

    def guardaLog(self, fichero: str):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(fichero, 'a', encoding='utf-8') as f:
            f.write(f"\n--- LOG HABITACIÓN: {self.__descripcion} [{timestamp}] ---\n")

            for b in self.__lista_bombillas:
                estado = "ON" if b.get_estado() else "OFF"
                info = f"ID: {b.get_id()} | Tipo: {b.get_tipo()} | Estado: {estado} | Intensidad: {b.get_intensidad()}%"
                f.write(info + "\n")

            for a in self.__lista_aires:
                estado = "ON" if a.get_estado() else "OFF"
                info = f"ID: {a.get_id()} | Desc: {a.get_descripcion()} | Estado: {estado} | Temp: {a.get_temperatura()}ºC"
                f.write(info + "\n")

            f.write("-" * 50 + "\n")


    def anadir_bombilla(self, bombilla_obj):
        if isinstance(bombilla_obj, Bombilla):
            self.__lista_bombillas.append(bombilla_obj)

    def anadir_aire(self, aire_obj):
        if isinstance(aire_obj, AireAcondicionado):
            self.__lista_aires.append(aire_obj)

    def quitar_bombilla(self, bombilla_obj):
        if bombilla_obj in self.__lista_bombillas:
            self.__lista_bombillas.remove(bombilla_obj)

    def quitar_aire(self, aire_obj):
        if aire_obj in self.__lista_aires:
            self.__lista_aires.remove(aire_obj)

    def get_descripcion(self):
        return self.__descripcion

    def get_bombillas(self):
        return self.__lista_bombillas

    def get_aires(self):
        return self.__lista_aires

    def get_numero_dispositivos(self):
        return len(self.__lista_bombillas) + len(self.__lista_aires)