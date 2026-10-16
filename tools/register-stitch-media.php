<?php
define('WP_USE_THEMES', false);
require_once '/var/www/html/wp-load.php';
require_once '/var/www/html/wp-admin/includes/image.php';
require_once '/var/www/html/wp-admin/includes/file.php';
require_once '/var/www/html/wp-admin/includes/media.php';

$files = glob('/var/www/html/wp-content/uploads/stitch/*.*');
$mapping = [];

foreach ($files as $file) {
    $filename = basename($file);
    $existing = get_posts([
        'post_type' => 'attachment',
        'meta_key' => '_wp_attached_file',
        'meta_value' => 'stitch/' . $filename,
        'posts_per_page' => 1
    ]);
    
    if (!empty($existing)) {
        $id = $existing[0]->ID;
    } else {
        $upload_dir = wp_upload_dir();
        $filetype = wp_check_filetype($filename, null);
        $attachment = [
            'guid' => $upload_dir['baseurl'] . '/stitch/' . $filename,
            'post_mime_type' => $filetype['type'] ?: 'image/webp',
            'post_title' => preg_replace('/\.[^.]+$/', '', $filename),
            'post_content' => '',
            'post_status' => 'inherit'
        ];
        $id = wp_insert_attachment($attachment, $file);
        $attach_data = wp_generate_attachment_metadata($id, $file);
        wp_update_attachment_metadata($id, $attach_data);
        update_post_meta($id, '_wp_attached_file', 'stitch/' . $filename);
    }
    
    $url = wp_get_attachment_url($id);
    $key = preg_replace('/\.[^.]+$/', '', $filename);
    $mapping[$key] = ['id' => $id, 'url' => $url];
}

echo json_encode($mapping, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
