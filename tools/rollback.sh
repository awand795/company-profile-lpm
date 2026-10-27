#!/usr/bin/env bash
# Rollback repo + deploy ulang ke tag/hash tertentu (tanpa rewrite history).
#   rollback.sh <tag-atau-hash> [--restore-db] [--whatif]
set -euo pipefail
TO="${1:-}"; RESTORE=0; WHATIF=0
for a in "$@"; do case "$a" in --restore-db) RESTORE=1;; --whatif) WHATIF=1;; esac; done
[[ -z "$TO" ]] && { echo "pakai: rollback.sh <ref> [--restore-db] [--whatif]"; exit 1; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
FILES=$(git diff --name-only "$TO" -- . | grep -v -e '^playwright_review/' -e '^scratch/' || true)
[[ -z "$FILES" ]] && { echo "Tidak ada perbedaan dengan $TO."; exit 0; }
echo "File yang akan di-restore ke $TO:"; echo "$FILES"
[[ $WHATIF -eq 1 ]] && exit 0
git restore --source="$TO" --staged --worktree -- $FILES
if [[ $RESTORE -eq 1 ]]; then
  git show "$TO:database/mt_site.sql" > /tmp/mt_rollback_dump.sql
  docker cp /tmp/mt_rollback_dump.sql lpm-wp-app:/tmp/restore.sql
  docker exec lpm-wp-app sh -c "mariadb -uwordpress -plotus_wp_password_2026 wordpress < /tmp/restore.sql && rm -f /tmp/restore.sql"
  rm -f /tmp/mt_rollback_dump.sql
  echo "OK database dari $TO diimpor (kata sandi admin perlu diatur ulang)"
fi
# --force: rollback memang sengaja menimpa data live (hash build lama tidak cocok).
python3 tools/build-stitch-elementor.py --force
bash sync-to-wp.sh
docker exec lpm-wp-app wp --allow-root --path=/var/www/html elementor flush-css >/dev/null
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
node tests/verify-revamp3.cjs | tail -2
git add $FILES
git commit -m "rollback ke $TO"
git push origin main
