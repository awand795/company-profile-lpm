#!/usr/bin/env python3
"""Regenerasi wp-integration/template-mastertruck.php dari index.html.

Single source of truth untuk markup: index.html. Prelude PHP (Template Name,
$mt_base/$mt_ver, dequeue khusus template) dipertahankan dari template lama
dan tidak disentuh generator.

Penggunaan:
    python3 tools/build-template.py           # tulis ulang template
    python3 tools/build-template.py --check   # hanya bandingkan; exit 1 bila beda
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
TPL = ROOT / "wp-integration" / "template-mastertruck.php"
OP = "<" + "?php "
CL = "?" + ">"


def build() -> str:
    src = INDEX.read_text(encoding="utf-8")
    old = TPL.read_text(encoding="utf-8") if TPL.exists() else ""
    doctype = "<!DOCTYPE html>"
    if doctype not in src:
        raise SystemExit("index.html tanpa doctype")
    if doctype not in old:
        raise SystemExit("template lama tanpa doctype — buat manual dulu")
    prelude = old[: old.index(doctype)]
    body = src[src.index(doctype):]

    mt = OP + "echo esc_url( $mt_base ); " + CL
    ver = OP + "echo esc_attr( $mt_ver ); " + CL

    body = body.replace('href="assets/', 'href="' + mt + "/")
    body = body.replace('src="assets/', 'src="' + mt + "/")
    body = body.replace(
        '<html lang="id">',
        "<html " + OP + "language_attributes(); " + CL + ">", 1)
    body = body.replace(
        '<meta charset="utf-8">',
        '<meta charset="' + OP + "bloginfo( 'charset' ); " + CL + '">', 1)
    body = body.replace(
        "<body>",
        "<body " + OP + "body_class(); " + CL + ">\n" + OP + "wp_body_open(); " + CL, 1)
    body = body.replace(
        "</head>", "    " + OP + "wp_head(); " + CL + "\n</head>", 1)
    body = body.replace(
        "</body>", "    " + OP + "wp_footer(); " + CL + "\n</body>", 1)

    # jQuery CDN ganda dibuang di WP (pakai bawaan inti WordPress).
    jq = '    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>\n'
    if jq not in body:
        raise SystemExit("baris jQuery CDN tak ditemukan di index.html")
    body = body.replace(jq, "")

    # Cache-busting semua URL aset template.
    body, n = re.subn(
        re.escape(mt) + r"/(css|js|lib|img|fonts)/([^\"]+)\"",
        mt + r"/\1/\2?ver=" + ver + '"', body)

    # Pengaman spinner tanpa dependensi.
    sp = "<!-- Spinner End -->"
    if body.count(sp) != 1:
        raise SystemExit("penanda Spinner End tidak unik")
    fb = (sp + "\n    <script>window.addEventListener(\"load\",function(){"
          "var s=document.getElementById(\"spinner\");if(s){s.classList.remove(\"show\");}"
          "setTimeout(function(){var x=document.getElementById(\"spinner\");"
          "if(x&&x.classList.contains(\"show\")){x.style.display=\"none\";}},4000);});</script>")
    body = body.replace(sp, fb)
    return prelude + body


def main() -> int:
    out = build()
    current = TPL.read_text(encoding="utf-8") if TPL.exists() else ""
    if "--check" in sys.argv:
        if out == current:
            print("PARITY OK: template sesuai hasil regen index.html")
            return 0
        print("PARITY FAIL: template berbeda dari hasil regen index.html")
        print("Jalankan tanpa --check untuk menulis ulang, lalu review diff.")
        return 1
    TPL.write_text(out, encoding="utf-8")
    print("template ditulis ulang: %s (%d bytes)" % (TPL, len(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
