"""Modelo: la venta en curso (el carrito de la Caja)."""
from dataclasses import dataclass
from typing import Dict, List

from .productos import Producto


@dataclass
class LineaVenta:
    producto: Producto
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        return self.producto.precio * self.cantidad


class Venta:
    def __init__(self):
        self._lineas: Dict[str, LineaVenta] = {}

    @property
    def lineas(self) -> List[LineaVenta]:
        return list(self._lineas.values())

    @property
    def total(self) -> float:
        return sum(linea.subtotal for linea in self._lineas.values())

    @property
    def vacia(self) -> bool:
        return not self._lineas

    def agregar(self, producto: Producto) -> bool:
        """Suma una unidad. Devuelve False si ya no hay existencias."""
        linea = self._lineas.get(producto.id)
        en_venta = linea.cantidad if linea else 0
        if en_venta >= producto.existencia:
            return False
        if linea:
            linea.cantidad += 1
        else:
            self._lineas[producto.id] = LineaVenta(producto)
        return True

    def limpiar(self) -> None:
        self._lineas.clear()
