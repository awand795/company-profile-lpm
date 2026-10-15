<#
.SYNOPSIS
    Bootstrap WordPress MASTER TRUCK dari nol (Windows PowerShell).
    Pasangan dari setup.sh (Linux/macOS).

.DESCRIPTION
    Alur:
      1. docker compose up -d, tunggu MariaDB siap
      2. Salin .htaccess, wp-content/uploads/, plugins kustom ke container
      3. Install WP-CLI di container (unduh wp-cli.phar)
      4. Import database/mt_site.sql (tersanitasi) -> WordPress langsung "ter-instal"
      5. Install + aktifkan theme astra + plugin versi pin docs/VERSIONS.md
      6. sync-to-wp.ps1 (template page + aset tema + media)
      7. Flush permalink & regenerasi CSS Elementor + reset kata sandi admin (prompt aman)
      8. Verifikasi HTTP 200 pada halaman utama

    BUTUH INTERNET sekali saat pertama: wp-cli.phar, theme astra, plugin
    elementor & kawan-kawan (unduhan dari wordpress.org).

.PARAMETER Rebuild
    Hancurkan volume Docker dulu (fresh total, semua data lokal hilang).

.PARAMETER SkipImport
    Lewati import database_dump.sql.

.PARAMETER Url
    Base URL untuk verifikasi. Default http://localhost:5000

.EXAMPLE
    .\setup.ps1
    .\setup.ps1 -Rebuild
#>
[CmdletBinding()]
param(
    [switch]$Rebuild,
    [switch]$SkipImport,
    [switch]$SkipAdminReset,
    [string]$Url = 'http://localhost:5000',
    [string]$App = 'lpm-wp-app',
    [string]$DbContainer = 'lpm-wp-db',
    [string]$DbUser = 'wordpress',
    [string]$DbPass = 'lotus_wp_password_2026',
    [string]$DbName = 'wordpress',
    [string]$DumpFile = 'database/mt_site.sql',
    [string]$ComposeFile = 'docker-compose.yml'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

function Write-Step($msg) { Write-Host ""; Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "  OK  $msg" -ForegroundColor Green }
function Fail($msg)       { Write-Host "  GAGAL $msg" -ForegroundColor Red; exit 1 }

# --- 0. Pra-syarat -----------------------------------------------------------
Write-Step "Cek prasyarat"
try { docker --version | Out-Null } catch { Fail "Docker tidak ditemukan. Install Docker Desktop dulu." }
try { git --version | Out-Null } catch { Fail "Git tidak ditemukan." }
try { python --version | Out-Null } catch { Fail "Python 3 tidak ditemukan (untuk tools/)." }
try { node --version | Out-Null } catch { Fail "Node.js tidak ditemukan (untuk tests/, lalu jalankan 'npm install' di tests/ dan 'npx playwright install chromium')." }

$composeOk = $false
docker compose version | Out-Null
if ($LASTEXITCODE -eq 0) { $compose = @('docker','compose'); $composeOk = $true }
else {
    $dc = Get-Command docker-compose -ErrorAction SilentlyContinue
    if ($dc) { $compose = @('docker-compose'); $composeOk = $true }
}
if (-not $composeOk) { Fail "Perintah 'docker compose' / 'docker-compose' tidak ditemukan." }
if (-not (Test-Path 'docker-compose.yml')) { Fail "docker-compose.yml tidak ada di $root" }
if (-not (Test-Path $DumpFile))  { Fail "$DumpFile tidak ada di $root (ekspor via tools/export-dump-sanitized.ps1)" }
Write-Ok "compose: $($compose -join ' ')"

# Sub-command setelah nama binari (untuk 'docker compose' -> 'compose').
$composeSub = @()
if ($compose.Count -gt 1) { $composeSub = $compose[1..($compose.Count - 1)] }
$composeSub += @('-f', $ComposeFile)

# --- 1. Stack ----------------------------------------------------------------
if ($Rebuild) {
    Write-Step "Rebuild volume (down -v)"
    & $compose[0] @composeSub down -v --remove-orphans
    if ($LASTEXITCODE -ne 0) { Fail "docker compose down -v gagal" }
}

Write-Step "docker compose up -d"
& $compose[0] @composeSub up -d
if ($LASTEXITCODE -ne 0) { Fail "docker compose up gagal" }
Write-Ok "stack naik"

Write-Step "Menunggu MariaDB siap"
$dbReady = $false
for ($i = 0; $i -lt 60; $i++) {
    docker exec -e "MYSQL_PWD=$DbPass" $DbContainer mariadb-admin ping -h"127.0.0.1" "-u$DbUser" --silent | Out-Null
    if ($LASTEXITCODE -eq 0) { $dbReady = $true; break }
    Start-Sleep -Seconds 2
}
if (-not $dbReady) { Fail "MariaDB tidak siap setelah 120 detik." }
Write-Ok "MariaDB siap"

# --- 2. Salin berkas statis --------------------------------------------------
Write-Step "Salin .htaccess + wp-content/uploads + plugins kustom"
if (Test-Path '.htaccess') {
    docker cp '.htaccess' "${App}:/var/www/html/.htaccess"
    if ($LASTEXITCODE -ne 0) { Fail "docker cp .htaccess gagal" }
    Write-Ok ".htaccess"
}
if (Test-Path 'wp-content/uploads') {
    docker cp 'wp-content/uploads/.' "${App}:/var/www/html/wp-content/uploads/"
    if ($LASTEXITCODE -ne 0) { Fail "docker cp uploads gagal" }
    $n = (Get-ChildItem -Path 'wp-content/uploads' -Recurse -File -Force | Measure-Object).Count
    Write-Ok "wp-content/uploads/ ($n file)"
}
foreach ($plug in @('mt-topbar','mt-booking','mt-login')) {
    if (Test-Path "wp-content/plugins/$plug") {
        docker cp "wp-content/plugins/$plug/." "${App}:/var/www/html/wp-content/plugins/$plug/"
        if ($LASTEXITCODE -ne 0) { Fail "docker cp $plug gagal" }
        Write-Ok "plugins/$plug/"
    }
}
docker exec $App chown -R www-data:www-data /var/www/html/.htaccess /var/www/html/wp-content/uploads /var/www/html/wp-content/plugins/mt-topbar /var/www/html/wp-content/plugins/mt-booking /var/www/html/wp-content/plugins/mt-login | Out-Null

function Invoke-Wp {
    param([Parameter(ValueFromRemainingArguments = $true)]$CmdArgs)
    docker exec $App wp --allow-root --path=/var/www/html @CmdArgs | Out-Null
    return $LASTEXITCODE -eq 0
}

# --- 3. WP-CLI ---------------------------------------------------------------
Write-Step "Pasang WP-CLI (di dalam container)"
docker exec $App sh -c 'command -v wp >/dev/null 2>&1 && exit 0
  echo "  mengunduh wp-cli.phar ..."
  curl -sSL -o /tmp/wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar || exit 11
  chmod +x /tmp/wp-cli.phar
  mv /tmp/wp-cli.phar /usr/local/bin/wp
  wp --version --allow-root >/dev/null || exit 12' 
if ($LASTEXITCODE -ne 0) { Fail "Gagal memasang WP-CLI (cek koneksi internet)." }
Write-Ok "WP-CLI siap"

# --- 4. Import database ------------------------------------------------------
if (-not $SkipImport) {
    Write-Step "Import $DumpFile (tersanitasi; kata sandi admin diatur ulang di langkah 7)"
    # Dump hasil ekspor Windows sering UTF-16 (BOM FF FE) yang ditolak klien
    # mariadb ("ASCII '\0' appeared..."). Konversi dulu ke UTF-8 bila perlu.
    $restoreSrc = $DumpFile
    $bom = New-Object byte[] 2
    $fs = [System.IO.File]::OpenRead((Join-Path (Get-Location) $DumpFile))
    $n = $fs.Read($bom, 0, 2); $fs.Close()
    if ($n -eq 2 -and $bom[0] -eq 0xFF -and $bom[1] -eq 0xFE) {
        $utf8Tmp = Join-Path ([System.IO.Path]::GetTempPath()) 'mt_restore_utf8.sql'
        $text = [System.IO.File]::ReadAllText((Join-Path (Get-Location) $DumpFile), [System.Text.Encoding]::Unicode)
        [System.IO.File]::WriteAllText($utf8Tmp, $text, (New-Object System.Text.UTF8Encoding $false))
        $restoreSrc = $utf8Tmp
        Write-Ok "dump UTF-16 dikonversi ke UTF-8"
    }
    docker cp $restoreSrc "${DbContainer}:/tmp/restore.sql"
    if ($LASTEXITCODE -ne 0) { Fail "docker cp dump gagal" }
    if ($restoreSrc -ne $DumpFile) { Remove-Item -Path $restoreSrc -Force -ErrorAction SilentlyContinue }
    docker exec -e "MYSQL_PWD=$DbPass" $DbContainer sh -c "mariadb -u'$DbUser' '$DbName' < /tmp/restore.sql && rm -f /tmp/restore.sql" | Out-Null
    if ($LASTEXITCODE -ne 0) { Fail "Import dump gagal." }
    Write-Ok "$DumpFile diimport"
} else {
    Write-Step "Lewati import database (-SkipImport)"
}

docker exec $App wp --allow-root --path=/var/www/html core is-installed | Out-Null
if ($LASTEXITCODE -ne 0) { Fail "WordPress belum terdeteksi ter-instal. Pastikan import dump sukses." }

Write-Step "Sinkronkan URL site"
$homeUrl = ''
docker exec $App wp --allow-root --path=/var/www/html option get home 2>$null | ForEach-Object { if (-not $homeUrl) { $homeUrl = $_.ToString().Trim() } }
if ($homeUrl -ne $Url) {
    if (-not (Invoke-Wp option update home $Url))      { Fail "Gagal update opsi home" }
    if (-not (Invoke-Wp option update siteurl $Url))   { Fail "Gagal update opsi siteurl" }
    docker exec $App wp --allow-root --path=/var/www/html search-replace $homeUrl $Url --skip-columns=guid --report-changed-only | Out-Null
    Write-Ok "home/siteurl: $homeUrl -> $Url (+search-replace konten)"
} else {
    Write-Ok "home/siteurl sudah $Url"
}

# --- 5. Theme & plugin (versi persis docs/VERSIONS.md) -----------------------
Write-Step "Theme astra 4.14.0 + plugin versi pin"
if (Invoke-Wp theme is-installed astra) {
    Write-Ok "theme astra sudah terpasang"
} else {
    if (-not (Invoke-Wp theme install astra --version=4.14.0 --activate)) { Fail "Gagal unduh theme astra (cek internet)." }
    Write-Ok "theme astra terpasang"
}
Invoke-Wp theme activate astra | Out-Null
if (Invoke-Wp theme is-active astra) { Write-Ok "theme astra aktif" }

$pins = @{ 'elementor' = '4.3.4'; 'astra-sites' = '4.7.8'; 'header-footer-elementor' = '2.9.5' }
foreach ($p in $pins.Keys) {
    if (Invoke-Wp plugin is-installed $p) {
        Write-Ok "plugin $p sudah terpasang"
    } else {
        if (-not (Invoke-Wp plugin install $p --version=$($pins[$p]))) { Fail "Gagal unduh plugin $p (cek internet)." }
        Write-Ok "plugin $p terpasang"
    }
    if (Invoke-Wp plugin activate $p) { Write-Ok "plugin $p aktif" }
}

foreach ($plug in @('mt-topbar','mt-booking','mt-login')) {
    if (Invoke-Wp plugin is-installed $plug) {
        Invoke-Wp plugin activate $plug | Out-Null
        Write-Ok "plugin $plug aktif"
    } else {
        Fail "plugin $plug tidak ditemukan di container (salinan gagal?)"
    }
}

# --- 6. Sinkronisasi template & media ---------------------------------------
Write-Step "Sinkronisasi wp-integration + media"
& (Join-Path $root 'sync-to-wp.ps1') -Container $App
if ($LASTEXITCODE -ne 0) { Fail "sync-to-wp.ps1 gagal." }

# --- 7. Flush permalink + regenerasi CSS Elementor --------------------------
Write-Step "Flush permalink & regenerasi CSS Elementor"
if (Invoke-Wp rewrite flush) { Write-Ok "permalink di-flush" }
$eval = '$ids = array_merge([59,4], range(24,29), [31,32,33,34]); foreach ($ids as $id) { delete_post_meta($id, "_elementor_css"); delete_post_meta($id, "_elementor_element_cache"); } echo count($ids);'
if (Invoke-Wp eval $eval) { Write-Ok "cache CSS Elementor dibersihkan" }
docker exec $App wp --allow-root --path=/var/www/html elementor flush-css | Out-Null
Write-Ok "elementor flush-css"

# --- 7b. Kata sandi admin (interaktif aman; tidak ditulis ke file/log) -------
if (-not $SkipAdminReset) {
    Write-Step "Atur ulang kata sandi admin"
    $admin = ''
    docker exec $App wp --allow-root --path=/var/www/html user list --role=administrator --field=user_login 2>$null | ForEach-Object { if (-not $admin) { $admin = $_.ToString().Trim() } }
    if (-not $admin) { Fail "Tidak ada user administrator di DB." }
    $sec = Read-Host "Kata sandi BARU untuk admin '$admin' (tidak ditampilkan)"
    if (-not $sec) { Fail "Kata sandi kosong." }
    $env:MT_NEW_PASS = $sec
    docker exec -e MT_NEW_PASS $App wp --allow-root --path=/var/www/html user update $admin --user_pass="$env:MT_NEW_PASS" --skip-email | Out-Null
    Remove-Item Env:MT_NEW_PASS -ErrorAction SilentlyContinue
    if ($LASTEXITCODE -ne 0) { Fail "Gagal mengatur ulang kata sandi." }
    Write-Ok "kata sandi admin '$admin' diperbarui (hanya di container lokal)"
} else {
    Write-Step "Lewati reset kata sandi admin (-SkipAdminReset)"
}

# --- 8. Verifikasi -----------------------------------------------------------
Write-Step "Verifikasi HTTP"
$allOk = $true
foreach ($p in @('/', '/wp-login.php')) {
    $code = '000'
    try {
        $resp = Invoke-WebRequest -Uri ($Url.TrimEnd('/') + $p) -UseBasicParsing -TimeoutSec 20
        $code = [string]$resp.StatusCode
    } catch { $code = '000' }
    if ($code -eq '200') { Write-Ok "$code  $p" }
    else { Write-Host "  $code  $p" -ForegroundColor Red; $allOk = $false }
}

Write-Step "Selesai"
Write-Host "  Site      : $Url/"
Write-Host "  Dashboard : $Url/wp-admin/"
Write-Host "  Portal    : http://localhost:3000/  (Web Fleet, repo terpisah)"
if ($allOk) { Write-Host "  Status    : semua halaman utama 200" -ForegroundColor Green }
else        { Write-Host "  Status    : ADA yang bukan 200 - cek log: docker logs $App" -ForegroundColor Red; exit 1 }
