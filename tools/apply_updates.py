import json
import os
import re

print("=== Starting Full Site Updates ===")

with open("scratch/post59_raw.json", "rb") as f:
    raw = f.read()
text = raw.decode("utf-16" if raw.startswith(b"\xff\xfe") else "utf-8", errors="ignore")
data = json.loads(text)

# 1. Section [0] - Topbar: hours -> 08.30 – 16.30
topbar_hours = data[0]['elements'][0]['elements'][1]['elements'][0]
topbar_hours['settings']['editor'] = '<div style="display:flex;align-items:center;justify-content:flex-end;gap:16px;color:#94a3b8;font-size:12px;white-space:nowrap;"><div class="topbar-hours-item" style="display:inline-flex;align-items:center;gap:6px;"><i class="fas fa-clock" style="color:#94a3b8;font-size:11px;"></i> <span style="color:#e2e8f0;">Senin – Sabtu: 08.30 – 16.30</span></div></div>'
print("1. Updated Topbar hours to 08.30 - 16.30")

# 2. Section [3] - Quick booking form: update option labels
booking_form_widget = data[3]['elements'][3]['elements'][0]['elements'][0]
booking_html = booking_form_widget['settings']['editor']
booking_html = booking_html.replace(
    '<option>Bengkel KIM III Medan — hari ini</option><option>Bengkel KIM III Medan — besok</option><option>Bengkel KIM III Medan — pekan ini</option>',
    '<option>Bengkel KIM 3 Medan — hari ini</option><option>Bengkel KIM 3 Medan — besok</option><option>Bengkel KIM 3 Medan — pekan ini</option>'
)
booking_form_widget['settings']['editor'] = booking_html
print("2. Updated Quick booking options")

# 3. Section [5] - Layanan Kami: remove "Konsultasi Servis" button in each card
layanan = data[5]
removed_buttons = 0
for row in layanan['elements'][3:]:
    for card in row.get('elements', []):
        old_len = len(card.get('elements', []))
        card['elements'] = [w for w in card.get('elements', []) if w.get('widgetType') != 'button']
        removed_buttons += (old_len - len(card['elements']))
print(f"3. Removed {removed_buttons} 'Konsultasi Servis' buttons in Layanan Kami")

# 4. Section [6] - Fasilitas: update titles & images, remove subtitles
facility_data = [
    {
        "title": "AREA PIT PERBAIKAN KENDARAAN YANG LUAS",
        "img_url": "http://localhost:8923/wp-content/uploads/stitch/facility_1.webp"
    },
    {
        "title": "HALAMAN & AREA PARKIR YANG LUAS",
        "img_url": "http://localhost:8923/wp-content/uploads/stitch/facility_2.webp"
    },
    {
        "title": "RUANG TUNGGU CUSTOMER (SMOKING AREA)",
        "img_url": "http://localhost:8923/wp-content/uploads/stitch/facility_3.webp"
    },
    {
        "title": "RUANG TUNGGU CUSTOMER (NO SMOKING AREA)",
        "img_url": "http://localhost:8923/wp-content/uploads/stitch/facility_4.webp"
    },
    {
        "title": "LAYAR UNTUK MONITORING PEKERJAAN MEKANIK",
        "img_url": "http://localhost:8923/wp-content/uploads/stitch/facility_5.webp"
    },
    {
        "title": "RUANGAN BACK OFFICE YANG NYAMAN",
        "img_url": "http://localhost:8923/wp-content/uploads/stitch/facility_6.webp"
    }
]

fasilitas = data[6]
fac_idx = 0
for row in fasilitas['elements'][3:]:
    for card in row.get('elements', []):
        info = facility_data[fac_idx]
        new_elements = []
        for w in card.get('elements', []):
            wt = w.get('widgetType')
            if wt == 'image':
                w['settings']['image']['url'] = info['img_url']
                new_elements.append(w)
            elif wt == 'heading':
                w['settings']['title'] = info['title']
                new_elements.append(w)
            elif wt == 'text-editor':
                # Remove subtitle!
                pass
        card['elements'] = new_elements
        fac_idx += 1
print("4. Updated Fasilitas cards: titles from Excel, images, removed all subtitles")

# 5. Section [7] - Testimoni: 5 real Google reviews
testi_cards_data = [
    {
        "id": "testi_hanna",
        "name": "Hanna Ahroni",
        "sub": "1 ulasan · 8 bulan lalu",
        "rating": 5,
        "text": "Ini bengkel truck umum, tapi standardnya sudah seperti bengkel truck di dealer resmi. Memang kalau sudah Indako Group, semuanya keren. Hasil service berkualitas dan semua SDM di sini sangat profesional. Salut. Sukses terus untuk Master Truck 🙏💪",
        "initial": "HA",
        "avatar_bg": "#37474f",
        "photo": None
    },
    {
        "id": "testi_wahyu",
        "name": "Wahyu Qura",
        "sub": "1 ulasan · 2 foto · 8 bulan lalu",
        "rating": 5,
        "text": "Bengkel truk terekomendasi di sekitaran KIM dan kota Medan sihh ini",
        "initial": "WQ",
        "avatar_bg": "#455a64",
        "photo": "http://localhost:8923/wp-content/uploads/stitch/review_wahyu_qura.webp"
    },
    {
        "id": "testi_faisal",
        "name": "Faisal adi Wiguna",
        "sub": "1 ulasan · 4 bulan lalu",
        "rating": 5,
        "text": "Bengkel umum, tapi kualitas rasa bengkel resmi. Mekanik handal, pengerjaan sesuai estimasi dan tepat waktu, karyawan ramah semuanya. Sukses selalu Master Truck 🙏👍",
        "initial": "FW",
        "avatar_bg": "#00695c",
        "photo": None
    },
    {
        "id": "testi_calixto",
        "name": "Calixto Tanner",
        "sub": "1 ulasan · 8 bulan lalu",
        "rating": 5,
        "text": "Pelayanan Bengkel Master Truck sangat profesional. Mekanik berpengalaman, pengerjaan cepat, dan penjelasan kerusakan jelas. Harga transparan dan sesuai pekerjaan. Sangat direkomendasikan 👍",
        "initial": "CT",
        "avatar_bg": "#c2185b",
        "photo": None
    },
    {
        "id": "testi_alvin",
        "name": "Alvin Winata",
        "sub": "4 ulasan · 1 foto · 8 bulan lalu",
        "rating": 5,
        "text": "Armada kami perbaikan di bengkel ini sudah mau jalan 2tahun, pelayanan OK dan hasil kerja yang baik. Keep up the good work 👍",
        "initial": "AW",
        "avatar_bg": "#1565c0",
        "photo": "http://localhost:8923/wp-content/uploads/stitch/review_alvin_winata.webp"
    }
]

# Update Section [7] header subtitle
data[7]['elements'][2]['settings']['editor'] = 'Ulasan nyata dari para pelanggan dan pengelola armada truk yang mempercayakan perawatannya di Master Truck.'

testi_row = data[7]['elements'][3]
new_testi_cards = []

for tc in testi_cards_data:
    photo_html = f"<div class='testi-photos'><img src='{tc['photo']}' alt='Foto ulasan {tc['name']}' loading='lazy'></div>" if tc['photo'] else ""
    
    card_html = (
        f"<div class='testi-card-inner'>"
        f"<div class='testi-header'>"
        f"<div class='testi-stars' role='img' aria-label='Nilai 5 dari 5'>"
        f"<i class='fas fa-star'></i><i class='fas fa-star'></i><i class='fas fa-star'></i><i class='fas fa-star'></i><i class='fas fa-star'></i>"
        f"</div>"
        f"<span class='testi-google-badge'><i class='fab fa-google'></i> Google Review</span>"
        f"</div>"
        f"<p class='testi-text'>&ldquo;{tc['text']}&rdquo;</p>"
        f"{photo_html}"
        f"<div class='testi-author'>"
        f"<div class='testi-avatar' style='background:{tc['avatar_bg']};color:#ffffff;'>{tc['initial']}</div>"
        f"<div>"
        f"<div class='testi-name'>{tc['name']}</div>"
        f"<div class='testi-sub'>{tc['sub']}</div>"
        f"</div>"
        f"</div>"
        f"</div>"
    )

    card_container = {
        "id": tc['id'],
        "elType": "container",
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "css_classes": "testi-card-col",
            "background_background": "classic",
            "background_color": "#ffffff",
            "border_border": "solid",
            "border_width": { "unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True },
            "border_color": "#e2e8f0",
            "border_radius": { "unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True },
            "padding": { "unit": "px", "top": "24", "right": "22", "bottom": "24", "left": "22", "isLinked": False }
        },
        "elements": [
            {
                "id": f"w_{tc['id']}",
                "elType": "widget",
                "settings": {
                    "editor": card_html,
                    "align": "left",
                    "typography_typography": "custom",
                    "typography_font_family": "Inter"
                },
                "elements": [],
                "widgetType": "text-editor"
            }
        ],
        "isInner": True
    }
    new_testi_cards.append(card_container)

testi_row['elements'] = new_testi_cards
print("5. Replaced Testimoni section with 5 authentic Google reviews in slideshow carousel")

# 6. Section [8] - Lokasi: heading -> Lokasi Bengkel, address, hours, gmaps link
lokasi = data[8]
lokasi_content_col = lokasi['elements'][2]['elements'][0]
lokasi_content_col['elements'][0]['settings']['title'] = 'Lokasi Bengkel'
lokasi_content_col['elements'][1]['settings']['editor'] = 'KIM 3, Jl. Pulau Pamagaran No.10, Tangkahan, Kec. Medan Labuhan, Kota Medan, Sumatera Utara 20251'
lokasi_content_col['elements'][3]['settings']['editor'] = 'Senin – Sabtu: 08.30 – 16.30'

# button "Buka di Google Maps"
btn_maps = lokasi['elements'][2]['elements'][1]['elements'][0]
btn_maps['settings']['link']['url'] = 'https://maps.app.goo.gl/toBFiJXcpDo2GatZ6'
print("6. Updated Lokasi Bengkel: Title 'Lokasi Bengkel', Address KIM 3, Hours 08.30-16.30, GMaps link")

# 7. Section [9] - Kontak/Footer: remove Workshop column, update address, update social map link
footer = data[9]
footer_cols = footer['elements'][0]['elements']
footer['elements'][0]['elements'] = [col for col in footer_cols if col.get('id') != '65e7f46']

# Set balanced width for the remaining 3 columns
footer['elements'][0]['elements'][0]['settings']['width'] = { 'unit': '%', 'size': 44 }
footer['elements'][0]['elements'][1]['settings']['width'] = { 'unit': '%', 'size': 28 }
footer['elements'][0]['elements'][2]['settings']['width'] = { 'unit': '%', 'size': 28 }

# Update description in Col 0 (id 1425250) widget 2 (id 28c1445)
footer['elements'][0]['elements'][0]['elements'][2]['settings']['editor'] = 'Bengkel perawatan, perbaikan, dan rekondisi armada truk niaga di KIM 3 Medan.'

# Social map link in Col 0 (id 1425250) widget 4 (id 17bdf1f)
social_widget = footer['elements'][0]['elements'][0]['elements'][4]
social_html = social_widget['settings']['editor']
social_html = social_html.replace(
    'https://www.google.com/maps/search/?api=1&query=Kawasan%20Industri%20Medan%20%28KIM%29%20III%2C%20Medan%2C%20Sumatera%20Utara',
    'https://maps.app.goo.gl/toBFiJXcpDo2GatZ6'
)
social_widget['settings']['editor'] = social_html
print("7. Removed Workshop column from footer (ss1 & ss2) and balanced remaining 3 columns")

# Save updated JSON to file
updated_json = json.dumps(data, ensure_ascii=False)
with open("scratch/post59_updated.json", "w", encoding="utf-8") as f:
    f.write(updated_json)

with open("elementor-exports/beranda-elementor.json", "w", encoding="utf-8") as f:
    f.write(updated_json)

print("Saved scratch/post59_updated.json and elementor-exports/beranda-elementor.json")
