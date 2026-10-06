import urllib.request
import re

# 1. Inline styles in rendered HTML
url = 'http://localhost:8080/'
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8', errors='ignore')

inline_styles = re.findall(r'style=[\'"][^\'"]*[\'"]', html)
print(f"Total inline style attributes in rendered HTML: {len(inline_styles)}")
unique_styles = set(inline_styles)
print(f"Unique inline style attributes ({len(unique_styles)}):")
for s in sorted(unique_styles)[:20]:
    print("  ", s)

# 2. Count !important in mastertruck.css and style.css
with open('wp-theme/carserv/assets/css/mastertruck.css', 'r', encoding='utf-8') as f:
    mt_css = f.read()
mt_importants = len(re.findall(r'!important', mt_css))

with open('wp-theme/carserv/assets/css/style.css', 'r', encoding='utf-8') as f:
    style_css = f.read()
style_importants = len(re.findall(r'!important', style_css))

print(f"\nTotal !important in mastertruck.css: {mt_importants}")
print(f"Total !important in style.css: {style_importants}")

# 3. Check what classes are styled in both style.css and mastertruck.css
def extract_classes(css):
    return set(re.findall(r'\.([a-zA-Z0-9_-]+)', css))

mt_classes = extract_classes(mt_css)
style_classes = extract_classes(style_css)
common_classes = mt_classes.intersection(style_classes)

print(f"\nClasses in mastertruck.css: {len(mt_classes)}")
print(f"Classes in style.css: {len(style_classes)}")
print(f"Common / overlapping classes: {len(common_classes)}")
sample_common = [c for c in common_classes if not c.startswith('btn') and not c.startswith('nav') and not c.startswith('col') and not c.startswith('d-')][:20]
print("Sample overlapping component classes:", sample_common)
