"""Vista: inicio de sesión (Ventur_Mockup_Login.svg)."""
import tkinter as tk

from . import tema
from .componentes import Aviso, Boton, Campo, TarjetaRedondeada


class VistaLogin(tk.Frame):
    def __init__(self, parent, eslogan, al_entrar):
        super().__init__(parent, bg=tema.FONDO)
        self._al_entrar = al_entrar
        self._logo = tema.cargar_imagen("logo_oscuro_login.png")

        tarjeta = TarjetaRedondeada(self, radio=12, width=450, height=600)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")
        form = tk.Frame(tarjeta.interior, bg=tema.TARJETA)
        form.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(form, image=self._logo, bg=tema.TARJETA).pack(pady=(0, 6))
        tk.Label(form, text=eslogan, bg=tema.TARJETA, fg=tema.TINTA_SUAVE,
                 font=tema.fuente(15)).pack()
        tk.Label(form, text="Iniciar sesión", bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(28, "bold")).pack(anchor="w", pady=(28, 14))

        self._aviso = Aviso(form, espacio_abajo=16, wraplength=316)
        self._aviso.pack(fill="x")

        tk.Label(form, text="Usuario", bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(16, "bold")).pack(anchor="w")
        self._usuario = Campo(form, placeholder="Tu usuario", ancho=360)
        self._usuario.pack(fill="x", pady=(6, 16))

        tk.Label(form, text="Contraseña", bg=tema.TARJETA, fg=tema.TINTA,
                 font=tema.fuente(16, "bold")).pack(anchor="w")
        self._contrasena = Campo(form, placeholder="Tu contraseña", oculto=True, ancho=360)
        self._contrasena.pack(fill="x", pady=(6, 24))

        Boton(form, "Entrar", self._entrar, ancho=360, alto=52, tamano=17).pack()
        tk.Label(form, text="Funciona sin conexión a internet", bg=tema.TARJETA,
                 fg=tema.TINTA_SUAVE, font=tema.fuente(14)).pack(pady=(22, 0))

        self._usuario.enlazar_enter(self._entrar)
        self._contrasena.enlazar_enter(self._entrar)
        self.after(150, self._enfocar_inicial)

    def _enfocar_inicial(self):
        try:
            self._usuario.enfocar()
        except tk.TclError:
            pass  # la vista ya se cerró

    def _entrar(self):
        self._al_entrar(self._usuario.valor(), self._contrasena.valor())

    def mostrar_error(self, mensaje):
        """El controlador lo llama cuando las credenciales no son válidas."""
        self._aviso.mostrar(mensaje, "error")
        self._contrasena.limpiar()
        self._contrasena.enfocar()
