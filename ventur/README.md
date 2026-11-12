# Ventur (tkinter + MVC)

Requiere Python 3.8+ con tkinter (viene incluido en python.org). No necesita instalar nada más.

    python main.py

## Acceso

| Usuario | Contraseña | Rol   |
|---------|------------|-------|
| admin   | admin123   | Dueña |

Cambia la contraseña en `models/autenticacion.py` (`CONTRASENA_DUENA`). Es una cuenta de
desarrollo: antes de usar el sistema de verdad conviene cambiarla.

## Estructura

    main.py                       punto de entrada
    models/                       datos y reglas, sin tkinter
      usuario.py                  Usuario y Rol (Dueña / Empleado)
      autenticacion.py            cuentas y verificación de contraseña (con hash)
      modulos.py                  módulos del panel y qué rol los ve
      productos.py                Producto (con estado) y RepositorioProductos
      venta.py                    la venta en curso de Caja
      marca.py                    nombre y eslogan
    views/                        todo lo visual
      tema.py                     paleta de los mockups, fuentes, utilidades
      componentes.py              Boton, Campo, Selector, Pildora, Aviso, TarjetaModulo...
      tabla.py                    tabla con botones y píldoras dentro de las filas
      vista_login.py              inicio de sesión
      vista_dashboard.py          panel de control (según rol)
      vista_base.py               barra "Volver al panel" + cuerpo común de los módulos
      vista_productos.py          módulo Productos
      vista_caja.py               módulo Caja
      formulario_producto.py      ventana de nuevo / editar producto
      vista_modulo.py             pantalla provisional de módulos sin construir
      ventana_principal.py        ventana raíz
    controllers/
      app_controller.py           une modelos y vistas: sesión, navegación, Productos, Caja
    assets/                       logo (versiones clara y oscura) e iconos
    tools/generar_iconos.py       regenera los iconos (solo si usas Pillow)

## Agregar un módulo

1. Añade un `Modulo(...)` en `models/modulos.py` (`solo_duena=True` si el empleado no debe verlo).
2. Pon su icono en `assets/iconos/<id>.png` (blanco sobre transparente, 28 px).
3. Crea su vista (hereda de `VistaBase`) y añade un `elif modulo.id == "..."` en
   `AppController.abrir_modulo`.

## Agregar un empleado

En `RepositorioUsuarios.__init__` (`models/autenticacion.py`) hay un ejemplo comentado.
