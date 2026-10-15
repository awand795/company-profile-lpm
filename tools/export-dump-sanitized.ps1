<#
.SYNOPSIS
    Ekspor dump database TERSANITASI untuk Git (RONDE 14).
    Dump asli hanya ke _backup_lokal_tidak_di_git (di luar repo).
#>
param(
    [string]$DbContainer = 'lpm-wp-db',
    [string]$Out = 'database/mt_site.sql',
    [string]$RawDir = ''
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
$args2 = @('--dbcontainer', $DbContainer, '--out', $Out)
if ($RawDir) { $args2 += @('--rawdir', $RawDir) }
python tools/export-dump-sanitized.py @args2
if ($LASTEXITCODE -ne 0) { exit 1 }
