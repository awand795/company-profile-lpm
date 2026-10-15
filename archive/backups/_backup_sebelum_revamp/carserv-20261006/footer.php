<?php
/**
 * Footer Template - CarServ Master Truck
 */
$theme_uri = get_template_directory_uri();
?>
    <!-- Footer Start -->
    <div id="contact" class="container-fluid bg-dark text-light footer pt-5 mt-5 wow fadeIn" data-wow-delay="0.1s">
        <div class="container py-5">
            <div class="row g-5">
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Lokasi &amp; Kontak</h4>
                    <p class="mb-2"><i class="fa fa-map-marker-alt me-3 text-primary"></i>KIM III No. 3A, Mabar, Medan Labuhan, Kota Medan 20242</p>
                    <p class="mb-2"><i class="fa fa-phone-alt me-3 text-primary"></i>(061) 8882-9999 / 0812-3456-7890</p>
                    <p class="mb-2"><i class="fa fa-envelope me-3 text-primary"></i>info@mastertruck.co.id</p>
                    <div class="d-flex pt-2">
                        <a class="btn btn-outline-light btn-social" href="#"><i class="fab fa-facebook-f"></i></a>
                        <a class="btn btn-outline-light btn-social" href="#"><i class="fab fa-instagram"></i></a>
                        <a class="btn btn-outline-light btn-social" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Jam Operasional</h4>
                    <h6 class="text-light">Senin - Jumat:</h6>
                    <p class="mb-4 text-muted">08.00 - 17.00 WIB</p>
                    <h6 class="text-light">Sabtu:</h6>
                    <p class="mb-4 text-muted">08.00 - 15.00 WIB</p>
                    <h6 class="text-light">Layanan Derek &amp; Panggilan:</h6>
                    <p class="mb-0 text-primary fw-bold">24 Jam / 7 Hari Siaga</p>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Layanan Utama</h4>
                    <a class="btn btn-link" href="#service">Overhaul Mesin Diesel</a>
                    <a class="btn btn-link" href="#service">Rem Angin &amp; Pneumatik</a>
                    <a class="btn btn-link" href="#service">Ban Komersial Dunlop</a>
                    <a class="btn btn-link" href="#service">Pelumas Pertamina &amp; Mobil</a>
                    <a class="btn btn-link" href="#service">Scanner Diagnostik ECU</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Portal Fleet</h4>
                    <p class="text-muted">Monitoring servis armada Anda secara real-time via sistem Web Fleet.</p>
                    <div class="position-relative mx-auto" style="max-width: 400px;">
                        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn btn-primary w-100 py-3 mb-2">
                            <i class="fa fa-desktop me-2"></i>Login Web Fleet
                        </a>
                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-secondary w-100 py-2">
                            <i class="fa fa-user-plus me-2"></i>Daftar Mitra Baru
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="copyright">
                <div class="row">
                    <div class="col-md-6 text-center text-md-start mb-3 mb-md-0">
                        &copy; 2026 <a class="border-bottom" href="#">PT MASTER TRUCK INDONESIA</a>, Seluruh Hak Cipta Dilindungi.
                    </div>
                    <div class="col-md-6 text-center text-md-end">
                        <div class="footer-menu">
                            <a href="#header-carousel">Beranda</a>
                            <a href="#about">Profil &amp; Sejarah</a>
                            <a href="http://localhost:3000/#login">Login Fleet</a>
                            <a href="http://localhost:3000/#register">Daftar Mitra</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Footer End -->

    <!-- Back to Top -->
    <a href="#" class="btn btn-lg btn-primary btn-lg-square back-to-top"><i class="bi bi-arrow-up"></i></a>

    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/wow/wow.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/easing/easing.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/waypoints/waypoints.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/counterup/counterup.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/owlcarousel/owl.carousel.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/tempusdominus/js/moment.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/tempusdominus/js/moment-timezone.min.js"></script>
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/lib/tempusdominus/js/tempusdominus-bootstrap-4.min.js"></script>

    <!-- Template Javascript -->
    <script src="<?php echo esc_url( $theme_uri ); ?>/assets/js/main.js"></script>

    <?php wp_footer(); ?>
</body>

</html>
