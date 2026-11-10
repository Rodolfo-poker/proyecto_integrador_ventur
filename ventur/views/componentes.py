"""Widgets reutilizables: tarjeta de módulo y botón."""
import tkinter as tk

from . import tema


class TarjetaModulo(tk.Canvas):
    """Tarjeta con icono y título. Se redibuja al cambiar de tamaño."""

    ALTO = 72

    def __init__(self, parent, modulo, al_hacer_clic):
        super().__init__(
            parent, height=self.ALTO, bg=tema.FONDO, highlightthickness=0,
            bd=0, cursor="hand2", takefocus=True,
        )
        self.modulo = modulo
        self._al_hacer_clic = al_hacer_clic
        self._activa = False
        self._icono = tema.cargar_imagen(f"iconos/{modulo.id}.png")
        self._fuente_titulo = tema.fuente(13, "bold")

        self.bind("<Configure>", lambda _e: self._dibujar())
        self.bind("<Enter>", lambda _e: self._marcar(True))
        self.bind("<Leave>", lambda _e: self._marcar(False))
        self.bind("<FocusIn>", lambda _e: self._marcar(True))
        self.bind("<FocusOut>", lambda _e: self._marcar(False))
        self.bind("<Button-1>", lambda _e: self._abrir())
        self.bind("<Return>", lambda _e: self._abrir())
        self.bind("<space>", lambda _e: self._abrir())

    def _marcar(self, activa):
        self._activa = activa
        self._dibujar()

    def _abrir(self):
        self._al_hacer_clic(self.modulo)

    def _dibujar(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10:
            return
        tema.rect_redondeado(
            self, 2, 2, w - 2, h - 2, 18,
            fill=tema.TARJETA_HOVER if self._activa else tema.TARJETA,
            outline=tema.TINTA if self._activa else tema.BORDE,
        )
        lado, x, y = 42, 18, (h - 42) // 2
        tema.rect_redondeado(self, x, y, x + lado, y + lado, 13,
                             fill=tema.TINTA, outline=tema.TINTA)
        self.create_image(x + lado / 2, y + lado / 2, image=self._icono)
        self.create_text(x + lado + 16, h / 2, text=self.modulo.titulo, anchor="w",
                         fill=tema.TINTA, font=self._fuente_titulo)


class Boton(tk.Label):
    """Botón plano (los tk.Button ignoran los colores en macOS y Windows)."""

    def __init__(self, parent, texto, comando, secundario=False):
        self._fondo = tema.TARJETA if secundario else tema.TINTA
        self._fondo_hover = tema.FONDO if secundario else "#32353F"
        super().__init__(
            parent, text=texto, bg=self._fondo,
            fg=tema.TINTA if secundario else tema.BLANCO,
            font=tema.fuente(11, "bold"), padx=18, pady=9, cursor="hand2", takefocus=True,
            highlightthickness=1 if secundario else 0,
            highlightbackground=tema.BORDE,
        )
        self.bind("<Button-1>", lambda _e: comando())
        self.bind("<Return>", lambda _e: comando())
        self.bind("<space>", lambda _e: comando())
        self.bind("<Enter>", lambda _e: self.config(bg=self._fondo_hover))
        self.bind("<Leave>", lambda _e: self.config(bg=self._fondo))
