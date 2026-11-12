"""Colores, tipografías y utilidades de dibujo compartidas por todas las vistas.

La paleta sale de los mockups (Ventur_Mockup_*.svg).
Los tamaños de letra están en PÍXELES, igual que en los mockups.
"""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"

# --- Base ---
FONDO = "#F8FAFC"
TARJETA = "#FFFFFF"
BORDE = "#E2E8F0"
TINTA = "#111827"
TINTA_SUAVE = "#475569"
BLANCO = "#FFFFFF"
FILA_ALTERNA = "#F8FAFC"

# --- Campos y botones ---
CAMPO_BORDE = "#64748B"
CAMPO_SOLO_LECTURA = "#F1F5F9"
BOTON_PRIMARIO_HOVER = "#1F2937"

# --- Encabezado del panel ---
HERO_PILDORA = "#1F2937"
HERO_TEXTO = "#E2E8F0"
VERDE_PUNTO = "#22C55E"

# --- Estados ---
OK_FONDO, OK_TEXTO = "#DCFCE7", "#166534"
AVISO_FONDO, AVISO_BORDE, AVISO_TEXTO = "#FEF3C7", "#D97706", "#92400E"
ERROR_FONDO, ERROR_BORDE, ERROR_TEXTO = "#FEE2E2", "#B91C1C", "#991B1B"
ROJO = "#B91C1C"


def _familia():
    if sys.platform == "darwin":
        return "Helvetica Neue"
    if sys.platform.startswith("win"):
        return "Segoe UI"
    return "DejaVu Sans"


FAMILIA = _familia()


def fuente(px, peso="normal"):
    """Fuente por tamaño en píxeles (el signo negativo le indica a tk que son px)."""
    return (FAMILIA, -px, peso)


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


def dinero(valor):
    """1200 -> '$1,200.00'"""
    return f"${valor:,.2f}"


def aplicar_estilos(raiz):
    """Estilo de las barras de desplazamiento (ttk)."""
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")  # el tema por defecto de Windows ignora los colores
    estilo.configure("Vertical.TScrollbar", background="#CBD5E1", troughcolor=TARJETA,
                     bordercolor=TARJETA, lightcolor="#CBD5E1", darkcolor="#CBD5E1",
                     arrowcolor=TINTA, relief="flat", gripcount=0)
    estilo.map("Vertical.TScrollbar", background=[("active", "#94A3B8")])
