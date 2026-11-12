"""Vista: ventana raíz. Solo sabe mostrar una vista a la vez."""
import tkinter as tk

from . import tema


class VentanaPrincipal(tk.Tk):
    ANCHO, ALTO = 1280, 800

    def __init__(self, titulo):
        super().__init__()
        self.title(titulo)
        self.configure(bg=tema.FONDO)
        self.minsize(1000, 640)
        tema.aplicar_estilos(self)
        self._centrar()
        try:
            self._icono = tema.cargar_imagen("icono_app.png")
            self.iconphoto(True, self._icono)
        except tk.TclError:
            pass  # el icono es opcional

        self.contenedor = tk.Frame(self, bg=tema.FONDO)
        self.contenedor.pack(fill="both", expand=True)
        self._vista_actual = None

    def _centrar(self):
        pantalla_w, pantalla_h = self.winfo_screenwidth(), self.winfo_screenheight()
        ancho = min(self.ANCHO, pantalla_w - 40)    # por si la pantalla es chica
        alto = min(self.ALTO, pantalla_h - 100)
        x = (pantalla_w - ancho) // 2
        y = max(0, (pantalla_h - alto) // 2 - 20)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def mostrar(self, vista):
        if self._vista_actual is not None:
            self._vista_actual.destroy()
        self._vista_actual = vista
        vista.pack(fill="both", expand=True)
