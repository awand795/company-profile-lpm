<?php
$json = file_get_contents('/tmp/beranda-stitch.json');
if (!$json) { echo "Gagal baca json\n"; exit(1); }

$revisions = get_children([
    'post_parent' => 59,
    'post_type' => 'revision',
    'post_status' => 'any',
]);
foreach ($revisions as $rev) {
    wp_delete_post($rev->ID, true);
}

update_post_meta(59, '_elementor_data', wp_slash($json));
update_post_meta(59, '_elementor_edit_mode', 'builder');
update_post_meta(59, '_elementor_template_type', 'wp-page');
update_post_meta(59, '_elementor_version', defined('ELEMENTOR_VERSION') ? ELEMENTOR_VERSION : '4.3.4');
update_post_meta(59, '_wp_page_template', 'elementor_canvas');

$now = current_time('mysql');
$now_gmt = current_time('mysql', 1);
global $wpdb;
$wpdb->update(
    $wpdb->posts,
    ['post_modified' => $now, 'post_modified_gmt' => $now_gmt],
    ['ID' => 59]
);
clean_post_cache(59);

delete_post_meta(59, '_elementor_element_cache');
if (class_exists('\\Elementor\\Plugin')) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
}
$post_css = new \Elementor\Core\Files\CSS\Post(59);
$post_css->update();
$kit = \Elementor\Plugin::$instance->kits_manager->get_active_kit();
$kit_css = new \Elementor\Core\Files\CSS\Post($kit->get_id());
$kit_css->update();
echo "Post 59 updated and CSS regenerated successfully on server!\n";
