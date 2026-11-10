# Ventur – Panel de control (tkinter + MVC)

Requiere Python 3.8+ con tkinter (viene incluido en python.org y en macOS/Windows).
No necesita instalar nada más.

    python main.py

## Estructura

    main.py                      punto de entrada
    models/                      datos puros, sin tkinter
      usuario.py                 Usuario y Plan
      marca.py                   nombre y eslogan
      modulos.py                 lista de módulos (aquí se agregan/quitan)
    views/                       todo lo visual, sin lógica de negocio
      tema.py                    colores, fuentes, rectángulos redondeados
      componentes.py             TarjetaModulo, Boton
      vista_dashboard.py         panel de control
      vista_modulo.py            pantalla provisional de cada módulo
      ventana_principal.py       ventana raíz
    controllers/
      app_controller.py          une modelos y vistas, maneja la navegación
    assets/                      logo en versiones clara/oscura e iconos
    tools/generar_iconos.py      regenera los iconos (solo si usas Pillow)

## Agregar un módulo

1. Añade un `Modulo(...)` en `models/modulos.py`.
2. Pon su icono en `assets/iconos/<id>.png` (blanco sobre transparente, ~28 px).
3. En `AppController.abrir_modulo` cambia la pantalla provisional por la vista real.
