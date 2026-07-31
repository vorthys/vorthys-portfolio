"""Генерирует растровые версии знака Vorthys: аватар, фавиконы, og-картинку."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

INK = (20, 22, 26)
PAPER = (244, 243, 239)
AMBER = (242, 194, 48)
MUTED = (138, 141, 147)

# Контуры знака в системе координат 64x64
V_FULL = [(6, 8), (22, 8), (32, 38), (42, 8), (58, 8), (38, 58), (26, 58)]
V_RIGHT = [(42, 8), (58, 8), (38, 58), (30, 58)]

SS = 4  # supersampling


def draw_mark(size, box_ratio=0.62, bg=INK, main=PAPER, accent=AMBER, radius_ratio=None):
    """Рисует знак по центру квадрата size x size."""
    canvas = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    s = size * SS

    if bg is not None:
        if radius_ratio:
            d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * radius_ratio), fill=bg)
        else:
            d.rectangle([0, 0, s, s], fill=bg)

    # знак вписывается в квадрат box_ratio от стороны, координаты 64x64 → пиксели
    box = s * box_ratio
    scale = box / 64.0
    off_x = (s - 64 * scale) / 2
    off_y = (s - 64 * scale) / 2

    def pts(seq):
        return [(off_x + x * scale, off_y + y * scale) for x, y in seq]

    d.polygon(pts(V_FULL), fill=main)
    d.polygon(pts(V_RIGHT), fill=accent)

    return canvas.resize((size, size), Image.LANCZOS)


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path)
    print("saved", name, img.size)


# --- аватар для GitHub / бирж: квадрат, знак с полями ---
save(draw_mark(512, box_ratio=0.58), "avatar-512.png")

# --- фавиконы: знак крупнее, чтобы читался в мелком размере ---
save(draw_mark(180, box_ratio=0.7, radius_ratio=0.22), "apple-touch-icon.png")
save(draw_mark(32, box_ratio=0.82), "favicon-32.png")
save(draw_mark(16, box_ratio=0.9), "favicon-16.png")

# --- .ico с двумя размерами ---
ico = draw_mark(64, box_ratio=0.86)
ico.save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("saved favicon.ico")

# --- og-картинка для превью ссылок ---
W, H = 1200, 630
og = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(og)

mark = draw_mark(300, box_ratio=0.95, bg=None)
og.paste(mark, (92, (H - 300) // 2), mark)

try:
    f_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 104)
    f_sub = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 38)
    f_small = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 28)
except OSError:
    f_title = f_sub = f_small = ImageFont.load_default()

x = 412
d.text((x, 196), "Vorthys", font=f_title, fill=PAPER)
d.text((x + 5, 326), "Web design & front-end", font=f_sub, fill=MUTED)
d.text((x + 5, 382), "Prague · vorthys.eu", font=f_small, fill=AMBER)

# перечень услуг прижат к низу — заполняет кадр и сразу говорит, чем занимаемся
d.text((x + 5, 462), "Landing pages · Business sites · Dashboards",
       font=f_small, fill=(99, 103, 110))

# янтарная линия снизу
d.rectangle([0, H - 10, W, H], fill=AMBER)

og.save(os.path.join(OUT, "og-image.png"), quality=92)
print("saved og-image.png", og.size)
