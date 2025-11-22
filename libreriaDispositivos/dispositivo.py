class Dispositivo:

    def __init__(self, nombre, nivel_inicial=0, min_val=0, max_val=100, estado=False):
        self._nombre = nombre
        self._nivelIntensidad = nivel_inicial
        self._minIntensidad = min_val
        self._maxIntensidad = max_val
        self._estado = estado
        # ID genérico (lo gestionarán los hijos o se puede mover aquí si se desea)
        self._id = "genérico"

    def encender(self):
        self._estado = True

    def apagar(self):
        self._estado = False

    def aumentarIntensidad(self, cantidad):
        nuevo_valor = self._nivelIntensidad + cantidad
        if nuevo_valor > self._maxIntensidad:
            raise ValueError(f"Error: No se puede aumentar a {nuevo_valor}. El máximo es {self._maxIntensidad}.")
        self._nivelIntensidad = nuevo_valor

    def disminuirIntensidad(self, cantidad):
        nuevo_valor = self._nivelIntensidad - cantidad
        if nuevo_valor < self._minIntensidad:
            raise ValueError(f"Error: No se puede disminuir a {nuevo_valor}. El mínimo es {self._minIntensidad}.")
        self._nivelIntensidad = nuevo_valor

    # Getters comunes
    def get_estado(self):
        return self._estado

    def get_nivel(self):
        return self._nivelIntensidad

    def get_nombre(self):
        return self._nombre