import time
import threading


class GestorTemporizadores:


    def programar_evento(self, dispositivo, accion, segundos, callback_final, callback_notificacion=None):
        hilo = threading.Thread(target=self._tarea_espera,
                                args=(dispositivo, accion, segundos, callback_final, callback_notificacion))
        hilo.daemon = True
        hilo.start()

    def _tarea_espera(self, dispositivo, accion, segundos, callback_final, callback_notificacion):
        time.sleep(segundos)

        if accion == "encender" or accion == "abrir":
            dispositivo.encender()
            if hasattr(dispositivo, 'aumentar'):
                if dispositivo.get_nivel() == 0: dispositivo.aumentar(100)

        elif accion == "apagar" or accion == "cerrar":
            dispositivo.apagar()
            if hasattr(dispositivo, 'disminuir'):
                pass

        if callback_notificacion:
            mensaje = f"¡Tiempo cumplido!\nAcción: {accion.upper()}\nDispositivo: {dispositivo.get_nombre()}"
            callback_notificacion(mensaje)

        if callback_final:
            callback_final()