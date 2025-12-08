import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog, colorchooser
from .libreriaDispositivo import Bombilla, AireAcondicionado, Persiana, Horno


class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, command=None, width=40, height=20, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.is_on = False
        self.bg_rect = self.create_rectangle(2, 2, width - 2, height - 2, fill="#555", outline="", width=0)
        self.create_arc(2, 2, height - 2, height - 2, start=90, extent=180, fill="#555", outline="")
        self.create_arc(width - height + 2, 2, width - 2, height - 2, start=-90, extent=180, fill="#555", outline="")
        self.knob = self.create_oval(4, 4, height - 4, height - 4, fill="white", outline="")
        self.bind("<Button-1>", self._toggle)

    def set_state(self, state):
        self.is_on = state
        bg = "#222" if self.is_on else "#999"
        x = self.winfo_reqwidth() - self.winfo_reqheight() + 4 if self.is_on else 4
        self.itemconfig(self.bg_rect, fill=bg)
        self.create_arc(2, 2, 18, 18, start=90, extent=180, fill=bg, outline="")
        self.create_arc(self.winfo_reqwidth() - 18, 2, self.winfo_reqwidth() - 2, 18, start=-90, extent=180, fill=bg,
                        outline="")
        r = self.winfo_reqheight() - 8
        self.coords(self.knob, x, 4, x + r, 4 + r)

    def _toggle(self, event=None):
        self.is_on = not self.is_on
        self.set_state(self.is_on)
        if self.command: self.command()


class VentanaPrincipal:
    def __init__(self, controlador):
        self._controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Casa piguino")
        self.ventana.geometry("1400x900")

        frame_top = tk.Frame(self.ventana, pady=15, bg="#f0f0f0")
        frame_top.pack(fill=tk.X)
        tk.Label(frame_top, text="🏠 LoloHouse", bg="#f0f0f0", fg="#333", font=("Helvetica", 16, "bold")).pack(
            side=tk.LEFT, padx=20)

        btn_s = {"bg": "#fff", "fg": "#333", "bd": 0, "padx": 10, "pady": 5, "relief": "flat"}
        tk.Button(frame_top, text="📂 Cargar", command=self.accion_cargar, **btn_s).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="➕ Habitación", command=self.accion_nueva_habitacion, **btn_s).pack(side=tk.LEFT,
                                                                                                      padx=5)
        tk.Button(frame_top, text="🗺️ Plano", command=self.accion_subir_plano, **btn_s).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="🗑️ Sin Plano", command=self.accion_quitar_plano, **btn_s).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_top, text="SALIR", bg="#333", fg="white", font=("Arial", 9, "bold"), bd=0, padx=15,
                  command=self.accion_salir).pack(side=tk.RIGHT, padx=20)
        self.lbl_consumo = tk.Label(frame_top, text="0 W", bg="#f0f0f0", fg="#555", font=("Arial", 12), padx=10)
        self.lbl_consumo.pack(side=tk.RIGHT, padx=10)

        self.canvas_plano = tk.Canvas(self.ventana, bg="#eef2f5", width=3000, height=3000, highlightthickness=0)
        hbar = tk.Scrollbar(self.ventana, orient=tk.HORIZONTAL, command=self.canvas_plano.xview)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        vbar = tk.Scrollbar(self.ventana, orient=tk.VERTICAL, command=self.canvas_plano.yview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_plano.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set, scrollregion=(0, 0, 3000, 3000))
        self.canvas_plano.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.canvas_plano.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas_plano.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas_plano.bind_all("<Button-5>", self._on_mousewheel)

        self._drag_data = {"x": 0, "y": 0, "item": None, "resizing": False}

    def iniciar(self):
        self.ventana.mainloop()

    def _on_mousewheel(self, e):
        if e.num == 5 or e.delta < 0:
            self.canvas_plano.yview_scroll(1, "units")
        elif e.num == 4 or e.delta > 0:
            self.canvas_plano.yview_scroll(-1, "units")

    def actualizar_etiqueta_consumo(self, w):
        self.lbl_consumo.config(text=f"{w} W")

    def construir_dashboard_visual(self, hub):
        self.canvas_plano.delete("all")
        if hub.get_plano():
            try:
                self.img_plano = tk.PhotoImage(file=hub.get_plano())
                self.canvas_plano.create_image(0, 0, image=self.img_plano, anchor="nw")
            except:
                pass
        for hab in hub.get_habitaciones(): self._dibujar_habitacion_redondeada(hab)

    def _dibujar_habitacion_redondeada(self, habitacion):
        x, y = habitacion.get_posicion()
        w, h = habitacion.get_dimensiones()
        bg_color = habitacion.get_color_fondo()

        tag_bg = f"bg_{id(habitacion)}"
        tag_group = f"group_{id(habitacion)}"

        # 1. Fondo
        self._create_rounded_rect(x, y, x + w, y + h, radius=20, fill=bg_color, outline="#ccc", width=1,
                                  tags=(tag_bg, tag_group))

        # 2. Frame
        frame_hab = tk.Frame(self.canvas_plano, bg=bg_color, width=w - 20, height=h - 20)
        frame_hab.pack_propagate(False)

        f_titulo = tk.Frame(frame_hab, bg=bg_color)
        f_titulo.pack(fill="x", pady=2)
        lbl_titulo = tk.Label(f_titulo, text=habitacion.get_descripcion(), bg=bg_color, fg="#333",
                              font=("Arial", 11, "bold"), cursor="fleur", anchor="w")
        lbl_titulo.pack(side="left", fill="x", expand=True)
        tk.Button(f_titulo, text="🎨", bd=0, bg=bg_color, cursor="hand2",
                  command=lambda h=habitacion: self._elegir_color_hab(h)).pack(side="right", padx=2)
        lbl_del = tk.Label(f_titulo, text="✖", bg=bg_color, fg="red", font=("Arial", 10, "bold"), cursor="hand2")
        lbl_del.pack(side="right", padx=5)
        lbl_del.bind("<Button-1>", lambda e, h=habitacion: self._controlador.eliminar_habitacion(h))

        canvas_int = tk.Canvas(frame_hab, bg=bg_color, highlightthickness=0)
        scroll_int = tk.Scrollbar(frame_hab, orient="vertical", command=canvas_int.yview)
        contenido = tk.Frame(canvas_int, bg=bg_color)
        contenido.bind("<Configure>", lambda e: canvas_int.configure(scrollregion=canvas_int.bbox("all")))
        win_int = canvas_int.create_window((0, 0), window=contenido, anchor="nw", width=w - 50)
        canvas_int.configure(yscrollcommand=scroll_int.set)
        canvas_int.pack(side="left", fill="both", expand=True)
        scroll_int.pack(side="right", fill="y")

        todos = habitacion.get_bombillas() + habitacion.get_aires()
        for disp in todos: self._dibujar_fila_dispositivo(contenido, disp, habitacion, bg_color)
        self._dibujar_form_add(contenido, habitacion, bg_color)

        # 3. Ventana en Canvas (Frame principal)
        # Importante: Añadimos tag_group
        win_frame = self.canvas_plano.create_window(x + 10, y + 10, window=frame_hab, anchor="nw", tags=tag_group)

        lbl_titulo.bind("<ButtonPress-1>", lambda e: self._start_drag(e, win_frame, tag_group))
        lbl_titulo.bind("<B1-Motion>", lambda e: self._do_drag(e, win_frame, tag_group))
        lbl_titulo.bind("<ButtonRelease-1>", lambda e: self._stop_drag(e, habitacion, win_frame))

        resizer = tk.Label(self.canvas_plano, text="⇲", bg=bg_color, fg="#555", cursor="sizing", font=("Arial", 14))
        win_resizer = self.canvas_plano.create_window(x + w - 15, y + h - 15, window=resizer, tags=tag_group)

        resizer.bind("<ButtonPress-1>", lambda e: self._start_resize(e, w, h))

        resizer.bind("<B1-Motion>",
                     lambda e: self._do_resize(e, habitacion, win_frame, tag_bg, win_resizer, frame_hab, canvas_int,
                                               win_int, bg_color))
        resizer.bind("<ButtonRelease-1>", lambda e: self._stop_resize(e, habitacion))

    def _dibujar_fila_dispositivo(self, padre, disp, habitacion, bg_hab):
        row = tk.Frame(padre, bg=bg_hab, pady=5)
        row.pack(fill="x", pady=2)
        f_head = tk.Frame(row, bg=bg_hab)
        f_head.pack(fill="x")

        icon = "💡"
        if isinstance(disp, AireAcondicionado):
            icon = "❄️"
        elif isinstance(disp, Persiana):
            icon = "🪟"
        elif isinstance(disp, Horno):
            icon = "🥘"

        tk.Button(f_head, text="⚙️", font=("Arial", 8), bd=0, bg=bg_hab,
                  command=lambda d=disp: self._controlador.editar_consumo(d)).pack(side="left")
        estado_txt = "ON" if disp.get_estado() else "OFF"
        if isinstance(disp, Persiana): estado_txt = "ABIERTO" if disp.get_estado() else "CERRADO"
        estado_bg = "#4CAF50" if disp.get_estado() else "#B0BEC5"
        tk.Label(f_head, text=estado_txt, bg=estado_bg, fg="white", font=("Arial", 7, "bold"), width=7).pack(
            side="left", padx=5)
        tk.Label(f_head, text=f"{icon} {disp.get_nombre()}", bg=bg_hab, font=("Segoe UI", 9, "bold")).pack(side="left",
                                                                                                           padx=5)
        tk.Button(f_head, text="🗑️", font=("Arial", 8), bd=0, bg=bg_hab, fg="red",
                  command=lambda d=disp, h=habitacion: self._controlador.eliminar_dispositivo(d, h)).pack(side="right")

        f_ctrl = tk.Frame(row, bg=bg_hab)
        f_ctrl.pack(fill="x", pady=2)

        t = ToggleSwitch(f_ctrl, width=30, height=16, command=lambda d=disp: self._controlador.toggle_dispositivo(d))
        t.set_state(disp.get_estado())
        t.pack(side="left")

        tk.Button(f_ctrl, text="⏱️", font=("Arial", 8), bd=0, bg=bg_hab,
                  command=lambda d=disp: self._mostrar_dialogo_timer_smart(d)).pack(side="left", padx=5)

        lbl_val = tk.Label(f_ctrl, text="", bg=bg_hab, font=("Arial", 8, "bold"), width=12, anchor="e")
        lbl_val.pack(side="right", padx=5)

        def _update_lbl(val):
            v_int = int(float(val))
            txt = f"{v_int}"
            if isinstance(disp, Bombilla):
                txt = f"Luz: {v_int}%"
            elif isinstance(disp, AireAcondicionado):
                txt = f"Aire: {v_int}ºC"
            elif isinstance(disp, Persiana):
                txt = f"Abierta: {v_int}%"
            elif isinstance(disp, Horno):
                txt = f"Horno: {v_int}ºC"
            lbl_val.config(text=txt)

        _update_lbl(disp.get_nivel())

        mx = 100;
        mn = 0
        if isinstance(disp, AireAcondicionado): mn = 16; mx = 30
        if isinstance(disp, Horno): mx = 250

        s = tk.Scale(f_ctrl, from_=mn, to=mx, orient="horizontal", showvalue=0, bg=bg_hab, bd=0, width=8,
                     troughcolor="#eee", command=_update_lbl)
        s.set(disp.get_nivel())
        s.bind("<ButtonRelease-1>", lambda e, d=disp, sc=s: self._controlador.cambiar_valor(d, sc.get()))
        s.pack(side="left", fill="x", expand=True)

        if isinstance(disp, Bombilla):
            col = disp.get_color();
            hex_c = '#%02x%02x%02x' % col
            tk.Label(f_ctrl, bg=hex_c, width=2, relief="solid", bd=1).pack(side="right", padx=2)
            tk.Button(f_ctrl, text="🎨", font=("Arial", 8), bd=0, bg=bg_hab,
                      command=lambda d=disp: self._elegir_color(d)).pack(side="right")
        elif isinstance(disp, AireAcondicionado):
            tk.Button(f_ctrl, text="🧠", font=("Arial", 8), bg=bg_hab, bd=0,
                      command=lambda d=disp: self._controlador.activar_enfriamiento_inteligente(d)).pack(side="right")

        ttk.Separator(padre, orient='horizontal').pack(fill='x', pady=5)

    def _dibujar_form_add(self, padre, habitacion, bg_hab):
        f = tk.Frame(padre, bg=bg_hab)
        f.pack(fill="x", pady=5)
        cb = ttk.Combobox(f, values=["Bombilla", "Aire", "Persiana", "Horno"], width=8, state="readonly");
        cb.current(0);
        cb.pack(side="left")
        en = tk.Entry(f, width=8);
        en.pack(side="left", padx=2)
        tk.Button(f, text="+", bg="#ddd", bd=0,
                  command=lambda: self._controlador.agregar_dispositivo(cb.get(), en.get(), habitacion)).pack(
            side="left")

    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2,
                  y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius,
                  y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1,
                  y1]
        return self.canvas_plano.create_polygon(points, **kwargs, smooth=True)

    def _mostrar_dialogo_timer_smart(self, disp):
        top = tk.Toplevel(self.ventana)
        top.title("Temporizador")
        top.geometry("280x180")
        accion = "Apagar" if disp.get_estado() else "Encender"
        if isinstance(disp, Persiana): accion = "Cerrar" if disp.get_estado() else "Abrir"
        tk.Label(top, text=f"¿Cuándo {accion} '{disp.get_nombre()}'?", font=("Arial", 10)).pack(pady=10)
        opciones = ["5 seg", "30 seg", "1 min", "5 min", "30 min", "1 hora", "20:00 (Hora)", "23:30 (Hora)"]
        combo = ttk.Combobox(top, values=opciones, width=20);
        combo.set("5 seg");
        combo.pack(pady=5)
        tk.Label(top, text="Escribe una hora (ej: 14:30) o selecciona tiempo", font=("Arial", 7), fg="gray").pack()
        tk.Button(top, text="ACTIVAR", bg="#4CAF50", fg="white",
                  command=lambda: [self._controlador.activar_temporizador_inteligente(disp, combo.get()),
                                   top.destroy()]).pack(pady=15)

    # --- MOVER ---
    def _start_drag(self, e, win_id, tag_group):
        self._drag_data["x"] = e.x_root;
        self._drag_data["y"] = e.y_root

    def _do_drag(self, e, win_id, tag_group):
        dx = e.x_root - self._drag_data["x"];
        dy = e.y_root - self._drag_data["y"]
        # MOVER SOLO EL GRUPO (que incluye fondo y resizer)
        self.canvas_plano.move(tag_group, dx, dy)
        # CORRECCIÓN: NO MOVER win_id AQUÍ porque ya está dentro del grupo o se mueve con él
        # PERO: Tkinter window items no siempre se mueven con tags.
        # Si ves que se separan, descomenta la siguiente línea:
        # self.canvas_plano.move(win_id, dx, dy)
        # En la versión anterior este era el bug (doble movimiento).
        # Si el frame tiene el tag_group, NO hay que moverlo explícitamente.
        self._drag_data["x"] = e.x_root;
        self._drag_data["y"] = e.y_root

    def _stop_drag(self, e, hab, win_id):
        x, y = self.canvas_plano.coords(win_id)
        self._controlador.mover_habitacion(hab, x - 10, y - 10)

    # --- RESIZE (CORREGIDO) ---
    def _start_resize(self, e, w, h):
        self._drag_data["resizing"] = True;
        self._drag_data["start_w"] = w;
        self._drag_data["start_h"] = h
        self._drag_data["start_x"] = e.x_root;
        self._drag_data["start_y"] = e.y_root

    def _do_resize(self, e, habitacion, win_frame, tag_bg, win_resizer, frame, canvas_int, win_int, bg_color):
        if not self._drag_data["resizing"]: return
        dx = e.x_root - self._drag_data["start_x"]
        dy = e.y_root - self._drag_data["start_y"]
        nw = max(250, self._drag_data["start_w"] + dx)
        nh = max(200, self._drag_data["start_h"] + dy)

        # 1. Obtener posición ACTUAL del frame (por si se ha movido)
        cur_coords = self.canvas_plano.coords(win_frame)
        if not cur_coords: return  # Seguridad
        cur_x, cur_y = cur_coords

        # El fondo empieza en (cur_x - 10, cur_y - 10)
        base_x = cur_x - 10
        base_y = cur_y - 10

        # 2. Borrar fondo viejo y crear nuevo en la posición correcta
        self.canvas_plano.delete(tag_bg)
        tag_group = f"group_{id(habitacion)}"
        self._create_rounded_rect(base_x, base_y, base_x + nw, base_y + nh, radius=20, fill=bg_color, outline="#ccc",
                                  width=1, tags=(tag_bg, tag_group))

        # 3. Mover Resizer
        self.canvas_plano.coords(win_resizer, base_x + nw - 15, base_y + nh - 15)

        # 4. Ajustar Frames
        frame.config(width=nw - 20, height=nh - 20)
        canvas_int.itemconfig(win_int, width=nw - 50)

        self._drag_data["last_w"] = nw
        self._drag_data["last_h"] = nh

    def _stop_resize(self, e, hab):
        if self._drag_data["resizing"]:
            self._drag_data["resizing"] = False
            w = self._drag_data.get("last_w", 300)
            h = self._drag_data.get("last_h", 300)
            self._controlador.redimensionar_habitacion(hab, w, h)

    # --- AUX ---
    def _elegir_color_hab(self, h):
        c = colorchooser.askcolor()[1]; self._controlador.cambiar_color_habitacion(h, c) if c else None

    def accion_nueva_habitacion(self):
        n = simpledialog.askstring("N", "Nombre:"); self._controlador.crear_habitacion(n) if n else None

    def accion_subir_plano(self):
        f = filedialog.askopenfilename(); self._controlador.cargar_plano(f) if f else None

    def accion_quitar_plano(self):
        self._controlador.quitar_plano()

    def accion_cargar(self):
        f = simpledialog.askstring("C", "Fichero:", initialvalue="datos_casa_v6.pkl"); self._controlador.cargar_datos(
            f) if f else None

    def accion_salir(self):
        self.ventana.destroy() if messagebox.askyesno("Salir", "¿Seguro que quieres cerrar la aplicación?") else None

    def mostrar_info(self, t, m):
        messagebox.showinfo(t, m)

    def mostrar_error(self, t, m):
        messagebox.showerror(t, m)

    def pedir_confirmacion(self, t, m):
        return messagebox.askyesno(t, m)

    def pedir_numero(self, t, m, i):
        return simpledialog.askinteger(t, m, initialvalue=i)

    def _elegir_color(self, b):
        c = colorchooser.askcolor()[0]; self._controlador.cambiar_color(b, (int(c[0]), int(c[1]),
                                                                            int(c[2]))) if c else None