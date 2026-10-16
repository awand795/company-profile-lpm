<?php
$raw = get_post_meta(59, '_elementor_data', true);
$data = json_decode($raw, true);
echo "Total sections: " . count($data) . PHP_EOL;
foreach ($data as $i => $sec) {
    $title = $sec['settings']['_title'] ?? $sec['settings']['css_classes'] ?? 'unnamed';
    echo "Sec $i: id=" . $sec['id'] . " title=" . $title . PHP_EOL;
}
