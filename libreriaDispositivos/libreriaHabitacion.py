from datetime import datetime
from .libreriaBombilla import Bombilla
from .libreriaAcondicionado import AireAcondicionado
from .logHistorico import LogHistorico

class Habitacion(LogHistorico):
    def __init__(self, descripcion):
        self.__descripcion = descripcion
        self.__lista_bombillas = []
        self.__lista_aires = []
        self._x = 50
        self._y = 50
        self._width = 320
        self._height = 350
        self._color_fondo = "#FFFFFF" # Nuevo: Color por defecto blanco

    # --- GESTIÓN VISUAL ---
    def set_posicion(self, x, y):
        self._x = x; self._y = y

    def get_posicion(self):
        if not hasattr(self, '_x'): self._x = 50
        if not hasattr(self, '_y'): self._y = 50
        return self._x, self._y

    def set_dimensiones(self, w, h):
        self._width = w; self._height = h

    def get_dimensiones(self):
        return getattr(self, '_width', 320), getattr(self, '_height', 350)

    def set_color_fondo(self, color):
        self._color_fondo = color

    def get_color_fondo(self):
        return getattr(self, '_color_fondo', "#FFFFFF")

    # --- LOG ---
    def guardaLog(self, fichero: str):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(fichero, 'a', encoding='utf-8') as f:
                f.write(f"\n--- LOG HABITACIÓN: {self.__descripcion} [{timestamp}] ---\n")
                todos = self.__lista_bombillas + self.__lista_aires
                for d in todos:
                    estado = "ON" if d.get_estado() else "OFF"
                    info = f"Disp: {d.get_nombre()} | Estado: {estado}"
                    f.write(info + "\n")
                f.write("-" * 50 + "\n")
        except: pass

    # --- GESTIÓN DISPOSITIVOS ---
    def anadir_bombilla(self, obj): self.__lista_bombillas.append(obj)
    def anadir_aire(self, obj): self.__lista_aires.append(obj)
    def quitar_bombilla(self, obj):
        if obj in self.__lista_bombillas: self.__lista_bombillas.remove(obj)
    def quitar_aire(self, obj):
        if obj in self.__lista_aires: self.__lista_aires.remove(obj)

    def get_descripcion(self): return self.__descripcion
    def get_bombillas(self): return self.__lista_bombillas
    def get_aires(self): return self.__lista_aires
    def get_numero_dispositivos(self): return len(self.__lista_bombillas) + len(self.__lista_aires)