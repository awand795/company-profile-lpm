#!/usr/bin/env bash
# Ekspor dump database TERSANITASI untuk Git (RONDE 14).
# Dump asli hanya ke _backup_lokal_tidak_di_git (di luar repo).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 tools/export-dump-sanitized.py --dbcontainer "${1:-lpm-wp-db}" --out "${2:-database/mt_site.sql}"
