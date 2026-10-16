import re
import json
import os
import subprocess

html_path = 'stitch_review/screen_desktop.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

img_tags = re.findall(r'<img[^>]+>', html)
images = []
seen = set()

for tag in img_tags:
    src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
    alt_match = re.search(r'(?:data-alt|alt)=["\']([^"\']+)["\']', tag)
    if src_match:
        src = src_match.group(1)
        alt = alt_match.group(1) if alt_match else ''
        if src not in seen:
            seen.add(src)
            images.append({'src': src, 'alt': alt})

print(f"Found {len(images)} unique images in Stitch HTML.")

out_json = 'stitch_review/images_list.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(images, f, indent=2)

os.makedirs('stitch_review/images', exist_ok=True)

# Download all images with curl
for idx, item in enumerate(images):
    url = item['src']
    filename = f"stitch_img_{idx+1}.webp" if "googleusercontent" in url else f"stitch_img_{idx+1}.png"
    filepath = os.path.join('stitch_review/images', filename)
    item['local_file'] = filepath
    print(f"Downloading [{idx+1}/{len(images)}] -> {filename}")
    cmd = ['curl.exe', '-L', url, '-o', filepath]
    subprocess.run(cmd, capture_output=True)

with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(images, f, indent=2)

print("All images downloaded successfully!")
