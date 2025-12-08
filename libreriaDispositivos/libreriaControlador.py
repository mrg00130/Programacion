import time
import threading
import os
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
        self.archivo_config = "config.txt"
        self.archivo_actual = self._leer_ultima_sesion()

    def iniciar_aplicacion(self):
        self.cargar_datos_inicio()
        self.vista.iniciar()

    def _leer_ultima_sesion(self):
        try:
            if os.path.exists(self.archivo_config):
                with open(self.archivo_config, "r") as f: return f.read().strip()
        except:
            pass
        return "datos_casa_v6.pkl"

    def _guardar_sesion_actual(self):
        try:
            if self.archivo_actual:
                with open(self.archivo_config, "w") as f: f.write(self.archivo_actual)
        except:
            pass

    def cargar_datos_inicio(self):
        if not self.archivo_actual: return
        try:
            self.modelo_hub.recuperar_hogar(self.archivo_actual)
            self.vista.construir_dashboard_visual(self.modelo_hub)
            self._actualizar_consumo()
            self.vista.ventana.after(500, lambda: self.vista.mostrar_info("Bienvenido",
                                                                          f"✅ Sesión restaurada: {self.archivo_actual}"))
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
            self.vista.mostrar_info("Éxito", f"Cargado: {nombre_fichero}")
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
        if isinstance(disp, Persiana): verbo_msg = "cerrar" if disp.get_estado() else "abrir"

        try:
            if ":" in entrada_str:
                now = datetime.now()
                partes = entrada_str.split(':')
                h = int(partes[0]);
                m = int(partes[1])
                objetivo = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if objetivo <= now: objetivo += timedelta(days=1)
                segundos = int((objetivo - now).total_seconds())
                msg = f"Programado: {verbo_msg} a las {entrada_str}"
            else:
                texto = entrada_str.lower()
                valor = int(''.join(filter(str.isdigit, texto)))
                if "min" in texto:
                    segundos = valor * 60
                elif "hor" in texto:
                    segundos = valor * 3600
                else:
                    segundos = valor
                msg = f"Cuenta atrás: {verbo_msg} en {segundos} seg"

            self.temporizador.programar_evento(disp, accion, segundos, lambda: self._guardar_y_refrescar())
            self.vista.mostrar_info("Reloj", msg)
        except:
            self.vista.mostrar_error("Error", "Formato no válido.")

    def toggle_dispositivo(self, disp):
        if disp.get_estado():
            disp.apagar()
        else:
            disp.encender()
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
        bombilla.cambiar_color(color);
        self._guardar_y_refrescar()

    def cambiar_color_habitacion(self, habitacion, color_hex):
        habitacion.set_color_fondo(color_hex)
        self._guardar_y_refrescar()

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
            self._guardar_y_refrescar()

    def eliminar_dispositivo(self, disp, habitacion):
        if self.vista.pedir_confirmacion("Borrar", "¿Eliminar?"):
            if disp in habitacion.get_bombillas():
                habitacion.quitar_bombilla(disp)
            elif disp in habitacion.get_aires():
                habitacion.quitar_aire(disp)
            self._guardar_y_refrescar()

    def eliminar_habitacion(self, habitacion):
        if self.vista.pedir_confirmacion("Borrar", f"¿Eliminar {habitacion.get_descripcion()}?"):
            self.modelo_hub.quitar_habitacion(habitacion)
            self._guardar_y_refrescar()

    # --- NUEVO: CREAR HABITACIÓN SIN SOLAPAR ---
    def crear_habitacion(self, nombre):
        if nombre:
            nueva = Habitacion(nombre)
            # Calcular posición en cascada
            num = self.modelo_hub.get_numero_habitaciones()
            offset = num * 40  # 40px más abajo y derecha por cada habitación
            nueva.set_posicion(50 + offset, 50 + offset)

            self.modelo_hub.anadir_habitacion(nueva)
            self._guardar_y_refrescar()

    def mover_habitacion(self, hab, x, y):
        hab.set_posicion(x, y)
        if self.archivo_actual: self.modelo_hub.guardar_hogar(self.archivo_actual)

    def redimensionar_habitacion(self, hab, w, h):
        hab.set_dimensiones(w, h)
        if self.archivo_actual: self.modelo_hub.guardar_hogar(self.archivo_actual)

    def activar_enfriamiento_inteligente(self, aire):
        def proceso():
            aire.encender()
            while aire.get_nivel() > 21 and aire.get_estado():
                time.sleep(1.5)
                aire.disminuir(1)
                self.vista.ventana.after(0, self._guardar_y_refrescar)

        t = threading.Thread(target=proceso);
        t.daemon = True;
        t.start()
        self.vista.mostrar_info("Smart", "Enfriando...")

    def accion_apagar_todo(self):
        if self.vista.pedir_confirmacion("Apagar Todo", "¿Seguro?"):
            for h in self.modelo_hub.get_habitaciones():
                for d in h.get_bombillas() + h.get_aires(): d.apagar()
            self._guardar_y_refrescar()

    def cargar_plano(self, r):
        self.modelo_hub.set_plano(r); self._guardar_y_refrescar()

    def quitar_plano(self):
        self.modelo_hub.set_plano(None); self._guardar_y_refrescar()

    def accion_salir(self):
        self.vista.ventana.destroy()

    def editar_consumo(self, d):
        w = self.vista.pedir_numero("Consumo", "Watios:", d.get_consumo_actual())
        if w: d.set_consumo_manual(w); self._guardar_y_refrescar()