<?php
/**
 * Plugin Name: MT Booking Form
 * Description: Shortcode [mt_booking_form] — form Booking Servis via WhatsApp. Editable terpisah, bisa dipakai di Elementor Shortcode widget.
 * Version: 1.0.0
 */
defined('ABSPATH') || exit;

function mt_booking_form_shortcode($atts) {
    $atts = shortcode_atts(array(
        'wa' => '6281234567890',
        'title' => 'Booking Servis Truk',
        'subtitle' => 'Isi form — langsung terkirim ke WhatsApp bengkel.',
    ), $atts, 'mt_booking_form');
    $wa = preg_replace('/[^0-9]/', '', $atts['wa']);
    if ($wa === '') { $wa = '6281234567890'; }
    ob_start();
    ?>
    <div class="booking-form-box">
        <h3 class="text-center mb-1"><?php echo esc_html($atts['title']); ?></h3>
        <p class="text-center text-muted mb-4"><?php echo esc_html($atts['subtitle']); ?></p>
        <form class="mt-booking-form" data-wa="<?php echo esc_attr($wa); ?>" onsubmit="return mtBookingSubmit(event, this);">
            <div class="row g-3">
                <div class="col-12 col-sm-6"><input type="text" name="bk_name" class="form-control" placeholder="Nama / Perusahaan" required /></div>
                <div class="col-12 col-sm-6"><input type="tel" name="bk_phone" class="form-control" placeholder="No. WhatsApp" required /></div>
                <div class="col-12 col-sm-6">
                    <select name="bk_service" class="form-select">
                        <option selected>Servis Rutin &amp; Cek 30 Bagian</option>
                        <option>Servis Mesin Besar</option>
                        <option>Rem Angin &amp; Kaki-Kaki</option>
                        <option>Ganti Oli</option>
                        <option>Ban Dunlop</option>
                        <option>Aki &amp; Kelistrikan</option>
                        <option>Derek Darurat 24 Jam</option>
                    </select>
                </div>
                <div class="col-12 col-sm-6"><input type="date" name="bk_date" class="form-control" required /></div>
                <div class="col-12"><textarea name="bk_notes" class="form-control" rows="3" placeholder="Nomor Polisi / Gejala Kerusakan"></textarea></div>
                <div class="col-12"><button type="submit" class="btn btn-primary w-100 py-3"><i class="fab fa-whatsapp me-2"></i>Kirim Permintaan Servis</button></div>
            </div>
        </form>
        <script>
        function mtBookingSubmit(e, form) {
            e.preventDefault();
            var wa = form.getAttribute('data-wa') || '6281234567890';
            function v(n){ var el = form.querySelector('[name="'+n+'"]'); return el ? encodeURIComponent(el.value) : ''; }
            var msg = 'Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:%0ANama:%20' + v('bk_name') + '%0ANo%20WA:%20' + v('bk_phone') + '%0ALayanan:%20' + v('bk_service') + '%0ATanggal:%20' + v('bk_date') + '%0ANoPol/Keterangan:%20' + v('bk_notes');
            window.open('https://wa.me/' + wa + '?text=' + msg, '_blank');
            return false;
        }
        </script>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('mt_booking_form', 'mt_booking_form_shortcode');
