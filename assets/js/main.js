(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 24) {
            $('.sticky-top').addClass('sticky-scrolled');
        } else {
            $('.sticky-top').removeClass('sticky-scrolled');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button (class-based agar ikon tetap di tengah)
    $(window).scroll(function () {
        if ($(this).scrollTop() > 400) {
            $('.back-to-top').addClass('show');
        } else {
            $('.back-to-top').removeClass('show');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter: hanya sekali, format ribuan id-ID tiap frame,
    // tak mengulang saat scroll bolak-balik
    var countersDone = false;
    function fmtID(n) {
        return Math.round(n).toLocaleString('id-ID');
    }
    function animateCount($el, target, dur) {
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            $el.text(fmtID(target));
            return;
        }
        var t0 = null;
        function step(ts) {
            if (!t0) {
                t0 = ts;
            }
            var p = Math.min((ts - t0) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            $el.text(fmtID(target * eased));
            if (p < 1) {
                requestAnimationFrame(step);
            } else {
                $el.text(fmtID(target));
            }
        }
        requestAnimationFrame(step);
    }
    function maybeCountUp() {
        if (countersDone) {
            return;
        }
        var $nums = $('[data-toggle="counter-up"]');
        if (!$nums.length || !$nums.first().offset()) {
            return;
        }
        if ($(window).scrollTop() + $(window).height() > $nums.first().offset().top + 40) {
            countersDone = true;
            $nums.each(function () {
                var $el = $(this);
                var target = parseInt($el.text().replace(/[^0-9]/g, ''), 10);
                if (!isNaN(target)) {
                    animateCount($el, target, 2000);
                }
            });
        }
    }
    $(window).on('scroll load', maybeCountUp);
    maybeCountUp();


    // Date and time picker
    if ($.fn.datetimepicker) {
        $('.date').datetimepicker({
            format: 'L'
        });
        $('.time').datetimepicker({
            format: 'LT'
        });
    }


    // Testimonials carousel
    if ($.fn.owlCarousel && $('.testimonial-carousel').length) {
        $(".testimonial-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            center: true,
            margin: 25,
            dots: true,
            loop: true,
            nav : false,
            responsive: {
                0:{
                    items:1
                },
                768:{
                    items:2
                },
                992:{
                    items:3
                }
            }
        });
    }

    // Set alt text for images missing alt (accessibility fix)
    $(document).ready(function () {
        // Skip images that already have alt text
        $('img').each(function () {
            var $img = $(this);
            if (!$img.attr('alt') || $img.attr('alt').trim() === '') {
                // Set alt based on image source or position
                var src = $img.attr('src') || '';
                if (src.includes('mastertruck_official_logo')) {
                    $img.attr('alt', 'Logo Master Truck');
                } else if (src.includes('stitch_img') && src.includes('.webp')) {
                    $img.attr('alt', 'Gambar layanan bengkel Master Truck');
                }
            }
        });
    });
    // Ronde 23: section & nav sesuai markup Stitch live (id & kelas aktual).
    $(document).ready(function () {
        const sections = document.querySelectorAll('#header-carousel, #layanan, #fleet, #fasilitas, #faq, #kontak');
        const navWidgets = document.querySelectorAll('.stitch-menu-panel a');

        function setActive(id) {
            navWidgets.forEach(function (a) {
                if (a.getAttribute('href') === '#' + id) {
                    a.classList.add('nav-link-active');
                } else {
                    a.classList.remove('nav-link-active');
                }
            });
        }

        if ('IntersectionObserver' in window && sections.length > 0 && navWidgets.length > 0) {
            const observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        const id = entry.target.getAttribute('id');
                        if (id) { setActive(id); }
                    }
                });
            }, {
                root: null,
                rootMargin: '-20% 0px -65% 0px',
                threshold: 0
            });

            sections.forEach(function (section) {
                observer.observe(section);
            });
        }
    });

    // Navbar mobile: tombol hamburger membuka/tutup panel collapse
    $(document).ready(function () {
        const $toggler = $('.navbar .navbar-toggler');
        const $panel = $('.navbar .navbar-menu-col');
        if (!$toggler.length || !$panel.length) { return; }
        function closeNav() {
            $panel.removeClass('show');
            $toggler.attr('aria-expanded', 'false');
        }
        $toggler.on('click', function (e) {
            e.preventDefault();
            const open = $panel.toggleClass('show').hasClass('show');
            $toggler.attr('aria-expanded', open ? 'true' : 'false');
        });
        // Link anchor: tutup panel DULU (reflow selesai) baru scroll —
        // kalau native navigation jalan duluan, layout shift saat panel
        // collapse menggeser target sehingga offset scroll-margin meleset.
        $panel.on('click', 'a', function (e) {
            const href = $(this).attr('href') || '';
            if (href.charAt(0) === '#') {
                e.preventDefault();
                closeNav();
                const target = document.querySelector(href);
                if (target) {
                    // Scroll ke posisi LAYOUT (offsetTop tak terpengaruh transform
                    // reveal — getBoundingClientRect masih membawa translateY saat
                    // transisi berjalan → landing meleset 16px). scroll-margin-top
                    // dibaca dari CSS agar tetap satu sumber dengan stylesheet.
                    const smt = parseFloat(getComputedStyle(target).scrollMarginTop) || 0;
                    let y = 0;
                    let node = target;
                    while (node) { y += node.offsetTop; node = node.offsetParent; }
                    window.scrollTo({ top: Math.max(0, y - smt), behavior: 'smooth' });
                    history.pushState(null, '', href);
                }
            } else {
                closeNav();
            }
        });
        $(document).on('keydown', function (e) { if (e.key === 'Escape') { closeNav(); } });
    });

    // ===== RONDE 21 (2c): hamburger menu mobile navbar Stitch =====
    // Tombol .stitch-nav-burger hanya tampil <= 991px (lihat mt-custom.css).
    $(document).ready(function () {
        var burger = document.querySelector('.stitch-nav-burger');
        var menuCol = document.querySelector('.stitch-menu-col');
        if (!burger || !menuCol) { return; }

        // Ronde 4 (1.3): <= 991px tombol Masuk/Daftar dipindahkan JS ke dalam
        // drawer (di dasar panel, selebar panel); >= 992px kembali ke bar.
        function placeNavActions() {
            var cta = document.querySelector('.stitch-nav-row > .stitch-cta-col') ||
                      document.querySelector('.stitch-menu-panel > .stitch-cta-col');
            var panel = document.querySelector('.stitch-menu-panel');
            var row = document.querySelector('.stitch-nav-row');
            if (!cta || !panel || !row) { return; }
            if (window.innerWidth <= 991) {
                if (cta.parentElement !== panel) { panel.appendChild(cta); }
            } else if (cta.parentElement !== row) {
                var menu = document.querySelector('.stitch-menu-col');
                if (menu && menu.nextSibling) { row.insertBefore(cta, menu.nextSibling); }
                else { row.appendChild(cta); }
            }
        }
        placeNavActions();
        window.addEventListener('resize', placeNavActions);

        // Ronde 25: tombol tutup jelas di dalam panel + fokus ter-trap + body terkunci.
        var closeBtn = null;
        var lastFocus = null;
        function focusables() {
            return [].slice.call(menuCol.querySelectorAll(
                'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
            )).filter(function (el) { return el.offsetParent !== null; });
        }
        function isOpen() { return menuCol.classList.contains('is-open'); }
        function closeMenu(restore) {
            if (!isOpen()) { return; }
            menuCol.classList.remove('is-open');
            burger.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('mt-drawer-open');
            if (restore !== false && lastFocus && lastFocus.focus) { lastFocus.focus(); }
            lastFocus = null;
        }
        function openMenu() {
            lastFocus = document.activeElement;
            menuCol.classList.add('is-open');
            burger.setAttribute('aria-expanded', 'true');
            document.body.classList.add('mt-drawer-open');
            var first = menuCol.querySelector('.stitch-menu-close') || focusables()[0];
            if (first && first.focus) { first.focus(); }
        }
        closeBtn = menuCol.querySelector('.stitch-menu-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                closeMenu();
            });
        }
        burger.addEventListener('click', function (e) {
            e.preventDefault();
            if (isOpen()) { closeMenu(); } else { openMenu(); }
        });
        // Klik tautan di panel: tutup panel, biarkan browser menggulir ke tujuan.
        menuCol.addEventListener('click', function (e) {
            var link = e.target && e.target.closest ? e.target.closest('a') : null;
            if (link) { closeMenu(false); }
        });
        document.addEventListener('click', function (e) {
            if (isOpen() && !menuCol.contains(e.target)) { closeMenu(false); }
        });
        document.addEventListener('keydown', function (e) {
            if (!isOpen()) { return; }
            if (e.key === 'Escape') { closeMenu(); return; }
            if (e.key !== 'Tab') { return; }
            var items = focusables();
            if (!items.length) { return; }
            var first = items[0];
            var last = items[items.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        });
        // Layar besar: pastikan kunci gulir dilepas.
        window.addEventListener('resize', function () {
            if (window.innerWidth > 991) {
                closeMenu(false);
                document.body.classList.remove('mt-drawer-open');
            }
        });
    });

    // ===== RONDE 25: titik indikator carousel (Layanan/Fasilitas/Testimoni) =====
    // Kartu di HP digeser horizontal (CSS scroll-snap); titik dibuat di sini agar
    // pengunjung tahu masih ada kartu berikutnya. Tanpa pustaka.
    $(document).ready(function () {
        var rows = [].slice.call(document.querySelectorAll(
            '.services-row-1, .services-row-2, .fac-row-1, .fac-row-2, .testimonials-row'
        ));
        rows.forEach(function (row) {
            if (row.getAttribute('data-mt-dots') === '1') { return; }
            var cards = [].slice.call(row.children).filter(function (el) {
                return el.nodeType === 1 && el.classList.contains('e-con');
            });
            if (cards.length < 2) { return; }
            row.setAttribute('data-mt-dots', '1');

            var dots = document.createElement('div');
            dots.className = 'mt-carousel-dots';
            cards.forEach(function (card, i) {
                var dot = document.createElement('button');
                dot.type = 'button';
                dot.setAttribute('aria-label', 'Ke kartu ' + (i + 1) + ' dari ' + cards.length);
                if (i === 0) { dot.setAttribute('aria-current', 'true'); }
                dot.addEventListener('click', function () {
                    var left = row.scrollLeft + (card.getBoundingClientRect().left - row.getBoundingClientRect().left) - 20;
                    if (row.scrollTo) {
                        row.scrollTo({ left: Math.max(0, left), behavior: 'smooth' });
                    } else {
                        row.scrollLeft = Math.max(0, left);
                    }
                });
                dots.appendChild(dot);
            });
            if (row.parentNode) { row.parentNode.insertBefore(dots, row.nextSibling); }

            var ticking = false;
            row.addEventListener('scroll', function () {
                if (ticking) { return; }
                ticking = true;
                window.requestAnimationFrame(function () {
                    ticking = false;
                    var anchor = row.getBoundingClientRect().left + 20;
                    var best = 0;
                    var bestGap = Infinity;
                    cards.forEach(function (card, i) {
                        var gap = Math.abs(card.getBoundingClientRect().left - anchor);
                        if (gap < bestGap) { bestGap = gap; best = i; }
                    });
                    [].forEach.call(dots.children, function (dot, i) {
                        if (i === best) { dot.setAttribute('aria-current', 'true'); }
                        else { dot.removeAttribute('aria-current'); }
                    });
                });
            }, { passive: true });
        });
    });

    // ===== RONDE 21 (2a): form booking -> pesan WhatsApp (tanpa pustaka) =====
    // URL dibangun dari 3 dropdown + atribut data-wa pada tombol (diisi builder).
    // window.MTBooking.url() dipakai tests/verify-stitch.cjs untuk menguji URL
    // tanpa benar-benar mengirim pesan.
    function mtBookingUrl() {
        var btn = document.getElementById('mt-booking-wa');
        if (!btn) { return null; }
        var wa = btn.getAttribute('data-wa') || '';
        function val(id) {
            var el = document.getElementById(id);
            return el ? el.value : '';
        }
        var msg = 'Halo Master Truck, saya ingin jadwal servis.\n' +
            'Unit: ' + val('mt-booking-unit') + '\n' +
            'Kebutuhan: ' + val('mt-booking-need') + '\n' +
            'Waktu: ' + val('mt-booking-time');
        return 'https://wa.me/' + wa + '?text=' + encodeURIComponent(msg);
    }
    window.MTBooking = { url: mtBookingUrl };

    $(document).ready(function () {
        var form = document.getElementById('mt-booking-form');
        var btn = document.getElementById('mt-booking-wa');
        if (!form || !btn) { return; }
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var url = mtBookingUrl();
            if (!url) { return; }
            btn.href = url;
            window.open(url, '_blank', 'noopener');
        });
    });

    // Hero 2-Slide Transition di Frontend (Elementor Native Sections)
    $(document).ready(function () {
        const $slides = $('.mt-hero-slide-item');
        if ($slides.length > 1 && !$('body').hasClass('elementor-editor-active')) {
            let current = 0;
            $slides.slice(1).addClass('slide-hidden');

            function showSlide(index) {
                current = index;
                $slides.addClass('slide-hidden');
                $slides.eq(current).removeClass('slide-hidden');
                $('.hero-slider-nav').each(function () {
                    $(this).find('.hero-slider-dot').removeClass('active').eq(current).addClass('active');
                });
            }

            $slides.each(function () {
                const $nav = $('<div class="hero-slider-nav"></div>');
                $slides.each(function (i) {
                    const $btn = $('<button type="button" class="hero-slider-dot' + (i === 0 ? ' active' : '') + '" aria-label="Slide ' + (i + 1) + '"></button>');
                    $btn.on('click', function (e) {
                        e.stopPropagation();
                        showSlide(i);
                    });
                    $nav.append($btn);
                });
                $(this).append($nav);
            });

            let timer = setInterval(function () {
                showSlide((current + 1) % $slides.length);
            }, 6000);

            $slides.hover(
                function () { clearInterval(timer); },
                function () {
                    timer = setInterval(function () {
                        showSlide((current + 1) % $slides.length);
                    }, 6000);
                }
            );
        }
    });

    // ===== Revamp lanjutan (2026-10-10): reveal, carousel HP, back-to-top =====
    $(document).ready(function () {
        document.body.classList.add('mt-js');
        var isPage59 = document.body.classList.contains('elementor-page-59');
        var inEditor = document.body.classList.contains('elementor-editor-active') ||
                       document.body.classList.contains('elementor-editor-preview') ||
                       window.location.search.indexOf('elementor-preview') !== -1;

        var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        // REVAMP6m I: matikan animasi masuk untuk screenshot/test otomatis.
        try {
            if (window.navigator && window.navigator.webdriver) {
                document.documentElement.classList.add('no-anim');
            }
        } catch (e) {}
        // REVAMP6m G: pill navbar jadi kaca saat scroll > 24px (tanpa CLS).
        if (isPage59 && !inEditor) {
            var mtNavPill = document.querySelector('.navbar-pill');
            if (mtNavPill) {
                var mtNavTick = function () {
                    mtNavPill.classList.toggle('is-scrolled', window.scrollY > 24);
                };
                window.addEventListener('scroll', mtNavTick, { passive: true });
                mtNavTick();
            }
        }
        if (isPage59 && !inEditor && !reduce && 'IntersectionObserver' in window) {
            var targets = document.querySelectorAll(
                'body.elementor-page-59 .elementor-59 > .e-con' +
                ':not(.navbar):not(.mt-hero-slide):not(.top-bar-custom):not(.mt-wa-float-section):not(.mt-action-bar), ' +
                'body.elementor-page-59 > .elementor > .elementor-top-section' +
                ':not(.navbar):not(.mt-hero-slide):not(.top-bar-custom):not(.mt-wa-float-section):not(.mt-action-bar), ' +
                'body.elementor-page-59 > .elementor > .e-con' +
                ':not(.navbar):not(.mt-hero-slide):not(.top-bar-custom):not(.mt-wa-float-section):not(.mt-action-bar)'
            );
            if (targets.length) {
                var io = new IntersectionObserver(function (entries) {
                    entries.forEach(function (en) {
                        if (en.isIntersecting) {
                            en.target.classList.add('is-inview');
                            io.unobserve(en.target);
                        }
                    });
                }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
                Array.prototype.forEach.call(targets, function (el) {
                    el.classList.add('mt-reveal');
                    io.observe(el);
                });
            }
        }

        // REVAMP6j E2: di editor Elementor, counter langsung nilai akhir (tanpa animasi).
        // Widget editor dirender async + animasi counter Elementor menimpa,
        // jadi snap diulang singkat (hanya mode editor, tanpa efek ke frontend).
        if (isPage59 && inEditor) {
            var mtSnapCounters = function () {
                Array.prototype.forEach.call(document.querySelectorAll('.elementor-counter-number'), function (el) {
                    var to = el.getAttribute('data-to-value');
                    if (to === null || to === '') { return; }
                    var delim = el.getAttribute('data-delimiter') || '';
                    var out = String(Math.round(parseFloat(to)));
                    if (delim) {
                        out = out.replace(/\B(?=(\d{3})+(?!\d))/g, delim);
                    }
                    if (el.textContent !== out) { el.textContent = out; }
                    if (el.getAttribute('data-duration') !== '0') { el.setAttribute('data-duration', '0'); }
                });
            };
            mtSnapCounters();
            var mtSnapTries = 0;
            var mtSnapTimer = setInterval(function () {
                mtSnapCounters();
                mtSnapTries++;
                if (mtSnapTries >= 30) { clearInterval(mtSnapTimer); }
            }, 500);
        }

        // 2) Carousel HP: matikan fade tepi kanan saat sudah di ujung scroll
        ['.sec-services-cards', '.sec-team-cards', '.sec-testimonial-cards'].forEach(function (sel) {
            Array.prototype.forEach.call(document.querySelectorAll(sel), function (sec) {
                var box = sec.querySelector(':scope > .elementor-container') || sec.querySelector(':scope > .e-con-inner') || sec;
                if (!box) { return; }
                var upd = function () {
                    var atEnd = box.scrollLeft + box.clientWidth >= box.scrollWidth - 4;
                    sec.classList.toggle('mt-scroll-end', atEnd);
                };
                box.addEventListener('scroll', upd, { passive: true });
                upd();
            });
        });

        // 3) Back-to-top & Floating WhatsApp (hanya homepage, di luar Elementor editor)
        if (isPage59 && !inEditor) {
            // Floating WhatsApp button
            // RONDE 21: nomor WA diambil dari builder (data-wa di tombol booking)
            // agar tidak ada nomor karangan di main.js.
            var mtWaSrc = document.getElementById('mt-booking-wa');
            var mtWaNumber = mtWaSrc ? (mtWaSrc.getAttribute('data-wa') || '') : '';
            if (!document.querySelector('.floating-wa-btn') && mtWaNumber) {
                var waBtn = document.createElement('a');
                waBtn.href = 'https://wa.me/' + mtWaNumber + '?text=' + encodeURIComponent('Halo Master Truck, saya butuh bantuan untuk armada saya.');
                waBtn.target = '_blank';
                waBtn.rel = 'noopener noreferrer';
                waBtn.className = 'floating-wa-btn';
                waBtn.setAttribute('aria-label', 'Chat WhatsApp');
                waBtn.innerHTML = '<i class="fab fa-whatsapp" aria-hidden="true"></i>';
                document.body.appendChild(waBtn);
                // REVAMP6j B5: sembunyikan WA saat foto hero tampil agar tak
                // menutupi pil foto; muncul lagi setelah hero lewat viewport.
                var mtHeroImg = document.querySelector('.mt-hero-slide .hero-truck-img');
                if (mtHeroImg && 'IntersectionObserver' in window) {
                    var mtWaIO = new IntersectionObserver(function (entries) {
                        entries.forEach(function (en) {
                            waBtn.classList.toggle('mt-wa-hidden', en.isIntersecting);
                        });
                    }, { threshold: 0.15 });
                    mtWaIO.observe(mtHeroImg);
                }
            }

            // Back to top button (lingkaran 48x48 di atas WA)
            if (!document.querySelector('.mt-back-top')) {
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'mt-back-top';
                btn.setAttribute('aria-label', 'Kembali ke atas');
                btn.innerHTML = '<i class="fas fa-arrow-up" aria-hidden="true"></i>';
                document.body.appendChild(btn);
                btn.addEventListener('click', function () {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
                var tick = function () {
                    btn.classList.toggle('is-visible', window.scrollY > 400);
                };
                window.addEventListener('scroll', tick, { passive: true });
                tick();
            }

            // 4) Scroll progress bar tipis di atas navbar
            if (!document.querySelector('.mt-scroll-progress')) {
                var bar = document.createElement('div');
                bar.className = 'mt-scroll-progress';
                bar.setAttribute('aria-hidden', 'true');
                document.body.appendChild(bar);
                var updateBar = function () {
                    var doc = document.documentElement;
                    var max = (doc.scrollHeight - window.innerHeight) || 1;
                    var pct = Math.min(100, Math.max(0, (window.scrollY / max) * 100));
                    bar.style.width = pct.toFixed(2) + '%';
                };
                window.addEventListener('scroll', updateBar, { passive: true });
                window.addEventListener('resize', updateBar, { passive: true });
                updateBar();
            }
        }
    });


    // =====================================================
    // RONDE 24 (3.2) — Bar aksi mobile sembunyi saat form fokus
    // =====================================================
    function mtInitActionBar() {
        var bar = document.querySelector('.mt-action-bar');
        if (!bar) return;
        document.addEventListener('focusin', function (e) {
            var t = e.target;
            if (t && t.matches && t.matches('input, select, textarea')) {
                bar.classList.add('is-hidden');
            }
        });
        document.addEventListener('focusout', function () {
            setTimeout(function () {
                var a = document.activeElement;
                if (!a || !a.matches || !a.matches('input, select, textarea')) {
                    bar.classList.remove('is-hidden');
                }
            }, 140);
        });
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', mtInitActionBar);
    } else {
        mtInitActionBar();
    }

})(jQuery);
