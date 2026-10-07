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
    $(document).ready(function () {
        const sections = document.querySelectorAll('#header-carousel, #about, #service, #principals, #distribution, #contact');
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

        if ('IntersectionObserver' in window && sections.length > 0 && navLinks.length > 0) {
            const observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        const id = entry.target.getAttribute('id');
                        if (id) {
                            navLinks.forEach(function (link) {
                                if (link.getAttribute('href') === '#' + id) {
                                    link.classList.add('active');
                                } else {
                                    link.classList.remove('active');
                                }
                            });
                        }
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

})(jQuery);

