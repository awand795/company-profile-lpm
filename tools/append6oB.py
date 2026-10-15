#!/usr/bin/env python3
"""Append blok REVAMP6o (Grup B) ke mt-custom.css (UTF-8). Sekali pakai."""
from pathlib import Path

BLOCK = """
/* ============================================================
   REVAMP6o - RONDE 14 Grup B: strip merek kompak (10-2026)
   Tanpa !important. Hook .sec-principals/.principal-wall-card
   dipertahankan agar test logo lama tetap berlaku.
   ============================================================ */
body.elementor-page-59 .elementor-59 .sec-brands .brand-strip-label{text-align:center;margin-bottom:20px}
body.elementor-page-59 .elementor-59 .sec-brands .brand-logo-row{flex-wrap:wrap;row-gap:20px}
body.elementor-page-59 .elementor-59 .sec-brands .principal-wall-card{border:0;background:transparent;box-shadow:none;padding:0}
body.elementor-page-59 .elementor-59 .sec-brands .brand-logo-img img{width:auto;max-width:120px;height:30px;object-fit:contain;margin:0 auto;display:block;filter:grayscale(1);opacity:.7;transition:filter .2s ease,opacity .2s ease,transform .2s ease}
body.elementor-page-59 .elementor-59 .sec-brands .principal-wall-card:hover .brand-logo-img img{filter:grayscale(0);opacity:1}
@media (hover:hover) and (min-width:1024px){body.elementor-page-59 .elementor-59 .sec-brands .principal-wall-card:hover{transform:none;box-shadow:none;border-color:transparent}}
"""

css = Path(__file__).resolve().parent.parent / "assets" / "css" / "mt-custom.css"
text = css.read_text(encoding="utf-8")
assert "REVAMP6o" not in text
css.write_text(text.rstrip("\n") + "\n" + BLOCK, encoding="utf-8")
print("blok Grup B ditambahkan")
