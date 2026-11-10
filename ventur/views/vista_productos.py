"""Vista: módulo Productos (tabla de artículos con buscador)."""
import tkinter as tk
from tkinter import ttk

from . import tema
from .vista_base import VistaBase, crear_entrada

STOCK_BAJO = 5  # a partir de aquí la existencia se marca en rojo


class VistaProductos(VistaBase):
    def __init__(self, parent, modulo, al_volver, al_buscar):
        super().__init__(parent, modulo, al_volver)
        self._al_buscar = al_buscar
        cuerpo = self.cuerpo

        self._conteo = tk.Label(cuerpo, anchor="w", bg=tema.TARJETA, fg=tema.TINTA_SUAVE,
                                font=tema.fuente(10))
        self._conteo.pack(side="bottom", fill="x", padx=24, pady=(0, 18))

        superior = tk.Frame(cuerpo, bg=tema.TARJETA)
        superior.pack(fill="x", padx=24, pady=(24, 14))
        tk.Label(superior, text="Buscar por código o descripción", bg=tema.TARJETA,
                 fg=tema.TINTA, font=tema.fuente(11, "bold")).pack(anchor="w", pady=(0, 6))
        self._texto = tk.StringVar()
        self._texto.trace_add("write", lambda *_: self._llenar())
        crear_entrada(superior, textvariable=self._texto).pack(fill="x", ipady=8)

        marco = tk.Frame(cuerpo, bg=tema.TARJETA)
        marco.pack(fill="both", expand=True, padx=24, pady=(0, 10))
        self._tabla = ttk.Treeview(
            marco, style="Ventur.Treeview", show="headings", selectmode="browse",
            columns=("id", "descripcion", "precio", "existencia"))
        for col, titulo, ancho, ancla in (
                ("id", "ID", 90, "center"),
                ("descripcion", "Descripción", 320, "w"),
                ("precio", "Precio venta", 150, "center"),
                ("existencia", "Existencia", 130, "center")):
            self._tabla.heading(col, text=titulo)
            self._tabla.column(col, width=ancho, anchor=ancla, stretch=(col == "descripcion"))
        self._tabla.tag_configure("par", background="#FAFAFC")
        self._tabla.tag_configure("bajo", foreground=tema.ERROR)
        barra = ttk.Scrollbar(marco, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=barra.set)
        self._tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self._llenar()

    def _llenar(self):
        productos = self._al_buscar(self._texto.get())
        self._tabla.delete(*self._tabla.get_children())
        for i, p in enumerate(productos):
            etiquetas = ["par"] if i % 2 else []
            if p.existencia <= STOCK_BAJO:
                etiquetas.append("bajo")
            self._tabla.insert("", "end", tags=etiquetas, values=(
                p.id, p.descripcion, tema.dinero(p.precio), p.existencia))
        n = len(productos)
        self._conteo.config(text=f"{n} producto{'' if n == 1 else 's'}")
