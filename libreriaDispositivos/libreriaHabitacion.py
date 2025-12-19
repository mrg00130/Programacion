from datetime import datetime
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
        self._color_fondo = "#FFFFFF"


    def set_posicion(self, x, y):
        self._x = x;
        self._y = y

    def get_posicion(self):
        return getattr(self, '_x', 50), getattr(self, '_y', 50)

    def set_dimensiones(self, w, h):
        self._width = w;
        self._height = h

    def get_dimensiones(self):
        return getattr(self, '_width', 320), getattr(self, '_height', 350)

    def set_color_fondo(self, color):
        self._color_fondo = color

    def get_color_fondo(self):
        raw_color = getattr(self, '_color_fondo', "#FFFFFF")

        if isinstance(raw_color, (tuple, list)):
            try:
                return '#%02x%02x%02x' % (int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))
            except:
                return "#FFFFFF"

        if not isinstance(raw_color, str) or not raw_color.startswith("#"):
            return "#FFFFFF"

        return raw_color

    def guardaLog(self, fichero: str):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(fichero, 'a', encoding='utf-8') as f:
                f.write(f"\n--- LOG HABITACIÓN: {self.__descripcion} [{timestamp}] ---\n")
                todos = self.__lista_bombillas + self.__lista_aires
                for d in todos:
                    estado = "ON" if d.get_estado() else "OFF"
                    if hasattr(d, 'get_nivel'):
                        info = f"Disp: {d.get_nombre()} | Estado: {estado} | Nivel: {d.get_nivel()}"
                    else:
                        info = f"Disp: {d.get_nombre()} | Estado: {estado}"
                    f.write(info + "\n")
                f.write("-" * 50 + "\n")
        except:
            pass

    def anadir_bombilla(self, obj):
        self.__lista_bombillas.append(obj)

    def anadir_aire(self, obj):
        self.__lista_aires.append(obj)

    def quitar_bombilla(self, obj):
        if obj in self.__lista_bombillas: self.__lista_bombillas.remove(obj)

    def quitar_aire(self, obj):
        if obj in self.__lista_aires: self.__lista_aires.remove(obj)

    def get_descripcion(self):
        return self.__descripcion

    def get_bombillas(self):
        return self.__lista_bombillas

    def get_aires(self):
        return self.__lista_aires

    def get_numero_dispositivos(self):
        return len(self.__lista_bombillas) + len(self.__lista_aires)