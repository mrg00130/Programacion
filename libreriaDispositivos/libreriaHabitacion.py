from libreriaDispositivos.libreriaBombilla import Bombilla
from libreriaDispositivos.libreriaAcondicionado import AireAcondicionado


class Habitacion:
    def __init__(self, descripcion="Habitación"):
        self._descripcion = descripcion
        self._bombillas = list()
        self._aires = list()

    def get_descripcion(self):
        return self._descripcion

    def get_bombillas(self):
        return self._bombillas

    def get_aires(self):
        return self._aires

    def anadir_bombilla(self, bombilla: Bombilla):
        if isinstance(bombilla, Bombilla):
            self._bombillas.append(bombilla)

    def quitar_bombilla(self, bombilla: Bombilla):
        if bombilla in self._bombillas:
            self._bombillas.remove(bombilla)

    def anadir_aire(self, aire: AireAcondicionado):
        if isinstance(aire, AireAcondicionado):
            self._aires.append(aire)

    def quitar_aire(self, aire: AireAcondicionado):
        if aire in self._aires:
            self._aires.remove(aire)

    def get_numero_bombillas(self):
        return len(self._bombillas)

    def get_numero_aires(self):
        return len(self._aires)

    def get_numero_dispositivos(self):
        return self.get_numero_bombillas() + self.get_numero_aires()


    #imprimir

    def __str__(self):
        info = f"\n--- Habitación: {self._descripcion} ({self.get_numero_dispositivos()} dispositivos) ---"

        if not self._bombillas and not self._aires:
            info += "\n  No hay dispositivos."
            return info

        for b in self._bombillas:
            info += f"\n{str(b)}"
        for a in self._aires:
            info += f"\n{str(a)}"

        return info