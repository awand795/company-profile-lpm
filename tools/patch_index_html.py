import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Address updates
html = html.replace("Kawasan Industri Medan (KIM) III, Medan, Sumatera Utara", "KIM 3, Jl. Pulau Pamagaran No.10, Tangkahan, Kec. Medan Labuhan, Kota Medan, Sumatera Utara 20251")
html = html.replace("KIM III, Medan, Sumatera Utara", "KIM 3, Jl. Pulau Pamagaran No.10, Tangkahan, Kec. Medan Labuhan, Kota Medan, Sumatera Utara 20251")

# Hours updates
html = re.sub(r'08\.00\s*–\s*20\.00', '08.30 – 16.30', html)
html = re.sub(r'08\.00\s*–\s*17\.00', '08.30 – 16.30', html)
html = re.sub(r'08\.00\s*-\s*17\.00', '08.30 - 16.30', html)

# GMaps link updates
html = re.sub(r'https://www\.google\.com/maps/search/\?[^"\'<>\s]+', 'https://maps.app.goo.gl/toBFiJXcpDo2GatZ6', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html for parity!")
