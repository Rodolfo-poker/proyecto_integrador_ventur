"""Controlador: conecta modelos y vistas, y decide la navegación."""
from models.marca import VENTUR
from models.modulos import RepositorioModulos
from models.usuario import Plan, Usuario
from views.ventana_principal import VentanaPrincipal
from views.vista_dashboard import VistaDashboard
from views.vista_modulo import VistaModulo


class AppController:
    def __init__(self):
        # --- Modelos ---
        self.marca = VENTUR
        self.usuario = Usuario(nombre="prax", plan=Plan("Multimarca Pro"))
        self.modulos = RepositorioModulos().todos()

        # --- Vista raíz ---
        self.ventana = VentanaPrincipal(self.marca.nombre)
        self.mostrar_dashboard()

    # --- Navegación ---
    def mostrar_dashboard(self):
        vista = VistaDashboard(
            self.ventana.contenedor, self.usuario, self.marca, self.modulos,
            al_abrir_modulo=self.abrir_modulo,
        )
        self.ventana.mostrar(vista)

    def abrir_modulo(self, modulo):
        vista = VistaModulo(self.ventana.contenedor, modulo, al_volver=self.mostrar_dashboard)
        self.ventana.mostrar(vista)

    def iniciar(self):
        self.ventana.mainloop()
