"""Vista: pantalla provisional de un módulo (se reemplaza al construir cada módulo)."""
import tkinter as tk

from . import tema
from .componentes import Boton


class VistaModulo(tk.Frame):
    def __init__(self, parent, modulo, al_volver):
        super().__init__(parent, bg=tema.FONDO)
        self._icono = tema.cargar_imagen(f"iconos/{modulo.id}.png")

        barra = tk.Frame(self, bg=tema.FONDO)
        barra.pack(fill="x", padx=32, pady=(28, 0))
        Boton(barra, "Volver al panel", al_volver).pack(side="left")

        tarjeta = tk.Frame(self, bg=tema.TARJETA, highlightbackground=tema.BORDE,
                           highlightthickness=1)
        tarjeta.pack(fill="both", expand=True, padx=32, pady=24)

        contenido = tk.Frame(tarjeta, bg=tema.TARJETA)
        contenido.place(relx=0.5, rely=0.45, anchor="center")

        icono = tk.Canvas(contenido, width=64, height=64, bg=tema.TARJETA,
                          highlightthickness=0)
        tema.rect_redondeado(icono, 1, 1, 63, 63, 18, fill=tema.TINTA, outline=tema.TINTA)
        icono.create_image(32, 32, image=self._icono)
        icono.pack(pady=(0, 18))

        tk.Label(contenido, text=modulo.titulo, bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(24, "bold")).pack()
        tk.Label(contenido, text=modulo.descripcion, bg=tema.TARJETA, fg=tema.TINTA_SUAVE,
                 font=tema.fuente(12), wraplength=460, justify="center").pack(pady=(8, 20))
        tk.Label(contenido, text="Este módulo todavía no está disponible.",
                 bg=tema.TARJETA, fg=tema.TINTA, font=tema.fuente(11)).pack()
