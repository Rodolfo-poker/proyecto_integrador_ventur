"""Vista base de los módulos: barra con "Volver al panel", título y un cuerpo vacío."""
import tkinter as tk

from . import tema
from .componentes import Boton


class VistaBase(tk.Frame):
    """Las vistas de cada módulo heredan de aquí y dibujan dentro de self.cuerpo."""

    def __init__(self, parent, modulo, al_volver):
        super().__init__(parent, bg=tema.FONDO)

        barra = tk.Frame(self, bg=tema.FONDO)
        barra.pack(fill="x", padx=32, pady=(28, 0))
        Boton(barra, "Volver al panel", al_volver).pack(side="left")
        textos = tk.Frame(barra, bg=tema.FONDO)
        textos.pack(side="left", padx=20)
        tk.Label(textos, text=modulo.titulo, bg=tema.FONDO, fg=tema.TINTA,
                 font=tema.fuente(20, "bold")).pack(anchor="w")
        tk.Label(textos, text=modulo.descripcion, bg=tema.FONDO, fg=tema.TINTA_SUAVE,
                 font=tema.fuente(11)).pack(anchor="w")

        self.cuerpo = tk.Frame(self, bg=tema.TARJETA, highlightbackground=tema.BORDE,
                               highlightthickness=1)
        self.cuerpo.pack(fill="both", expand=True, padx=32, pady=(20, 28))


def crear_entrada(parent, **opciones):
    """Campo de texto con el estilo de Ventur."""
    return tk.Entry(parent, font=tema.fuente(12), relief="flat", bg=tema.TARJETA,
                    fg=tema.TINTA, insertbackground=tema.TINTA, highlightthickness=1,
                    highlightbackground=tema.BORDE, highlightcolor=tema.TINTA, **opciones)
