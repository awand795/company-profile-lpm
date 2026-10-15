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
// Cakupan: /wp-login.php, ?action=lostpassword, ?action=rp/resetpass,
// ?action=register, pesan error/sukses, tautan, tombol (target: 0 string Inggris).
function mt_login_id_map() {
	return array(
		// Form masuk
		'Username or Email Address' => 'Email atau Nama Pengguna',
		'Password'                  => 'Kata Sandi',
		'Remember Me'               => 'Ingat saya',
		'Log In'                    => 'Masuk',
		'Log in'                    => 'Masuk',
		'Lost your password?'       => 'Lupa kata sandi?',
		// Tautan kembali ke situs (panah dirender di luar string di WP 6.8+)
		'Go to %s'                 => 'Kembali ke %s',
		'&larr; Go to %s'           => '← Kembali ke %s',
		'← Go to %s'                => '← Kembali ke %s',
		'&larr; Back to %s'         => '← Kembali ke %s',
		'Back to %s'                => 'Kembali ke %s',
		// Lupa kata sandi
		'Get New Password'          => 'Kirim Tautan Reset',
		'Please enter your username or email address. You will receive an email message with instructions on how to reset your password.'
			=> 'Masukkan nama pengguna atau alamat email Anda. Anda akan menerima email berisi petunjuk untuk mengatur ulang kata sandi.',
		// Atur ulang kata sandi (rp / resetpass)
		'New password'              => 'Kata sandi baru',
		'Confirm new password'      => 'Konfirmasi kata sandi baru',
		'Strength indicator'        => 'Indikator kekuatan',
		'Reset Password'            => 'Atur Ulang Kata Sandi',
		'Hint: The password should be at least twelve characters long. To make it stronger, use upper and lower case letters, numbers, and symbols like ! " ? $ % ^ &amp; ).'
			=> 'Tips: kata sandi minimal dua belas karakter. Agar lebih kuat, gabungkan huruf besar dan kecil, angka, serta simbol seperti ! " ? $ % ^ & ).',
		'Hint: The password should be at least twelve characters long. To make it stronger, use upper and lower case letters, numbers, and symbols like ! " ? $ % ^ & ).'
			=> 'Tips: kata sandi minimal dua belas karakter. Agar lebih kuat, gabungkan huruf besar dan kecil, angka, serta simbol seperti ! " ? $ % ^ & ).',
		// Tampilkan/sembunyikan kata sandi
		'Show password'             => 'Tampilkan kata sandi',
		'Hide password'             => 'Sembunyikan kata sandi',
		'Show'                      => 'Tampilkan',
		'Hide'                      => 'Sembunyikan',
		// Pesan status umum
		'You are now logged out.'   => 'Anda telah keluar.',
		'Check your email for the confirmation link, then visit the login page.'
			=> 'Periksa email Anda untuk tautan konfirmasi, lalu kunjungi halaman masuk.',
		'Confirmation link sent. Please check your email.'
			=> 'Tautan konfirmasi terkirim. Silakan periksa email Anda.',
		'Check your email for a link to reset your password. If you don\'t receive an email, please check your spam folder.'
			=> 'Periksa email Anda untuk tautan mengatur ulang kata sandi. Jika tidak ada email, periksa folder spam.',
		'Your password has been reset. <a href="%s">Log in</a>'
			=> 'Kata sandi Anda telah diatur ulang. <a href="%s">Masuk</a>',
		'Registration complete. Please check your email, then visit the <a href="%s">login page</a>.'
			=> 'Pendaftaran selesai. Periksa email Anda, lalu kunjungi <a href="%s">halaman masuk</a>.',
		'This link has expired. Please request a new one using the link below.'
			=> 'Tautan ini telah kedaluwarsa. Minta tautan baru melalui tautan di bawah.',
		// Bantuan tooltip & dialog (aria-label)
		'Help'                      => 'Bantuan',
		'Close'                     => 'Tutup',
		'Selecting "Remember Me" increases the length of time until you&#8217;re asked to log in again on this device. To keep your account secure, use this option only on your personal devices.'
			=> 'Memilih "Ingat saya" memperpanjang masa Anda tetap masuk di perangkat ini. Demi keamanan akun, gunakan opsi ini hanya di perangkat pribadi Anda.',
		// Galat nama pengguna tidak terdaftar (sumber persis wp-includes/user.php)
		'<strong>Error:</strong> The username <strong>%s</strong> is not registered on this site. If you are unsure of your username, try your email address instead.'
			=> '<strong>Galat:</strong> Nama pengguna <strong>%s</strong> tidak terdaftar di situs ini. Jika Anda tidak yakin dengan nama pengguna Anda, coba alamat email Anda.',
		'The username %s is not registered on this site. If you are unsure of your username, try your email address instead.'
			=> 'Nama pengguna %s tidak terdaftar di situs ini. Jika Anda tidak yakin dengan nama pengguna Anda, coba alamat email Anda.',
		// Tautan reset kedaluwarsa (halaman rp, kunci tidak valid)
		'<strong>Error:</strong> Your password reset link appears to be invalid. Please request a new link below.'
			=> '<strong>Galat:</strong> Tautan pengaturan ulang kata sandi Anda tampaknya tidak valid. Minta tautan baru di bawah.',
		'Your password reset link appears to be invalid. Please request a new link below.'
			=> 'Tautan pengaturan ulang kata sandi Anda tampaknya tidak valid. Minta tautan baru di bawah.',
		'The username field is empty.' => 'Kolom nama pengguna masih kosong.',
		'The password field is empty.' => 'Kolom kata sandi masih kosong.',
		'The email field is empty.'   => 'Kolom email masih kosong.',
		'Invalid username.'         => 'Nama pengguna tidak valid.',
		'Invalid email address.'    => 'Alamat email tidak valid.',
		'There is no account with that username or email address.'
			=> 'Tidak ada akun dengan nama pengguna atau alamat email tersebut.',
		'<strong>Error:</strong> There is no account with that username or email address.'
			=> '<strong>Galat:</strong> Tidak ada akun dengan nama pengguna atau alamat email tersebut.',
		'<strong>Error:</strong> The email could not be sent. Your site may not be correctly configured to send emails. <a href="%s">Get support for resetting your password</a>.'
			=> '<strong>Galat:</strong> Email tidak dapat dikirim. Situs Anda mungkin belum dikonfigurasi untuk mengirim email. <a href="%s">Dapatkan bantuan mengatur ulang kata sandi</a>.',
		'The password you entered for the email address %s is incorrect.'
			=> 'Kata sandi yang Anda masukkan untuk alamat email %s salah.',
		'The password you entered for the username %s is incorrect.'
			=> 'Kata sandi yang Anda masukkan untuk nama pengguna %s salah.',
		'<strong>Error:</strong> Invalid username. <a href="%s">Lost your password?</a>'
			=> '<strong>Galat:</strong> Nama pengguna tidak valid. <a href="%s">Lupa kata sandi?</a>',
		'<strong>Error:</strong> User registration is currently not allowed.'
			=> '<strong>Galat:</strong> Pendaftaran pengguna saat ini tidak diizinkan.',
	);
}
add_filter( 'gettext', function ( $translated_text, $text, $domain ) {
	if ( 'default' === $domain ) {
		$map = mt_login_id_map();
		if ( isset( $map[ $text ] ) ) {
			return $map[ $text ];
		}
	}
	return $translated_text;
}, 20, 3 );
add_filter( 'ngettext', function ( $translation, $single, $plural, $number, $domain ) {
	if ( 'default' === $domain ) {
		$map = mt_login_id_map();
		$key = ( 1 === (int) $number ) ? $single : $plural;
		if ( isset( $map[ $key ] ) ) {
			return $map[ $key ];
		}
	}
	return $translation;
}, 20, 5 );
// _x() dengan konteks (mis. tautan "Go to site") lewat filter ini, bukan gettext.
add_filter( 'gettext_with_context', function ( $translation, $text, $context, $domain ) {
	if ( 'default' === $domain ) {
		$map = mt_login_id_map();
		if ( isset( $map[ $text ] ) ) {
			return $map[ $text ];
		}
	}
	return $translation;
}, 20, 4 );

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
			<h2 class="mt-login-panel-heading">Perawatan Andal<br>untuk Truk Anda</h2>
			<p class="mt-login-panel-desc">Bengkel khusus armada niaga di Kawasan Industri Medan III. Servis rutin, perbaikan mesin, dan suku cadang asli bergaransi.</p>
			<ul class="mt-login-panel-features">
				<li>
					<span class="mt-feature-check"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
					<span class="mt-feature-text">Sparepart asli langsung distributor resmi</span>
				</li>
				<li>
					<span class="mt-feature-check"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
					<span class="mt-feature-text">Garansi pengerjaan & teknisi berpengalaman</span>
				</li>
				<li>
					<span class="mt-feature-check"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
					<span class="mt-feature-text">Layanan derek jemput siaga 24 jam</span>
				</li>
			</ul>
		</div>

		<figure class="mt-login-photo">
			<img src="/wp-content/uploads/2026/10/mt6-hero-bengkel.webp" alt="Mekanik memeriksa truk di bengkel Master Truck" width="1600" height="1067" fetchpriority="high">
			<span class="mt-login-pill mt-login-pill-sla">99,8% selesai tepat waktu</span><?php /* TODO: konfirmasi pemilik (klaim 99,8% belum terverifikasi). */ ?>
			<span class="mt-login-pill mt-login-pill-derek"><span class="mt-login-dot"></span>Derek siaga 24 jam</span>
		</figure>

		<div class="mt-login-panel-footer">
			<p>&copy; <?php echo date( 'Y' ); ?> Master Truck. Hak cipta dilindungi.</p>
		</div>
	</div>
	<div class="mt-login-right">
	<?php
} );

// 4b. Tutup kolom kanan (pusat vertikal kartu form + tautan bawah)
add_action( 'login_footer', function () {
	?>
	</div>
	<?php
}, 20 );

// 5. Sambutan dan judul formulir dalam kartu login
add_filter( 'login_message', function ( $message ) {
	$action = isset( $_GET['action'] ) ? sanitize_key( $_GET['action'] ) : 'login';
	$out = '<div class="mt-login-card-intro">';
	if ( 'lostpassword' === $action ) {
		$out .= '<p class="mt-card-eyebrow">Lupa Kata Sandi</p>';
		$out .= '<h1 class="mt-card-title">Atur Ulang Sandi</h1>';
		$out .= '<p class="mt-card-subtitle">Masukkan email Anda untuk menerima tautan pembuatan kata sandi baru.</p>';
	} elseif ( 'rp' === $action || 'resetpass' === $action ) {
		$out .= '<p class="mt-card-eyebrow">Sandi Baru</p>';
		$out .= '<h1 class="mt-card-title">Buat Kata Sandi Baru</h1>';
		$out .= '<p class="mt-card-subtitle">Masukkan kata sandi baru untuk akun Anda.</p>';
	} else {
		$out .= '<p class="mt-card-eyebrow">Selamat Datang Kembali</p>';
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

// 7. Placeholder, susunan baris bantuan, status kirim, hint Caps Lock
add_action( 'login_footer', function () {
	?>
	<script>
	(function () {
		var user = document.getElementById('user_login');
		if (user && !user.getAttribute('placeholder')) {
			user.setAttribute('placeholder', 'nama@contoh.com');
		}
		var pass = document.getElementById('user_pass');
		if (pass && !pass.getAttribute('placeholder')) {
			pass.setAttribute('placeholder', 'Kata sandi Anda');
		}
		var pass1 = document.getElementById('pass1');
		if (pass1 && !pass1.getAttribute('placeholder')) {
			pass1.setAttribute('placeholder', 'Kata sandi Anda');
		}
		var pass2 = document.getElementById('pass2');
		if (pass2 && !pass2.getAttribute('placeholder')) {
			pass2.setAttribute('placeholder', 'Ulangi kata sandi');
		}
		// Baris bantuan satu baris: ingat saya (kiri) + lupa sandi (kanan),
		// tombol kirim tetap di bawahnya; urutan tab mengikuti urutan visual.
		var form = document.querySelector('#login form');
		var remember = form ? form.querySelector('.forgetmenot') : null;
		var nav = document.querySelector('#login #nav');
		var submit = form ? form.querySelector('p.submit') : null;
		if (form && remember && nav && submit) {
			var row = document.createElement('div');
			row.className = 'mt-login-help-row';
			form.insertBefore(row, submit);
			row.appendChild(remember);
			row.appendChild(nav);
		}
		// Status kirim: kunci tombol + teks Memproses + spinner CSS.
		var btn = document.querySelector('#login #wp-submit');
		if (form && btn) {
			form.addEventListener('submit', function () {
				if (!form.checkValidity || form.checkValidity()) {
					btn.disabled = true;
					btn.classList.add('mt-is-loading');
					var wrap = btn.closest('p.submit');
					if (wrap) { wrap.classList.add('mt-loading-spinner'); }
					if (!btn.getAttribute('data-label')) {
						btn.setAttribute('data-label', btn.value);
					}
					btn.value = 'Memproses…';
				}
			});
		}
		// Hint Caps Lock di bawah field sandi.
		var capsTargets = [document.getElementById('user_pass'), document.getElementById('pass1')].filter(Boolean);
		capsTargets.forEach(function (field) {
			var hint = document.createElement('p');
			hint.className = 'mt-caps-hint';
			hint.textContent = 'Caps Lock aktif';
			hint.hidden = true;
			var box = field.closest('.user-pass-wrap') || field.closest('p');
			if (box) { box.appendChild(hint); }
			field.addEventListener('keyup', function (e) {
				var on = e.getModifierState ? e.getModifierState('CapsLock') : false;
				hint.hidden = !on;
			});
			field.addEventListener('blur', function () { hint.hidden = true; });
		});
	})();
	</script>
	<?php
} );
