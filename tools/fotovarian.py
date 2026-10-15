#!/usr/bin/env python3
"""A1: 3 varian foto hero + contact sheet (Pillow, sekali jalan)."""
from PIL import Image, ImageOps
from pathlib import Path

SRC = Path('wp-content/uploads/2026/10/mt6-hero-bengkel.webp')
OUT = Path('playwright_review/sesudah_revamp6o')
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert('RGB')
print('sumber:', img.size)

LUT_G = [min(255, round(255 * (i / 255) ** 0.85)) for i in range(256)]
a = Image.merge('RGB', [c.point(LUT_G) for c in img.split()])

def grade(im, amt=10):
    r, g, b = im.split()
    L = im.convert('L')
    r = Image.composite(Image.new('L', im.size, 0), r, L.point(lambda v: int(amt * v / 255)))
    b = Image.composite(Image.new('L', im.size, 255), b, L.point(lambda v: int(amt * v / 255)))
    return Image.merge('RGB', (r, g, b))

b = grade(a)

LUT_C = [min(255, max(0, round(128 + (i - 128) * 1.08))) for i in range(256)]
c = Image.merge('RGB', [ch.point(LUT_C) for ch in b.split()])

for name, im in [('a-gamma', a), ('b-grading', b), ('c-kontras', c)]:
    p = OUT / f'hero-{name}.webp'
    im.save(p, 'WEBP', quality=82, method=6)
    print(name, p.stat().st_size // 1024, 'KB')

# contact sheet: asli + 3 varian
thumb_w = 640
items = [('ASLI', img), ('(a) gamma 0.85', a), ('(b) + grading biru', b), ('(c) + kontras', c)]
thumbs = []
for label, im in items:
    t = im.copy()
    t.thumbnail((thumb_w, 10_000))
    thumbs.append((label, t))
W = thumb_w * 2 + 30
H = max(thumbs[0][1].height + thumbs[1][1].height, thumbs[2][1].height + thumbs[3][1].height) + 30
sheet = Image.new('RGB', (W, H), 'white')
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
pos = [(10, 10), (thumb_w + 20, 10), (10, 10 + thumbs[0][1].height + 10), (thumb_w + 20, 10 + thumbs[2][1].height + 10)]
for (label, t), (x, y) in zip(thumbs, pos):
    sheet.paste(t, (x, y))
    d.text((x + 8, y + 8), label, fill='yellow')
sheet.save(OUT / 'foto-varian.png')
print('contact sheet ok')
