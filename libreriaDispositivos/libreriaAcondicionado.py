
class AireAcondicionado:
    def __init__(self, descripcion="Aire", estado=True, temperatura=24):
        self._descripcion = descripcion
        self._estado = estado
        self._temperatura = temperatura
    def get_descripcion(self):
        return self._descripcion

    def get_estado(self):
        return self._estado

    def get_temperatura(self):
        return self._temperatura

    def set_temperatura(self, temp):
        if 24 <= temp <= 38:
            self._temperatura = temp
        else:
            pass
    def encender(self):
        self._estado = True

    def apagar(self):
        self._estado = False

    def __str__(self):
        estado_str = "encendido" if self._estado else "apagado"
        info = (
            f"  - Aire Acondicionado ({self._descripcion}):\n"
            f"    Estado: {estado_str}\n"
            f"    Temperatura: {self._temperatura}°C"
        )
        return info