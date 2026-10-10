#!/usr/bin/env bash
# Verifikasi paritas: assets/ <-> mirror wp-integration/ <-> template <-> situs tersaji.
#   ./tools/verify-parity.sh              # peringatan saja (exit 0)
#   ./tools/verify-parity.sh --strict     # exit 1 bila ada mismatch
# Variabel: MT_URL (default http://localhost:8080), MT_APP (default lotus-wp-app)
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
STRICT=0
[[ "${1:-}" == "--strict" ]] && STRICT=1
URL="${MT_URL:-http://localhost:8080}"
APP="${MT_APP:-lotus-wp-app}"
WARN=0

warn() { printf '  \033[1;33mWARN\033[0m  %s\n' "$*"; WARN=$((WARN+1)); }
ok()   { printf '  \033[1;32mOK\033[0m    %s\n' "$*"; }

# 1. Mirror vs assets (checksum per file)
if command -v sha256sum >/dev/null 2>&1; then
  mismatch=0
  while IFS= read -r -d '' f; do
    rel="${f#wp-integration/mastertruck/}"
    # File lawas di root mirror (tak dipakai template, jangan hapus membabi buta).
    if [[ "$rel" == "style.css" || "$rel" == "main.js" ]]; then
      continue
    fi
    if [[ -f "assets/$rel" ]]; then
      a="$(sha256sum < "assets/$rel")"; b="$(sha256sum < "$f")"
      [[ "$a" != "$b" ]] && { warn "mirror basi: $rel"; mismatch=1; }
    else
      warn "mirror tanpa sumber: $rel"
      mismatch=1
    fi
  done < <(find wp-integration/mastertruck -type f -print0)
  [[ $mismatch -eq 0 ]] && ok "mirror identik dengan assets/"
else
  warn "sha256sum tak ada, lewati cek mirror"
fi

# 2. Template hasil regen vs ter-commit
if command -v python3 >/dev/null 2>&1; then
  if python3 tools/build-template.py --check >/dev/null 2>&1; then
    ok "template sesuai regen index.html"
  else
    warn "template berbeda dari regen index.html (jalankan tools/build-template.py)"
  fi
else
  warn "python3 tak ada, lewati cek regen template"
fi

# 3. Homepage tersaji = Elementor full (migrasi 2026-10-07)
home="$(curl -s --max-time 20 "$URL/" || true)"
if [[ -z "$home" ]]; then
  warn "tidak bisa mengunduh $URL/ (container mati?)"
else
  miss=0
  for m in 'header-carousel' 'hero-brand-pill' 'about-check-list' 'fact-strip' 'service-grid-card' 'principal-wall-card' 'booking-section-wrapper' 'derek-stat-card' 'team-enterprise-card' 'testimonial-enterprise-card' 'faqAccordion' 'footer-clean' 'floating-wa-btn' 'mt-mastertruck' 'elementor'; do
    grep -q "$m" <<<"$home" || { warn "marker hilang di homepage: $m"; miss=1; }
  done
  for m in 'bg-dark' 'brand-badge-card' 'template-mastertruck'; do
    grep -q "$m" <<<"$home" && { warn "sisa lama di homepage: $m"; miss=1; }
  done
  [[ $miss -eq 0 ]] && ok "homepage tersaji = Elementor full"
fi

# 4. Homepage FULL ELEMENTOR (migrasi 2026-10-07)
if docker ps --filter "name=^/${APP}$" --format '{{.Names}}' 2>/dev/null | grep -q .; then
  tpl="$(docker exec "$APP" wp post meta get 59 _wp_page_template --allow-root --path=/var/www/html 2>/dev/null || true)"
  mode="$(docker exec "$APP" wp post meta get 59 _elementor_edit_mode --allow-root --path=/var/www/html 2>/dev/null || true)"
  if [[ "$mode" == "builder" && "$tpl" != "template-mastertruck.php" ]]; then
    ok "homepage(ID 59) Elementor full (template: ${tpl:-default})"
  else
    warn "homepage bukan Elementor full (tpl='${tpl:-?}' mode='${mode:-?}')"
  fi
else
  warn "container $APP tidak jalan, lewati cek meta template"
fi

echo "Parity: $WARN peringatan."
[[ $STRICT -eq 1 && $WARN -gt 0 ]] && exit 1
exit 0
