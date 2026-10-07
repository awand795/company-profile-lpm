<?php
/**
 * Master Truck Landing Page Fields Editor
 * Menambahkan metabox pengaturan konten di Halaman Beranda (Pages -> Beranda).
 */
defined( 'ABSPATH' ) || exit;

/**
 * Daftar semua field yang dapat diedit di Landing Page beserta nilai bawaannya.
 */
function mt_get_landing_fields_schema() {
	return array(
		'hero' => array(
			'title'  => '🎯 Hero Banner & Slider',
			'fields' => array(
				// Slide 1
				'hero_s1_pill'       => array( 'label' => 'Slide 1 — Badge / Label Atas', 'type' => 'text', 'default' => 'PT Master Truck Indonesia • KIM III Medan' ),
				'hero_s1_title'      => array( 'label' => 'Slide 1 — Judul Utama (bisa pakai HTML <span>)', 'type' => 'text', 'default' => 'Master Truck: Bengkel Truk <span class="hero-brand-highlight">Terpercaya</span> di Medan' ),
				'hero_s1_lead'       => array( 'label' => 'Slide 1 — Deskripsi Singkat', 'type' => 'textarea', 'default' => 'Sudah 15 tahun kami merawat truk sekaligus menjual oli, ban, dan aki asli langsung dari pabriknya — dipercaya 120+ perusahaan.' ),
				'hero_s1_stat1_num'  => array( 'label' => 'Slide 1 — Statistik 1 (Angka)', 'type' => 'text', 'default' => '15' ),
				'hero_s1_stat1_lbl'  => array( 'label' => 'Slide 1 — Statistik 1 (Label)', 'type' => 'text', 'default' => 'Tahun Berpengalaman' ),
				'hero_s1_stat2_num'  => array( 'label' => 'Slide 1 — Statistik 2 (Angka)', 'type' => 'text', 'default' => '120+' ),
				'hero_s1_stat2_lbl'  => array( 'label' => 'Slide 1 — Statistik 2 (Label)', 'type' => 'text', 'default' => 'Perusahaan Pelanggan' ),
				'hero_s1_stat3_num'  => array( 'label' => 'Slide 1 — Statistik 3 (Angka)', 'type' => 'text', 'default' => '2.500' ),
				'hero_s1_stat3_lbl'  => array( 'label' => 'Slide 1 — Statistik 3 (Label)', 'type' => 'text', 'default' => 'Truk per Tahun' ),
				'hero_s1_btn1_text'  => array( 'label' => 'Slide 1 — Teks Tombol Utama', 'type' => 'text', 'default' => 'Jadwalkan Servis' ),
				'hero_s1_btn1_url'   => array( 'label' => 'Slide 1 — Link Tombol Utama', 'type' => 'text', 'default' => '#booking' ),
				'hero_s1_btn2_text'  => array( 'label' => 'Slide 1 — Teks Tombol Kedua', 'type' => 'text', 'default' => 'Portal Web Fleet' ),
				'hero_s1_btn2_url'   => array( 'label' => 'Slide 1 — Link Tombol Kedua', 'type' => 'text', 'default' => 'http://localhost:3000/#login' ),
				// Slide 2
				'hero_s2_pill'       => array( 'label' => 'Slide 2 — Badge / Label Atas', 'type' => 'text', 'default' => 'PT Master Truck Indonesia • Distributor Nasional Resmi' ),
				'hero_s2_title'      => array( 'label' => 'Slide 2 — Judul Utama (bisa pakai HTML <span>)', 'type' => 'text', 'default' => 'Master Truck: <span class="hero-brand-highlight">Sparepart Truk Asli</span> dari Pabrik' ),
				'hero_s2_lead'       => array( 'label' => 'Slide 2 — Deskripsi Singkat', 'type' => 'textarea', 'default' => 'Oli Pertamina, oli Mobil, ban Dunlop & aki GS Astra — dijamin asli dari pabriknya, dengan harga khusus untuk pelanggan perusahaan.' ),
				'hero_s2_stat1_num'  => array( 'label' => 'Slide 2 — Statistik 1 (Angka)', 'type' => 'text', 'default' => '15' ),
				'hero_s2_stat1_lbl'  => array( 'label' => 'Slide 2 — Statistik 1 (Label)', 'type' => 'text', 'default' => 'Tahun Berpengalaman' ),
				'hero_s2_stat2_num'  => array( 'label' => 'Slide 2 — Statistik 2 (Angka)', 'type' => 'text', 'default' => '120+' ),
				'hero_s2_stat2_lbl'  => array( 'label' => 'Slide 2 — Statistik 2 (Label)', 'type' => 'text', 'default' => 'Perusahaan Pelanggan' ),
				'hero_s2_stat3_num'  => array( 'label' => 'Slide 2 — Statistik 3 (Angka)', 'type' => 'text', 'default' => '2.500' ),
				'hero_s2_stat3_lbl'  => array( 'label' => 'Slide 2 — Statistik 3 (Label)', 'type' => 'text', 'default' => 'Truk per Tahun' ),
				'hero_s2_btn1_text'  => array( 'label' => 'Slide 2 — Teks Tombol Utama', 'type' => 'text', 'default' => 'Lihat Produk OEM' ),
				'hero_s2_btn1_url'   => array( 'label' => 'Slide 2 — Link Tombol Utama', 'type' => 'text', 'default' => '#principals' ),
				'hero_s2_btn2_text'  => array( 'label' => 'Slide 2 — Teks Tombol Kedua', 'type' => 'text', 'default' => 'Daftar Fleet' ),
				'hero_s2_btn2_url'   => array( 'label' => 'Slide 2 — Link Tombol Kedua', 'type' => 'text', 'default' => 'http://localhost:3000/#register' ),
			),
		),
		'features' => array(
			'title'  => '⚡ 4 Keunggulan Ringkas (Features Strip)',
			'fields' => array(
				'feat_1_title' => array( 'label' => 'Fitur 1 — Judul', 'type' => 'text', 'default' => 'Cek Menyeluruh' ),
				'feat_1_desc'  => array( 'label' => 'Fitur 1 — Keterangan', 'type' => 'text', 'default' => 'Truk dicek 30 bagian, ada foto buktinya, bergaransi resmi.' ),
				'feat_2_title' => array( 'label' => 'Fitur 2 — Judul', 'type' => 'text', 'default' => 'Teknisi Ahli' ),
				'feat_2_desc'  => array( 'label' => 'Fitur 2 — Keterangan', 'type' => 'text', 'default' => 'Montir khusus truk berpengalaman belasan tahun.' ),
				'feat_3_title' => array( 'label' => 'Fitur 3 — Judul', 'type' => 'text', 'default' => 'Barang Asli' ),
				'feat_3_desc'  => array( 'label' => 'Fitur 3 — Keterangan', 'type' => 'text', 'default' => 'Oli, ban, dan aki langsung dari pabriknya. Dijamin asli.' ),
				'feat_4_title' => array( 'label' => 'Fitur 4 — Judul', 'type' => 'text', 'default' => 'Pantau Online' ),
				'feat_4_desc'  => array( 'label' => 'Fitur 4 — Keterangan', 'type' => 'text', 'default' => 'Lihat progress servis dan tagihan dari HP kapan saja.' ),
			),
		),
		'about' => array(
			'title'  => '🏢 Tentang Kami (About Us)',
			'fields' => array(
				'about_pill'       => array( 'label' => 'Badge / Label Bagian', 'type' => 'text', 'default' => 'Tentang Kami' ),
				'about_title'      => array( 'label' => 'Judul Tentang Kami', 'type' => 'text', 'default' => 'Master Truck, Bengkel Truk Kepercayaan Anda di Medan' ),
				'about_desc1'      => array( 'label' => 'Paragraf 1 (Profil & Fasilitas)', 'type' => 'textarea', 'default' => 'PT Master Truck Indonesia ada di Kawasan Industri Medan III (KIM III). Kami merawat segala jenis truk dan mesin besar, sekaligus toko resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra.' ),
				'about_desc2'      => array( 'label' => 'Paragraf 2 (Transparansi Servis)', 'type' => 'textarea', 'default' => 'Semua pengerjaan tercatat dan bisa dipantau online — ada foto buktinya sebelum Anda bayar.' ),
				'about_point1'     => array( 'label' => 'Poin Keunggulan 1', 'type' => 'text', 'default' => 'Segala jenis truk: tronton, trailer, dump truck, mesin besar' ),
				'about_point2'     => array( 'label' => 'Poin Keunggulan 2', 'type' => 'text', 'default' => 'Progress servis terpantau dari HP, lengkap dengan foto' ),
				'about_point3'     => array( 'label' => 'Poin Keunggulan 3', 'type' => 'text', 'default' => 'Barang 100% asli dari pabrik, bisa bayar tempo' ),
				'about_exp_years'  => array( 'label' => 'Badge Pengalaman (Angka)', 'type' => 'text', 'default' => '15 Tahun' ),
				'about_exp_label'  => array( 'label' => 'Badge Pengalaman (Teks)', 'type' => 'text', 'default' => 'Pengalaman' ),
				'about_btn1_text'  => array( 'label' => 'Teks Tombol WhatsApp', 'type' => 'text', 'default' => 'Hubungi Kami' ),
				'about_btn1_url'   => array( 'label' => 'Link Tombol WhatsApp', 'type' => 'text', 'default' => 'https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada' ),
			),
		),
		'facts' => array(
			'title'  => '📊 Fakta & Statistik (Counter)',
			'fields' => array(
				'fact_1_num' => array( 'label' => 'Counter 1 (Angka)', 'type' => 'text', 'default' => '15' ),
				'fact_1_lbl' => array( 'label' => 'Counter 1 (Label)', 'type' => 'text', 'default' => 'Tahun Berpengalaman' ),
				'fact_2_num' => array( 'label' => 'Counter 2 (Angka)', 'type' => 'text', 'default' => '45' ),
				'fact_2_lbl' => array( 'label' => 'Counter 2 (Label)', 'type' => 'text', 'default' => 'Teknisi Ahli' ),
				'fact_3_num' => array( 'label' => 'Counter 3 (Angka)', 'type' => 'text', 'default' => '120' ),
				'fact_3_lbl' => array( 'label' => 'Counter 3 (Label)', 'type' => 'text', 'default' => 'Perusahaan Pelanggan' ),
				'fact_4_num' => array( 'label' => 'Counter 4 (Angka)', 'type' => 'text', 'default' => '2500' ),
				'fact_4_lbl' => array( 'label' => 'Counter 4 (Label)', 'type' => 'text', 'default' => 'Truk per Tahun' ),
			),
		),
		'services' => array(
			'title'  => '🛠️ 4 Layanan Utama',
			'fields' => array(
				// Layanan 1
				'svc_1_title' => array( 'label' => 'Layanan 1 — Judul', 'type' => 'text', 'default' => 'Cek Mesin Komputer' ),
				'svc_1_item1' => array( 'label' => 'Layanan 1 — Poin 1', 'type' => 'text', 'default' => 'Mesin dicek pakai komputer' ),
				'svc_1_item2' => array( 'label' => 'Layanan 1 — Poin 2', 'type' => 'text', 'default' => 'Kelistrikan & aki 24 volt' ),
				'svc_1_item3' => array( 'label' => 'Layanan 1 — Poin 3', 'type' => 'text', 'default' => 'Hasilnya dikirim ke HP Anda' ),
				// Layanan 2
				'svc_2_title' => array( 'label' => 'Layanan 2 — Judul', 'type' => 'text', 'default' => 'Servis Mesin Besar' ),
				'svc_2_item1' => array( 'label' => 'Layanan 2 — Poin 1', 'type' => 'text', 'default' => 'Turun mesin, bergaransi' ),
				'svc_2_item2' => array( 'label' => 'Layanan 2 — Poin 2', 'type' => 'text', 'default' => 'Stel injektor biar irit' ),
				'svc_2_item3' => array( 'label' => 'Layanan 2 — Poin 3', 'type' => 'text', 'default' => 'Sparepart asli pabrik' ),
				// Layanan 3
				'svc_3_title' => array( 'label' => 'Layanan 3 — Judul', 'type' => 'text', 'default' => 'Ban & Rem Angin' ),
				'svc_3_item1' => array( 'label' => 'Layanan 3 — Poin 1', 'type' => 'text', 'default' => 'Ban Dunlop segala ukuran' ),
				'svc_3_item2' => array( 'label' => 'Layanan 3 — Poin 2', 'type' => 'text', 'default' => 'Servis rem angin + kampas' ),
				'svc_3_item3' => array( 'label' => 'Layanan 3 — Poin 3', 'type' => 'text', 'default' => 'Cek kaki-kaki & per daun' ),
				// Layanan 4
				'svc_4_title' => array( 'label' => 'Layanan 4 — Judul', 'type' => 'text', 'default' => 'Ganti Oli' ),
				'svc_4_item1' => array( 'label' => 'Layanan 4 — Poin 1', 'type' => 'text', 'default' => 'Oli Pertamina & Mobil asli' ),
				'svc_4_item2' => array( 'label' => 'Layanan 4 — Poin 2', 'type' => 'text', 'default' => 'Ganti filter sekalian' ),
				'svc_4_item3' => array( 'label' => 'Layanan 4 — Poin 3', 'type' => 'text', 'default' => 'Bisa beli drum / pail' ),
			),
		),
		'booking' => array(
			'title'  => '🚨 Derek 24 Jam & Booking Form',
			'fields' => array(
				'book_pill'      => array( 'label' => 'Badge Darurat', 'type' => 'text', 'default' => 'Derek Siaga 24 Jam' ),
				'book_title'     => array( 'label' => 'Judul Derek Darurat', 'type' => 'text', 'default' => 'Truk Mogok? Kami Jemput Kapan Saja' ),
				'book_desc1'     => array( 'label' => 'Paragraf Jangkauan Derek', 'type' => 'textarea', 'default' => 'Mogok di Medan, Belawan, Tebing Tinggi, atau lintas Sumatera? Mobil derek kami siap menjemput dan membawa truk Anda ke bengkel.' ),
				'book_desc2'     => array( 'label' => 'Paragraf Manfaat Mitra Fleet', 'type' => 'textarea', 'default' => 'Daftar jadi pelanggan perusahaan: bisa bayar tempo, harga khusus, dan gratis pantau servis online.' ),
				'book_phone'     => array( 'label' => 'Nomor Derek Darurat (Teks Tampil)', 'type' => 'text', 'default' => '0812-3456-7890' ),
				'book_wa'        => array( 'label' => 'Nomor WhatsApp Penerima Booking (Format 628...)', 'type' => 'text', 'default' => '6281234567890' ),
			),
		),
		'contact_footer' => array(
			'title'  => '📍 Kontak & Footer',
			'fields' => array(
				'foot_address'       => array( 'label' => 'Alamat Lengkap Workshop', 'type' => 'text', 'default' => 'KIM III, Medan — Sumatera Utara' ),
				'foot_phone'         => array( 'label' => 'Nomor Telepon Kantor', 'type' => 'text', 'default' => '061-8888-1234 / 0812-3456-7890' ),
				'foot_email'         => array( 'label' => 'Email Customer Service', 'type' => 'text', 'default' => 'cs@mastertruk.co.id' ),
				'foot_hours_bengkel' => array( 'label' => 'Jam Operasional Bengkel', 'type' => 'text', 'default' => 'Senin - Sabtu: 08.00 - 17.00 WIB' ),
				'foot_hours_derek'   => array( 'label' => 'Jam Derek Darurat', 'type' => 'text', 'default' => '24 Jam Nonstop' ),
				'foot_copyright'     => array( 'label' => 'Teks Hak Cipta (Footer Bawah)', 'type' => 'textarea', 'default' => '© MASTER TRUCK, Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.' ),
			),
		),
	);
}

/**
 * Helper fungsi untuk membaca isi field (dari post meta, option, atau default).
 */
if ( ! function_exists( 'mt_get_content' ) ) {
	function mt_get_content( $key, $default = '' ) {
		$post_id = get_the_ID() ?: (int) get_option( 'page_on_front' );
		if ( $post_id ) {
			$val = get_post_meta( $post_id, '_mt_' . $key, true );
			if ( '' !== $val && false !== $val && null !== $val ) {
				return $val;
			}
		}
		$opts = get_option( 'mt_landing_options', array() );
		if ( is_array( $opts ) && isset( $opts[ $key ] ) && '' !== $opts[ $key ] ) {
			return $opts[ $key ];
		}
		return $default;
	}
}

/**
 * Daftarkan Meta Box pada halaman depan / template mastertruck.
 */
add_action( 'add_meta_boxes', function () {
	global $post;
	if ( ! $post || 'page' !== $post->post_type ) {
		return;
	}
	$front_id = (int) get_option( 'page_on_front' );
	$tpl      = get_post_meta( $post->ID, '_wp_page_template', true );

	// Tampilkan hanya jika ini halaman depan atau memakai template-mastertruck.php
	if ( $post->ID === $front_id || 'template-mastertruck.php' === $tpl || 59 === $post->ID ) {
		add_meta_box(
			'mt_landing_editor_metabox',
			'🚛 Editor Konten Landing Page (Master Truck Enterprise)',
			'mt_render_landing_meta_box',
			'page',
			'normal',
			'high'
		);
	}
} );

/**
 * Render formulir metabox dengan navigasi tab modern.
 */
function mt_render_landing_meta_box( $post ) {
	wp_nonce_field( 'mt_save_landing_data', 'mt_landing_nonce' );
	$schema = mt_get_landing_fields_schema();
	?>
	<style>
		.mt-editor-wrap { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin-top: 10px; }
		.mt-editor-nav { display: flex; flex-wrap: wrap; gap: 6px; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 20px; }
		.mt-tab-btn { background: #F1F5F9; border: 1px solid #CBD5E1; color: #334155; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 13px; cursor: pointer; transition: all 0.15s; }
		.mt-tab-btn:hover { background: #E2E8F0; color: #0F172A; }
		.mt-tab-btn.active { background: #2563EB; border-color: #2563EB; color: #FFFFFF; }
		.mt-tab-pane { display: none; }
		.mt-tab-pane.active { display: block; animation: mtFadeIn 0.2s ease-in-out; }
		@keyframes mtFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
		.mt-field-row { margin-bottom: 16px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px 16px; }
		.mt-field-row label { display: block; font-weight: 600; font-size: 13px; color: #1E293B; margin-bottom: 6px; }
		.mt-field-row input[type="text"], .mt-field-row textarea { width: 100%; border: 1px solid #CBD5E1; border-radius: 4px; padding: 8px 12px; font-size: 13px; box-sizing: border-box; }
		.mt-field-row input[type="text"]:focus, .mt-field-row textarea:focus { border-color: #2563EB; outline: none; box-shadow: 0 0 0 2px rgba(37,99,235,0.2); }
		.mt-field-hint { font-size: 11.5px; color: #64748B; margin-top: 4px; }
		.mt-badge-default { display: inline-block; background: #E2E8F0; color: #475569; font-size: 11px; padding: 2px 6px; border-radius: 4px; margin-left: 6px; font-family: monospace; }
	</style>

	<div class="mt-editor-wrap">
		<p style="font-size: 13px; color: #475569; margin-bottom: 14px;">
			✏️ Ubah teks di bawah ini lalu klik tombol <strong>Perbarui (Update)</strong> di sebelah kanan atas untuk langsung melihat perubahannya di website. Jika kolom dikosongkan, teks bawaan asli akan otomatis digunakan.
		</p>
		<div class="mt-editor-nav" id="mt-editor-tabs">
			<?php $first = true; foreach ( $schema as $tab_key => $tab_data ) : ?>
				<button type="button" class="mt-tab-btn <?php echo $first ? 'active' : ''; ?>" data-target="mt-tab-<?php echo esc_attr( $tab_key ); ?>">
					<?php echo esc_html( $tab_data['title'] ); ?>
				</button>
			<?php $first = false; endforeach; ?>
		</div>

		<div class="mt-editor-content">
			<?php $first = true; foreach ( $schema as $tab_key => $tab_data ) : ?>
				<div class="mt-tab-pane <?php echo $first ? 'active' : ''; ?>" id="mt-tab-<?php echo esc_attr( $tab_key ); ?>">
					<h3 style="font-size: 15px; margin: 0 0 16px; color: #1E293B;"><?php echo esc_html( $tab_data['title'] ); ?></h3>
					<?php foreach ( $tab_data['fields'] as $field_key => $field_meta ) :
						$val = get_post_meta( $post->ID, '_mt_' . $field_key, true );
						$placeholder = $field_meta['default'];
					?>
						<div class="mt-field-row">
							<label for="mt_<?php echo esc_attr( $field_key ); ?>">
								<?php echo esc_html( $field_meta['label'] ); ?>
							</label>
							<?php if ( 'textarea' === $field_meta['type'] ) : ?>
								<textarea id="mt_<?php echo esc_attr( $field_key ); ?>" name="mt_data[<?php echo esc_attr( $field_key ); ?>]" rows="3" placeholder="<?php echo esc_attr( $placeholder ); ?>"><?php echo esc_textarea( $val ); ?></textarea>
							<?php else : ?>
								<input type="text" id="mt_<?php echo esc_attr( $field_key ); ?>" name="mt_data[<?php echo esc_attr( $field_key ); ?>]" value="<?php echo esc_attr( $val ); ?>" placeholder="<?php echo esc_attr( $placeholder ); ?>">
							<?php endif; ?>
							<div class="mt-field-hint">
								Bawaan: <span class="mt-badge-default"><?php echo esc_html( mb_strimwidth( $placeholder, 0, 80, '...' ) ); ?></span>
							</div>
						</div>
					<?php endforeach; ?>
				</div>
			<?php $first = false; endforeach; ?>
		</div>
	</div>

	<script>
		(function() {
			var tabBtns = document.querySelectorAll('#mt-editor-tabs .mt-tab-btn');
			tabBtns.forEach(function(btn) {
				btn.addEventListener('click', function(e) {
					e.preventDefault();
					var targetId = this.getAttribute('data-target');
					tabBtns.forEach(function(b) { b.classList.remove('active'); });
					document.querySelectorAll('.mt-tab-pane').forEach(function(p) { p.classList.remove('active'); });
					this.classList.add('active');
					var targetPane = document.getElementById(targetId);
					if (targetPane) { targetPane.classList.add('active'); }
				});
			});
		})();
	</script>
	<?php
}

/**
 * Simpan data saat halaman disimpan / diperbarui (save_post).
 */
add_action( 'save_post_page', function ( $post_id ) {
	if ( ! isset( $_POST['mt_landing_nonce'] ) || ! wp_verify_nonce( $_POST['mt_landing_nonce'], 'mt_save_landing_data' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_page', $post_id ) ) {
		return;
	}

	if ( isset( $_POST['mt_data'] ) && is_array( $_POST['mt_data'] ) ) {
		$schema = mt_get_landing_fields_schema();
		$all_fields = array();
		foreach ( $schema as $sec ) {
			foreach ( $sec['fields'] as $k => $f ) {
				$all_fields[ $k ] = $f;
			}
		}

		$options_save = array();
		foreach ( $all_fields as $key => $meta ) {
			if ( isset( $_POST['mt_data'][ $key ] ) ) {
				$raw = wp_unslash( $_POST['mt_data'][ $key ] );
				// Untuk judul yang mengizinkan span highlight atau link
				$clean = wp_kses_post( trim( $raw ) );
				if ( '' === $clean ) {
					delete_post_meta( $post_id, '_mt_' . $key );
				} else {
					update_post_meta( $post_id, '_mt_' . $key, $clean );
					$options_save[ $key ] = $clean;
				}
			}
		}
		if ( ! empty( $options_save ) ) {
			update_option( 'mt_landing_options', $options_save );
		}
	}
} );

/**
 * Tambahkan shortcut "Edit Teks Beranda" di Admin Bar atas saat melihat website.
 */
add_action( 'admin_bar_menu', function ( $wp_admin_bar ) {
	if ( ! is_user_logged_in() || ! current_user_can( 'edit_pages' ) ) {
		return;
	}
	$front_id = (int) get_option( 'page_on_front' ) ?: 59;
	$wp_admin_bar->add_node( array(
		'id'    => 'mt_edit_landing',
		'title' => '✏️ Edit Teks Beranda',
		'href'  => admin_url( 'post.php?post=' . $front_id . '&action=edit' ),
		'meta'  => array( 'title' => 'Ubah teks dan banner halaman beranda' ),
	) );
}, 80 );
