# AUDIT WARNA — RONDE 23 (REVAMP16), Tema Terang Selaras Logo

Tanggal: 2026-10-27 · Target: Beranda WordPress Page 59 (builder `tools/build-stitch-elementor.py`)

## Aturan baru

1. **Emas tidak pernah menjadi warna teks** — emas hanya untuk garis (border/underline/poin ✅), ikon `<i>`/SVG, titik indikator, bintang, dan latar tint `#FBF4E1`.
2. Tanpa gradasi emas (`linear-gradient` yang memuat `#C69A43`/`#8A5F12`) dan tanpa `background-clip:text`.
3. Tanpa section dengan latar hitam/gelap penuh — semua section terang (putih/`#F7F8FA`/`#F1F3F5`).
4. Tanpa biru default WordPress/Elementor.
5. Tombol utama seluruh situs = solid **Ink `#0B0C10`** teks putih (hover Charcoal `#1B1F27`); tombol WhatsApp tetap hijau brand `#25D366`.

## Tabel pemetaan warna lama → peran baru → nilai baru

| Warna lama (tema hitam-emas) | Peran baru | Nilai baru | Dipakai untuk |
| --- | --- | --- | --- |
| `#090909` (ink lama) | Ink / Primary | `#0B0C10` (Global Colors: primary) | Judul, tombol utama, hover nav |
| `#16161A` / `#1F1F24` | Charcoal | `#1B1F27` | Hover tombol utama |
| `#0F2A5C`, `#2563EB` (era biru) | Navy | `#0F1B33` (Global Colors: accent) | Ring fokus keyboard (outline 2px) |
| `#475569`, `#E8E8D8` (teks isi) | Text | `#3F4651` (Global Colors: text) | Paragraf & teks isi |
| `#989898`, `#5B554A` | Muted | `#6B7280` (custom: r23muted) | Meta kecil di latar putih |
| `#D8D8D8`, `#989898` | Silver | `#C9CDD3` (custom: r23silver) | Border chip merek, back-top hover |
| `#E9E1CF`, `#E8E8E8`, `rgba white 0.12` | Border | `#E3E6EA` (custom: r23border) | Border kartu & pemisah |
| `#15130F`, `#0B0C10` (latar section) | Surface | `#F7F8FA` (custom: r23surface) | Latar section selang-seling, footer |
| `#F6F1E6`, `#FBF8F1` | Tint | `#F1F3F5` (custom: r23tint) | Topbar, panel ::before hero, pil nav aktif, hover |
| `#AE7A26`, `#C69A43` (gradasi tombol emas) | Emas aksen (garis/ikon saja) | `#C69A43` (custom: r23gold) | Garis bawah hafalan, ikon tombol utama, badge border |
| `#8F6318`, `#AE7A26` | Emas tua (ikon di terang) | `#8A5F12` (Global Colors: secondary) | Ikon di latar terang (ikon saja, bukan teks) |
| `#F8E8A8`, grad tombol hijau lampu emas | Gold Tint | `#FBF4E1` (custom: r23goldtint) | Latar ikon chip, badge "Paling Populer", avatar inisial |
| `#1A1405` (teks di atas emas) | Putih / Teks Ink | `#FFFFFF` atau `#0B0C10` | Teks di atas tombol solid & chip tint |
| `#075E54`, `#1DA851` (hijau WA campur) | WA brand | `#25D366` (hover `#128C7E`) | Semua tombol WhatsApp (tetap) |

## Alias C-panel lama yang dipetakan (tanpa menyunting tiap baris call-site)

| Alias lama | Diarahkan ke |
| --- | --- |
| `primary` | Ink `#0B0C10` |
| `secondary`, `gold_600`, `gold_700` | Emas tua `#8A5F12` |
| `gold_400`, `gold_500` | Emas `#C69A43` |
| `on_gold` | Putih `#FFFFFF` |
| `silver` | Ink (judul) · `silver_2` → text · `silver_3` → muted |
| `ivory` → Surface `#F7F8FA` · `ivory_2` → Tint `#F1F3F5` |
| `line` | Border `#E3E6EA` |

## Global Colors kit (Elementor Site Settings)

- **System**: Primary `#0B0C10` (Ink) · Secondary `#8A5F12` (Emas tua) · Text `#3F4651` · Accent `#0F1B33` (Navy)
- **Custom**: r23muted `#6B7280` · r23surface `#F7F8FA` · r23tint `#F1F3F5` · r23border `#E3E6EA` · r23silver `#C9CDD3` · r23gold `#C69A43` · r23goldtint `#FBF4E1`
- Diperbarui otomatis saat deploy oleh blok `KIT_COLORS_PHP` di builder (`wp post meta update` pada kit aktif, lalu regen CSS kit).
- Semua warna widget utama sudah direferensikan via `__globals__` (helper `grole()` + `add_globals()`), fallback hex tetap ada.

## Pengecualian kontras yang disengaja

- Tombol/link WhatsApp: teks putih di atas hijau brand `#25D366` — disengaja (kontras 1.98–3.10) karena WA tetap pakai warna brand resmi WhatsApp, bukan warna tema.
- Semua teks lain terukur ≥ 4,5:1 (large text ≥ 3:1) oleh `tests/test-ronde23-verify.cjs`.
