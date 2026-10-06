<?php
/**
 * Footer Template - CarServ Master Truck Enterprise
 * "Industrial-Clean White" Theme
 */
$theme_uri     = get_template_directory_uri();
$web_fleet_url = 'http://localhost:3000';
?>
    <!-- Footer Start (Industrial-Clean White) -->
    <footer id="contact" class="footer-clean mt-section--border-top">
        <div class="container pb-5">
            <div class="row g-4 g-lg-5">
                <div class="col-lg-4 col-md-6">
                    <h4 class="footer-heading">PT MASTER TRUCK INDONESIA</h4>
                    <p class="mb-4">Pusat bengkel rekayasa spesialis armada truk niaga &amp; alat berat, serta distributor resmi pelumas industri, ban komersial, dan suku cadang OEM di Sumatera Utara.</p>
                    
                    <div class="footer-contact-item">
                        <i class="bi bi-geo-alt-fill"></i>
                        <span>KIM III No. 3A, Mabar, Medan Labuhan, Kota Medan 20242</span>
                    </div>
                    <div class="footer-contact-item">
                        <i class="bi bi-telephone-fill"></i>
                        <span>(061) 8882-9999 / 0812-3456-7890</span>
                    </div>
                    <div class="footer-contact-item">
                        <i class="bi bi-envelope-fill"></i>
                        <span>info@mastertruck.co.id</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-6">
                    <h4 class="footer-heading">Navigasi</h4>
                    <ul class="footer-links">
                        <li><a href="#hero">Beranda</a></li>
                        <li><a href="#about">Profil Perusahaan</a></li>
                        <li><a href="#service">Layanan Bengkel</a></li>
                        <li><a href="#principals">Prinsipal OEM</a></li>
                        <li><a href="#distribution">Jaringan Distribusi</a></li>
                        <li><a href="#booking">Jadwal Servis</a></li>
                    </ul>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h4 class="footer-heading">Layanan Unggulan</h4>
                    <ul class="footer-links">
                        <li><a href="#service">Overhaul Mesin Diesel Common Rail</a></li>
                        <li><a href="#service">Sistem Rem Angin &amp; Pneumatik</a></li>
                        <li><a href="#service">Diagnostik Komputer ECU 24V</a></li>
                        <li><a href="#service">Distributor Pelumas Pertamina &amp; Mobil</a></li>
                        <li><a href="#service">Ban Komersial Dunlop &amp; Spooring</a></li>
                        <li><a href="#booking">Derek Evakuasi Truk Heavy-Duty 24 Jam</a></li>
                    </ul>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h4 class="footer-heading">Operasional &amp; Web Fleet</h4>
                    <div class="mb-3">
                        <div class="fw-bold text-dark">Senin &ndash; Jumat:</div>
                        <span class="text-muted">08.00 &ndash; 17.00 WIB</span>
                    </div>
                    <div class="mb-3">
                        <div class="fw-bold text-dark">Sabtu:</div>
                        <span class="text-muted">08.00 &ndash; 15.00 WIB</span>
                    </div>
                    <div class="mb-4">
                        <div class="fw-bold text-brand-primary">Derek Evakuasi Darurat:</div>
                        <span class="badge bg-danger text-white fw-semibold px-2 py-1">Siaga 24 Jam Penuh</span>
                    </div>
                    <div class="d-flex gap-2">
                        <a href="<?php echo esc_url( $web_fleet_url . '/#login' ); ?>" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary btn-sm flex-fill">
                            <i class="bi bi-box-arrow-in-right"></i> Login Fleet
                        </a>
                        <a href="<?php echo esc_url( $web_fleet_url . '/#register' ); ?>" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm flex-fill">
                            <i class="bi bi-person-plus"></i> Daftar
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="copyright-bar">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-7 text-center text-md-start mb-2 mb-md-0">
                        &copy; <?php echo date('Y'); ?> <strong class="text-dark">PT MASTER TRUCK INDONESIA</strong>. Seluruh Hak Cipta Dilindungi. KIM III Medan.
                    </div>
                    <div class="col-md-5 text-center text-md-end">
                        <a href="#hero" class="text-muted text-decoration-none me-3">Kembali ke Atas</a>
                        <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" class="text-muted text-decoration-none">Bantuan Hotline</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
    <!-- Footer End -->

    <!-- Floating Buttons (Single WhatsApp + Stacked Back-to-Top) -->
    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck%2C%20saya%20ingin%20konsultasi%20armada" target="_blank" rel="noopener noreferrer" class="floating-wa-btn" aria-label="Hubungi WhatsApp">
        <i class="bi bi-whatsapp"></i>
    </a>
    <a href="#" class="back-to-top" aria-label="Kembali ke atas">
        <i class="bi bi-arrow-up"></i>
    </a>

    <?php wp_footer(); ?>
</body>

</html>
