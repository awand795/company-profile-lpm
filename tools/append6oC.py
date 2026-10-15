#!/usr/bin/env python3
"""Append blok REVAMP6o (Grup C) ke mt-custom.css (UTF-8). Sekali pakai."""
from pathlib import Path

BLOCK = """
/* ============================================================
   REVAMP6o - RONDE 14 Grup C: token, smooth, bar CTA mobile (10-2026)
   Tanpa !important.
   ============================================================ */

/* --- O-C1. Token desain + hover kartu seragam --- */
body.elementor-page-59{--mt-radius-card:24px;--mt-radius-pill:999px;--mt-border:#E2E8F0;--mt-shadow-sm:0 1px 2px rgba(15,23,42,.04);--mt-shadow-md:0 10px 24px -10px rgba(15,23,42,.12);--mt-shadow-lg:0 24px 60px rgba(15,42,92,.12)}
@media (hover:hover){
body.elementor-page-59 .elementor-59 .service-grid-card:hover,
body.elementor-page-59 .elementor-59 .feature-col-1:hover,
body.elementor-page-59 .elementor-59 .feature-col-2:hover,
body.elementor-page-59 .elementor-59 .feature-col-3:hover,
body.elementor-page-59 .elementor-59 .feature-col-4:hover,
body.elementor-page-59 .elementor-59 .step-col:hover,
body.elementor-page-59 .elementor-59 .team-enterprise-card:hover,
body.elementor-page-59 .elementor-59 .testimonial-enterprise-card:hover{transform:translateY(-4px);box-shadow:var(--mt-shadow-sm),var(--mt-shadow-lg);border-color:#CBD5E1}
}

/* --- O-C2. Scroll halus (mati saat reduced-motion; margin anchor tetap 118px teruji) --- */
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}

/* --- O-C5. Bar CTA mobile: fixed hanya <=767px, statis di editor --- */
body.elementor-page-59 .elementor-59 .mt-mobile-cta{display:none}
@media (max-width:767.98px){
body.elementor-page-59 .elementor-59 .mt-mobile-cta{display:block;position:fixed;left:0;right:0;bottom:0;z-index:1021;background:rgba(255,255,255,.96);border-top:1px solid #E2E8F0;box-shadow:0 -8px 24px rgba(15,23,42,.08);padding-bottom:env(safe-area-inset-bottom)}
body.elementor-page-59 .elementor-59 .mt-mobile-cta .mt-mobile-cta-row{flex-wrap:nowrap;gap:12px}
body.elementor-page-59 .elementor-59 .mt-mobile-cta .elementor-button{min-height:56px;width:100%}
body.elementor-page-59{padding-bottom:76px}
body.elementor-page-59 .floating-wa-btn{display:none}
}
body.elementor-editor-active .elementor-59 .mt-mobile-cta,
body.elementor-editor-preview .elementor-59 .mt-mobile-cta{display:block;position:static;box-shadow:none}
"""

css = Path(__file__).resolve().parent.parent / "assets" / "css" / "mt-custom.css"
text = css.read_text(encoding="utf-8")
assert "REVAMP6o - RONDE 14 Grup C" not in text
css.write_text(text.rstrip("\n") + "\n" + BLOCK, encoding="utf-8")
print("blok Grup C ditambahkan")
