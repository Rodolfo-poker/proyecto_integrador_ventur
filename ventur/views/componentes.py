"""Widgets reutilizables: botón, píldora, tarjeta, campo de texto, selector, aviso y tarjeta de módulo."""
import tkinter as tk
from tkinter import font as tkfont

from . import tema


def _fondo_de(parent):
    try:
        return parent.cget("bg")
    except tk.TclError:
        return tema.FONDO


class Boton(tk.Canvas):
    """Botón con esquinas redondeadas (tamaño fijo, como en los mockups)."""

    # estilo: (fondo, texto, borde, fondo al pasar el mouse)
    ESTILOS = {
        "primario": (tema.TINTA, tema.BLANCO, None, tema.BOTON_PRIMARIO_HOVER),
        "secundario": (tema.TARJETA, tema.TINTA, tema.TINTA, tema.FONDO),
        "peligro": (tema.TARJETA, tema.ROJO, tema.ROJO, "#FEF2F2"),
        "campo": (tema.TARJETA, tema.TINTA, tema.CAMPO_BORDE, tema.FONDO),
    }

    def __init__(self, parent, texto, comando, estilo="primario", ancho=None, alto=44,
                 tamano=16, radio=6):
        self._tamano = tamano
        if ancho is None:
            medidor = tkfont.Font(family=tema.FAMILIA, size=-tamano, weight="bold")
            ancho = medidor.measure(texto) + 48
        super().__init__(parent, width=ancho, height=alto, bg=_fondo_de(parent),
                         highlightthickness=0, bd=0, cursor="hand2", takefocus=True)
        self._ancho, self._alto = ancho, alto
        self._texto = texto
        self._comando = comando
        self._estilo = estilo
        self._radio = radio
        self._activo = False

        self.bind("<Enter>", lambda _e: self._marcar(True))
        self.bind("<Leave>", lambda _e: self._marcar(False))
        self.bind("<FocusIn>", lambda _e: self._marcar(True))
        self.bind("<FocusOut>", lambda _e: self._marcar(False))
        self.bind("<Button-1>", lambda _e: self._comando())
        self.bind("<Return>", lambda _e: self._comando())
        self.bind("<space>", lambda _e: self._comando())
        self._dibujar()

    def poner_texto(self, texto):
        self._texto = texto
        self._dibujar()

    def _marcar(self, activo):
        self._activo = activo
        self._dibujar()

    def _dibujar(self):
        self.delete("all")
        fondo, color, borde, hover = self.ESTILOS[self._estilo]
        tema.rect_redondeado(
            self, 2, 2, self._ancho - 2, self._alto - 2, self._radio,
            fill=hover if self._activo else fondo,
            outline=borde or (hover if self._activo else fondo),
            width=2 if borde else 1)
        self.create_text(self._ancho / 2, self._alto / 2, text=self._texto, fill=color,
                         font=tema.fuente(self._tamano, "bold"))


class Pildora(tk.Canvas):
    """Etiqueta redonda (estado de producto, insignias)."""

    def __init__(self, parent, texto, fondo, color, tamano=14, alto=28, relleno=32):
        medidor = tkfont.Font(family=tema.FAMILIA, size=-tamano, weight="bold")
        ancho = medidor.measure(texto) + relleno
        super().__init__(parent, width=ancho, height=alto, bg=_fondo_de(parent),
                         highlightthickness=0, bd=0)
        tema.rect_redondeado(self, 1, 1, ancho - 1, alto - 1, alto // 2 - 1,
                             fill=fondo, outline=fondo)
        self.create_text(ancho / 2, alto / 2, text=texto, fill=color,
                         font=tema.fuente(tamano, "bold"))


class TarjetaRedondeada(tk.Canvas):
    """Recuadro blanco con borde y esquinas redondeadas. Se dibuja dentro de .interior"""

    def __init__(self, parent, radio=8, relleno=tema.TARJETA, borde=tema.BORDE, **opciones):
        super().__init__(parent, bg=_fondo_de(parent), highlightthickness=0, bd=0, **opciones)
        self._radio, self._relleno, self._borde = radio, relleno, borde
        self._margen = int(radio * 0.3) + 2   # para no tapar las esquinas redondeadas
        self.interior = tk.Frame(self, bg=relleno)
        self._ventana = self.create_window(self._margen, self._margen,
                                           window=self.interior, anchor="nw")
        self.bind("<Configure>", self._redibujar)

    def _redibujar(self, evento):
        self.delete("fondo")
        tema.rect_redondeado(self, 1, 1, evento.width - 1, evento.height - 1, self._radio,
                             fill=self._relleno, outline=self._borde, tags="fondo")
        self.tag_lower("fondo")
        self.itemconfigure(self._ventana, width=max(1, evento.width - 2 * self._margen),
                           height=max(1, evento.height - 2 * self._margen))


class Aviso(tk.Frame):
    """Franja de aviso (roja = error, amarilla = advertencia). Ocupa 0 de alto si está oculta."""

    ESTILOS = {
        "error": (tema.ERROR_FONDO, tema.ERROR_BORDE, tema.ERROR_TEXTO),
        "aviso": (tema.AVISO_FONDO, tema.AVISO_BORDE, tema.AVISO_TEXTO),
    }

    def __init__(self, parent, espacio_abajo=16, wraplength=0):
        super().__init__(parent, bg=_fondo_de(parent))
        self._espacio = espacio_abajo
        self._caja = tk.Frame(self, highlightthickness=1)
        self._etiqueta = tk.Label(self._caja, anchor="w", justify="left",
                                  font=tema.fuente(15, "bold"), padx=20, pady=13,
                                  wraplength=wraplength)
        self._caja.bind("<Configure>", lambda e: self._etiqueta.config(
            wraplength=max(100, e.width - 44)))

    def mostrar(self, texto, tipo="error"):
        fondo, borde, color = self.ESTILOS[tipo]
        self._caja.config(bg=fondo, highlightbackground=borde, highlightcolor=borde)
        self._etiqueta.config(text=texto, bg=fondo, fg=color)
        self._caja.pack(fill="x", pady=(0, self._espacio))
        self._etiqueta.pack(fill="x")

    def ocultar(self):
        self._caja.pack_forget()


class Campo(tk.Canvas):
    """Campo de texto de 48 px con borde redondeado, texto de ejemplo y lupa opcional.

    Lee el texto con .valor() (devuelve "" si solo se está viendo el texto de ejemplo).
    """

    ALTO = 48

    def __init__(self, parent, placeholder="", buscador=False, oculto=False,
                 solo_lectura=False, al_cambiar=None, ancho=200):
        self._fondo = tema.CAMPO_SOLO_LECTURA if solo_lectura else tema.TARJETA
        super().__init__(parent, width=ancho, height=self.ALTO, bg=_fondo_de(parent),
                         highlightthickness=0, bd=0)
        self._placeholder = placeholder
        self._buscador = buscador
        self._oculto = oculto
        self._solo_lectura = solo_lectura
        self._al_cambiar = al_cambiar
        self._enfocado = False
        self._ph_activo = False     # se está mostrando el texto de ejemplo
        self._interno = False       # cambios hechos por nosotros (no avisar)
        self._visible = False       # contraseña visible

        self._izq = 48 if buscador else 16
        self._der = 16
        if oculto:
            medidor = tkfont.Font(family=tema.FAMILIA, size=-14, weight="bold")
            self._der = 16 + max(medidor.measure("Mostrar"), medidor.measure("Ocultar")) + 8

        self._variable = tk.StringVar()
        self.entrada = tk.Entry(
            self, textvariable=self._variable, font=tema.fuente(16), relief="flat", bd=0,
            highlightthickness=0, bg=self._fondo, fg=tema.TINTA, insertbackground=tema.TINTA,
            readonlybackground=self._fondo)
        self._ventana = self.create_window(self._izq, self.ALTO / 2,
                                           window=self.entrada, anchor="w")
        self._ver = None
        if oculto:
            self._ver = self.create_text(0, self.ALTO / 2, text="Mostrar", anchor="e",
                                         fill=tema.TINTA, font=tema.fuente(14, "bold"),
                                         tags="ver")
            self.tag_bind("ver", "<Button-1>", lambda _e: self._alternar_visible())
            self.tag_bind("ver", "<Enter>", lambda _e: self.config(cursor="hand2"))
            self.tag_bind("ver", "<Leave>", lambda _e: self.config(cursor=""))

        self.bind("<Configure>", lambda _e: self._dibujar())
        self.bind("<Button-1>", lambda _e: self.entrada.focus_set())
        self.entrada.bind("<FocusIn>", self._al_enfocar)
        self.entrada.bind("<FocusOut>", self._al_desenfocar)
        self._variable.trace_add("write", self._cambio)
        if solo_lectura:
            self.entrada.config(state="readonly")
        self._mostrar_ph()

    # ---- API ----
    def valor(self):
        return "" if self._ph_activo else self._variable.get()

    def establecer(self, texto):
        self._ocultar_ph()
        self._interno = True
        self._variable.set(texto)
        self._interno = False
        if not texto and not self._enfocado:
            self._mostrar_ph()

    def limpiar(self):
        self.establecer("")

    def enfocar(self):
        self.entrada.focus_set()

    def enlazar_enter(self, funcion):
        self.entrada.bind("<Return>", lambda _e: funcion())

    # ---- Interno ----
    def _cambio(self, *_):
        if not self._interno and self._al_cambiar:
            self._al_cambiar(self.valor())

    def _mostrar_ph(self):
        if (self._ph_activo or self._solo_lectura or not self._placeholder
                or self._variable.get()):
            return
        self._ph_activo = True
        self._interno = True
        self.entrada.config(fg=tema.CAMPO_BORDE, show="")
        self._variable.set(self._placeholder)
        self._interno = False

    def _ocultar_ph(self):
        if not self._ph_activo:
            return
        self._interno = True
        self._variable.set("")
        self._interno = False
        self._ph_activo = False
        self.entrada.config(fg=tema.TINTA, show=self._caracter_oculto())

    def _caracter_oculto(self):
        return "•" if self._oculto and not self._visible else ""

    def _alternar_visible(self):
        self._visible = not self._visible
        self.itemconfigure(self._ver, text="Ocultar" if self._visible else "Mostrar")
        if not self._ph_activo:
            self.entrada.config(show=self._caracter_oculto())

    def _al_enfocar(self, _evento):
        self._enfocado = True
        self._ocultar_ph()
        self._dibujar()

    def _al_desenfocar(self, _evento):
        self._enfocado = False
        self._mostrar_ph()
        self._dibujar()

    def _dibujar(self):
        w, h = self.winfo_width(), self.ALTO
        if w < 20:
            return
        self.delete("borde")
        tema.rect_redondeado(
            self, 2, 2, w - 2, h - 2, 6, fill=self._fondo, tags="borde",
            outline=tema.TINTA if self._enfocado else tema.CAMPO_BORDE,
            width=2 if self._enfocado else 1)
        if self._buscador:   # lupa
            self.create_oval(16, h / 2 - 10, 32, h / 2 + 6, outline=tema.CAMPO_BORDE,
                             width=2, tags="borde")
            self.create_line(30, h / 2 + 4, 37, h / 2 + 11, fill=tema.CAMPO_BORDE,
                             width=2, tags="borde")
        self.tag_lower("borde")
        self.coords(self._ventana, self._izq, h / 2)
        self.itemconfigure(self._ventana, width=max(10, w - self._izq - self._der))
        if self._ver is not None:
            self.coords(self._ver, w - 16, h / 2)


class Selector(tk.Canvas):
    """Lista desplegable con el aspecto de los mockups."""

    ALTO = 48

    def __init__(self, parent, opciones, valor, al_cambiar=None, ancho=220):
        super().__init__(parent, width=ancho, height=self.ALTO, bg=_fondo_de(parent),
                         highlightthickness=0, bd=0, cursor="hand2", takefocus=True)
        self._opciones = list(opciones)
        self._valor = valor
        self._al_cambiar = al_cambiar
        self._activo = False
        self.bind("<Configure>", lambda _e: self._dibujar())
        self.bind("<Button-1>", lambda _e: self._abrir())
        self.bind("<Return>", lambda _e: self._abrir())
        self.bind("<space>", lambda _e: self._abrir())
        self.bind("<Enter>", lambda _e: self._marcar(True))
        self.bind("<Leave>", lambda _e: self._marcar(False))
        self.bind("<FocusIn>", lambda _e: self._marcar(True))
        self.bind("<FocusOut>", lambda _e: self._marcar(False))

    @property
    def valor(self):
        return self._valor

    def establecer_opciones(self, opciones):
        """Cambia las opciones; si el valor actual ya no existe, elige la primera."""
        self._opciones = list(opciones)
        if self._valor not in self._opciones and self._opciones:
            self._valor = self._opciones[0]
        self._dibujar()

    def _marcar(self, activo):
        self._activo = activo
        self._dibujar()

    def _dibujar(self):
        w, h = self.winfo_width(), self.ALTO
        if w < 20:
            return
        self.delete("all")
        tema.rect_redondeado(
            self, 2, 2, w - 2, h - 2, 6, fill=tema.FONDO if self._activo else tema.TARJETA,
            outline=tema.TINTA if self._activo else tema.CAMPO_BORDE,
            width=2 if self._activo else 1)
        self.create_text(16, h / 2, text=self._valor, anchor="w", fill=tema.TINTA,
                         font=tema.fuente(16))
        self.create_line(w - 34, h / 2 - 4, w - 26, h / 2 + 4, w - 18, h / 2 - 4,
                         fill=tema.TINTA, width=2)

    def _abrir(self):
        menu = tk.Menu(self, tearoff=0, font=tema.fuente(14), bg=tema.TARJETA, fg=tema.TINTA,
                       activebackground=tema.TINTA, activeforeground=tema.BLANCO, bd=0)
        for opcion in self._opciones:
            menu.add_command(label=opcion, command=lambda o=opcion: self._elegir(o))
        try:
            menu.tk_popup(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())
        finally:
            menu.grab_release()

    def _elegir(self, opcion):
        cambio = opcion != self._valor
        self._valor = opcion
        self._dibujar()
        if cambio and self._al_cambiar:
            self._al_cambiar(opcion)


class TarjetaModulo(tk.Canvas):
    """Tarjeta del panel: icono, título y, opcionalmente, una insignia (ej. "2 alertas")."""

    ALTO = 88

    def __init__(self, parent, modulo, al_hacer_clic, insignia=None):
        super().__init__(parent, height=self.ALTO, bg=tema.FONDO, highlightthickness=0,
                         bd=0, cursor="hand2", takefocus=True)
        self.modulo = modulo
        self._al_hacer_clic = al_hacer_clic
        self._insignia = insignia
        self._activa = False
        self._icono = tema.cargar_imagen(f"iconos/{modulo.id}.png")
        self._medidor = tkfont.Font(family=tema.FAMILIA, size=-14, weight="bold")

        self.bind("<Configure>", lambda _e: self._dibujar())
        self.bind("<Enter>", lambda _e: self._marcar(True))
        self.bind("<Leave>", lambda _e: self._marcar(False))
        self.bind("<FocusIn>", lambda _e: self._marcar(True))
        self.bind("<FocusOut>", lambda _e: self._marcar(False))
        self.bind("<Button-1>", lambda _e: self._abrir())
        self.bind("<Return>", lambda _e: self._abrir())
        self.bind("<space>", lambda _e: self._abrir())

    def _marcar(self, activa):
        self._activa = activa
        self._dibujar()

    def _abrir(self):
        self._al_hacer_clic(self.modulo)

    def _dibujar(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10:
            return
        tema.rect_redondeado(
            self, 2, 2, w - 2, h - 2, 8,
            fill=tema.FONDO if self._activa else tema.TARJETA,
            outline=tema.TINTA if self._activa else tema.BORDE)
        lado, x = 54, 20
        y = (h - lado) / 2
        tema.rect_redondeado(self, x, y, x + lado, y + lado, 8,
                             fill=tema.TINTA, outline=tema.TINTA)
        self.create_image(x + lado / 2, h / 2, image=self._icono)
        self.create_text(x + lado + 20, h / 2, text=self.modulo.titulo, anchor="w",
                         fill=tema.TINTA, font=tema.fuente(20, "bold"))
        if self._insignia:
            ancho = self._medidor.measure(self._insignia) + 36
            x2 = w - 16
            tema.rect_redondeado(self, x2 - ancho, h / 2 - 16, x2, h / 2 + 16, 16,
                                 fill=tema.AVISO_FONDO, outline=tema.AVISO_FONDO)
            self.create_text(x2 - ancho / 2, h / 2, text=self._insignia,
                             fill=tema.AVISO_TEXTO, font=tema.fuente(14, "bold"))
