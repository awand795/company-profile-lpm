#!/usr/bin/env python3
"""
RONDE 22 (B5): og:image 1200x630 tema HITAM-EMAS + favicon dari LOGO resmi
(mastertruck_official_logo.png — diukur: latar #090909, emas #CEA44B).

- OG: foto bengkel di-cover lalu digelapkan ke arah ink (0.60), logo resmi
  menempel tanpa kotak (latar logo = latar OG), garis emas + teks silver/emas.
- Favicon: kotak ink + logo di-contain (ukuran sama dengan file lama agar
  turunan WP Site Icon -150x150 / -300x300 cukup ditimpa).

Pemakaian: python tools/makeog.py
"""
from PIL import Image
from pathlib import Path

OUT = Path('wp-content/uploads/2026/10')
LOGO = Path('wp-content/uploads/stitch/mastertruck_official_logo.png')

INK = (9, 9, 9)          # #090909 — sama dengan sudut logo
GOLD = (198, 154, 67)    # #C69A43 — emas utama
GOLD_L = (228, 189, 100)  # #E4BD64
SILVER = (216, 216, 216)  # #D8D8D8

ARIALBD = 'C:/Windows/Fonts/arialbd.ttf'
ARIAL = 'C:/Windows/Fonts/arial.ttf'

logo = Image.open(LOGO).convert('RGB')

# --- og:image 1200x630: cover-crop + gelap ink + logo + teks emas ---
W, H = 1200, 630
hero = Image.open(OUT / 'mt6-hero-terang.webp').convert('RGB')
scale = max(W / hero.width, H / hero.height)
bg = hero.resize((int(hero.width * scale) + 1, int(hero.height * scale) + 1), Image.LANCZOS)
x = (bg.width - W) // 2
y = int((bg.height - H) * 0.35)
bg = bg.crop((x, y, x + W, y + H))
ink = Image.new('RGB', (W, H), INK)
og = Image.blend(bg, ink, 0.60)          # foto tetap terlihat, nada hitam

# logo resmi (latar sama persis = tanpa kotak terlihat)
lh = 132
lw = int(logo.width * lh / logo.height)
og.paste(logo.resize((lw, lh), Image.LANCZOS), (74, 64))

# garis aksen emas + teks
from PIL import ImageDraw, ImageFont
d = ImageDraw.Draw(og)
d.rectangle([76, 236, 76 + 240, 241], fill=GOLD)
d.text((76, 274), 'Bengkel Truk KIM III Medan',
       font=ImageFont.truetype(ARIALBD, 54), fill=SILVER)
d.text((76, 348), 'Spesialis Truk & Armada Niaga',
       font=ImageFont.truetype(ARIAL, 34), fill=GOLD_L)
d.rectangle([0, H - 8, W, H], fill=GOLD)
og.save(OUT / 'mt-og-cover.webp', 'WEBP', quality=84, method=6)
print('og:', (OUT / 'mt-og-cover.webp').stat().st_size // 1024, 'KB')


# --- favicon: kotak ink + logo contain (turunan ukuran ditimpa) ---
def favicon(size, name):
    im = Image.new('RGB', (size, size), INK)
    avail = int(size * 0.94)
    lw = avail
    lh = int(logo.height * lw / logo.width)
    if lh > avail:
        lh = avail
        lw = int(logo.width * lh / logo.height)
    l2 = logo.resize((lw, lh), Image.LANCZOS)
    im.paste(l2, ((size - lw) // 2, (size - lh) // 2))
    im.save(OUT / name, 'PNG')
    print(name, (OUT / name).stat().st_size // 1024, 'KB')


favicon(512, 'mt-favicon-512.png')
favicon(180, 'mt-favicon-180.png')
favicon(32, 'mt-favicon-32.png')
favicon(16, 'mt-favicon-16.png')

# turunan yang di-generate WP Site Icon (ada di container, bukan di repo)
from PIL import Image as _I
base = _I.open(OUT / 'mt-favicon-512.png')
base.resize((150, 150), Image.LANCZOS).save(OUT / 'mt-favicon-512-150x150.png')
base.resize((300, 300), Image.LANCZOS).save(OUT / 'mt-favicon-512-300x300.png')
print('turunan 150/300 dibuat')