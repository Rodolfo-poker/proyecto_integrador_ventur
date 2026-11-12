"""Vista base de los módulos: botón "Volver al panel", título y un recuadro vacío (cuerpo)."""
import tkinter as tk

from . import tema
from .componentes import Boton, TarjetaRedondeada


class VistaBase(tk.Frame):
    """Las pantallas de cada módulo heredan de aquí y dibujan dentro de self.cuerpo."""

    def __init__(self, parent, modulo, al_volver):
        super().__init__(parent, bg=tema.FONDO)

        barra = tk.Frame(self, bg=tema.FONDO)
        barra.pack(fill="x", padx=40, pady=(32, 0))
        Boton(barra, "Volver al panel", al_volver, ancho=150, alto=52).pack(side="left")
        textos = tk.Frame(barra, bg=tema.FONDO)
        textos.pack(side="left", padx=30)
        tk.Label(textos, text=modulo.titulo, bg=tema.FONDO, fg=tema.TINTA,
                 font=tema.fuente(32, "bold")).pack(anchor="w")
        tk.Label(textos, text=modulo.descripcion, bg=tema.FONDO, fg=tema.TINTA_SUAVE,
                 font=tema.fuente(17)).pack(anchor="w")

        tarjeta = TarjetaRedondeada(self, radio=8)
        tarjeta.pack(fill="both", expand=True, padx=40, pady=(36, 40))
        self.cuerpo = tarjeta.interior
