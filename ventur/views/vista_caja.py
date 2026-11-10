"""Vista: módulo Caja (punto de venta)."""
import tkinter as tk
from tkinter import messagebox, ttk

from . import tema
from .componentes import Boton
from .vista_base import VistaBase, crear_entrada


class VistaCaja(VistaBase):
    def __init__(self, parent, modulo, al_volver, al_agregar, al_cobrar, al_vaciar, venta):
        super().__init__(parent, modulo, al_volver)
        self._al_agregar = al_agregar
        cuerpo = self.cuerpo

        # --- Fila inferior: total y botones (se empaqueta primero para quedar abajo) ---
        inferior = tk.Frame(cuerpo, bg=tema.TARJETA)
        inferior.pack(side="bottom", fill="x", padx=24, pady=(0, 24))
        self._total = tk.Label(inferior, bg=tema.TARJETA, fg=tema.TINTA,
                               font=tema.fuente(22, "bold"))
        self._total.pack(side="left")
        self._boton_cobrar = Boton(inferior, "Procesar cobro ($0.00)", al_cobrar)
        self._boton_cobrar.pack(side="right")
        Boton(inferior, "Vaciar", al_vaciar, secundario=True).pack(side="right", padx=(0, 10))

        # --- Fila superior: captura de producto ---
        superior = tk.Frame(cuerpo, bg=tema.TARJETA)
        superior.pack(fill="x", padx=24, pady=(24, 6))
        tk.Label(superior, text="Código o nombre del producto", bg=tema.TARJETA,
                 fg=tema.TINTA, font=tema.fuente(11, "bold")).pack(anchor="w", pady=(0, 6))
        fila = tk.Frame(superior, bg=tema.TARJETA)
        fila.pack(fill="x")
        self._entrada = crear_entrada(fila)
        self._entrada.pack(side="left", fill="x", expand=True, ipady=8)
        self._entrada.bind("<Return>", lambda _e: self._agregar())
        Boton(fila, "Agregar", self._agregar).pack(side="left", padx=(10, 0))
        self._mensaje = tk.Label(superior, anchor="w", bg=tema.TARJETA, font=tema.fuente(10))
        self._mensaje.pack(fill="x", pady=(8, 0))

        # --- Tabla de la venta ---
        marco = tk.Frame(cuerpo, bg=tema.TARJETA)
        marco.pack(fill="both", expand=True, padx=24, pady=(6, 16))
        self._tabla = ttk.Treeview(
            marco, style="Ventur.Treeview", show="headings", selectmode="browse",
            columns=("producto", "cantidad", "precio", "subtotal"))
        for col, titulo, ancho, ancla in (
                ("producto", "Producto", 320, "w"),
                ("cantidad", "Cant.", 80, "center"),
                ("precio", "Precio", 140, "center"),
                ("subtotal", "Subtotal", 150, "center")):
            self._tabla.heading(col, text=titulo)
            self._tabla.column(col, width=ancho, anchor=ancla, stretch=(col == "producto"))
        self._tabla.tag_configure("par", background="#FAFAFC")
        barra = ttk.Scrollbar(marco, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=barra.set)
        self._tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.actualizar(venta)
        self._entrada.focus_set()

    def _agregar(self):
        # El controlador responde True si se agregó; entonces limpiamos el campo.
        if self._al_agregar(self._entrada.get()):
            self._entrada.delete(0, "end")
        self._entrada.focus_set()

    def actualizar(self, venta, mensaje="", error=False):
        """Redibuja la tabla, el total y el mensaje a partir del modelo Venta."""
        self._tabla.delete(*self._tabla.get_children())
        for i, linea in enumerate(venta.lineas):
            self._tabla.insert("", "end", tags=["par"] if i % 2 else [], values=(
                linea.producto.descripcion, linea.cantidad,
                tema.dinero(linea.producto.precio), tema.dinero(linea.subtotal)))
        self._total.config(text=f"Total: {tema.dinero(venta.total)}")
        self._boton_cobrar.config(text=f"Procesar cobro ({tema.dinero(venta.total)})")
        self._mensaje.config(text=mensaje, fg=tema.ERROR if error else tema.TINTA_SUAVE)

    def avisar(self, titulo, texto):
        messagebox.showinfo(titulo, texto, parent=self)
