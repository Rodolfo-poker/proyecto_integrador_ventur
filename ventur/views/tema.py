"""Colores, tipografías y utilidades de dibujo compartidas por todas las vistas."""
import sys
import tkinter as tk
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"

# Paleta tomada del logo: negro azulado sobre blanco.
FONDO = "#F3F4F7"
TARJETA = "#FFFFFF"
TARJETA_HOVER = "#F8F8FB"
BORDE = "#E3E5EB"
TINTA = "#1B1D24"
TINTA_SUAVE = "#6A6F7D"
ENCABEZADO = "#1B1D24"
ENCABEZADO_PILDORA = "#2C2F3A"
ENCABEZADO_TEXTO_SUAVE = "#A9AEBB"
VERDE = "#3DDC97"
BLANCO = "#FFFFFF"


def _familia():
    if sys.platform == "darwin":
        return "Helvetica Neue"
    if sys.platform.startswith("win"):
        return "Segoe UI"
    return "DejaVu Sans"


FAMILIA = _familia()


def fuente(tamano, peso="normal"):
    return (FAMILIA, tamano, peso)


def cargar_imagen(ruta_relativa):
    """Carga un PNG de assets/. Quien la llame debe guardar la referencia."""
    return tk.PhotoImage(file=str(ASSETS / ruta_relativa))


def rect_redondeado(canvas, x1, y1, x2, y2, r, **opciones):
    """Dibuja un rectángulo con esquinas redondeadas en un Canvas."""
    puntos = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(puntos, smooth=True, **opciones)
