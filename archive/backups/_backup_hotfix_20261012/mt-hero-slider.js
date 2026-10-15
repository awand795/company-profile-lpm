/**
 * mt-hero-slider.js — Lightweight Enterprise Hero Slider (<= 60 lines)
 * 2 Native Elementor Slides, Autoplay 7s, Fade 400ms, Accessible
 */
document.addEventListener('DOMContentLoaded', () => {
    if (document.body.classList.contains('elementor-editor-active')) return;
    const slider = document.querySelector('.mt-hero-slider');
    if (!slider) return;
    const slides = slider.querySelectorAll('.mt-hero-slide');
    if (slides.length < 2) return;

    const prevBtn = slider.querySelector('.mt-hero-nav__prev');
    const nextBtn = slider.querySelector('.mt-hero-nav__next');
    const dots = slider.querySelectorAll('.mt-hero-dot');
    const counter = slider.querySelector('.mt-hero-counter');

    let current = 0, timer = null;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function showSlide(index) {
        current = (index + slides.length) % slides.length;
        slides.forEach((s, i) => {
            const active = i === current;
            s.classList.toggle('is-active', active);
            s.setAttribute('aria-hidden', !active);
            s.querySelectorAll('a, button, input').forEach(f => f.tabIndex = active ? 0 : -1);
        });
        dots.forEach((d, i) => d.classList.toggle('is-active', i === current));
        if (counter) counter.textContent = `0${current + 1} / 0${slides.length}`;
    }

    function next() { showSlide(current + 1); }
    function prev() { showSlide(current - 1); }
    function startAuto() { if (!reducedMotion) { stopAuto(); timer = setInterval(next, 7000); } }
    function stopAuto() { if (timer) { clearInterval(timer); timer = null; } }

    if (nextBtn) nextBtn.addEventListener('click', () => { next(); startAuto(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { prev(); startAuto(); });
    dots.forEach((d, idx) => d.addEventListener('click', () => { showSlide(idx); startAuto(); }));

    slider.addEventListener('mouseenter', stopAuto);
    slider.addEventListener('mouseleave', startAuto);
    slider.addEventListener('focusin', stopAuto);
    slider.addEventListener('focusout', startAuto);

    let startX = 0;
    slider.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
    slider.addEventListener('touchend', (e) => {
        const diff = e.changedTouches[0].clientX - startX;
        if (Math.abs(diff) > 50) { diff > 0 ? prev() : next(); startAuto(); }
    }, { passive: true });

    showSlide(0);
    startAuto();
});
