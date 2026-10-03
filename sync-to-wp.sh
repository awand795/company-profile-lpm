#!/usr/bin/env bash
# Mirror dari sync-to-wp.ps1 untuk Linux/macOS.
# Menyalin wp-integration/* ke folder theme WordPress aktif di container.
#
#   ./sync-to-wp.sh
#   ./sync-to-wp.sh -c lotus-wp-app -t astra
set -euo pipefail

CONTAINER="lotus-wp-app"
THEME=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--container) CONTAINER="$2"; shift 2 ;;
    -t|--theme) THEME="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [-c container] [-t theme]"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/wp-integration"
[[ -d "$SRC" ]] || { echo "Folder wp-integration tidak ditemukan di $SRC" >&2; exit 1; }

if ! docker ps --filter "name=^/${CONTAINER}$" --format '{{.Names}}' | grep -q .; then
  echo "Container '$CONTAINER' tidak berjalan. Jalankan dulu: docker compose up -d" >&2
  exit 1
fi

if [[ -z "$THEME" ]]; then
  THEME="$(docker exec "$CONTAINER" php -r 'define("ABSPATH","/var/www/html/"); require ABSPATH."wp-load.php"; echo get_option("template");' 2>/dev/null || true)"
fi
[[ -n "$THEME" ]] || { echo "Tidak bisa menentukan theme aktif. Pakai: $0 -t <slug>" >&2; exit 1; }

echo "Theme aktif : $THEME"
THEME_PATH="/var/www/html/wp-content/themes/$THEME"
docker exec "$CONTAINER" mkdir -p "$THEME_PATH/mastertruck"
docker cp "$SRC/mastertruck/." "$CONTAINER:$THEME_PATH/mastertruck/"
echo "OK  mastertruck/"
docker cp "$SRC/template-mastertruck.php" "$CONTAINER:$THEME_PATH/template-mastertruck.php"
echo "OK  template-mastertruck.php"
docker exec "$CONTAINER" chown -R www-data:www-data "$THEME_PATH/mastertruck" "$THEME_PATH/template-mastertruck.php"
echo ""
echo "Sinkronisasi selesai. Theme: $THEME"
echo "Template: Page Editor -> Page Template -> 'Master Truck Landing'"
