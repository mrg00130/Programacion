# libreriaDispositivos/libreriaBombilla.py

class Bombilla:
    def __init__(self, tipo="lámpara", estado=True, intensidad=100, color=(255, 255, 255)):
        self._tipo = tipo
        self._estado = estado  # True = encendida, False = apagada
        self._intensidad = intensidad
        self._color = color

    # --- Getters (para obtener valores) ---
    def get_tipo(self):
        return self._tipo

    def get_estado(self):
        return self._estado

    def get_intensidad(self):
        return self._intensidad

    def get_color(self):
        return self._color

    # --- Setters (para cambiar valores) ---
    def set_intensidad(self, valor):
        if 0 <= valor <= 100:
            self._intensidad = valor
        else:
            pass

    def set_color(self, r, g, b):
        self._color = (r, g, b)

    # --- Métodos de acción ---
    def encender(self):
        self._estado = True

    def apagar(self):
        self._estado = False

    # Imprimir
    def __str__(self):
        estado_str = "encendida" if self._estado else "apagada"
        info = (
            f"  - Bombilla ({self._tipo}):\n"
            f"    Estado: {estado_str}\n"
            f"    Intensidad: {self._intensidad}%\n"
            f"    Color (RGB): {self._color}"
        )
        return info