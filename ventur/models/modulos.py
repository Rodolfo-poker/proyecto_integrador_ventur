"""Modelo: módulos disponibles en el panel de control.

El orden de la lista es el orden en que aparecen en pantalla
(de izquierda a derecha y de arriba hacia abajo).
E-Commerce se quitó a propósito.
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Modulo:
    id: str            # también es el nombre del PNG en assets/iconos/
    titulo: str
    descripcion: str


class RepositorioModulos:
    _MODULOS = [
        Modulo("apartados", "Apartados", "Productos apartados con anticipo para entregar después."),
        Modulo("caja", "Caja", "Punto de venta y cobro."),
        Modulo("categorias", "Categorías", "Organiza tu catálogo por categorías."),
        Modulo("clientes", "Clientes", "Directorio de clientes e historial de compras."),
        Modulo("comisiones", "Comisiones Marcas", "Comisiones por venta de cada marca."),
        Modulo("descuentos", "Descuentos", "Promociones y descuentos activos."),
        Modulo("marcas", "Marcas", "Administra las marcas que vendes."),
        Modulo("ordenes", "Órdenes", "Pedidos y su estado."),
        Modulo("productos", "Productos", "Catálogo, precios y existencias."),
        Modulo("registros", "Registros Caja", "Aperturas, cierres y movimientos de caja."),
        Modulo("tickets", "Tickets", "Consulta y reimprime tickets de venta."),
        Modulo("verificacion", "Verificación inventario", "Conteos y conciliación de existencias."),
    ]

    def todos(self) -> List[Modulo]:
        return list(self._MODULOS)
