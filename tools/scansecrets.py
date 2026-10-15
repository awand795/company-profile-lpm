#!/usr/bin/env python3
"""0.2.2 Pemindaian rahasia pada file yang akan di-commit (teks saja)."""
import re
from pathlib import Path

PATS = ['password', 'passwd', 'secret', 'token', 'api_key', 'DB_PASSWORD',
        'AUTH_KEY', 'SECURE_AUTH', 'NONCE_', '-----BEGIN', 'Bearer ',
        'ghp_', 'AKIA', 'smtp']
SKIP_DIRS = {'.git', 'node_modules', '_backup_lokal_tidak_di_git'}
SKIP_EXT = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.sql', '.pack', '.idx'}
SKIP_FILES = {'package-lock.json'}

root = Path('.')
hits = []
for f in root.rglob('*'):
    if not f.is_file():
        continue
    if any(d in f.parts for d in SKIP_DIRS):
        continue
    if f.suffix.lower() in SKIP_EXT or f.name in SKIP_FILES:
        continue
    try:
        if f.stat().st_size > 2_000_000:
            continue
        text = f.read_text(encoding='utf-8', errors='strict')
    except Exception:
        continue
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for p in PATS:
            if p.lower() in low:
                hits.append((str(f), i, p, line.strip()[:100]))
                break

print(f'{len(hits)} baris mencurigakan:')
seen = set()
with open('scan-hits.txt', 'w', encoding='utf-8') as fh:
    for f, i, p, line in hits:
        key = (f, p)
        if key in seen:
            continue
        seen.add(key)
        fh.write(f'{f}:{i} [{p}] {line}\n')
for f, i, p, line in hits[:60]:
    try:
        print(f'{f}:{i} [{p}] {line}')
    except UnicodeEncodeError:
        print(f'{f}:{i} [{p}] (non-ascii)')
