<?php
$raw = get_post_meta(59, '_elementor_data', true);
$data = json_decode($raw, true);
echo json_encode($data[1], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
