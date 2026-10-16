const { execSync } = require('child_process');

const php = `
require '/var/www/html/wp-load.php';
$raw = get_post_meta(59, '_elementor_data', true);
$data = json_decode($raw, true);
echo "Total sections: " . count($data) . "\\n";
foreach ($data as $i => $sec) {
    $title = $sec['settings']['_title'] ?? $sec['settings']['css_classes'] ?? 'unnamed';
    echo "Sec $i: id=" . $sec['id'] . " title=" . $title . "\\n";
}
`;

const res = execSync(`docker exec lpm-wp-app php -r ${JSON.stringify(php)}`, { encoding: 'utf-8' });
console.log(res);
