"""Tabla personalizada: encabezado oscuro, filas alternadas y widgets dentro de las celdas.

Un ttk.Treeview no puede llevar botones ni píldoras de color dentro de las filas,
por eso las tablas de Ventur se arman con frames.
"""
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

from . import tema


@dataclass(frozen=True)
class Columna:
    titulo: str
    ancho: int              # ancho mínimo en píxeles
    ancla: str = "w"        # "w" izquierda, "center" centro, "e" derecha
    expande: bool = False   # True: esta columna se lleva el espacio sobrante


def texto(contenido, peso="normal", color=tema.TINTA, tamano=16):
    """Celda de texto simple."""
    def crear(padre):
        return tk.Label(padre, text=contenido, bg=padre.cget("bg"), fg=color,
                        font=tema.fuente(tamano, peso))
    return crear


class TablaPersonalizada(tk.Frame):
    """Cada celda es una función que recibe el frame de la fila y devuelve un widget."""

    ALTO_ENCABEZADO = 44
    _STICKY = {"w": "w", "e": "e", "center": ""}

    def __init__(self, parent, columnas, alto_fila=56):
        super().__init__(parent, bg=parent.cget("bg"))
        self._columnas = list(columnas)
        self._alto_fila = alto_fila
        self._contador = 0

        marco = tk.Frame(self, bg=self.cget("bg"))
        barra = ttk.Scrollbar(marco, orient="vertical")
        ancho_barra = barra.winfo_reqwidth()

        # Encabezado (con el mismo margen derecho que ocupa la barra para que alineen)
        self._encabezado = tk.Frame(self, bg=tema.TINTA, height=self.ALTO_ENCABEZADO)
        self._encabezado.pack(side="top", fill="x", padx=(0, ancho_barra))
        self._encabezado.grid_propagate(False)
        self._encabezado.grid_rowconfigure(0, weight=1)
        self._configurar_columnas(self._encabezado)
        for i, col in enumerate(self._columnas):
            tk.Label(self._encabezado, text=col.titulo, bg=tema.TINTA, fg=tema.BLANCO,
                     font=tema.fuente(15, "bold")).grid(
                row=0, column=i, sticky=self._STICKY[col.ancla], padx=self._relleno(col))

        # Cuerpo con desplazamiento
        marco.pack(side="top", fill="both", expand=True)
        self._lienzo = tk.Canvas(marco, bg=self.cget("bg"), highlightthickness=0, bd=0,
                                 yscrollincrement=20)
        barra.config(command=self._lienzo.yview)
        self._lienzo.configure(yscrollcommand=barra.set)
        self._interior = tk.Frame(self._lienzo, bg=self.cget("bg"))
        self._ventana = self._lienzo.create_window(0, 0, window=self._interior, anchor="nw")
        self._lienzo.bind("<Configure>",
                          lambda e: self._lienzo.itemconfigure(self._ventana, width=e.width))
        self._interior.bind("<Configure>", lambda _e: self._lienzo.configure(
            scrollregion=self._lienzo.bbox("all")))
        barra.pack(side="right", fill="y")
        self._lienzo.pack(side="left", fill="both", expand=True)

        for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind_all(evento, self._rueda, add="+")

    # ---- API ----
    def limpiar(self):
        for hijo in self._interior.winfo_children():
            hijo.destroy()
        self._contador = 0

    def agregar_fila(self, celdas, acento=None):
        """celdas: una función por columna. acento: color de la barra lateral de la fila."""
        fondo = tema.TARJETA if self._contador % 2 == 0 else tema.FILA_ALTERNA
        self._contador += 1
        fila = tk.Frame(self._interior, bg=fondo, height=self._alto_fila)
        fila.pack(fill="x")
        fila.grid_propagate(False)
        fila.grid_rowconfigure(0, weight=1)
        self._configurar_columnas(fila)
        for i, (crear, col) in enumerate(zip(celdas, self._columnas)):
            crear(fila).grid(row=0, column=i, sticky=self._STICKY[col.ancla],
                             padx=self._relleno(col))
        if acento:
            tk.Frame(fila, bg=acento, width=5).place(x=0, y=0, relheight=1)

    # ---- Interno ----
    def _configurar_columnas(self, marco):
        for i, col in enumerate(self._columnas):
            marco.grid_columnconfigure(i, minsize=col.ancho, weight=1 if col.expande else 0)

    @staticmethod
    def _relleno(col):
        return {"w": (20, 0), "e": (0, 20), "center": 0}[col.ancla]

    def _rueda(self, evento):
        """Rueda del mouse: solo desplaza si el cursor está sobre esta tabla."""
        try:
            if not self.winfo_exists():
                return
            bajo = self.winfo_containing(evento.x_root, evento.y_root)
        except (tk.TclError, KeyError):
            return
        while bajo is not None and bajo is not self:
            bajo = getattr(bajo, "master", None)
        if bajo is None:
            return
        if self._lienzo.yview() == (0.0, 1.0):
            return  # todo cabe, no hay nada que desplazar
        if evento.num == 4:
            paso = -1
        elif evento.num == 5:
            paso = 1
        else:
            paso = -1 if evento.delta > 0 else 1
        self._lienzo.yview_scroll(paso * 3, "units")
