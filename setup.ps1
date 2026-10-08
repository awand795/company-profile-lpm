<#
.SYNOPSIS
    Bootstrap WordPress MASTER TRUCK dari nol (Windows PowerShell).
    Pasangan dari setup.sh (Linux/macOS).

.DESCRIPTION
    Alur:
      1. docker compose up -d, tunggu MariaDB siap
      2. Salin .htaccess, wp-content/uploads/, plugins/mt-topbar/ ke container
      3. Install WP-CLI di container (unduh wp-cli.phar)
      4. Import database_dump.sql   -> WordPress langsung "ter-instal"
      5. Install + aktifkan theme astra, plugin elementor & astra-sites
      6. sync-to-wp.ps1 (template page + aset tema + media)
      7. Flush permalink & regenerasi CSS Elementor
      8. Verifikasi HTTP 200 pada halaman utama

    BUTUH INTERNET sekali saat pertama: wp-cli.phar, theme astra, plugin
    elementor & astra-sites (unduhan dari wordpress.org / GitHub).

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
    [string]$Url = 'http://localhost:5000',
    [string]$App = 'lpm-wp-app',
    [string]$DbContainer = 'lpm-wp-db',
    [string]$DbUser = 'wordpress',
    [string]$DbPass = 'lotus_wp_password_2026',
    [string]$DbName = 'wordpress'
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

$composeOk = $false
docker compose version | Out-Null
if ($LASTEXITCODE -eq 0) { $compose = @('docker','compose'); $composeOk = $true }
else {
    $dc = Get-Command docker-compose -ErrorAction SilentlyContinue
    if ($dc) { $compose = @('docker-compose'); $composeOk = $true }
}
if (-not $composeOk) { Fail "Perintah 'docker compose' / 'docker-compose' tidak ditemukan." }
if (-not (Test-Path 'docker-compose.yml')) { Fail "docker-compose.yml tidak ada di $root" }
if (-not (Test-Path 'database_dump.sql'))  { Fail "database_dump.sql tidak ada di $root" }
Write-Ok "compose: $($compose -join ' ')"

# Sub-command setelah nama binari (untuk 'docker compose' -> 'compose').
$composeSub = @()
if ($compose.Count -gt 1) { $composeSub = $compose[1..($compose.Count - 1)] }

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
Write-Step "Salin .htaccess + wp-content/uploads + plugins/mt-topbar + mt-booking"
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
if (Test-Path 'wp-content/plugins/mt-topbar') {
    docker cp 'wp-content/plugins/mt-topbar/.' "${App}:/var/www/html/wp-content/plugins/mt-topbar/"
    if ($LASTEXITCODE -ne 0) { Fail "docker cp mt-topbar gagal" }
    Write-Ok "plugins/mt-topbar/"
}
if (Test-Path 'wp-content/plugins/mt-booking') {
    docker cp 'wp-content/plugins/mt-booking/.' "${App}:/var/www/html/wp-content/plugins/mt-booking/"
    if ($LASTEXITCODE -ne 0) { Fail "docker cp mt-booking gagal" }
    Write-Ok "plugins/mt-booking/"
}
docker exec $App chown -R www-data:www-data /var/www/html/.htaccess /var/www/html/wp-content/uploads /var/www/html/wp-content/plugins/mt-topbar /var/www/html/wp-content/plugins/mt-booking | Out-Null

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
    Write-Step "Import database_dump.sql"
    # Dump hasil ekspor Windows sering UTF-16 (BOM FF FE) yang ditolak klien
    # mariadb ("ASCII '\0' appeared..."). Konversi dulu ke UTF-8 bila perlu.
    $restoreSrc = 'database_dump.sql'
    $bom = New-Object byte[] 2
    $fs = [System.IO.File]::OpenRead((Join-Path (Get-Location) 'database_dump.sql'))
    $n = $fs.Read($bom, 0, 2); $fs.Close()
    if ($n -eq 2 -and $bom[0] -eq 0xFF -and $bom[1] -eq 0xFE) {
        $utf8Tmp = Join-Path ([System.IO.Path]::GetTempPath()) 'mt_restore_utf8.sql'
        $text = [System.IO.File]::ReadAllText((Join-Path (Get-Location) 'database_dump.sql'), [System.Text.Encoding]::Unicode)
        [System.IO.File]::WriteAllText($utf8Tmp, $text, (New-Object System.Text.UTF8Encoding $false))
        $restoreSrc = $utf8Tmp
        Write-Ok "dump UTF-16 dikonversi ke UTF-8"
    }
    docker cp $restoreSrc "${DbContainer}:/tmp/restore.sql"
    if ($LASTEXITCODE -ne 0) { Fail "docker cp dump gagal" }
    if ($restoreSrc -ne 'database_dump.sql') { Remove-Item -Path $restoreSrc -Force -ErrorAction SilentlyContinue }
    docker exec -e "MYSQL_PWD=$DbPass" $DbContainer sh -c "mariadb -u'$DbUser' '$DbName' < /tmp/restore.sql && rm -f /tmp/restore.sql" | Out-Null
    if ($LASTEXITCODE -ne 0) { Fail "Import dump gagal." }
    Write-Ok "database_dump.sql diimport"
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
    Write-Ok "home/siteurl: $homeUrl -> $Url"
} else {
    Write-Ok "home/siteurl sudah $Url"
}

# --- 5. Theme & plugin -------------------------------------------------------
Write-Step "Theme astra + plugin elementor, astra-sites, mt-topbar"
if (Invoke-Wp theme is-installed astra) {
    Write-Ok "theme astra sudah terpasang"
} else {
    if (-not (Invoke-Wp theme install astra --activate)) { Fail "Gagal unduh theme astra (cek internet)." }
    Write-Ok "theme astra terpasang"
}
Invoke-Wp theme activate astra | Out-Null
if (Invoke-Wp theme is-active astra) { Write-Ok "theme astra aktif" }

foreach ($p in @('elementor','astra-sites','header-footer-elementor')) {
    if (Invoke-Wp plugin is-installed $p) {
        Write-Ok "plugin $p sudah terpasang"
    } else {
        if (-not (Invoke-Wp plugin install $p)) { Fail "Gagal unduh plugin $p (cek internet)." }
        Write-Ok "plugin $p terpasang"
    }
    if (Invoke-Wp plugin activate $p) { Write-Ok "plugin $p aktif" }
}

if (Invoke-Wp plugin is-installed mt-topbar) {
    Invoke-Wp plugin activate mt-topbar | Out-Null
    Write-Ok "plugin mt-topbar aktif"
} else {
    Fail "plugin mt-topbar tidak ditemukan di container (salinan gagal?)"
}
if (Test-Path 'wp-content/plugins/mt-booking') {
    Invoke-Wp plugin activate mt-booking | Out-Null
    Write-Ok "plugin mt-booking aktif"
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

# --- 8. Verifikasi -----------------------------------------------------------
Write-Step "Verifikasi HTTP"
$allOk = $true
foreach ($p in @('/', '/profil/', '/produk/', '/wilayah/', '/kontak/', '/layanan-overhaul/')) {
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
