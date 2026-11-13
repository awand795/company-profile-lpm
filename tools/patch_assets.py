import os

css_snippet = """
/* ===== CAROUSEL TESTIMONI & FOOTER 3-KOLOM (UPDATE 2026-11) ===== */
body.elementor-page-59 .stitch-sec-testimonials .testimonials-row {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    scroll-behavior: smooth !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
    gap: 20px !important;
    scrollbar-width: none !important;
    padding: 10px 4px 16px 4px !important;
    margin: 0 !important;
}
body.elementor-page-59 .stitch-sec-testimonials .testimonials-row::-webkit-scrollbar {
    display: none !important;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-card-col {
    flex: 0 0 380px !important;
    width: 380px !important;
    max-width: 380px !important;
    scroll-snap-align: start !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 24px 22px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-card-col:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.09) !important;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-card-inner {
    display: flex;
    flex-direction: column;
    height: 100%;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-stars {
    color: #f59e0b;
    font-size: 14px;
    letter-spacing: 2px;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-google-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    color: #475569;
    background: #f1f5f9;
    padding: 3px 8px;
    border-radius: 6px;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-google-badge i {
    color: #4285f4;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-text {
    font-family: 'Inter', sans-serif;
    font-size: 14.5px;
    color: #1e293b;
    line-height: 1.6;
    margin-bottom: 16px;
    flex-grow: 1;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-photos {
    margin-bottom: 14px;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-photos img {
    width: 100%;
    height: 140px;
    object-fit: cover;
    display: block;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-author {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 14px;
    border-top: 1px solid #f1f5f9;
    margin-top: auto;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-avatar {
    width: 44px;
    height: 44px;
    flex: 0 0 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 800;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14.5px;
    font-weight: 700;
    color: #0f172a;
}
body.elementor-page-59 .stitch-sec-testimonials .testi-sub {
    font-size: 12.5px;
    color: #64748b;
}

/* Controls Testimoni */
.testi-carousel-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-top: 24px;
}
.testi-nav-btn {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #0f172a;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.testi-nav-btn:hover {
    background: #00236f;
    color: #ffffff;
    border-color: #00236f;
    transform: scale(1.05);
}
.testi-dots {
    display: flex;
    align-items: center;
    gap: 8px;
}
.testi-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #cbd5e1;
    border: none;
    cursor: pointer;
    padding: 0;
    transition: all 0.25s ease;
}
.testi-dot.active {
    width: 24px;
    border-radius: 10px;
    background: #00236f;
}

@media (max-width: 991.98px) {
    body.elementor-page-59 .stitch-sec-testimonials .testi-card-col {
        flex: 0 0 320px !important;
        width: 320px !important;
        max-width: 320px !important;
    }
}

@media (max-width: 640px) {
    body.elementor-page-59 .stitch-sec-testimonials .testi-card-col {
        flex: 0 0 88% !important;
        width: 88% !important;
        max-width: 88% !important;
    }
}

/* Footer 3 Kolom Seimbang */
@media (min-width: 992px) {
    body.elementor-page-59 .footer-col-brand {
        width: 45% !important;
        flex: 0 0 45% !important;
    }
    body.elementor-page-59 .footer-col-links {
        width: 27% !important;
        flex: 0 0 27% !important;
    }
    body.elementor-page-59 .footer-col-cert {
        width: 28% !important;
        flex: 0 0 28% !important;
    }
}
"""

js_snippet = """
    // ===== Testimonials Auto-Slide Carousel Engine (Google Reviews) =====
    (function initTestimonialsCarousel() {
        function setup() {
            var row = document.querySelector('.stitch-sec-testimonials .testimonials-row');
            if (!row) return;

            var isHovered = false;
            row.addEventListener('mouseenter', function() { isHovered = true; });
            row.addEventListener('mouseleave', function() { isHovered = false; });
            row.addEventListener('touchstart', function() { isHovered = true; }, { passive: true });
            row.addEventListener('touchend', function() {
                setTimeout(function() { isHovered = false; }, 3000);
            }, { passive: true });

            var interval = setInterval(function() {
                if (isHovered) return;
                var maxScroll = row.scrollWidth - row.clientWidth;
                var card = row.querySelector('.testi-card-col');
                var step = card ? (card.offsetWidth + 20) : 380;

                if (row.scrollLeft + step >= maxScroll - 15) {
                    row.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    row.scrollBy({ left: step, behavior: 'smooth' });
                }
            }, 3800);

            if (!document.querySelector('.testi-carousel-controls')) {
                var controls = document.createElement('div');
                controls.className = 'testi-carousel-controls';
                controls.innerHTML = '<button type="button" class="testi-nav-btn prev" aria-label="Ulasan sebelumnya"><i class="fas fa-chevron-left"></i></button>' +
                    '<div class="testi-dots"></div>' +
                    '<button type="button" class="testi-nav-btn next" aria-label="Ulasan berikutnya"><i class="fas fa-chevron-right"></i></button>';
                
                row.parentNode.appendChild(controls);

                var prevBtn = controls.querySelector('.prev');
                var nextBtn = controls.querySelector('.next');
                var dotsContainer = controls.querySelector('.testi-dots');
                var cards = row.querySelectorAll('.testi-card-col');

                cards.forEach(function(_, i) {
                    var dot = document.createElement('button');
                    dot.className = 'testi-dot' + (i === 0 ? ' active' : '');
                    dot.setAttribute('aria-label', 'Lihat ulasan ' + (i + 1));
                    dot.addEventListener('click', function() {
                        var c = cards[i];
                        if (c) {
                            row.scrollTo({ left: c.offsetLeft - row.offsetLeft, behavior: 'smooth' });
                        }
                    });
                    dotsContainer.appendChild(dot);
                });

                prevBtn.addEventListener('click', function() {
                    var card = row.querySelector('.testi-card-col');
                    var step = card ? (card.offsetWidth + 20) : 380;
                    if (row.scrollLeft <= 15) {
                        row.scrollTo({ left: row.scrollWidth - row.clientWidth, behavior: 'smooth' });
                    } else {
                        row.scrollBy({ left: -step, behavior: 'smooth' });
                    }
                });

                nextBtn.addEventListener('click', function() {
                    var card = row.querySelector('.testi-card-col');
                    var step = card ? (card.offsetWidth + 20) : 380;
                    var maxScroll = row.scrollWidth - row.clientWidth;
                    if (row.scrollLeft + step >= maxScroll - 15) {
                        row.scrollTo({ left: 0, behavior: 'smooth' });
                    } else {
                        row.scrollBy({ left: step, behavior: 'smooth' });
                    }
                });

                row.addEventListener('scroll', function() {
                    var center = row.scrollLeft + (row.clientWidth / 2);
                    var activeIdx = 0;
                    cards.forEach(function(card, idx) {
                        var left = card.offsetLeft - row.offsetLeft;
                        var right = left + card.offsetWidth;
                        if (center >= left && center <= right) {
                            activeIdx = idx;
                        }
                    });
                    var dots = dotsContainer.querySelectorAll('.testi-dot');
                    dots.forEach(function(d, idx) {
                        if (idx === activeIdx) d.classList.add('active');
                        else d.classList.remove('active');
                    });
                }, { passive: true });
            }
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setup);
        } else {
            setup();
        }
    })();
"""

# Update assets/css/mt-custom.css
with open("assets/css/mt-custom.css", "r", encoding="utf-8") as f:
    css_content = f.read()

if "/* ===== CAROUSEL TESTIMONI & FOOTER 3-KOLOM (UPDATE 2026-11) ===== */" not in css_content:
    css_content += "\n" + css_snippet + "\n"
    with open("assets/css/mt-custom.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Updated assets/css/mt-custom.css")

# Also mirror to wp-integration/mastertruck/css/mt-custom.css
with open("wp-integration/mastertruck/css/mt-custom.css", "w", encoding="utf-8") as f:
    f.write(css_content)
print("Updated wp-integration/mastertruck/css/mt-custom.css")

# Update assets/js/main.js
with open("assets/js/main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

if "initTestimonialsCarousel" not in js_content:
    # insert before the closing })(jQuery);
    idx = js_content.rfind("})(jQuery);")
    if idx != -1:
        js_content = js_content[:idx] + js_snippet + "\n\n" + js_content[idx:]
    else:
        js_content += "\n" + js_snippet + "\n"
    with open("assets/js/main.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Updated assets/js/main.js")

# Also mirror to wp-integration/mastertruck/js/main.js
with open("wp-integration/mastertruck/js/main.js", "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated wp-integration/mastertruck/js/main.js")
