from abc import ABC, abstractmethod


class Dispositivo(ABC):
    def __init__(self, nombre, nivel_inicial=0, min_val=0, max_val=100, estado=False):
        self._nombre = nombre
        self._nivel = nivel_inicial
        self._min = min_val
        self._max = max_val
        self._estado = estado
        self._id = "genérico"
        self._consumo_manual = None

    def encender(self):
        self._estado = True

    def apagar(self):
        self._estado = False

    def set_consumo_manual(self, w):
        self._consumo_manual = w

    def get_consumo_actual(self):
        if not self._estado: return 0
        manual = getattr(self, '_consumo_manual', None)
        if manual is not None: return manual
        return self._nivel if self._nivel > 0 else 100

    @abstractmethod
    def aumentar(self, cantidad=0):
        pass

    @abstractmethod
    def disminuir(self, cantidad=0):
        pass

    def get_estado(self):
        return self._estado

    def get_nivel(self):
        return self._nivel

    def get_nombre(self):
        return self._nombre


# --- DISPOSITIVOS ---

class Bombilla(Dispositivo):
    def __init__(self, nombre="Lámpara", intensidad=100, color=(255, 255, 255)):
        super().__init__(nombre, intensidad, 0, 100)
        self._color = color

    def aumentar(self, c=0): self._nivel = min(self._max, self._nivel + (10 if c == 0 else c))

    def disminuir(self, c=0): self._nivel = max(self._min, self._nivel - (10 if c == 0 else c))

    def cambiar_color(self, c): self._color = c

    def get_color(self): return self._color

    def cambiar_intensidad(self, v): self._nivel = v


class AireAcondicionado(Dispositivo):
    def __init__(self, nombre="Aire", temperatura=24):
        super().__init__(nombre, temperatura, 16, 30)

    # ESTOS SON LOS MÉTODOS QUE TE FALTABAN Y DABAN ERROR
    def aumentar(self, c=0): self._nivel = min(self._max, self._nivel + (1 if c == 0 else c))

    def disminuir(self, c=0): self._nivel = max(self._min, self._nivel - (1 if c == 0 else c))

    def cambiar_temperatura(self, v): self._nivel = v


class Persiana(Dispositivo):
    def __init__(self, nombre="Persiana", apertura=0):
        super().__init__(nombre, apertura, 0, 100)

    def aumentar(self, c=0): self._nivel = min(self._max, self._nivel + (20 if c == 0 else c))

    def disminuir(self, c=0): self._nivel = max(self._min, self._nivel - (20 if c == 0 else c))

    def cambiar_intensidad(self, v): self._nivel = v


class Horno(Dispositivo):
    def __init__(self, nombre="Horno", temperatura=0):
        super().__init__(nombre, temperatura, 0, 250)

    def aumentar(self, c=0): self._nivel = min(self._max, self._nivel + (50 if c == 0 else c))

    def disminuir(self, c=0): self._nivel = max(self._min, self._nivel - (50 if c == 0 else c))

    def cambiar_temperatura(self, v): self._nivel = v