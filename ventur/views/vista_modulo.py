"""Vista: pantalla provisional para los módulos que todavía no se construyen."""
import tkinter as tk

from . import tema
from .vista_base import VistaBase


class VistaModulo(VistaBase):
    def __init__(self, parent, modulo, al_volver):
        super().__init__(parent, modulo, al_volver)
        self._icono = tema.cargar_imagen(f"iconos/{modulo.id}.png")

        centro = tk.Frame(self.cuerpo, bg=tema.TARJETA)
        centro.place(relx=0.5, rely=0.45, anchor="center")
        icono = tk.Canvas(centro, width=64, height=64, bg=tema.TARJETA, highlightthickness=0)
        tema.rect_redondeado(icono, 1, 1, 63, 63, 12, fill=tema.TINTA, outline=tema.TINTA)
        icono.create_image(32, 32, image=self._icono)
        icono.pack(pady=(0, 18))
        tk.Label(centro, text="Este módulo todavía no está disponible.", bg=tema.TARJETA,
                 fg=tema.TINTA, font=tema.fuente(18, "bold")).pack()
        tk.Label(centro, text="Se construirá en una siguiente fase.", bg=tema.TARJETA,
                 fg=tema.TINTA_SUAVE, font=tema.fuente(15)).pack(pady=(6, 0))
