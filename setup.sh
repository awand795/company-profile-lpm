#!/usr/bin/env bash
# =============================================================================
# MASTER TRUCK — Bootstrap WordPress dari nol (Linux/macOS/WSL/Git Bash)
# Pasangan dari setup.ps1 (Windows PowerShell).
#
#   ./setup.sh            # compose up + import dump + install tema/plugin + sync
#   ./setup.sh --rebuild  # hancurkan volume lama dulu (fresh total)
#   ./setup.sh --skip-import  # lewati import database_dump.sql
#
# Alur:
#   1. docker compose up -d, tunggu MariaDB siap
#   2. Salin .htaccess, wp-content/uploads/, plugins/mt-topbar/ ke container
#   3. Install WP-CLI di container (unduh wp-cli.phar)
#   4. Import database_dump.sql  -> WordPress langsung "ter-instal"
#   5. Install + aktifkan theme astra, plugin elementor & astra-sites
#   6. sync-to-wp.sh (template page + aset tema + media)
#   7. Flush permalink & regenerate CSS Elementor
#   8. Verifikasi HTTP 200 pada halaman utama
#
# BUTUH INTERNET sekali saat pertama: wp-cli.phar, theme astra, plugin
# elementor & astra-sites (unduhan dari wordpress.org / GitHub).
# =============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

APP="${MT_APP:-lotus-wp-app}"
DB="${MT_DB:-lotus-wp-db}"
DB_USER="${MT_DB_USER:-wordpress}"
DB_PASS="${MT_DB_PASS:-lotus_wp_password_2026}"
DB_NAME="${MT_DB_NAME:-wordpress}"
URL="${MT_URL:-http://localhost:8080}"
DO_REBUILD=0
DO_IMPORT=1

for arg in "$@"; do
  case "$arg" in
    -r|--rebuild)   DO_REBUILD=1 ;;
    --skip-import)  DO_IMPORT=0 ;;
    -h|--help)
      sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Argumen tidak dikenal: $arg (lihat --help)" >&2; exit 1 ;;
  esac
done

step() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
ok()   { printf '  \033[1;32mOK\033[0m  %s\n' "$*"; }
fail() { printf '  \033[1;31mGAGAL\033[0m %s\n' "$*" >&2; exit 1; }

# --- 0. Pra-syarat -----------------------------------------------------------
step "Cek prasyarat"
command -v docker >/dev/null 2>&1 || fail "docker tidak ditemukan. Install Docker Desktop / docker engine dulu."
if docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  fail "Perintah 'docker compose' / 'docker-compose' tidak ada."
fi
[[ -f docker-compose.yml ]] || fail "docker-compose.yml tidak ditemukan di $ROOT"
[[ -f database_dump.sql ]]  || fail "database_dump.sql tidak ditemukan di $ROOT"
ok "compose: $COMPOSE"

# --- 1. Stack ----------------------------------------------------------------
if [[ $DO_REBUILD -eq 1 ]]; then {
  step "Rebuild volume (down -v)"
  $COMPOSE down -v --remove-orphans
} fi

step "docker compose up -d"
$COMPOSE up -d
ok "stack naik"

step "Menunggu MariaDB siap"
db_ready=0
for _ in $(seq 1 60); do
  if docker exec -e "MYSQL_PWD=$DB_PASS" "$DB" mariadb-admin ping -h127.0.0.1 -u"$DB_USER" --silent >/dev/null 2>&1; then
    db_ready=1; break
  fi
  sleep 2
done
[[ $db_ready -eq 1 ]] || fail "MariaDB tidak siap setelah 120 detik."
ok "MariaDB siap"

# --- 2. Salin berkas statis ke container ------------------------------------
step "Salin .htaccess + wp-content/uploads + plugins/mt-topbar"
if [[ -f .htaccess ]]; then
  docker cp .htaccess "$APP:/var/www/html/.htaccess" || fail "docker cp .htaccess gagal"
  ok ".htaccess"
fi
if [[ -d wp-content/uploads ]]; then
  docker cp wp-content/uploads/. "$APP:/var/www/html/wp-content/uploads/" || fail "docker cp uploads gagal"
  ok "wp-content/uploads/ ($(find wp-content/uploads -type f | wc -l | tr -d ' ') file)"
fi
if [[ -d wp-content/plugins/mt-topbar ]]; then
  docker cp wp-content/plugins/mt-topbar/. "$APP:/var/www/html/wp-content/plugins/mt-topbar/" || fail "docker cp mt-topbar gagal"
  ok "plugins/mt-topbar/"
fi
docker exec "$APP" chown -R www-data:www-data \
  /var/www/html/.htaccess \
  /var/www/html/wp-content/uploads \
  /var/www/html/wp-content/plugins/mt-topbar || true

# --- 3. WP-CLI ---------------------------------------------------------------
step "Pasang WP-CLI (di dalam container)"
docker exec "$APP" sh -c 'command -v wp >/dev/null 2>&1 && exit 0
  echo "  mengunduh wp-cli.phar ..."
  curl -sSL -o /tmp/wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar || exit 11
  chmod +x /tmp/wp-cli.phar
  mv /tmp/wp-cli.phar /usr/local/bin/wp
  wp --version --allow-root >/dev/null || exit 12' || fail "Gagal memasang WP-CLI (cek koneksi internet)."
WP="docker exec $APP wp --allow-root --path=/var/www/html"
$WP --version >/dev/null || fail "WP-CLI tidak bisa dijalankan."
ok "WP-CLI siap"

# --- 4. Import database ------------------------------------------------------
if [[ $DO_IMPORT -eq 1 ]]; then
  step "Import database_dump.sql"
  RESTORE_SRC="database_dump.sql"
  # Dump hasil ekspor Windows sering UTF-16 (BOM FFFE) yang ditolak klien
  # mariadb ("ASCII '\0' appeared..."). Konversi dulu ke UTF-8 bila perlu.
  if file database_dump.sql | grep -qi 'UTF-16'; then
    command -v iconv >/dev/null 2>&1 || fail "Dump UTF-16 butuh 'iconv' untuk konversi."
    iconv -f UTF-16 -t UTF-8 database_dump.sql -o /tmp/mt_restore_utf8.sql \
      || fail "Konversi UTF-16 -> UTF-8 gagal."
    RESTORE_SRC="/tmp/mt_restore_utf8.sql"
    ok "dump UTF-16 dikonversi ke UTF-8"
  fi
  docker cp "$RESTORE_SRC" "$DB:/tmp/restore.sql"
  docker exec -e "MYSQL_PWD=$DB_PASS" "$DB" sh -c "mariadb -u'$DB_USER' '$DB_NAME' < /tmp/restore.sql && rm -f /tmp/restore.sql" \
    || fail "Import dump gagal."
  [[ "$RESTORE_SRC" == /tmp/mt_restore_utf8.sql ]] && rm -f /tmp/mt_restore_utf8.sql
  ok "database_dump.sql diimport"
else
  step "Lewati import database (--skip-import)"
fi

$WP core is-installed >/dev/null 2>&1 || fail "WordPress belum terdeteksi ter-instal. Pastikan import dump sukses."

step "Sinkronkan URL site"
STORAGE_URL="$($WP option get home 2>/dev/null || true)"
if [[ "$STORAGE_URL" != "$URL" ]]; then
  $WP option update home   "$URL" >/dev/null || fail "Gagal update opsi home"
  $WP option update siteurl "$URL" >/dev/null || fail "Gagal update opsi siteurl"
  ok "home/siteurl: $STORAGE_URL -> $URL"
else
  ok "home/siteurl sudah $URL"
fi

# --- 5. Theme & plugin -------------------------------------------------------
step "Theme astra + plugin elementor, astra-sites, mt-topbar"
if $WP theme is-installed astra >/dev/null 2>&1; then
  ok "theme astra sudah terpasang"
else
  $WP theme install astra --activate >/dev/null || fail "Gagal unduh theme astra (cek internet)."
  ok "theme astra terpasang"
fi
$WP theme activate astra >/dev/null 2>&1 || true
$WP theme is-active astra >/dev/null 2>&1 && ok "theme astra aktif" || true

for p in elementor astra-sites header-footer-elementor; do
  if $WP plugin is-installed "$p" >/dev/null 2>&1; then
    ok "plugin $p sudah terpasang"
  else
    $WP plugin install "$p" >/dev/null || fail "Gagal unduh plugin $p (cek internet)."
    ok "plugin $p terpasang"
  fi
  $WP plugin activate "$p" >/dev/null 2>&1 && ok "plugin $p aktif" || true
done

if $WP plugin is-installed mt-topbar >/dev/null 2>&1; then
  $WP plugin activate mt-topbar >/dev/null 2>&1 || true
  ok "plugin mt-topbar aktif"
else
  fail "plugin mt-topbar tidak ditemukan di container (salinan gagal?)"
fi

# --- 6. Sinkronisasi template & media ---------------------------------------
step "Sinkronisasi wp-integration + media"
bash "$ROOT/sync-to-wp.sh" -c "$APP" || fail "sync-to-wp.sh gagal."

# --- 7. Flush permalink + regenerasi CSS Elementor --------------------------
step "Flush permalink & regenerasi CSS Elementor"
$WP rewrite flush >/dev/null 2>&1 && ok "permalink di-flush" || true
$WP eval '
  $ids = array_merge([59,4], range(24,29), [31,32,33,34]);
  foreach ($ids as $id) { delete_post_meta($id, "_elementor_css"); delete_post_meta($id, "_elementor_element_cache"); }
  echo count($ids);
' >/dev/null 2>&1 && ok "cache CSS Elementor dibersihkan" || true

# --- 8. Verifikasi -----------------------------------------------------------
step "Verifikasi HTTP"
paths=( "/" "/profil/" "/produk/" "/wilayah/" "/kontak/" "/layanan-overhaul/" )
all_ok=1
for p in "${paths[@]}"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$URL$p" || echo 000)
  if [[ "$code" == "200" ]]; then ok "$code  $p"; else printf '  \033[1;31m%s\033[0m  %s\n' "$code" "$p"; all_ok=0; fi
done

step "Selesai"
echo "  Site      : $URL/"
echo "  Dashboard : $URL/wp-admin/"
echo "  Portal    : http://localhost:3000/  (Web Fleet, repo terpisah)"
[[ $all_ok -eq 1 ]] && echo "  Status    : semua halaman utama 200" || { echo "  Status    : ADA yang bukan 200 — cek log: docker logs $APP"; exit 1; }
