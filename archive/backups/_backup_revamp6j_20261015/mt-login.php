<?php
/**
 * Plugin Name: Master Truck Custom Login
 * Description: Tampilan halaman login WordPress bernuansa Master Truck (light enterprise, split-screen desktop, bahasa Indonesia).
 * Version: 1.0.0
 * Author: Antigravity
 */
defined( 'ABSPATH' ) || exit;

// 1. Matikan dropdown bahasa di halaman login
add_filter( 'login_display_language_dropdown', '__return_false' );

// 2. URL dan teks logo WordPress -> Master Truck
add_filter( 'login_headerurl', function () {
	return home_url( '/' );
} );

add_filter( 'login_headertext', function () {
	return 'MASTER TRUCK';
} );

// 3. Terjemahan bahasa Indonesia untuk formulir login standar
add_filter( 'gettext', function ( $translated_text, $text, $domain ) {
	if ( 'default' === $domain ) {
		switch ( $text ) {
			case 'Username or Email Address':
				return 'Email atau Nama Pengguna';
			case 'Password':
				return 'Kata Sandi';
			case 'Remember Me':
				return 'Ingat saya';
			case 'Log In':
				return 'Masuk';
			case 'Lost your password?':
				return 'Lupa kata sandi?';
			case '&larr; Go to %s':
			case '← Go to %s':
				return '← Kembali ke %s';
			case 'Get New Password':
				return 'Kirim Tautan Reset';
			case 'Show password':
				return 'Tampilkan';
			case 'Hide password':
				return 'Sembunyikan';
		}
	}
	return $translated_text;
}, 20, 3 );

// 4. Panel kiri untuk tampilan split-screen (desktop)
add_action( 'login_header', function () {
	?>
	<div class="mt-login-panel-left">
		<div class="mt-login-panel-brand">
			<div class="mt-login-brand-chip">
				<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<rect x="1" y="3" width="15" height="13"></rect>
					<polygon points="16 8 20 8 23 11 23 16 16 16 8"></polygon>
					<circle cx="5.5" cy="18.5" r="2.5"></circle>
					<circle cx="18.5" cy="18.5" r="2.5"></circle>
				</svg>
			</div>
			<div class="mt-login-brand-text">
				<span class="mt-login-brand-name">MASTER TRUCK</span>
				<span class="mt-login-brand-tagline">Bengkel Truk KIM III Medan</span>
			</div>
		</div>

		<div class="mt-login-panel-center">
			<h2 class="mt-login-panel-heading">Perawatan Andal untuk Armada Anda</h2>
			<p class="mt-login-panel-desc">Bengkel khusus truk dan distributor resmi di Kawasan Industri Medan III.</p>
			<ul class="mt-login-panel-features">
				<li>
					<span class="mt-feature-check">✓</span>
					<span class="mt-feature-text">Sparepart asli</span>
				</li>
				<li>
					<span class="mt-feature-check">✓</span>
					<span class="mt-feature-text">Garansi pengerjaan</span>
				</li>
				<li>
					<span class="mt-feature-check">✓</span>
					<span class="mt-feature-text">Derek 24 jam</span>
				</li>
			</ul>
		</div>

		<div class="mt-login-panel-footer">
			<p>&copy; <?php echo date( 'Y' ); ?> Master Truck. Hak cipta dilindungi.</p>
		</div>
	</div>
	<?php
} );

// 5. Sambutan dan judul formulir dalam kartu login
add_filter( 'login_message', function ( $message ) {
	$action = isset( $_GET['action'] ) ? sanitize_key( $_GET['action'] ) : 'login';
	$out = '<div class="mt-login-card-intro">';
	if ( 'lostpassword' === $action ) {
		$out .= '<h1 class="mt-card-title">Atur Ulang Sandi</h1>';
		$out .= '<p class="mt-card-subtitle">Masukkan email Anda untuk menerima tautan pembuatan kata sandi baru.</p>';
	} elseif ( 'rp' === $action || 'resetpass' === $action ) {
		$out .= '<h1 class="mt-card-title">Buat Kata Sandi Baru</h1>';
		$out .= '<p class="mt-card-subtitle">Masukkan kata sandi baru untuk akun Anda.</p>';
	} else {
		$out .= '<h1 class="mt-card-title">Masuk ke Dasbor</h1>';
		$out .= '<p class="mt-card-subtitle">Khusus pengelola situs Master Truck.</p>';
	}
	$out .= '</div>';
	return $out . $message;
} );

// 6. Muat stylesheet dan font
add_action( 'login_enqueue_scripts', function () {
	// Muat font Plus Jakarta Sans & Inter dari tema Astra Master Truck
	$theme_fonts_url = get_site_url( null, '/wp-content/themes/astra/mastertruck/css/fonts.css' );
	wp_enqueue_style( 'mt-login-fonts', $theme_fonts_url, array(), '1.0' );

	// Stylesheet plugin mt-login
	$ver = file_exists( __DIR__ . '/mt-login.css' ) ? (string) filemtime( __DIR__ . '/mt-login.css' ) : '1.0.0';
	wp_enqueue_style( 'mt-login-style', plugins_url( 'mt-login.css', __FILE__ ), array( 'mt-login-fonts' ), $ver );
} );
