#!/usr/bin/env python3
"""C3+C4: og:image 1200x630 + favicon MT (Pillow, sekali jalan)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path('wp-content/uploads/2026/10')
ARIALBD = 'C:/Windows/Fonts/arialbd.ttf'
ARIAL = 'C:/Windows/Fonts/arial.ttf'

hero = Image.open(OUT / 'mt6-hero-terang.webp').convert('RGB')

# --- og:image 1200x630: cover-crop + overlay terang + chip + teks ---
W, H = 1200, 630
scale = max(W / hero.width, H / hero.height)
bg = hero.resize((int(hero.width * scale) + 1, int(hero.height * scale) + 1), Image.LANCZOS)
x = (bg.width - W) // 2
y = int((bg.height - H) * 0.35)
bg = bg.crop((x, y, x + W, y + H))
overlay = Image.new('RGB', (W, H), (239, 246, 255))
og = Image.blend(bg, overlay, 0.28)
d = ImageDraw.Draw(og)
f_big = ImageFont.truetype(ARIALBD, 64)
f_sub = ImageFont.truetype(ARIAL, 34)
# chip biru
d.rounded_rectangle([70, 66, 150, 146], radius=22, fill=(37, 99, 235))
d.text((110, 106), 'MT', font=ImageFont.truetype(ARIALBD, 44), fill='white', anchor='mm')
d.text((180, 78), 'MASTER TRUCK', font=f_big, fill=(15, 42, 92))
d.text((180, 158), 'Bengkel Truk KIM III Medan', font=f_sub, fill=(71, 85, 105))
og.save(OUT / 'mt-og-cover.webp', 'WEBP', quality=82, method=6)
print('og:', (OUT / 'mt-og-cover.webp').stat().st_size // 1024, 'KB')

# --- favicon MT: 512 + 180 + 32 + 16 ---
def favicon(size, name):
    im = Image.new('RGB', (size, size), (37, 99, 235))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 5, fill=(37, 99, 235))
    f = ImageFont.truetype(ARIALBD, int(size * 0.48))
    d.text((size // 2, size // 2), 'MT', font=f, fill='white', anchor='mm')
    im.save(OUT / name, 'PNG')
    print(name, (OUT / name).stat().st_size // 1024, 'KB')

favicon(512, 'mt-favicon-512.png')
favicon(180, 'mt-favicon-180.png')
favicon(32, 'mt-favicon-32.png')
favicon(16, 'mt-favicon-16.png')
