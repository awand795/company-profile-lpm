# -*- coding: utf-8 -*-
"""
tests/remove-dead-css.py — RONDE 21 (Butir 6): buang aturan CSS mati.

Membaca daftar selector mati (tests/dead-selectors.json, hasil audit crawl
semua halaman publish) lalu menghapus aturan yang seluruh selectornya mati
dari assets/css/mt-custom.css. @media/@supports dipertahankan (kosongnya
dibuang), @keyframes/@font-face/`@layer` tidak disentuh.

Pakai:  python tests/remove-dead-css.py [--apply]
Tanpa --apply hanya laporan (dry-run).
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "css" / "mt-custom.css"
DEAD = ROOT / "tests" / "dead-selectors.json"


def norm(sel: str) -> str:
    sel = re.sub(r"/\*.*?\*/", " ", sel, flags=re.S)
    sel = re.sub(r"\s+", " ", sel).strip()
    # samakan spasi di sekitar kombinator (CSSOM selalu menulis "a > b")
    sel = re.sub(r"\s*([>+~])\s*", r" \1 ", sel)
    # samakan spasi di sekitar koma (CSSOM selalu menulis "a, b")
    return re.sub(r"\s*,\s*", ", ", sel).strip()


def strip_comments(src: str) -> str:
    """Kembalikan teks dengan komentar diganti spasi (posisi karakter tetap)."""
    out = []
    i = 0
    n = len(src)
    while i < n:
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(" " * (j - i))
            i = j
        else:
            out.append(src[i])
            i += 1
    return "".join(out)


def find_close(src: str, start: int) -> int:
    """Indeks karakter '}' penutup blok yang dibuka '{' di src[start]."""
    depth = 0
    i = start
    n = len(src)
    while i < n:
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def main() -> int:
    apply = "--apply" in sys.argv
    dead = {norm(s) for s in json.loads(DEAD.read_text(encoding="utf-8"))}
    src = CSS.read_text(encoding="utf-8")
    clean = strip_comments(src)

    cuts = []          # (start, end) rentang yang dibuang)
    stats = {"rules": 0, "dead": 0, "dead_bytes": 0}

    i = 0
    n = len(clean)

    def walk(stop_at_brace: bool) -> None:
        """Parsir isi satu blok (depth saat ini)."""
        nonlocal i
        while i < n:
            # lewati spasi & baris kosong
            while i < n and clean[i] in " \t\r\n":
                i += 1
            if i >= n:
                return
            if clean[i] == "}" and stop_at_brace:
                return
            j = clean.find("{", i)
            if j == -1:
                return
            prelude = clean[i:j]
            close = find_close(clean, j)
            if close == -1:
                return
            if prelude.lstrip().startswith("@"):
                name = prelude.lstrip().split(None, 1)[0].lower()
                if name in ("@keyframes", "@-webkit-keyframes", "@font-face",
                            "@counter-style", "@property", "@layer"):
                    i = close + 1                      # blok sistem: biarkan
                    continue
                if name in ("@media", "@supports", "@container", "@scope"):
                    save = i
                    i = j + 1
                    walk(True)
                    # i menunjuk pada '}' penutup
                    inner = src[save:close]
                    if not re.search(r"[^{}@\s]", inner[len(prelude) + 1:]):
                        pass  # biarkan; blok kosong dibersihkan di bawah
                    i = close + 1
                    continue
                i = close + 1
                continue
            # aturan style biasa
            stats["rules"] += 1
            sel_norm = norm(prelude)
            if sel_norm in dead:
                stats["dead"] += 1
                stats["dead_bytes"] += close + 1 - i
                # seret spasi/baris sebelumnya bila aturan sendiri diawali baris
                start = i
                if src[:start].endswith("\n"):
                    line_start = src.rfind("\n", 0, start - 1) + 1
                    if src[line_start:start].strip() == "":
                        start = line_start
                # seret sisa baris & baris berikutnya bila hanya '\n' tersisa
                end = close + 1
                nl = src.find("\n", end)
                if nl != -1 and src[end:nl].strip() == "":
                    end = nl + 1
                cuts.append((start, end))
            i = close + 1

    walk(False)

    # buang aturan yang sudah dipotong, lalu satukan
    out = []
    prev = 0
    removed_rules = []
    for start, end in sorted(cuts):
        removed_rules.append(norm(src[start:end])[:100])
        out.append(src[prev:start])
        prev = end
    out.append(src[prev:])
    result = "".join(out)

    # bersihkan blok @media/@supports yang kini kosong
    result = re.sub(r"@[a-z-]+\([^)]*\)\s*\{\s*\}", "", result)
    result = re.sub(r"\n{3,}", "\n\n", result)

    print(f"aturan: {stats['rules']}, mati dihapus: {stats['dead']} "
          f"({stats['dead_bytes']} byte sumber)")
    print(f"ukuran: {len(src.encode('utf-8'))} -> {len(result.encode('utf-8'))} byte")
    if not apply:
        print("(dry-run, pakai --apply untuk menulis)")
        return 0
    CSS.write_text(result, encoding="utf-8", newline="\n")
    print("tulis:", CSS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
