#!/usr/bin/env bash
# Ekspor dump database TERSANITASI untuk Git (RONDE 14).
# Dump asli hanya ke _backup_lokal_tidak_di_git (di luar repo).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
# Ronde 4: di Git Bash (Windows) `python3` bisa jadi alias toko Microsoft yang
# selalu gagal — pakai `python` bila tersedia dan berfungsi.
PY=python3
if command -v python >/dev/null 2>&1 && python --version >/dev/null 2>&1; then
  PY=python
fi
echo "interpreter: $PY"
"$PY" tools/export-dump-sanitized.py --dbcontainer "${1:-lpm-wp-db}" --out "${2:-database/mt_site.sql}"
