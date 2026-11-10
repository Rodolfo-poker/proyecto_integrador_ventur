"""Modelo: productos y su repositorio (por ahora en memoria).

Cuando tengas base de datos, solo se reemplaza el interior de
RepositorioProductos; las vistas y el controlador no cambian.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Producto:
    id: str
    descripcion: str
    precio: float
    existencia: int


class RepositorioProductos:
    def __init__(self):
        self._items = {p.id: p for p in [
            Producto("001", "Camisa Deportiva M", 320.00, 24),
            Producto("002", "Pantalón Mezclilla", 550.00, 12),
            Producto("003", "Tenis Running", 1200.00, 6),
            Producto("004", "Llaveros Batman", 600.0, 4),
        ]}

    def todos(self) -> List[Producto]:
        return list(self._items.values())

    def obtener(self, id_producto: str) -> Optional[Producto]:
        return self._items.get(id_producto.strip())

    def buscar(self, texto: str) -> List[Producto]:
        """Productos cuyo código o descripción contienen el texto."""
        texto = texto.strip().lower()
        if not texto:
            return self.todos()
        return [p for p in self._items.values()
                if texto in p.id.lower() or texto in p.descripcion.lower()]

    def descontar(self, id_producto: str, cantidad: int) -> None:
        self._items[id_producto].existencia -= cantidad
