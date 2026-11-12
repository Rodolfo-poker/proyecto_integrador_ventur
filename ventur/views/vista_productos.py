"""Vista: módulo Productos (Ventur_Mockup_Productos.svg)."""
import tkinter as tk

from models.productos import AGOTADO, DISPONIBLE, STOCK_BAJO

from . import tema
from .componentes import Boton, Campo, Pildora, Selector
from .tabla import Columna, TablaPersonalizada, texto
from .vista_base import VistaBase

TODAS = "Todas las categorías"

# estado -> (texto de la píldora, fondo, color del texto, color de la barra lateral)
_ESTADOS = {
    DISPONIBLE: ("Disponible", tema.OK_FONDO, tema.OK_TEXTO, None),
    STOCK_BAJO: ("Stock bajo", tema.AVISO_FONDO, tema.AVISO_TEXTO, tema.AVISO_BORDE),
    AGOTADO: ("Agotado", tema.ERROR_FONDO, tema.ERROR_TEXTO, tema.ROJO),
}

_COLUMNAS = [
    Columna("ID", 106),
    Columna("Descripción", 200, "w", expande=True),
    Columna("Categoría", 180),
    Columna("Precio venta", 150, "e"),
    Columna("Existencia", 120, "center"),
    Columna("Estado", 150),
    Columna("Acciones", 170, "center"),
]


def _pildora(contenido, fondo, color):
    return lambda padre: Pildora(padre, contenido, fondo, color)


def _boton(contenido, comando):
    return lambda padre: Boton(padre, contenido, comando, estilo="secundario",
                               ancho=96, alto=32, tamano=14)


class VistaProductos(VistaBase):
    def __init__(self, parent, modulo, al_volver, al_buscar, al_categorias, al_nuevo, al_editar):
        super().__init__(parent, modulo, al_volver)
        self._al_buscar = al_buscar
        self._al_categorias = al_categorias
        self._al_editar = al_editar
        cuerpo = self.cuerpo

        self._resumen = tk.Label(cuerpo, anchor="w", bg=tema.TARJETA, fg=tema.TINTA_SUAVE,
                                 font=tema.fuente(15))
        self._resumen.pack(side="bottom", fill="x", padx=24, pady=(10, 24))

        superior = tk.Frame(cuerpo, bg=tema.TARJETA)
        superior.pack(fill="x", padx=24, pady=(24, 20))
        tk.Label(superior, text="Buscar por código, nombre o categoría", bg=tema.TARJETA,
                 fg=tema.TINTA, font=tema.fuente(16, "bold")).pack(anchor="w", pady=(0, 8))
        fila = tk.Frame(superior, bg=tema.TARJETA)
        fila.pack(fill="x")
        fila.grid_columnconfigure(0, weight=1)
        self._busqueda = Campo(fila, placeholder="Ej. 001, Camisa, Ropa", buscador=True,
                               al_cambiar=lambda _texto: self._llenar())
        self._busqueda.grid(row=0, column=0, sticky="ew")
        self._categoria = Selector(fila, [TODAS] + list(al_categorias()), TODAS,
                                   al_cambiar=lambda _valor: self._llenar(), ancho=220)
        self._categoria.grid(row=0, column=1, padx=16)
        Boton(fila, "Nuevo producto", al_nuevo, ancho=160, alto=48).grid(row=0, column=2)

        self._tabla = TablaPersonalizada(cuerpo, _COLUMNAS, alto_fila=56)
        self._tabla.pack(fill="both", expand=True, padx=24)

        self._llenar()

    def refrescar(self):
        """Vuelve a leer los productos (después de crear o editar uno)."""
        self._categoria.establecer_opciones([TODAS] + list(self._al_categorias()))
        self._llenar()

    def _llenar(self):
        categoria = self._categoria.valor
        productos = self._al_buscar(self._busqueda.valor(),
                                    None if categoria == TODAS else categoria)
        self._tabla.limpiar()
        for p in productos:
            etiqueta, fondo, color, acento = _ESTADOS[p.estado]
            self._tabla.agregar_fila([
                texto(p.id),
                texto(p.descripcion),
                texto(p.categoria, color=tema.TINTA_SUAVE),
                texto(tema.dinero(p.precio)),
                texto(str(p.existencia), peso="bold"),
                _pildora(etiqueta, fondo, color),
                _boton("Editar", lambda p=p: self._al_editar(p)),
            ], acento=acento)

        total = len(productos)
        alertas = sum(1 for p in productos if p.con_alerta)
        if total == 0:
            self._resumen.config(text="No se encontraron productos.")
        else:
            self._resumen.config(
                text=f"{total} producto{'' if total == 1 else 's'} · "
                     f"{alertas} con alerta de existencias")
