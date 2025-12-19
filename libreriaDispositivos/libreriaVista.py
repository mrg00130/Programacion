import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog, colorchooser
from .libreriaDispositivo import Bombilla, AireAcondicionado, Persiana, Horno


class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, command=None, width=44, height=24, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.is_on = False
        self.color_off = "#E0E0E0";
        self.color_on = "#4CD964";
        self.color_border = "#D1D1D1"
        self.bg_rect = self.create_rectangle(2, 2, width - 2, height - 2, fill=self.color_off,
                                             outline=self.color_border, width=1)
        self.create_arc(2, 2, height - 2, height - 2, start=90, extent=180, fill=self.color_off,
                        outline=self.color_border, style=tk.CHORD)
        self.create_arc(width - height + 2, 2, width - 2, height - 2, start=-90, extent=180, fill=self.color_off,
                        outline=self.color_border, style=tk.CHORD)
        self.knob = self.create_oval(4, 4, height - 4, height - 4, fill="white", outline="#CCCCCC")
        self.bind("<Button-1>", self._toggle)

    def set_state(self, state):
        self.is_on = state
        color = self.color_on if self.is_on else self.color_off
        x = self.winfo_reqwidth() - self.winfo_reqheight() + 4 if self.is_on else 4
        self.itemconfig(self.bg_rect, fill=color, outline=color)
        self.create_arc(2, 2, 22, 22, start=90, extent=180, fill=color, outline=color)
        self.create_arc(self.winfo_reqwidth() - 22, 2, self.winfo_reqwidth() - 2, 22, start=-90, extent=180, fill=color,
                        outline=color)
        r = self.winfo_reqheight() - 8
        self.coords(self.knob, x, 4, x + r, 4 + r)
        self.tag_raise(self.knob)

    def _toggle(self, event=None):
        self.is_on = not self.is_on
        self.set_state(self.is_on)
        if self.command: self.command()


class VentanaPrincipal:
    def __init__(self, controlador):
        self._controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Lolo house v0.98 - Pastel Edition")
        self.ventana.geometry("1400x900")
        self.ventana.protocol("WM_DELETE_WINDOW", self.accion_salir)

        self._cache_widgets = {}

        frame_top = tk.Frame(self.ventana, pady=8, bg="#2c3e50")
        frame_top.pack(fill=tk.X)
        tk.Label(frame_top, text="🏠 Lolo House", bg="#2c3e50", fg="white", font=("Segoe UI", 16, "bold")).pack(
            side=tk.LEFT, padx=20)
        tk.Label(frame_top, text="v0.98", bg="#2c3e50", fg="#95a5a6", font=("Arial", 9)).pack(side=tk.LEFT, pady=5)

        btn_s = {"bg": "#34495e", "fg": "white", "bd": 0, "padx": 12, "pady": 5, "relief": "flat",
                 "activebackground": "#1abc9c"}
        tk.Button(frame_top, text="📂 Cargar", command=self.accion_cargar, **btn_s).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="➕ Habitación", command=self.accion_nueva_habitacion, **btn_s).pack(side=tk.LEFT,
                                                                                                      padx=5)
        tk.Button(frame_top, text="🗺️ Plano", command=self.accion_subir_plano, **btn_s).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="🗑️ Sin Plano", command=self.accion_quitar_plano, **btn_s).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_top, text="SALIR", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), bd=0, padx=15,
                  command=self.accion_salir).pack(side=tk.RIGHT, padx=20)
        self.lbl_consumo = tk.Label(frame_top, text="0 W", bg="#2c3e50", fg="#f1c40f", font=("Consolas", 14, "bold"),
                                    padx=10)
        self.lbl_consumo.pack(side=tk.RIGHT, padx=10)

        self.canvas_plano = tk.Canvas(self.ventana, bg="#ecf0f1", width=3000, height=3000, highlightthickness=0)
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
        self.lbl_consumo.config(text=f"⚡ {w} W")

    def construir_dashboard_visual(self, hub):
        self.canvas_plano.delete("all")
        self._cache_widgets = {}
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
        tag_bg = f"bg_{id(habitacion)}";
        tag_group = f"group_{id(habitacion)}"

        self._create_rounded_rect(x + 4, y + 4, x + w + 4, y + h + 4, radius=20, fill="#CCCCCC", outline="",
                                  tags=(tag_bg, tag_group))
        self._create_rounded_rect(x, y, x + w, y + h, radius=20, fill=bg_color, outline="#bdc3c7", width=1,
                                  tags=(tag_bg, tag_group))

        frame_hab = tk.Frame(self.canvas_plano, bg=bg_color, width=w - 20, height=h - 20)
        frame_hab.pack_propagate(False)

        f_titulo = tk.Frame(frame_hab, bg=bg_color)
        f_titulo.pack(fill="x", pady=5)
        lbl_titulo = tk.Label(f_titulo, text=habitacion.get_descripcion(), bg=bg_color, fg="#2c3e50",
                              font=("Segoe UI", 12, "bold"), cursor="fleur", anchor="w")
        lbl_titulo.pack(side="left", fill="x", expand=True, padx=5)

        tk.Button(f_titulo, text="🎨", bd=0, bg=bg_color, cursor="hand2", font=("Segoe UI", 10),
                  command=lambda h=habitacion: self._mostrar_paleta_colores(h)).pack(side="right", padx=2)

        lbl_del = tk.Label(f_titulo, text="✖", bg=bg_color, fg="#e74c3c", font=("Arial", 12, "bold"), cursor="hand2")
        lbl_del.pack(side="right", padx=8)
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

        win_frame = self.canvas_plano.create_window(x + 10, y + 10, window=frame_hab, anchor="nw", tags=tag_group)

        lbl_titulo.bind("<ButtonPress-1>",
                        lambda e: [self.canvas_plano.tag_raise(tag_group), self._start_drag(e, win_frame, tag_group)])
        lbl_titulo.bind("<B1-Motion>", lambda e: self._do_drag(e, win_frame, tag_group, habitacion))
        lbl_titulo.bind("<ButtonRelease-1>", lambda e: self._stop_drag(e, habitacion, win_frame))

        resizer = tk.Label(self.canvas_plano, text="⇲", bg=bg_color, fg="#95a5a6", cursor="sizing", font=("Arial", 16))
        win_resizer = self.canvas_plano.create_window(x + w - 15, y + h - 15, window=resizer, tags=tag_group)
        resizer.bind("<ButtonPress-1>", lambda e: [self.canvas_plano.tag_raise(tag_group), self._start_resize(e, w, h)])
        resizer.bind("<B1-Motion>",
                     lambda e: self._do_resize(e, habitacion, win_frame, tag_bg, win_resizer, frame_hab, canvas_int,
                                               win_int, bg_color))
        resizer.bind("<ButtonRelease-1>", lambda e: self._stop_resize(e, habitacion))

    def _dibujar_fila_dispositivo(self, padre, disp, habitacion, bg_hab):
        row = tk.Frame(padre, bg=bg_hab, pady=8, padx=2)
        row.pack(fill="x")
        f_head = tk.Frame(row, bg=bg_hab)
        f_head.pack(fill="x")

        icono_char = "❓";
        color_badge = "#95a5a6";
        etiqueta_barra = "Nivel"
        if isinstance(disp, Bombilla):
            icono_char = "💡"; color_badge = "#f1c40f"; etiqueta_barra = "Brillo"
        elif isinstance(disp, AireAcondicionado):
            icono_char = "❄️"; color_badge = "#3498db"; etiqueta_barra = "Temp"
        elif isinstance(disp, Persiana):
            icono_char = "🪟"; color_badge = "#9b59b6"; etiqueta_barra = "Apertura"
        elif isinstance(disp, Horno):
            icono_char = "🥘"; color_badge = "#e67e22"; etiqueta_barra = "Horno"

        tk.Button(f_head, text="⚙️", font=("Segoe UI", 8), bd=0, bg=bg_hab, cursor="hand2",
                  command=lambda d=disp: self._controlador.editar_consumo(d)).pack(side="left")
        lbl_icon = tk.Label(f_head, text=icono_char, bg=color_badge, fg="white", font=("Segoe UI Emoji", 12), width=3)
        lbl_icon.pack(side="left", padx=5)
        tk.Label(f_head, text=disp.get_nombre(), bg=bg_hab, font=("Segoe UI", 10, "bold"), fg="#333").pack(side="left")
        tk.Button(f_head, text="🗑️", font=("Segoe UI", 9), bd=0, bg=bg_hab, fg="#e74c3c", cursor="hand2",
                  command=lambda d=disp, h=habitacion: self._controlador.eliminar_dispositivo(d, h)).pack(side="right")

        f_ctrl = tk.Frame(row, bg=bg_hab)
        f_ctrl.pack(fill="x", pady=4)

        t = ToggleSwitch(f_ctrl, width=44, height=24, command=lambda d=disp: self._controlador.toggle_dispositivo(d))
        t.set_state(disp.get_estado())
        t.pack(side="left", padx=2)

        btn_timer = tk.Button(f_ctrl, text="⏱️ Prog.", font=("Segoe UI", 8), bg="#ecf0f1", fg="#2c3e50", bd=0,
                              relief="solid", cursor="hand2",
                              command=lambda d=disp: self._mostrar_dialogo_timer_smart(d))
        btn_timer.pack(side="left", padx=8)

        tk.Label(f_ctrl, text=etiqueta_barra + ":", bg=bg_hab, font=("Segoe UI", 7, "bold"), fg="black").pack(
            side="left")

        lbl_val = tk.Label(f_head, text="", bg=bg_hab, font=("Segoe UI", 9, "underline"), fg="#2980b9", cursor="hand2",
                           anchor="e")
        lbl_val.pack(side="right", padx=5)
        lbl_val.bind("<Button-1>", lambda e, d=disp: self._pedir_valor_manual(d))

        def _update_lbl(val):
            v_int = int(float(val))
            txt = f"{v_int}"
            if isinstance(disp, Bombilla):
                txt = f"{v_int}%"
            elif isinstance(disp, AireAcondicionado):
                txt = f"{v_int}ºC"
            elif isinstance(disp, Persiana):
                txt = f"{v_int}%"
            elif isinstance(disp, Horno):
                txt = f"{v_int}ºC"
            lbl_val.config(text=txt)

        _update_lbl(disp.get_nivel())

        mx = 100;
        mn = 0
        if isinstance(disp, AireAcondicionado): mn = 16; mx = 30
        if isinstance(disp, Horno): mx = 250

        s = tk.Scale(f_ctrl, from_=mn, to=mx, orient="horizontal", showvalue=0, bg=bg_hab, bd=0, width=10,
                     troughcolor="#ecf0f1", activebackground="#bdc3c7", highlightthickness=0, command=_update_lbl)
        s.set(disp.get_nivel())
        s.bind("<ButtonRelease-1>", lambda e, d=disp, sc=s: self._controlador.cambiar_valor(d, sc.get()))
        s.pack(side="left", fill="x", expand=True, padx=5)

        self._cache_widgets[id(disp)] = (lbl_val, s)

        if isinstance(disp, Bombilla):
            col = disp.get_color();
            hex_c = '#%02x%02x%02x' % col
            tk.Label(f_ctrl, bg=hex_c, width=2, relief="ridge", bd=1).pack(side="right", padx=2)
            tk.Button(f_ctrl, text="🎨", font=("Arial", 9), bd=0, bg=bg_hab, cursor="hand2",
                      command=lambda d=disp: self._elegir_color(d)).pack(side="right")
        elif isinstance(disp, AireAcondicionado):
            tk.Button(f_ctrl, text="❄️ Clima", font=("Segoe UI", 8), bg="#d6eaf8", bd=0, cursor="hand2",
                      command=lambda d=disp: self._pedir_temp_clima(d)).pack(side="right")

        ttk.Separator(padre, orient='horizontal').pack(fill='x', pady=2)

    def _mostrar_paleta_colores(self, habitacion):
        top = tk.Toplevel(self.ventana)
        top.title("Color Habitación")
        top.geometry("260x220")
        top.resizable(False, False)

        tk.Label(top, text="Selecciona un tono pastel:", font=("Segoe UI", 10, "bold")).pack(pady=5)

        frame_cols = tk.Frame(top)
        frame_cols.pack(padx=10, pady=5)

        colores = [
            "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
            "#E6E6FA", "#F0F8FF", "#F5F5DC", "#FFE4E1", "#FFF0F5",
            "#E0FFFF", "#FAFAD2", "#D3D3D3", "#FFC0CB", "#D8BFD8"
        ]

        r = 0;
        c = 0
        for col in colores:
            btn = tk.Button(frame_cols, bg=col, width=4, height=2, relief="ridge",
                            command=lambda c=col: [self._controlador.cambiar_color_habitacion(habitacion, c),
                                                   top.destroy()])
            btn.grid(row=r, column=c, padx=3, pady=3)
            c += 1
            if c > 4:
                c = 0;
                r += 1

        tk.Button(top, text="Color Específico...", font=("Segoe UI", 8),
                  command=lambda: [self._elegir_color_hab(habitacion), top.destroy()]).pack(pady=10)

    def actualizar_widget_individual(self, disp):
        if id(disp) in self._cache_widgets:
            lbl, slider = self._cache_widgets[id(disp)]
            val = disp.get_nivel()
            slider.set(val)
            txt = f"{val}"
            if isinstance(disp, Bombilla):
                txt = f"{val}%"
            elif isinstance(disp, AireAcondicionado):
                txt = f"{val}ºC"
            elif isinstance(disp, Persiana):
                txt = f"{val}%"
            elif isinstance(disp, Horno):
                txt = f"{val}ºC"
            lbl.config(text=txt)

    def _pedir_valor_manual(self, disp):
        act = disp.get_nivel()
        nuevo = simpledialog.askinteger("Valor Manual", f"Introduce valor para {disp.get_nombre()}:", initialvalue=act)
        if nuevo is not None:
            self._controlador.cambiar_valor(disp, nuevo)
            self.actualizar_widget_individual(disp)

    def _pedir_temp_clima(self, aire):
        temp = simpledialog.askinteger("Climatización", f"¿Temperatura deseada para {aire.get_nombre()}?", minvalue=16,
                                       maxvalue=30, initialvalue=21)
        if temp: self._controlador.simular_climatizacion(aire, temp)

    def _dibujar_form_add(self, padre, habitacion, bg_hab):
        f = tk.Frame(padre, bg=bg_hab, pady=5);
        f.pack(fill="x")
        style = ttk.Style();
        style.theme_use('clam');
        style.configure("TCombobox", fieldbackground="white", background="#ecf0f1")
        cb = ttk.Combobox(f, values=["Bombilla", "Aire", "Persiana", "Horno"], width=10, state="readonly");
        cb.current(0);
        cb.pack(side="left", padx=2)
        en = tk.Entry(f, width=12, relief="solid", bd=1);
        en.pack(side="left", padx=2)
        accion_add = lambda: self._controlador.agregar_dispositivo(cb.get(), en.get(), habitacion)
        tk.Button(f, text="➕ Añadir", bg="#2ecc71", fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=5,
                  cursor="hand2", command=accion_add).pack(side="left", padx=5)
        en.bind("<Return>", lambda event: accion_add())

    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2,
                  y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius,
                  y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1,
                  y1]
        return self.canvas_plano.create_polygon(points, **kwargs, smooth=True)

    def _mostrar_dialogo_timer_smart(self, disp):
        top = tk.Toplevel(self.ventana)
        top.title("Programar")
        top.geometry("280x180");
        top.configure(bg="white")
        accion = "Apagar" if disp.get_estado() else "Encender"
        if isinstance(disp, Persiana): accion = "Cerrar" if disp.get_estado() else "Abrir"
        tk.Label(top, text=f"Programar {accion} '{disp.get_nombre()}'", font=("Segoe UI", 11, "bold"), bg="white",
                 fg="#2c3e50").pack(pady=10)
        opciones = ["5 seg", "30 seg", "1 min", "5 min", "30 min", "1 hora", "20:00 (Hora)", "23:30 (Hora)"]
        combo = ttk.Combobox(top, values=opciones, width=22);
        combo.set("5 seg");
        combo.pack(pady=5)
        tk.Label(top, text="Ejemplo: '5 min' o '18:30'", font=("Segoe UI", 8), fg="gray", bg="white").pack()
        tk.Button(top, text="ACTIVAR TEMPORIZADOR", bg="#3498db", fg="white", font=("Segoe UI", 9, "bold"), bd=0,
                  padx=10, pady=5, cursor="hand2",
                  command=lambda: [self._controlador.activar_temporizador_inteligente(disp, combo.get()),
                                   top.destroy()]).pack(pady=15)

    def _verificar_colision(self, box_propuesto, habitacion_actual):
        x1, y1, x2, y2 = box_propuesto
        pad = 5
        x1 += pad;
        y1 += pad;
        x2 -= pad;
        y2 -= pad
        for hab in self._controlador.modelo_hub.get_habitaciones():
            if hab == habitacion_actual: continue
            hx, hy = hab.get_posicion()
            hw, hh = hab.get_dimensiones()
            hx2, hy2 = hx + hw, hy + hh
            no_solapa = (x2 < hx) or (x1 > hx2) or (y2 < hy) or (y1 > hy2)
            if not no_solapa: return True
        return False

    def _start_drag(self, e, win_id, tag_group):
        self._drag_data["x"] = e.x_root;
        self._drag_data["y"] = e.y_root

    def _do_drag(self, e, win_id, tag_group, habitacion):
        dx = e.x_root - self._drag_data["x"];
        dy = e.y_root - self._drag_data["y"]
        coords = self.canvas_plano.coords(win_id)
        cur_x, cur_y = coords[0], coords[1]
        real_x = cur_x - 10;
        real_y = cur_y - 10
        w, h = habitacion.get_dimensiones()
        futura_x = real_x + dx;
        futura_y = real_y + dy
        if futura_y < 50: return
        if futura_x < 0: return
        box_actual = (real_x, real_y, real_x + w, real_y + h)
        box_futuro = (futura_x, futura_y, futura_x + w, futura_y + h)
        choca_ahora = self._verificar_colision(box_actual, habitacion)
        choca_futuro = self._verificar_colision(box_futuro, habitacion)
        if not choca_ahora and choca_futuro: return
        self.canvas_plano.move(tag_group, dx, dy)
        self._drag_data["x"] = e.x_root;
        self._drag_data["y"] = e.y_root

    def _stop_drag(self, e, hab, win_id):
        x, y = self.canvas_plano.coords(win_id)
        self._controlador.mover_habitacion(hab, x - 10, y - 10)

    def _start_resize(self, e, w, h):
        self._drag_data["resizing"] = True;
        self._drag_data["start_w"] = w;
        self._drag_data["start_h"] = h
        self._drag_data["start_x"] = e.x_root;
        self._drag_data["start_y"] = e.y_root

    def _do_resize(self, e, habitacion, win_frame, tag_bg, win_resizer, frame, canvas_int, win_int, bg_color):
        if not self._drag_data["resizing"]: return
        dx = e.x_root - self._drag_data["start_x"];
        dy = e.y_root - self._drag_data["start_y"]
        nw = max(250, self._drag_data["start_w"] + dx);
        nh = max(200, self._drag_data["start_h"] + dy)
        coords = self.canvas_plano.coords(win_frame)
        if not coords: return
        cur_x, cur_y = coords;
        base_x = cur_x - 10;
        base_y = cur_y - 10
        box_actual = (base_x, base_y, base_x + self._drag_data["start_w"], base_y + self._drag_data["start_h"])
        box_futuro = (base_x, base_y, base_x + nw, base_y + nh)
        choca_ahora = self._verificar_colision(box_actual, habitacion)
        choca_futuro = self._verificar_colision(box_futuro, habitacion)
        if not choca_ahora and choca_futuro: return
        self.canvas_plano.delete(tag_bg)
        tag_group = f"group_{id(habitacion)}"
        self._create_rounded_rect(base_x + 4, base_y + 4, base_x + nw + 4, base_y + nh + 4, radius=20, fill="#CCCCCC",
                                  outline="", tags=(tag_bg, tag_group))
        self._create_rounded_rect(base_x, base_y, base_x + nw, base_y + nh, radius=20, fill=bg_color, outline="#bdc3c7",
                                  width=1, tags=(tag_bg, tag_group))
        self.canvas_plano.coords(win_resizer, base_x + nw - 15, base_y + nh - 15)
        frame.config(width=nw - 20, height=nh - 20)
        canvas_int.itemconfig(win_int, width=nw - 50)
        self._drag_data["last_w"] = nw;
        self._drag_data["last_h"] = nh

    def _stop_resize(self, e, hab):
        if self._drag_data["resizing"]:
            self._drag_data["resizing"] = False
            w = self._drag_data.get("last_w", 300);
            h = self._drag_data.get("last_h", 300)
            self._controlador.redimensionar_habitacion(hab, w, h)

    def accion_cargar(self):
        f = filedialog.askopenfilename(title="Cargar Hogar", filetypes=[("Archivos PKL", "*.pkl"), ("Todos", "*.*")])
        if f: self._controlador.cargar_datos(f)

    def accion_salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que quieres cerrar la aplicación?"):
            self._controlador.accion_salir();
            try:
                self.ventana.destroy()
            except:
                pass

    def _elegir_color_hab(self, h):
        c = colorchooser.askcolor()[1]; self._controlador.cambiar_color_habitacion(h, c) if c else None

    def accion_nueva_habitacion(self):
        n = simpledialog.askstring("N", "Nombre:"); self._controlador.crear_habitacion(n) if n else None

    def accion_subir_plano(self):
        f = filedialog.askopenfilename(); self._controlador.cargar_plano(f) if f else None

    def accion_quitar_plano(self):
        self._controlador.quitar_plano()

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