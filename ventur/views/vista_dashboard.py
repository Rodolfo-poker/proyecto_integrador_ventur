"""Vista: panel de control (Ventur_Mockup_Panel_Duena.svg / Panel_Empleado.svg)."""
import tkinter as tk
from tkinter import font as tkfont

from . import tema
from .componentes import TarjetaModulo


class EncabezadoPanel(tk.Canvas):
    """Banner oscuro con saludo, rol, logo y botón "Cerrar sesión"."""

    ALTO = 220

    def __init__(self, parent, usuario, al_cerrar_sesion):
        super().__init__(parent, height=self.ALTO, bg=tema.FONDO, highlightthickness=0, bd=0)
        self._usuario = usuario
        self._al_cerrar = al_cerrar_sesion
        self._logo = tema.cargar_imagen("logo_claro_header.png")
        self._f_pildora = tkfont.Font(family=tema.FAMILIA, size=-14, weight="bold")
        self._fondo_cerrar = None

        self.tag_bind("cerrar", "<Button-1>", lambda _e: self._al_cerrar())
        self.tag_bind("cerrar", "<Enter>", lambda _e: self._resaltar_cerrar(True))
        self.tag_bind("cerrar", "<Leave>", lambda _e: self._resaltar_cerrar(False))
        self.bind("<Configure>", lambda _e: self._dibujar())

    def _resaltar_cerrar(self, activo):
        self.config(cursor="hand2" if activo else "")
        if self._fondo_cerrar is not None:
            self.itemconfigure(self._fondo_cerrar,
                               fill=tema.HERO_PILDORA if activo else tema.TINTA)

    def _pildora(self, x, y, texto, con_punto=False):
        alto = 32
        ancho = self._f_pildora.measure(texto) + 36 + (20 if con_punto else 0)
        tema.rect_redondeado(self, x, y, x + ancho, y + alto, 16,
                             fill=tema.HERO_PILDORA, outline=tema.HERO_PILDORA)
        cx = x + 18
        if con_punto:
            self.create_oval(cx, y + alto / 2 - 5, cx + 10, y + alto / 2 + 5,
                             fill=tema.VERDE_PUNTO, outline=tema.VERDE_PUNTO)
            cx += 20
        self.create_text(cx, y + alto / 2, text=texto, anchor="w", fill=tema.BLANCO,
                         font=tema.fuente(14, "bold"))

    def _dibujar(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10:
            return
        tema.rect_redondeado(self, 1, 1, w - 1, h - 1, 12,
                             fill=tema.TINTA, outline=tema.TINTA)
        self._pildora(32, 24, "Panel de control", con_punto=True)
        self.create_text(32, 122, text=f"Hola, {self._usuario.nombre}", anchor="sw",
                         fill=tema.BLANCO, font=tema.fuente(52, "bold"))
        self.create_text(32, 154, text=self._usuario.descripcion, anchor="sw",
                         fill=tema.HERO_TEXTO, font=tema.fuente(18))
        self._pildora(32, 164, f"Rol: {self._usuario.rol.value}")
        self.create_image(w - 36, 22, anchor="ne", image=self._logo)

        ancho, alto = 176, 40
        x1, y1 = w - 32 - ancho, h - 20 - alto
        self._fondo_cerrar = tema.rect_redondeado(
            self, x1, y1, x1 + ancho, y1 + alto, 6, fill=tema.TINTA,
            outline=tema.BLANCO, width=2, tags="cerrar")
        self.create_text(x1 + ancho / 2, y1 + alto / 2, text="Cerrar sesión",
                         fill=tema.BLANCO, font=tema.fuente(15, "bold"), tags="cerrar")


class VistaDashboard(tk.Frame):
    COLUMNAS = 3

    def __init__(self, parent, usuario, modulos, insignias, al_abrir_modulo, al_cerrar_sesion):
        """insignias: {id_modulo: texto}, p. ej. {"alertas": "2 alertas"}"""
        super().__init__(parent, bg=tema.FONDO)

        EncabezadoPanel(self, usuario, al_cerrar_sesion).pack(fill="x", padx=40, pady=(32, 14))

        rejilla = tk.Frame(self, bg=tema.FONDO)
        rejilla.pack(fill="x", padx=22)
        for col in range(self.COLUMNAS):
            rejilla.grid_columnconfigure(col, weight=1, uniform="columnas")
        for indice, modulo in enumerate(modulos):
            fila, col = divmod(indice, self.COLUMNAS)
            TarjetaModulo(rejilla, modulo, al_abrir_modulo, insignias.get(modulo.id)).grid(
                row=fila, column=col, sticky="ew", padx=18, pady=10)
