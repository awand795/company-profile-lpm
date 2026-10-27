<?php
/**
 * Plugin Name: MT Topbar Clean
 * Description: Topbar korporat MASTER TRUCK (kontak + link Login/Daftar), pengaturan konten di Appearance > Topbar Master Truck. Update-safe.
 * Version: 1.2.0
 */
defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/mt-landing-fields.php';

function mt_topbar_defaults() {
	// TODO: konfirmasi pemilik — nilai sementara disatukan dengan tools/build-stitch-elementor.py (SITE_DATA).
	return array(
		'phone'          => '061-8888-1234',
		'wa'             => '0812-3456-7890',
		'email'          => 'cs@mastertruk.co.id',
		'hours'          => 'Senin–Sabtu 08.00–17.00',
		'fleet_login'    => 'http://localhost:3000/#login',
		'fleet_register' => 'http://localhost:3000/#register',
		'reg_label'      => 'Daftar',
	);
}

function mt_topbar_opt( $key ) {
	$opts    = get_option( 'mt_topbar', array() );
	$defaults = mt_topbar_defaults();
	$value   = is_array( $opts ) && isset( $opts[ $key ] ) ? trim( (string) $opts[ $key ] ) : '';
	return '' !== $value ? $value : ( isset( $defaults[ $key ] ) ? $defaults[ $key ] : '' );
}

/* ------------------------------------------------------------------ enqueue */
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'dashicons' );
	/* Master Truck Light 1:1 dari template PHP — single source assets/css/.
	   Dimirror ke astra/mastertruck/ oleh sync-to-wp. */
	$base_rel = '/wp-content/themes/astra/mastertruck';
	$base_path = ABSPATH . ltrim( $base_rel, '/' );
	$ver = function ( $rel ) use ( $base_path ) {
		$p = $base_path . $rel;
		return file_exists( $p ) ? (string) filemtime( $p ) : '1.0';
	};
	$site = get_site_url( null, $base_rel );
	wp_enqueue_style( 'mt-bootstrap', $site . '/css/bootstrap.min.css', array(), $ver( '/css/bootstrap.min.css' ) );
	wp_enqueue_style( 'mt-fonts', $site . '/css/fonts.css', array(), $ver( '/css/fonts.css' ) );
	wp_enqueue_style( 'mt-fontawesome', $site . '/vendor/fontawesome/css/all.min.css', array(), $ver( '/vendor/fontawesome/css/all.min.css' ) );
	wp_enqueue_style( 'mt-animate', $site . '/lib/animate/animate.min.css', array(), $ver( '/lib/animate/animate.min.css' ) );
	wp_enqueue_style( 'mt-style', $site . '/css/style.css', array( 'mt-bootstrap' ), $ver( '/css/style.css' ) );
	wp_enqueue_style( 'mt-mastertruck', $site . '/css/mastertruck.css', array( 'elementor-frontend', 'mt-style' ), $ver( '/css/mastertruck.css' ) );
	/* REVAMP4: elementor-bridge.css tidak lagi di-enqueue (styling pindah ke
	   kontrol native Elementor; sisa kebutuhan ada di mt-custom.css ~38 baris).
	   Berkas bridge tetap di repo sebagai arsip. */
	wp_enqueue_style( 'mt-custom', $site . '/css/mt-custom.css', array( 'elementor-frontend' ), $ver( '/css/mt-custom.css' ) );
	/* JS libs persis template PHP (carousel, counter, wow, main.js). */
	wp_enqueue_script( 'mt-bootstrap-bundle', 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js', array( 'jquery' ), '5.0.0', true );
	foreach ( array( '/lib/wow/wow.min.js' => 'mt-wow', '/lib/easing/easing.min.js' => 'mt-easing', '/lib/waypoints/waypoints.min.js' => 'mt-waypoints', '/lib/counterup/counterup.min.js' => 'mt-counterup', '/js/main.js' => 'mt-main' ) as $rel => $h ) {
		wp_enqueue_script( $h, $site . $rel, array( 'jquery' ), $ver( $rel ), true );
	}
}, 20 );

/* Helper: deteksi editor / preview Elementor & wp-admin */
function mt_is_elementor_editor_or_preview() {
	if ( is_admin() ) {
		return true;
	}
	if ( class_exists( '\Elementor\Plugin' ) ) {
		if ( isset( \Elementor\Plugin::$instance->preview ) && \Elementor\Plugin::$instance->preview->is_preview_mode() ) {
			return true;
		}
		if ( isset( \Elementor\Plugin::$instance->editor ) && \Elementor\Plugin::$instance->editor->is_edit_mode() ) {
			return true;
		}
	}
	if ( isset( $_GET['elementor-preview'] ) || ( isset( $_GET['action'] ) && 'elementor' === $_GET['action'] ) ) {
		return true;
	}
	return false;
}

/* REVAMP7: Redirect 301 halaman arsip legacy ke homepage Page 59 */
add_action( 'template_redirect', function() {
	if ( ! is_admin() && function_exists( 'is_page' ) && is_page( array( 13, 30, 'beranda', 'beranda-baru' ) ) ) {
		wp_safe_redirect( home_url( '/' ), 301 );
		exit;
	}
} );

/* REVAMP4 & REVAMP7: halaman Beranda (ID 59) full-Elementor — lepas stylesheet legacy
   hanya di frontend murni. JANGAN sentuh saat editor/preview aktif, dan
   JANGAN dequeue dashicons saat admin bar aktif (is_user_logged_in / is_admin_bar_showing). */
add_action( 'wp_print_styles', function () {
	if ( mt_is_elementor_editor_or_preview() ) {
		return;
	}
	if ( function_exists( 'is_page' ) && is_page( 59 ) ) {
		$styles_to_dequeue = array( 'mt-bootstrap', 'mt-style', 'mt-mastertruck', 'mt-fontawesome' );
		if ( ! is_admin_bar_showing() && ! is_user_logged_in() ) {
			$styles_to_dequeue[] = 'dashicons';
		}
		foreach ( $styles_to_dequeue as $h ) {
			wp_dequeue_style( $h );
			wp_deregister_style( $h );
		}
		// Bundle bootstrap CDN tak dipakai komponen kustom halaman 59 (hemat koneksi pihak ketiga).
		wp_dequeue_script( 'mt-bootstrap-bundle' );
		wp_deregister_script( 'mt-bootstrap-bundle' );
	}
}, 100 );

/* REVAMP4: rampingkan <head> di Beranda — matikan skrip emoji WP (tak dipakai)
   dan tambah meta description (skor SEO/A11y Lighthouse). */
add_action( 'init', function () {
	if ( is_admin() ) { return; }
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
} );
// Konten Bahasa Indonesia -> atribut lang="id-ID" (tanpa unduh language pack).
add_filter( 'locale', function ( $loc ) { return 'id_ID'; } );
// Beri landmark main pada root Elementor (tanpa mengubah struktur DOM).
add_filter( 'the_content', function ( $c ) {
	if ( mt_is_elementor_editor_or_preview() ) {
		return $c;
	}
	if ( function_exists( 'is_page' ) && is_page( 59 ) && strpos( $c, 'data-elementor-type="wp-page"' ) !== false ) {
		$c = str_replace( 'data-elementor-type="wp-page"', 'role="main" data-elementor-type="wp-page"', $c );
	}
	return $c;
}, 999 );
add_action( 'wp_head', function () {
	if ( is_admin() || mt_is_elementor_editor_or_preview() ) {
		return;
	}
	if ( function_exists( 'is_page' ) && is_page( 59 ) ) {
		// Deskripsi manual hanya dikeluarkan bila plugin SEO TIDAK aktif (mencegah duplikasi).
		if ( ! defined( 'RANK_MATH_VERSION' ) && ! class_exists( 'RankMath' ) ) {
			echo '<meta name="description" content="PT Master Truck Indonesia — bengkel spesialis truk niaga & distributor resmi Pertamina, Mobil Delvac, Dunlop, GS Astra di KIM III Medan. Servis armada, overhaul, derek 24 jam." />' . "\n";
		}
		echo '<link rel="preload" as="image" href="/wp-content/uploads/stitch/stitch_img_2.webp" fetchpriority="high" />' . "\n";
	}
	// Meta theme-color selalu dikeluarkan tepat 1x
	echo '<meta name="theme-color" content="#0B0C10" />' . "\n";
}, 1 );

/* REVAMP6o C3: pratinjau bagikan (OG/Twitter) khusus beranda bila plugin SEO tidak aktif.
   Tanpa duplikasi bila plugin SEO aktif (Rank Math atau Yoast). */
add_action( 'wp_head', function () {
	if ( is_admin() || mt_is_elementor_editor_or_preview() ) {
		return;
	}
	if ( ! function_exists( 'is_page' ) || ! is_page( 59 ) ) {
		return;
	}
	if ( function_exists( 'yoast_breadcrumb' ) || defined( 'WPSEO_VERSION' )
		|| defined( 'RANK_MATH_VERSION' ) || class_exists( 'RankMath' ) ) {
		return;
	}
	$home = home_url( '/' );
	$og_img = home_url( '/wp-content/uploads/2026/10/mt-og-cover.webp' );
	$title = 'MASTER TRUCK — Bengkel Truk KIM III Medan';
	$desc = 'Bengkel khusus truk di Kawasan Industri Medan. Servis rutin, perbaikan mesin, dan sparepart asli, semua beres di satu tempat.';
	echo '<meta property="og:title" content="' . esc_attr( $title ) . '" />' . "\n";
	echo '<meta property="og:description" content="' . esc_attr( $desc ) . '" />' . "\n";
	echo '<meta property="og:type" content="website" />' . "\n";
	echo '<meta property="og:url" content="' . esc_url( $home ) . '" />' . "\n";
	echo '<meta property="og:image" content="' . esc_url( $og_img ) . '" />' . "\n";
	echo '<meta property="og:image:width" content="1200" />' . "\n";
	echo '<meta property="og:image:height" content="630" />' . "\n";
	echo '<meta property="og:image:alt" content="' . esc_attr( $title ) . '" />' . "\n";
	echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
}, 2 );

/* RONDE 20: Schema JSON-LD terintegrasi Rank Math (LocalBusiness/AutoRepair & FAQPage) */
add_filter( 'rank_math/json_ld', function( $data, $jsonld ) {
	if ( is_admin() ) {
		return $data;
	}

	$home      = home_url( '/' );
	$logo_url  = home_url( '/wp-content/uploads/2026/10/stitch_logo_transparan.png' );
	$image_url = home_url( '/wp-content/uploads/2026/10/mt-og-cover.webp' );

	// 1. AutoRepair / LocalBusiness Entity
	$local_business = array(
		'@type'                     => array( 'AutoRepair', 'LocalBusiness' ),
		'@id'                       => home_url( '/#localbusiness' ),
		'name'                      => 'Master Truck',
		'legalName'                 => 'PT Master Truck Indonesia',
		'url'                       => $home,
		'logo'                      => array(
			'@type'      => 'ImageObject',
			'@id'        => home_url( '/#logo' ),
			'url'        => $logo_url,
			'contentUrl' => $logo_url,
			'caption'    => 'Master Truck',
			'inLanguage' => 'id',
		),
		'image'                     => array(
			'@type'      => 'ImageObject',
			'@id'        => $image_url,
			'url'        => $image_url,
			'caption'    => 'Bengkel Truk Medan - Master Truck KIM III',
			'inLanguage' => 'id',
		),
		'description'               => 'Bengkel spesialis truk niaga, kalibrasi mesin diesel, overhaul, dan penyedia suku cadang OEM di KIM III Medan.',
		'priceRange'                => '$$',
		'areaServed'                => array(
			'@type' => 'City',
			'name'  => 'Medan',
		),
		'address'                   => array(
			'@type'           => 'PostalAddress',
			'streetAddress'   => 'Kawasan Industri Medan (KIM) III', // # TODO: konfirmasi pemilik — alamat jalan lengkap (nomor kaveling/blok)
			'addressLocality' => 'Medan',
			'addressRegion'   => 'Sumatera Utara',
			'postalCode'      => '20242',
			'addressCountry'  => 'ID',
		),
		'openingHoursSpecification' => array(
			array(
				'@type'     => 'OpeningHoursSpecification',
				'dayOfWeek' => array( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' ),
				'opens'     => '08:00',
				'closes'    => '20:00',
			),
		),
		// # TODO: konfirmasi pemilik — nomor telepon resmi belum dikonfirmasi, kosongkan agar tidak memuat klaim palsu
	);

	// Bila konstanta PHONE_TEL sudah dikonfirmasi pemilik di masa depan:
	if ( defined( 'PHONE_TEL' ) && PHONE_TEL && strpos( PHONE_TEL, 'TODO' ) === false ) {
		$local_business['telephone'] = PHONE_TEL;
	}

	// Masukkan ke graph
	$data['local_business'] = $local_business;
	if ( isset( $data['publisher'] ) ) {
		$data['publisher'] = array( '@id' => home_url( '/#localbusiness' ) );
	}

	// Khusus Beranda (Page 59): hapus Article snippet dan tambahkan FAQPage
	if ( ( function_exists( 'is_front_page' ) && is_front_page() ) || ( function_exists( 'is_page' ) && is_page( 59 ) ) ) {
		foreach ( $data as $k => $v ) {
			if ( isset( $v['@type'] ) && 'Article' === $v['@type'] ) {
				unset( $data[ $k ] );
			}
		}

		// 2. FAQPage Entity
		$data['faq'] = array(
			'@type'      => 'FAQPage',
			'@id'        => home_url( '/#faq' ),
			'mainEntity' => array(
				array(
					'@type'          => 'Question',
					'name'           => 'Apakah Master Truck melayani servis panggilan atau darurat di jalan?',
					'acceptedAnswer' => array(
						'@type' => 'Answer',
						// Teks harus SAMA dengan akordeon FAQ Beranda (tools/build-stitch-elementor.py).
						'text'  => 'Ya. Kami memiliki mobil bengkel keliling dan truk derek 25 ton yang siaga 24 jam untuk evakuasi truk, perbaikan ban, kelistrikan, dan rem angin di Medan dan sekitarnya.',
					),
				),
				array(
					'@type'          => 'Question',
					'name'           => 'Merek truk apa saja yang bisa dilayani bengkel Master Truck?',
					'acceptedAnswer' => array(
						'@type' => 'Answer',
						'text'  => 'Truk niaga merek Scania, Volvo, Hino, Mitsubishi Fuso, Isuzu, Mercedes-Benz, MAN, dan UD Trucks. Untuk merek tertentu, hubungi kami dulu supaya ketersediaan suku cadangnya bisa dicek lebih dulu.',
					),
				),
				array(
					'@type'          => 'Question',
					'name'           => 'Bagaimana jaminan suku cadang dan garansi pengerjaan turun mesin?',
					'acceptedAnswer' => array(
						'@type' => 'Answer',
						'text'  => 'Suku cadang kami jamin keasliannya. Untuk pengerjaan turun mesin dan transmisi, ada garansi tertulis hingga 180 Hari atau 50.000 KM.',
					),
				),
				array(
					'@type'          => 'Question',
					'name'           => 'Bagaimana kerja sama perawatan armada untuk perusahaan?',
					'acceptedAnswer' => array(
						'@type' => 'Answer',
						'text'  => 'Kami menyediakan kontrak perawatan bulanan maupun tahunan. Perusahaan Anda mendapat jadwal servis tanpa antre, diskon suku cadang hingga 18%, laporan digital, dan pilihan bayar termin setelah disetujui.',
					),
				),
				array(
					'@type'          => 'Question',
					'name'           => 'Apakah ada tempat penyimpanan truk yang menginap?',
					'acceptedAnswer' => array(
						'@type' => 'Answer',
						'text'  => 'Ada. Area bengkel seluas 8.000 m² dijaga petugas keamanan 24 jam dengan kamera pengawas di setiap stall dan area parkir.',
					),
				),
			),
		);
	}

	return $data;
}, 99, 2 );


/* ------------------------------------------------------- topbar di frontend */
function mt_render_topbar_html() {
	static $rendered = false;
	if ( $rendered ) { return; }
	/* Beranda Elementor (ID 59) sudah memuat topbar+navbar sendiri di dalam page —
	   jangan render ganda. */
	if ( function_exists( 'is_page' ) && is_page( 59 ) ) { return; }
	$rendered = true;
	$phone    = mt_topbar_opt( 'phone' );
	$wa       = mt_topbar_opt( 'wa' );
	$email    = mt_topbar_opt( 'email' );
	$hours    = mt_topbar_opt( 'hours' );
	$login    = mt_topbar_opt( 'fleet_login' );
	$register = mt_topbar_opt( 'fleet_register' );
	$reg_lbl  = mt_topbar_opt( 'reg_label' );
	?>
	<div class="mt-topbar">
		<div class="mt-topbar-inner">
			<div class="mt-topbar-left">
				<span class="mt-tb-item"><span class="dashicons dashicons-phone"></span> <?php echo esc_html( $phone ); ?></span>
				<span class="mt-tb-item"><span class="dashicons dashicons-whatsapp"></span> <?php echo esc_html( $wa ); ?></span>
				<span class="mt-tb-item mt-tb-mail"><span class="dashicons dashicons-email"></span> <?php echo esc_html( $email ); ?></span>
				<span class="mt-tb-item mt-tb-hours"><span class="dashicons dashicons-clock"></span> <?php echo esc_html( $hours ); ?></span>
			</div>
			<div class="mt-topbar-right">
				<a href="<?php echo esc_url( $login ); ?>" target="_blank" rel="noopener">Login</a>
				<span class="mt-tb-sep">|</span>
				<a href="<?php echo esc_url( $register ); ?>" target="_blank" rel="noopener" class="mt-tb-reg"><?php echo esc_html( $reg_lbl ); ?></a>
			</div>
		</div>
	</div>
	<?php
}
add_action( 'astra_header_before', 'mt_render_topbar_html' );
add_action( 'neve_before_header_wrapper_hook', 'mt_render_topbar_html' );

/* ------------------------------------------------------------ halamanaturan */
add_action( 'admin_menu', function () {
	add_theme_page(
		'Topbar Master Truck',
		'Topbar Master Truck',
		'edit_theme_options',
		'mt-topbar',
		'mt_topbar_settings_page'
	);
} );

add_action( 'admin_init', function () {
	register_setting( 'mt_topbar_group', 'mt_topbar', array( 'sanitize_callback' => 'mt_topbar_sanitize' ) );

	add_settings_section( 'mt_topbar_main', 'Kontak & tombol topbar', '__return_false', 'mt-topbar' );

	$fields = array(
		'phone'          => array( 'Nomor telepon', 'text' ),
		'wa'             => array( 'Nomor WhatsApp', 'text' ),
		'email'          => array( 'Email', 'text' ),
		'hours'          => array( 'Jam operasional', 'text' ),
		'fleet_login'    => array( 'URL tombol "Login"', 'url' ),
		'fleet_register' => array( 'URL tombol "Daftar"', 'url' ),
		'reg_label'      => array( 'Label tombol kanan', 'text' ),
	);

	foreach ( $fields as $key => $field ) {
		add_settings_field(
			$key,
			$field[0],
			function () use ( $key, $field ) {
				printf(
					'<input type="%1$s" class="regular-text" name="mt_topbar[%2$s]" value="%3$s">',
					esc_attr( $field[1] ),
					esc_attr( $key ),
					esc_attr( mt_topbar_opt( $key ) )
				);
			},
			'mt-topbar',
			'mt_topbar_main'
		);
	}
} );

function mt_topbar_sanitize( $input ) {
	$types  = array(
		'fleet_login'    => 'url',
		'fleet_register' => 'url',
	);
	$clean  = array();
	foreach ( mt_topbar_defaults() as $key => $default ) {
		$value         = isset( $input[ $key ] ) ? trim( wp_unslash( (string) $input[ $key ] ) ) : '';
		$clean[ $key ] = ( isset( $types[ $key ] ) && 'url' === $types[ $key ] )
			? esc_url_raw( $value )
			: sanitize_text_field( $value );
	}
	return $clean;
}

function mt_topbar_settings_page() {
	?>
	<div class="wrap">
		<h1>Topbar Master Truck</h1>
		<p class="description">Teks yang tampil di baris paling atas situs (di atas header). Kosongkan untuk memakai nilai bawaan.</p>
		<form method="post" action="options.php">
			<?php
			settings_fields( 'mt_topbar_group' );
			do_settings_sections( 'mt-topbar' );
			submit_button( 'Simpan Topbar' );
			?>
		</form>
	</div>
	<?php
}

add_filter( 'wp_resource_hints', function ( $urls, $relation_type ) {
	if ( 'preconnect' === $relation_type ) {
		$urls[] = 'https://fonts.googleapis.com';
		$urls[] = array(
			'href'        => 'https://fonts.gstatic.com',
			'crossorigin' => 'anonymous',
		);
	}
	return $urls;
}, 10, 2 );
