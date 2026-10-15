#!/usr/bin/env python3
"""0.4 Arsipkan _backup_* -> archive/backups (PINDAH, bukan salin).

Hanya file teks kode yang masuk arsip Git:
  py, css, js, cjs, json, php, html, md, ps1, sh (<= 1 MB).
Lainnya (sql/dump/zip/gambar/video/besar/node_modules/vendor/kunci)
  -> _backup_lokal_tidak_di_git/<tanggal>/ (di luar repo, tidak di-git).
"""
import shutil
from datetime import date
from pathlib import Path

ROOT = Path('.')
ARCH = ROOT / 'archive' / 'backups'
ARCH.mkdir(parents=True, exist_ok=True)
LOKAL = ROOT.parent / '_backup_lokal_tidak_di_git' / date.today().strftime('%Y%m%d')
LOKAL.mkdir(parents=True, exist_ok=True)

CODE_EXT = {'.py', '.css', '.js', '.cjs', '.json', '.php', '.html', '.md', '.ps1', '.sh'}
MAX = 1_000_000

moved_code, moved_lokal, skipped = 0, 0, []
for d in sorted(ROOT.glob('_backup_*')):
    if not d.is_dir():
        continue
    dest = ARCH / d.name
    dest.mkdir(parents=True, exist_ok=True)
    for f in list(d.rglob('*')):
        if not f.is_file():
            continue
        rel = f.relative_to(d)
        if f.suffix.lower() in CODE_EXT and f.stat().st_size <= MAX:
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(target))
            moved_code += 1
        else:
            target = LOKAL / d.name / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(target))
            moved_lokal += 1
    # hapus dir kosong
    for sub in sorted(d.rglob('*'), reverse=True):
        if sub.is_dir() and not any(sub.iterdir()):
            sub.rmdir()
    if d.exists() and not any(d.iterdir()):
        d.rmdir()
        print(f'{d.name} -> arsip (dir lama dihapus)')
    else:
        skipped.append(d.name)
        print(f'{d.name} -> arsip (SISA, cek manual)')

print(f'\ncode -> archive: {moved_code} file')
print(f'binari -> lokal: {moved_lokal} file')
print('tersisa:', skipped)
