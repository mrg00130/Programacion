import time
import threading
import os
import sys
from datetime import datetime, timedelta
from .libreriaHub import Hub
from .libreriaVista import VentanaPrincipal
from .libreriaDispositivo import Bombilla, AireAcondicionado, Persiana, Horno
from .libreriaHabitacion import Habitacion
from .libreriaTemporizadores import GestorTemporizadores


class ControladorSmartHome:
    def __init__(self):
        self.modelo_hub = Hub()
        self.vista = VentanaPrincipal(self)
        self.temporizador = GestorTemporizadores()


        ruta_este_fichero = os.path.abspath(__file__)

        carpeta_libreria = os.path.dirname(ruta_este_fichero)

        self.ruta_proyecto = os.path.dirname(carpeta_libreria)

        self.archivo_config = os.path.join(self.ruta_proyecto, "config.txt")
        self.archivo_log_sesion = os.path.join(self.ruta_proyecto, "historial_sesiones.txt")
        self.archivo_default = os.path.join(self.ruta_proyecto, "datos_casa_v6.pkl")  # Nombre por defecto

        self.archivo_actual = self._leer_ultima_sesion()

        self._registrar_evento(
            f"\n{'=' * 40}\nINICIO SESIÓN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 40}")

    def iniciar_aplicacion(self):
        self.cargar_datos_inicio()
        self.vista.iniciar()

    def _registrar_evento(self, mensaje):
        try:
            hora = datetime.now().strftime("%H:%M:%S")
            with open(self.archivo_log_sesion, "a", encoding="utf-8") as f:
                f.write(f"[{hora}] {mensaje}\n")
        except:
            pass

    def _leer_ultima_sesion(self):
        try:
            if os.path.exists(self.archivo_config):
                with open(self.archivo_config, "r") as f:
                    nombre_archivo = f.read().strip()
                    ruta_completa = os.path.join(self.ruta_proyecto, nombre_archivo)

                    if os.path.exists(ruta_completa):
                        return ruta_completa
                    elif os.path.exists(nombre_archivo):
                        return nombre_archivo
        except:
            pass

        return self.archivo_default

    def _guardar_sesion_actual(self):
        try:
            if self.archivo_actual:

                nombre_base = os.path.basename(self.archivo_actual)
                with open(self.archivo_config, "w") as f: f.write(nombre_base)
        except:
            pass

    def cargar_datos_inicio(self):
        if not self.archivo_actual or not os.path.exists(self.archivo_actual):
            self._registrar_evento("No se encontró archivo previo. Iniciando vacío.")
            return
        try:
            self.modelo_hub.recuperar_hogar(self.archivo_actual)
            self.vista.construir_dashboard_visual(self.modelo_hub)
            self._actualizar_consumo()
            nombre_limpio = os.path.basename(self.archivo_actual)
            self.vista.ventana.after(500, lambda: self.vista.mostrar_info("Bienvenido",
                                                                          f"✅ Sesión restaurada: {nombre_limpio}"))
            self._registrar_evento(f"Carga automática: {nombre_limpio}")
        except:
            pass

    def cargar_datos(self, nombre_fichero):
        if not nombre_fichero: return
        try:
            self.modelo_hub.recuperar_hogar(nombre_fichero)
            self.archivo_actual = nombre_fichero
            self._guardar_sesion_actual()
            self.vista.construir_dashboard_visual(self.modelo_hub)
            self._actualizar_consumo()
            self.vista.mostrar_info("Éxito", f"Cargado: {os.path.basename(nombre_fichero)}")
            self._registrar_evento(f"Carga manual: {nombre_fichero}")
        except Exception as e:
            self.vista.mostrar_error("Error", str(e))


    def _guardar_y_refrescar(self):
        if self.archivo_actual:
            self.modelo_hub.guardar_hogar(self.archivo_actual)
            self._guardar_sesion_actual()
        self.vista.ventana.after(0, lambda: self.vista.construir_dashboard_visual(self.modelo_hub))
        self.vista.ventana.after(0, self._actualizar_consumo)

    def _actualizar_consumo(self):
        total = 0
        for h in self.modelo_hub.get_habitaciones():
            for d in h.get_bombillas() + h.get_aires(): total += d.get_consumo_actual()
        self.vista.actualizar_etiqueta_consumo(total)

    def activar_temporizador_inteligente(self, disp, entrada_str):
        segundos = 0
        accion = "apagar" if disp.get_estado() else "encender"
        verbo_msg = accion
        if isinstance(disp, Persiana):
            verbo_msg = "cerrar" if disp.get_estado() else "abrir"
            accion = "cerrar" if disp.get_estado() else "abrir"

        try:
            if ":" in entrada_str:
                now = datetime.now()
                partes = entrada_str.split(':')
                h = int(partes[0]);
                m = int(partes[1])
                objetivo = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if objetivo <= now: objetivo += timedelta(days=1)
                segundos = int((objetivo - now).total_seconds())
                msg_log = f"Programado {verbo_msg} {disp.get_nombre()} a las {entrada_str}"
            else:
                texto = entrada_str.lower()
                valor = int(''.join(filter(str.isdigit, texto)))
                if "min" in texto:
                    segundos = valor * 60
                elif "hor" in texto:
                    segundos = valor * 3600
                else:
                    segundos = valor
                msg_log = f"Temporizador {verbo_msg} {disp.get_nombre()} en {segundos}s"

            self._registrar_evento(msg_log)

            def notificar_seguro(texto):
                self.vista.ventana.after(0, lambda: self.vista.mostrar_info("⏰ Temporizador", texto))

            self.temporizador.programar_evento(disp, accion, segundos, lambda: self._guardar_y_refrescar(),
                                               notificar_seguro)
            self.vista.mostrar_info("Reloj", msg_log)
        except Exception as e:
            self.vista.mostrar_error("Error", f"Formato no válido: {e}")

    def toggle_dispositivo(self, disp):
        if disp.get_estado():
            disp.apagar()
        else:
            disp.encender()
        self._registrar_evento(f"Switch {disp.get_nombre()}: {'ON' if disp.get_estado() else 'OFF'}")
        self._guardar_y_refrescar()

    def cambiar_valor(self, disp, valor):
        try:
            val = int(float(valor))
            if val < disp._min: val = disp._min
            if val > disp._max: val = disp._max
            disp._nivel = val
            if self.archivo_actual: self.modelo_hub.guardar_hogar(self.archivo_actual)
            self._actualizar_consumo()
        except:
            pass

    def cambiar_color(self, bombilla, color):
        try:
            bombilla.cambiar_color(color); self._guardar_y_refrescar()
        except:
            pass

    def editar_consumo(self, d):
        w = self.vista.pedir_numero("Manual", f"Watios fijos {d.get_nombre()}:", d.get_consumo_actual())
        if w is not None: d.set_consumo_manual(w); self._guardar_y_refrescar()

    def agregar_dispositivo(self, tipo, nombre, habitacion):
        if not nombre: return
        d = None
        if tipo == "Bombilla":
            d = Bombilla(nombre)
        elif tipo == "Aire":
            d = AireAcondicionado(nombre)
        elif tipo == "Persiana":
            d = Persiana(nombre)
        elif tipo == "Horno":
            d = Horno(nombre)
        if d:
            if isinstance(d, Bombilla):
                habitacion.anadir_bombilla(d)
            else:
                habitacion.anadir_aire(d)
            self._registrar_evento(f"Añadido {tipo} '{nombre}'")
            self._guardar_y_refrescar()

    def eliminar_dispositivo(self, disp, habitacion):
        if self.vista.pedir_confirmacion("Borrar", f"¿Eliminar {disp.get_nombre()}?"):
            if isinstance(disp, Bombilla):
                habitacion.quitar_bombilla(disp)
            else:
                habitacion.quitar_aire(disp)
            self._guardar_y_refrescar()

    def eliminar_habitacion(self, habitacion):
        if self.vista.pedir_confirmacion("Borrar", f"¿Eliminar {habitacion.get_descripcion()}?"):
            self.modelo_hub.quitar_habitacion(habitacion);
            self._guardar_y_refrescar()

    def crear_habitacion(self, nombre):
        if nombre:
            nueva = Habitacion(nombre)
            num = self.modelo_hub.get_numero_habitaciones()
            offset = num * 40
            nueva.set_posicion(50 + offset, 50 + offset)
            self.modelo_hub.anadir_habitacion(nueva);
            self._guardar_y_refrescar()

    def mover_habitacion(self, hab, x, y):
        hab.set_posicion(x, y)
        if self.archivo_actual: self.modelo_hub.guardar_hogar(self.archivo_actual)

    def redimensionar_habitacion(self, hab, w, h):
        hab.set_dimensiones(w, h)
        if self.archivo_actual: self.modelo_hub.guardar_hogar(self.archivo_actual)

    def cambiar_color_habitacion(self, habitacion, color_hex):
        habitacion.set_color_fondo(color_hex);
        self._guardar_y_refrescar()

    def cargar_plano(self, r):
        self.modelo_hub.set_plano(r); self._guardar_y_refrescar()

    def quitar_plano(self):
        self.modelo_hub.set_plano(None); self._guardar_y_refrescar()

    def simular_climatizacion(self, aire, temp_objetivo):
        self._registrar_evento(f"Climatizando {aire.get_nombre()} a {temp_objetivo}ºC")

        def proceso():
            aire.encender()
            while aire.get_nivel() != temp_objetivo and aire.get_estado():
                time.sleep(0.8)
                current = aire.get_nivel()
                if current > temp_objetivo:
                    aire.disminuir(1)
                elif current < temp_objetivo:
                    aire.aumentar(1)
                self.vista.ventana.after(0, lambda: self.vista.actualizar_widget_individual(aire))
                self.vista.ventana.after(0, self._actualizar_consumo)
            self.vista.ventana.after(0, self._guardar_y_refrescar)
            if aire.get_estado(): self._registrar_evento(f"{aire.get_nombre()} alcanzó {temp_objetivo}ºC")

        t = threading.Thread(target=proceso);
        t.daemon = True;
        t.start()

    def accion_salir(self):
        self._registrar_evento("Cierre de aplicación.")