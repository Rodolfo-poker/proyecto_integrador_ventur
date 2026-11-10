"""
Genera los iconos de los módulos como PNG blancos con fondo transparente.

Solo hace falta ejecutarlo si quieres cambiar los iconos (requiere Pillow).
La aplicación en sí NO necesita Pillow: lee los PNG ya generados.

    pip install pillow
    python tools/generar_iconos.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

SALIDA = Path(__file__).resolve().parent.parent / "assets" / "iconos"
LIENZO = 192          # se dibuja grande y se reduce (suaviza los bordes)
TAM_FINAL = 28        # tamaño del icono dentro de la tarjeta
TRAZO = 13
BLANCO = (255, 255, 255, 255)


class Pincel:
    def __init__(self):
        self.img = Image.new("RGBA", (LIENZO, LIENZO), (255, 255, 255, 0))
        self.d = ImageDraw.Draw(self.img)

    def _punto(self, x, y):
        r = TRAZO / 2
        self.d.ellipse((x - r, y - r, x + r, y + r), fill=BLANCO)

    def linea(self, *pts, cerrada=False):
        pts = list(pts) + ([pts[0]] if cerrada else [])
        self.d.line(pts, fill=BLANCO, width=TRAZO, joint="curve")
        for p in pts:
            self._punto(*p)

    def rect(self, x1, y1, x2, y2, r=16):
        self.d.rounded_rectangle((x1, y1, x2, y2), radius=r, outline=BLANCO, width=TRAZO)

    def circulo(self, cx, cy, r, relleno=False):
        self.d.ellipse((cx - r, cy - r, cx + r, cy + r),
                       outline=None if relleno else BLANCO,
                       fill=BLANCO if relleno else None, width=TRAZO)

    def arco(self, caja, ini, fin):
        self.d.arc(caja, ini, fin, fill=BLANCO, width=TRAZO)

    def guardar(self, nombre):
        SALIDA.mkdir(parents=True, exist_ok=True)
        self.img.resize((TAM_FINAL, TAM_FINAL), Image.LANCZOS).save(SALIDA / f"{nombre}.png")


def apartados():
    p = Pincel()
    p.rect(26, 38, 166, 80, 12)
    p.rect(40, 80, 152, 156, 12)
    p.linea((80, 108), (112, 108))
    p.guardar("apartados")


def caja():
    p = Pincel()
    p.rect(24, 52, 168, 150, 20)
    p.linea((24, 90), (168, 90))
    p.circulo(134, 124, 8, relleno=True)
    p.guardar("caja")


def categorias():
    p = Pincel()
    for x, y in ((28, 28), (108, 28), (28, 108), (108, 108)):
        p.rect(x, y, x + 56, y + 56, 12)
    p.guardar("categorias")


def clientes():
    p = Pincel()
    p.circulo(80, 66, 26)
    p.arco((30, 108, 130, 208), 180, 360)
    p.circulo(140, 78, 18)
    p.arco((116, 112, 170, 170), 200, 340)
    p.guardar("clientes")


def comisiones():
    p = Pincel()
    p.circulo(60, 60, 20)
    p.circulo(132, 132, 20)
    p.linea((152, 40), (40, 152))
    p.guardar("comisiones")


def descuentos():
    p = Pincel()
    p.linea((36, 36), (100, 36), (160, 96), (100, 156), (36, 96), cerrada=True)
    p.circulo(72, 72, 8, relleno=True)
    p.guardar("descuentos")


def marcas():
    p = Pincel()
    p.linea((56, 30), (136, 30), (136, 162), (96, 128), (56, 162), cerrada=True)
    p.guardar("marcas")


def ordenes():
    p = Pincel()
    p.rect(44, 42, 148, 166, 16)
    p.rect(72, 24, 120, 56, 10)
    p.linea((68, 98), (124, 98))
    p.linea((68, 130), (124, 130))
    p.guardar("ordenes")


def productos():
    p = Pincel()
    p.linea((96, 26), (156, 61), (156, 131), (96, 166), (36, 131), (36, 61), cerrada=True)
    p.linea((36, 61), (96, 96), (156, 61))
    p.linea((96, 96), (96, 166))
    p.guardar("productos")


def registros():
    p = Pincel()
    p.rect(38, 28, 154, 164, 16)
    p.linea((66, 70), (126, 70))
    p.linea((66, 98), (126, 98))
    p.linea((66, 126), (104, 126))
    p.guardar("registros")


def tickets():
    p = Pincel()
    p.rect(22, 50, 170, 142, 16)
    for y in range(66, 132, 22):
        p.linea((122, y), (122, y + 8))
    p.linea((50, 82), (92, 82))
    p.linea((50, 110), (80, 110))
    p.guardar("tickets")


def verificacion():
    p = Pincel()
    p.rect(30, 30, 162, 162, 20)
    p.linea((62, 98), (88, 124), (132, 70))
    p.guardar("verificacion")


if __name__ == "__main__":
    for fn in (apartados, caja, categorias, clientes, comisiones, descuentos,
               marcas, ordenes, productos, registros, tickets, verificacion):
        fn()
    print(f"Iconos generados en {SALIDA}")
