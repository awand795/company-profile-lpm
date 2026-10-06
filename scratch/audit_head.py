import urllib.request
import re

url = 'http://localhost:8080/'
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8', errors='ignore')

print("Page length:", len(html))
print("Has mt-section--booking:", "mt-section--booking" in html)
print("Has stats-overlap-wrapper:", "stats-overlap-wrapper" in html)
print("Has elementor:", "elementor" in html)

print("\n--- Fonts links ---")
for m in re.finditer(r'<link[^>]*fonts\.googleapis\.com[^>]*>', html):
    print(m.group(0))

print("\n--- All Stylesheets ---")
for m in re.finditer(r'<link[^>]*rel=[\'"]stylesheet[\'"][^>]*>', html):
    print(m.group(0))

print("\n--- Body tag ---")
m = re.search(r'<body[^>]*>', html)
if m:
    print(m.group(0))
