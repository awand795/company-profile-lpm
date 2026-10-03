<?php
/**
 * Template Name: Bizniz - Master Truck
 * Template Post Type: page
 *
 * Rekonstruksi template halaman "Beranda - Master Truck" (OkeTheme Bizniz inspiration).
 * Isi halaman (post_content) adalah dokumen Bizniz yang pembungkus <head>/<style>/<link>-nya
 * ter-strip: [ <title> + CSS mentah ] + [ body HTML mulai dari "<!-- TOP BAR" ].
 * Template ini memisahkan keduanya dan merender dokumen HTML utuh TANPA filter
 * the_content (tanpa wpautop/wptexturize yang merusak CSS: "--var" -> en-dash).
 *
 * PERINGATAN: jangan edit halaman ini via editor blok Gutenberg — akan merusak
 * markup lagi. Edit via revisi/DB, lalu hard-refresh browser (Ctrl+Shift+R).
 *
 * File ini disalin ke: /wp-content/themes/astra/template-bizniz.php
 * (nama file wajib persis, karena postmeta _wp_page_template = template-bizniz.php)
 */

defined( 'ABSPATH' ) || exit;

while ( have_posts() ) {
	the_post();
	$content = get_post_field( 'post_content', get_the_ID() );

	// 1. Buang <title> duplikat dari konten (title resmi dipasang di <head>).
	$content = preg_replace( '#<title[^>]*>.*?</title>#is', '', $content );

	// 2. Pisahkan CSS (atas) dan body HTML (bawah) pada penanda yang stabil.
	$marker = '<!-- TOP BAR';
	$pos    = strpos( $content, $marker );
	if ( false !== $pos ) {
		$css  = trim( substr( $content, 0, $pos ) );
		$body = trim( substr( $content, $pos ) );
	} else {
		// Fallback: potong pada tag body pertama bila penanda hilang.
		if ( preg_match( '/<(div|header|section|nav|main|footer)[ >]/', $content, $m, PREG_OFFSET_CAPTURE ) ) {
			$css  = trim( substr( $content, 0, $m[0][1] ) );
			$body = trim( substr( $content, $m[0][1] ) );
		} else {
			$css  = '';
			$body = trim( $content );
		}
	}

	// 3. Amankan: CSS tidak boleh mengandung penutup </style> (tidak ada di data).
	$css = str_ireplace( '</style', '<\\/style', $css );
	?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>MASTER TRUCK &ndash; Bengkel Perawatan &amp; Perbaikan Truk dan Armada Niaga</title>
	<meta name="description" content="MASTER TRUCK — bengkel spesialis perawatan truk niaga &amp; alat berat di KIM III Medan, distributor resmi pelumas, ban, aki &amp; sparepart OEM.">
	<!-- Google Fonts: Inter & Plus Jakarta Sans (Gaya Bizniz Theme OkeTheme) -->
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
	<!-- FontAwesome 5 untuk ikon Bizniz Theme -->
	<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
	<style>
<?php echo $css; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- CSS admin-authored dari konten halaman. ?>
	</style>
</head>
<body <?php body_class( 'bizniz-mastertruck' ); ?>>
<?php echo $body; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- body HTML admin-authored dari konten halaman. ?>
</body>
</html>
	<?php
}
