"""Vista: módulo Caja (Ventur_Mockup_Caja.svg)."""
import tkinter as tk
from tkinter import messagebox

from models.productos import UMBRAL_STOCK_BAJO

from . import tema
from .componentes import Aviso, Boton, Campo
from .tabla import Columna, TablaPersonalizada, texto
from .vista_base import VistaBase

_COLUMNAS = [
    Columna("Producto", 200, "w", expande=True),
    Columna("Cant.", 220, "center"),
    Columna("Precio", 140, "e"),
    Columna("Subtotal", 160, "e"),
    Columna("Quitar", 170, "center"),
]


class VistaCaja(VistaBase):
    def __init__(self, parent, modulo, al_volver, al_agregar, al_cambiar_cantidad,
                 al_quitar, al_vaciar, al_cobrar, venta):
        super().__init__(parent, modulo, al_volver)
        self._al_agregar = al_agregar
        self._al_cambiar_cantidad = al_cambiar_cantidad
        self._al_quitar = al_quitar
        cuerpo = self.cuerpo

        # --- Abajo: cobro, línea divisoria y avisos (se empaquetan primero) ---
        cobro = tk.Frame(cuerpo, bg=tema.TARJETA)
        cobro.pack(side="bottom", fill="x", padx=24, pady=(0, 20))
        self._total = tk.Label(cobro, bg=tema.TARJETA, fg=tema.TINTA, font=tema.fuente(36, "bold"))
        self._total.pack(side="left")
        self._boton_cobrar = Boton(cobro, "Procesar cobro ($0.00)", al_cobrar,
                                   ancho=300, alto=56, tamano=17)
        self._boton_cobrar.pack(side="right")
        Boton(cobro, "Vaciar", al_vaciar, estilo="secundario", ancho=140, alto=56,
              tamano=17).pack(side="right", padx=(0, 20))
        tk.Frame(cuerpo, height=2, bg=tema.BORDE).pack(side="bottom", fill="x", padx=24,
                                                       pady=(0, 20))
        self._aviso = Aviso(cuerpo, espacio_abajo=16, wraplength=1000)
        self._aviso.pack(side="bottom", fill="x", padx=24)

        # --- Arriba: captura del producto ---
        superior = tk.Frame(cuerpo, bg=tema.TARJETA)
        superior.pack(fill="x", padx=24, pady=(24, 20))
        tk.Label(superior, text="Código o nombre del producto", bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(16, "bold")).pack(anchor="w", pady=(0, 8))
        fila = tk.Frame(superior, bg=tema.TARJETA)
        fila.pack(fill="x")
        fila.grid_columnconfigure(0, weight=1)
        self._busqueda = Campo(fila, placeholder="Escribe o escanea el código", buscador=True)
        self._busqueda.grid(row=0, column=0, sticky="ew")
        self._busqueda.enlazar_enter(self._agregar)
        Boton(fila, "Agregar", self._agregar, ancho=136, alto=48).grid(
            row=0, column=1, padx=(16, 0))

        # --- Centro: líneas de la venta ---
        self._tabla = TablaPersonalizada(cuerpo, _COLUMNAS, alto_fila=60)
        self._tabla.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.actualizar(venta)
        self.after(150, self._enfocar_inicial)

    def _enfocar_inicial(self):
        try:
            self._busqueda.enfocar()
        except tk.TclError:
            pass  # la vista ya se cerró

    def _agregar(self):
        # El controlador responde True si se agregó; entonces limpiamos el campo.
        if self._al_agregar(self._busqueda.valor()):
            self._busqueda.limpiar()
        self._busqueda.enfocar()

    # ---- Celdas ----
    def _stepper(self, linea):
        id_producto = linea.producto.id

        def crear(padre):
            fondo = padre.cget("bg")
            marco = tk.Frame(padre, bg=fondo)
            Boton(marco, "−", lambda: self._al_cambiar_cantidad(id_producto, -1), estilo="campo",
                  ancho=36, alto=36, tamano=22).pack(side="left")
            tk.Label(marco, text=str(linea.cantidad), width=3, bg=fondo, fg=tema.TINTA,
                     font=tema.fuente(17, "bold")).pack(side="left")
            Boton(marco, "+", lambda: self._al_cambiar_cantidad(id_producto, +1), estilo="campo",
                  ancho=36, alto=36, tamano=22).pack(side="left")
            return marco
        return crear

    def _boton_quitar(self, id_producto):
        return lambda padre: Boton(padre, "Quitar", lambda: self._al_quitar(id_producto),
                                   estilo="peligro", ancho=96, alto=32, tamano=14)

    # ---- Actualización desde el modelo ----
    def actualizar(self, venta, error=""):
        """Redibuja tabla, total y avisos a partir del modelo Venta."""
        self._tabla.limpiar()
        for linea in venta.lineas:
            p = linea.producto
            self._tabla.agregar_fila([
                texto(p.descripcion),
                self._stepper(linea),
                texto(tema.dinero(p.precio)),
                texto(tema.dinero(linea.subtotal), peso="bold"),
                self._boton_quitar(p.id),
            ])
        self._total.config(text=f"Total: {tema.dinero(venta.total)}")
        self._boton_cobrar.poner_texto(f"Procesar cobro ({tema.dinero(venta.total)})")

        if error:
            self._aviso.mostrar(error, "error")
            return
        avisos = self._avisos_de_stock(venta)
        if avisos:
            self._aviso.mostrar(avisos, "aviso")
        else:
            self._aviso.ocultar()

    @staticmethod
    def _avisos_de_stock(venta):
        lineas = []
        for linea in venta.lineas:
            if linea.restantes > UMBRAL_STOCK_BAJO:
                continue
            nombre = linea.producto.descripcion
            if linea.restantes <= 0:
                lineas.append(f"Agotado: con esta venta se terminan las piezas de {nombre}.")
            elif linea.restantes == 1:
                lineas.append(f"Stock bajo: después de esta venta queda 1 pieza de {nombre}.")
            else:
                lineas.append(f"Stock bajo: después de esta venta quedan "
                              f"{linea.restantes} piezas de {nombre}.")
        return "\n".join(lineas)

    def avisar(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje, parent=self)
