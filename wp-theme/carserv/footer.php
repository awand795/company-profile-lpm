<?php
/**
 * Footer Template - CarServ Master Truck Enterprise
 */
$theme_uri  = get_template_directory_uri();
$mt_contact = mt_get_contact_data();
?>
    <!-- Footer Start (Clean Light Enterprise Design) -->
    <footer id="contact" class="footer-clean pt-5 mt-5">
        <div class="container py-4">
            <div class="row g-4 g-lg-5">
                <div class="col-lg-4 col-md-6">
                    <h4 class="mb-3 footer-heading">PT MASTER TRUCK INDONESIA</h4>
                    <p class="mb-3 text-muted">Pusat bengkel rekayasa spesialis armada truk niaga &amp; alat berat, serta distributor resmi pelumas industri, ban komersial, dan suku cadang OEM di Sumatera Utara.</p>
                    <div class="d-flex align-items-start mb-2">
                        <i class="fa fa-map-marker-alt text-primary me-3 mt-1"></i>
                        <span><?php echo esc_html( $mt_contact['address_full'] ); ?></span>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <span>
                            <a href="tel:<?php echo esc_attr( $mt_contact['phone_raw'] ); ?>" class="text-decoration-none fw-bold text-dark"><?php echo esc_html( $mt_contact['phone'] ); ?></a>
                            &bull;
                            <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck" target="_blank" rel="noopener noreferrer" class="text-decoration-none fw-bold text-dark"><?php echo esc_html( $mt_contact['wa'] ); ?></a>
                        </span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="fa fa-envelope text-primary me-3"></i>
                        <span><a href="mailto:<?php echo esc_attr( $mt_contact['email'] ); ?>" class="text-decoration-none text-dark"><?php echo esc_html( $mt_contact['email'] ); ?></a></span>
                    </div>
                    <div class="d-flex gap-2 pt-1">
                        <a class="btn-social" href="<?php echo esc_url( $mt_contact['social']['facebook'] ); ?>" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a class="btn-social" href="<?php echo esc_url( $mt_contact['social']['instagram'] ); ?>" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a class="btn-social" href="<?php echo esc_url( $mt_contact['social']['whatsapp'] ); ?>" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>

                <div class="col-lg-2 col-md-6">
                    <h4 class="mb-3 footer-heading">Navigasi</h4>
                    <a class="btn-link" href="#header-carousel">Beranda</a>
                    <a class="btn-link" href="#about">Profil</a>
                    <a class="btn-link" href="#service">Layanan</a>
                    <a class="btn-link" href="#principals">Produk</a>
                    <a class="btn-link" href="#distribution">Distribusi</a>
                    <a class="btn-link" href="#contact">Kontak</a>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h4 class="mb-3 footer-heading">Layanan Bengkel</h4>
                    <a class="btn-link" href="#service">Overhaul Mesin Diesel</a>
                    <a class="btn-link" href="#service">Sistem Rem Angin &amp; Pneumatik</a>
                    <a class="btn-link" href="#service">Scanner Diagnostik ECU</a>
                    <a class="btn-link" href="#service">Penggantian Pelumas Resmi</a>
                    <a class="btn-link" href="#service">Spooring &amp; Ban Komersial</a>
                    <a class="btn-link" href="#booking">Layanan Derek 24 Jam Siaga</a>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h4 class="mb-3 footer-heading">Jam Operasional</h4>
                    <div class="mb-2">
                        <div class="fw-bold text-dark">Senin &ndash; Jumat:</div>
                        <small class="text-muted"><?php echo esc_html( $mt_contact['hours_weekday'] ); ?></small>
                    </div>
                    <div class="mb-2">
                        <div class="fw-bold text-dark">Sabtu:</div>
                        <small class="text-muted"><?php echo esc_html( $mt_contact['hours_saturday'] ); ?></small>
                    </div>
                    <div class="mb-4">
                        <div class="fw-bold text-primary">Emergency &amp; Derek:</div>
                        <span class="badge bg-danger-subtle text-danger fw-semibold px-2 py-1">Siaga 24 Jam / 7 Hari</span>
                    </div>
                    <div class="d-flex gap-2">
                        <a href="<?php echo mt_fleet_url( '#login' ); ?>" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary btn-sm flex-fill">
                            <i class="fa fa-sign-in-alt me-1"></i> Login Fleet
                        </a>
                        <a href="<?php echo mt_fleet_url( '#register' ); ?>" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm flex-fill">
                            <i class="fa fa-user-plus me-1"></i> Daftar Mitra
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="container">
            <div class="copyright">
                <div class="row align-items-center">
                    <div class="col-md-6 text-center text-md-start mb-2 mb-md-0">
                        &copy; <?php echo date( 'Y' ); ?> <a href="#">PT MASTER TRUCK INDONESIA</a>. Seluruh Hak Cipta Dilindungi.
                    </div>
                    <div class="col-md-6 text-center text-md-end">
                        <div class="footer-menu">
                            <a href="#header-carousel">Beranda</a>
                            <a href="#about">Tentang Kami</a>
                            <a href="<?php echo mt_fleet_url( '#login' ); ?>" target="_blank" rel="noopener noreferrer">Login Fleet</a>
                            <a href="<?php echo mt_fleet_url( '#register' ); ?>" target="_blank" rel="noopener noreferrer">Daftar Mitra</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
    <!-- Footer End -->

    <!-- Floating Buttons (Stacked: Back to Top above WhatsApp) -->
    <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck" class="floating-wa-btn" target="_blank" rel="noopener noreferrer" aria-label="Konsultasi WhatsApp">
        <i class="fab fa-whatsapp"></i>
    </a>
    <a href="#" class="back-to-top" aria-label="Kembali ke atas">
        <i class="fa fa-arrow-up"></i>
    </a>

    <?php wp_footer(); ?>
</body>

</html>
