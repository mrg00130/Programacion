import time
import threading


class GestorTemporizadores:


    def programar_evento(self, dispositivo, accion, segundos, callback_final):
        hilo = threading.Thread(target=self._tarea_espera, args=(dispositivo, accion, segundos, callback_final))
        hilo.daemon = True  # El hilo muere si cierras el programa
        hilo.start()

    def _tarea_espera(self, dispositivo, accion, segundos, callback_final):
        # Esta función se ejecuta en paralelo
        print(f"[TIMER] Esperando {segundos}s para {accion} {dispositivo.get_nombre()}...")
        time.sleep(segundos)

        # Ejecutamos la acción
        if accion == "encender":
            dispositivo.encender()
        elif accion == "apagar":
            dispositivo.apagar()

        print(f"[TIMER] Acción {accion} ejecutada.")

        # Avisamos al controlador para que actualice la pantalla
        if callback_final:
            callback_final()