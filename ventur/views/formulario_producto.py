"""Vista: ventana para crear o editar un producto (flujo "Formulario" del mapa de navegación)."""
import tkinter as tk

from . import tema
from .componentes import Aviso, Boton, Campo


class FormularioProducto(tk.Toplevel):
    """Ventana modal. al_guardar(datos) devuelve un mensaje de error, o None si todo salió bien."""

    def __init__(self, master, titulo, datos, codigo_editable, al_guardar):
        super().__init__(master, bg=tema.TARJETA)
        self.title(titulo)
        self.resizable(False, False)
        self.transient(master)
        self._al_guardar = al_guardar
        self._campos = {}

        cont = tk.Frame(self, bg=tema.TARJETA)
        cont.pack(fill="both", expand=True, padx=32, pady=28)
        tk.Label(cont, text=titulo, bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(26, "bold")).pack(anchor="w", pady=(0, 18))
        self._aviso = Aviso(cont, espacio_abajo=16, wraplength=412)
        self._aviso.pack(fill="x")

        rejilla = tk.Frame(cont, bg=tema.TARJETA)
        rejilla.pack(fill="x")
        rejilla.grid_columnconfigure(0, weight=1, uniform="campos")
        rejilla.grid_columnconfigure(1, weight=1, uniform="campos")

        self._agregar_campo(rejilla, datos, "id", "Código", 0, 0, placeholder="Ej. 006",
                            solo_lectura=not codigo_editable)
        self._agregar_campo(rejilla, datos, "categoria", "Categoría", 0, 1,
                            placeholder="Ej. Ropa")
        self._agregar_campo(rejilla, datos, "descripcion", "Descripción", 1, 0, columnas=2,
                            placeholder="Ej. Camisa Deportiva M")
        self._agregar_campo(rejilla, datos, "precio", "Precio de venta", 2, 0, placeholder="0.00")
        self._agregar_campo(rejilla, datos, "existencia", "Existencia", 2, 1, placeholder="0")

        botones = tk.Frame(cont, bg=tema.TARJETA)
        botones.pack(fill="x", pady=(6, 0))
        Boton(botones, "Guardar", self._guardar, ancho=150, alto=48).pack(side="right")
        Boton(botones, "Cancelar", self.destroy, estilo="secundario", ancho=130,
              alto=48).pack(side="right", padx=(0, 12))

        self.bind("<Escape>", lambda _e: self.destroy())
        self._centrar_sobre(master)
        try:
            self.wait_visibility()   # grab_set exige que la ventana ya sea visible
            self.grab_set()
        except tk.TclError:
            pass
        primero = "descripcion" if not codigo_editable else "id"
        self._campos[primero].enfocar()

    def _agregar_campo(self, rejilla, datos, clave, etiqueta, fila, columna, columnas=1,
                       **opciones):
        marco = tk.Frame(rejilla, bg=tema.TARJETA)
        if columnas == 2:
            relleno = (0, 0)
        else:
            relleno = (0, 8) if columna == 0 else (8, 0)
        marco.grid(row=fila, column=columna, columnspan=columnas, sticky="ew", padx=relleno,
                   pady=(0, 16))
        tk.Label(marco, text=etiqueta, bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(15, "bold")).pack(anchor="w", pady=(0, 6))
        campo = Campo(marco, ancho=220, **opciones)
        campo.pack(fill="x")
        campo.establecer(datos.get(clave, ""))
        campo.enlazar_enter(self._guardar)
        self._campos[clave] = campo

    def _centrar_sobre(self, master):
        self.update_idletasks()
        ancho, alto = self.winfo_reqwidth(), self.winfo_reqheight()
        x = master.winfo_rootx() + (master.winfo_width() - ancho) // 2
        y = master.winfo_rooty() + (master.winfo_height() - alto) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _guardar(self):
        datos = {clave: campo.valor() for clave, campo in self._campos.items()}
        error = self._al_guardar(datos)
        if error:
            self._aviso.mostrar(error, "error")
        else:
            self.destroy()
