#!/usr/bin/env bash
# Mirror dari sync-to-wp.ps1 untuk Linux/macOS.
# Menyalin wp-integration/* ke folder theme WordPress aktif di container,
# plus media wp-content/uploads/ dan plugin mt-topbar (bila folder-nya ada).
#
#   ./sync-to-wp.sh
#   ./sync-to-wp.sh -c lotus-wp-app -t astra
set -euo pipefail

# Ronde 4: di Git Bash (Windows) MSYS mengonversi argumen absolut yang diawali
# "/" menjadi jalur Windows (mis. /var/www/... -> C:/Program Files/Git/var/www/...).
# Kecualikan jalur container (/var/...); jalur sumber repo tetap dikonversi
# agar docker cp di Windows tetap menemukan file.
export MSYS2_ARG_CONV_EXCL="/var"

CONTAINER="lpm-wp-app"
THEME=""
LEGACY_TEMPLATE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--container) CONTAINER="$2"; shift 2 ;;
    -t|--theme) THEME="$2"; shift 2 ;;
    --legacy-template) LEGACY_TEMPLATE=true; shift 1 ;;
    -h|--help)
      echo "Usage: $0 [-c container] [-t theme] [--legacy-template]"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/wp-integration"
[[ -d "$SRC" ]] || { echo "Folder wp-integration tidak ditemukan di $SRC" >&2; exit 1; }

# Catatan Ronde 4: filter `name=` pada Docker versi ini tidak lagi memasukkan
# awalan "/" pada nama kontainer — pola lama `^/nama$` selalu kosong.
if ! docker ps --filter "name=^/?${CONTAINER}$" --format '{{.Names}}' | grep -q .; then
  echo "Container '$CONTAINER' tidak berjalan. Jalankan dulu: docker compose up -d" >&2
  exit 1
fi

if [[ -z "$THEME" ]]; then
  THEME="$(docker exec "$CONTAINER" php -r 'define("ABSPATH","/var/www/html/"); require ABSPATH."wp-load.php"; echo get_option("template");' 2>/dev/null || true)"
fi
[[ -n "$THEME" ]] || { echo "Tidak bisa menentukan theme aktif. Pakai: $0 -t <slug>" >&2; exit 1; }

echo "Theme aktif : $THEME"
THEME_PATH="/var/www/html/wp-content/themes/$THEME"

# CATATAN RONDE 7: Beranda resmi diedit via Elementor Page 59.
# Template PHP lama (template-mastertruck.php) tidak dibangun ulang otomatis kecuali flag --legacy-template diberikan.
if [[ "$LEGACY_TEMPLATE" = true ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 "$ROOT/tools/build-template.py" || echo "WARN  regen template gagal, pakai file ter-commit" >&2
  else
    echo "WARN  python3 tak ada, template tidak diregenerasi" >&2
  fi
  docker cp "$SRC/template-mastertruck.php" "$CONTAINER:$THEME_PATH/template-mastertruck.php"
  echo "OK  template-mastertruck.php (Legacy)"
  if [[ -f "$SRC/template-bizniz.php" ]]; then
    docker cp "$SRC/template-bizniz.php" "$CONTAINER:$THEME_PATH/template-bizniz.php"
    echo "OK  template-bizniz.php (Legacy)"
  fi
fi
docker exec "$CONTAINER" mkdir -p "$THEME_PATH/mastertruck"
# Ronde 4: `docker cp src/. dest` ternyata menyalin FOLDER src ke dalam dest
# (menghasilkan mastertruck/mastertruck/), sehingga file yang dimuat halaman
# tidak pernah ter-update. Salin file per file agar isi ikut terbarui.
while IFS= read -r rel; do
  [[ -n "$rel" ]] || continue
  docker exec "$CONTAINER" mkdir -p "$THEME_PATH/mastertruck/$(dirname "$rel")"
  docker cp "$SRC/mastertruck/$rel" "$CONTAINER:$THEME_PATH/mastertruck/$rel"
done < <(cd "$SRC/mastertruck" && find . -type f | sed 's|^./||')
echo "OK  mastertruck/ (file per file)"
docker exec "$CONTAINER" chown -R www-data:www-data \
  "$THEME_PATH/mastertruck" "$THEME_PATH/template-mastertruck.php" "$THEME_PATH/template-bizniz.php" 2>/dev/null || true

# Media (slide hero, logo merek, avatar) — opsional bila folder belum ada.
if [[ -d "$ROOT/wp-content/uploads" ]]; then
  docker cp "$ROOT/wp-content/uploads/." "$CONTAINER:/var/www/html/wp-content/uploads/"
  docker exec "$CONTAINER" chown -R www-data:www-data /var/www/html/wp-content/uploads || true
  echo "OK  wp-content/uploads/ ($(find "$ROOT/wp-content/uploads" -type f | wc -l | tr -d ' ') file)"
fi

# Plugin topbar korporat (diaktifkan setup.sh).
if [[ -d "$ROOT/wp-content/plugins/mt-topbar" ]]; then
  docker cp "$ROOT/wp-content/plugins/mt-topbar/." "$CONTAINER:/var/www/html/wp-content/plugins/mt-topbar/"
  docker exec "$CONTAINER" chown -R www-data:www-data /var/www/html/wp-content/plugins/mt-topbar
  echo "OK  plugins/mt-topbar/"
fi

# Plugin admin bersih (diaktifkan setup.sh).
for plug in mt-booking mt-login mt-admin; do
  if [[ -d "$ROOT/wp-content/plugins/$plug" ]]; then
    docker cp "$ROOT/wp-content/plugins/$plug/." "$CONTAINER:/var/www/html/wp-content/plugins/$plug/"
    docker exec "$CONTAINER" chown -R www-data:www-data "/var/www/html/wp-content/plugins/$plug"
    docker exec "$CONTAINER" wp plugin activate "$plug" --allow-root --path=/var/www/html >/dev/null 2>&1 || true
    echo "OK  plugins/$plug/"
  fi
done

# Homepage ID 59 sekarang FULL ELEMENTOR (migrasi 2026-10-07).
# JANGAN paksa kembali ke template-mastertruck.php — itu menonaktifkan Elementor.
# Pastikan homepage pakai template default + Elementor builder.
CUR_TPL="$(docker exec "$CONTAINER" wp post meta get 59 _wp_page_template --allow-root --path=/var/www/html 2>/dev/null || true)"
if [[ "$CUR_TPL" == "template-mastertruck.php" ]]; then
  docker exec "$CONTAINER" wp post meta delete 59 _wp_page_template --allow-root --path=/var/www/html >/dev/null 2>&1 || true
  echo "OK  homepage(ID 59) dilepas dari template-mastertruck.php -> Elementor (was: template-mastertruck.php)"
else
  echo "OK  homepage(ID 59) Elementor (template: ${CUR_TPL:-default})"
fi
docker exec "$CONTAINER" wp rewrite flush --allow-root --path=/var/www/html >/dev/null 2>&1 || true

# Verifikasi paritas repo <-> deploy (non-fatal, hanya peringatan).
bash "$ROOT/tools/verify-parity.sh" || true

echo ""
echo "Sinkronisasi selesai. Theme: $THEME"
echo "Homepage ID 59: Elementor full (Edit with Elementor)"
