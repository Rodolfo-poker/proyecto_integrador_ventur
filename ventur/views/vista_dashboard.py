"""Vista: panel de control (encabezado, tarjetas de módulos y pie de página)."""
import tkinter as tk
from tkinter import font as tkfont

from . import tema
from .componentes import TarjetaModulo


class EncabezadoPanel(tk.Canvas):
    """Banner oscuro con saludo, plan activo y el logo de Ventur."""

    ALTO = 196

    def __init__(self, parent, usuario):
        super().__init__(parent, height=self.ALTO, bg=tema.FONDO, highlightthickness=0, bd=0)
        self._usuario = usuario
        self._logo = tema.cargar_imagen("logo_claro_header.png")
        self._f_pildora = tkfont.Font(family=tema.FAMILIA, size=10, weight="bold")
        self._f_saludo = tkfont.Font(family=tema.FAMILIA, size=30, weight="bold")
        self._f_sub = tkfont.Font(family=tema.FAMILIA, size=12)
        self.bind("<Configure>", lambda _e: self._dibujar())

    def _pildora(self, x, y, texto, con_punto=False):
        pad, alto = 14, 28
        extra = 16 if con_punto else 0
        ancho = self._f_pildora.measure(texto) + pad * 2 + extra
        tema.rect_redondeado(self, x, y, x + ancho, y + alto, 14,
                             fill=tema.ENCABEZADO_PILDORA, outline=tema.ENCABEZADO_PILDORA)
        cx = x + pad
        if con_punto:
            self.create_oval(cx, y + alto / 2 - 4, cx + 8, y + alto / 2 + 4,
                             fill=tema.VERDE, outline=tema.VERDE)
            cx += 16
        self.create_text(cx, y + alto / 2, text=texto, anchor="w",
                         fill=tema.BLANCO, font=self._f_pildora)

    def _dibujar(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10:
            return
        tema.rect_redondeado(self, 1, 1, w - 1, h - 1, 28,
                             fill=tema.ENCABEZADO, outline=tema.ENCABEZADO)
        self._pildora(36, 26, "Panel de control", con_punto=True)
        self.create_text(36, 70, text=f"Hola, {self._usuario.nombre}", anchor="nw",
                         fill=tema.BLANCO, font=self._f_saludo)
        self.create_text(36, 118, anchor="nw", fill=tema.ENCABEZADO_TEXTO_SUAVE,
                         font=self._f_sub,
                         text="Tus accesos rápidos y el estado de tu cuenta, en un solo lugar.")
        self._pildora(36, 152, f"Plan {self._usuario.plan.nombre}")
        self.create_image(w - 44, h / 2, anchor="e", image=self._logo)


class VistaDashboard(tk.Frame):
    COLUMNAS = 3

    def __init__(self, parent, usuario, marca, modulos, al_abrir_modulo):
        super().__init__(parent, bg=tema.FONDO)
        self._logo_pie = tema.cargar_imagen("logo_oscuro_footer.png")

        # El pie se empaqueta primero para que siempre quede abajo.
        self._construir_pie(marca)

        EncabezadoPanel(self, usuario).pack(fill="x", padx=32, pady=(28, 18))

        rejilla = tk.Frame(self, bg=tema.FONDO)
        rejilla.pack(fill="x", padx=24)
        for col in range(self.COLUMNAS):
            rejilla.grid_columnconfigure(col, weight=1, uniform="columnas")
        for indice, modulo in enumerate(modulos):
            fila, col = divmod(indice, self.COLUMNAS)
            TarjetaModulo(rejilla, modulo, al_abrir_modulo).grid(
                row=fila, column=col, sticky="ew", padx=8, pady=7)

    def _construir_pie(self, marca):
        pie = tk.Frame(self, bg=tema.TARJETA)
        pie.pack(side="bottom", fill="x")
        tk.Frame(pie, height=1, bg=tema.BORDE).pack(fill="x")

        bloque = tk.Frame(pie, bg=tema.TARJETA)
        bloque.pack(anchor="w", padx=40, pady=22)
        tk.Label(bloque, image=self._logo_pie, bg=tema.TARJETA).pack(side="left", padx=(0, 14))
        textos = tk.Frame(bloque, bg=tema.TARJETA)
        textos.pack(side="left")
        tk.Label(textos, text=marca.nombre, bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(14, "bold")).pack(anchor="w")
        tk.Label(textos, text=marca.eslogan, bg=tema.TARJETA, fg=tema.TINTA_SUAVE,
                 font=tema.fuente(11)).pack(anchor="w")
