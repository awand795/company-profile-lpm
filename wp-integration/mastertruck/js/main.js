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
        if ($(this).scrollTop() > 35) {
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

    // Section Active Scrollspy via IntersectionObserver
    // Nav Elementor = widget .nav-menu-link (bukan .nav-link bootstrap),
    // href dibaca dari tombol di dalamnya.
    $(document).ready(function () {
        const sections = document.querySelectorAll('#header-carousel, #about, #service, #testimonial, #faq, #contact');
        const navWidgets = document.querySelectorAll('.navbar-right-inner .nav-menu-link');

        function setActive(id) {
            navWidgets.forEach(function (widget) {
                const a = widget.querySelector('a');
                if (a && a.getAttribute('href') === '#' + id) {
                    widget.classList.add('nav-link-active');
                } else {
                    widget.classList.remove('nav-link-active');
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
        var inEditor = document.body.classList.contains('elementor-editor-active');

        // 1) Reveal halus per section — sekali tampil lalu unobserve.
        //    Kecualikan: navbar (sticky), hero (jangan berkedip), topbar, WA float.
        var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (isPage59 && !inEditor && !reduce && 'IntersectionObserver' in window) {
            var targets = document.querySelectorAll(
                'body.elementor-page-59 .elementor-top-section' +
                ':not(.navbar):not(.mt-hero-slide):not(.top-bar-custom):not(.mt-wa-float-section)'
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

        // 2) Carousel HP: matikan fade tepi kanan saat sudah di ujung scroll
        ['.sec-services-cards', '.sec-team-cards', '.sec-testimonial-cards'].forEach(function (sel) {
            Array.prototype.forEach.call(document.querySelectorAll(sel), function (sec) {
                var box = sec.querySelector(':scope > .elementor-container');
                if (!box) { return; }
                var upd = function () {
                    var atEnd = box.scrollLeft + box.clientWidth >= box.scrollWidth - 4;
                    sec.classList.toggle('mt-scroll-end', atEnd);
                };
                box.addEventListener('scroll', upd, { passive: true });
                upd();
            });
        });

        // 3) Back-to-top (hanya homepage, di luar Elementor editor)
        if (isPage59 && !inEditor) {
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
    });

})(jQuery);

