"""Controlador: conecta modelos y vistas, y decide la navegación."""
from models.marca import VENTUR
from models.modulos import RepositorioModulos
from models.productos import RepositorioProductos
from models.usuario import Plan, Usuario
from models.venta import Venta
from views.tema import dinero
from views.ventana_principal import VentanaPrincipal
from views.vista_caja import VistaCaja
from views.vista_dashboard import VistaDashboard
from views.vista_modulo import VistaModulo
from views.vista_productos import VistaProductos


class AppController:
    def __init__(self):
        # --- Modelos ---
        self.marca = VENTUR
        self.usuario = Usuario(nombre="prax", plan=Plan("Multimarca Pro"))
        self.modulos = RepositorioModulos().todos()
        self.productos = RepositorioProductos()
        self.venta = Venta()          # la venta en curso persiste aunque salgas de Caja
        self._vista_caja = None

        # --- Vista raíz ---
        self.ventana = VentanaPrincipal(self.marca.nombre)
        self.mostrar_dashboard()

    # ---------------- Navegación ----------------
    def mostrar_dashboard(self):
        vista = VistaDashboard(
            self.ventana.contenedor, self.usuario, self.marca, self.modulos,
            al_abrir_modulo=self.abrir_modulo,
        )
        self.ventana.mostrar(vista)

    def abrir_modulo(self, modulo):
        padre = self.ventana.contenedor
        if modulo.id == "productos":
            vista = VistaProductos(padre, modulo, self.mostrar_dashboard,
                                   al_buscar=self.productos.buscar)
        elif modulo.id == "caja":
            vista = VistaCaja(padre, modulo, self.mostrar_dashboard,
                              al_agregar=self.caja_agregar,
                              al_cobrar=self.caja_cobrar,
                              al_vaciar=self.caja_vaciar,
                              venta=self.venta)
            self._vista_caja = vista
        else:
            vista = VistaModulo(padre, modulo, al_volver=self.mostrar_dashboard)
        self.ventana.mostrar(vista)

    # ---------------- Caja ----------------
    def caja_agregar(self, texto):
        """Busca el producto y lo suma a la venta. Devuelve True si se agregó."""
        texto = texto.strip()
        if not texto:
            return self._caja_error("Escribe el código o el nombre del producto.")

        coincidencias = self.productos.buscar(texto)
        producto = self.productos.obtener(texto)
        if producto is None and len(coincidencias) == 1:
            producto = coincidencias[0]

        if not coincidencias:
            return self._caja_error(f"No se encontró «{texto}».")
        if producto is None:
            return self._caja_error(
                f"Hay {len(coincidencias)} coincidencias. Escribe el código o más del nombre.")
        if not self.venta.agregar(producto):
            return self._caja_error(f"No hay más existencias de {producto.descripcion}.")

        self._vista_caja.actualizar(self.venta, f"Agregado: {producto.descripcion}")
        return True

    def caja_cobrar(self):
        if self.venta.vacia:
            self._caja_error("Agrega al menos un producto para cobrar.")
            return
        total = self.venta.total
        for linea in self.venta.lineas:
            self.productos.descontar(linea.producto.id, linea.cantidad)
        self.venta.limpiar()
        self._vista_caja.actualizar(self.venta, "Venta registrada.")
        self._vista_caja.avisar(self.marca.nombre, f"Cobro realizado: {dinero(total)}")

    def caja_vaciar(self):
        self.venta.limpiar()
        self._vista_caja.actualizar(self.venta, "Venta vaciada.")

    def _caja_error(self, mensaje):
        self._vista_caja.actualizar(self.venta, mensaje, error=True)
        return False

    def iniciar(self):
        self.ventana.mainloop()
