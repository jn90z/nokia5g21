<#
.SYNOPSIS
  Inventory PanicOpticon archives and prepare a small shareable analysis bundle.
.EXAMPLE
  .\tools\prepare-research.ps1 -Archives "C:\Downloads\part1.zip","C:\Downloads\part2.zip"
.NOTES
  PowerShell 5.1+; requires Python 3.11+ for the optional firmware scanner.
  Does not execute any extracted files. Original archives remain unchanged.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string[]]$Archives,
  [string]$OutputDirectory = "reports\panicopticon",
  [switch]$Extract,
  [switch]$ScanFirmware
)
$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not [IO.Path]::IsPathRooted($OutputDirectory)) {
  $OutputDirectory = Join-Path $repoRoot $OutputDirectory
}
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$archiveRecords = @()
$entryRecords = @()
$extractRoot = Join-Path $repoRoot "firmware\panicopticon"
foreach ($archive in $Archives) {
  $file = Get-Item -LiteralPath $archive -ErrorAction Stop
  if ($file.Extension -ine ".zip") { throw "Only .zip archives are supported: $($file.FullName)" }
  $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  $archiveRecords += [pscustomobject]@{ Name=$file.Name; SizeBytes=$file.Length; SHA256=$hash }
  Add-Type -AssemblyName System.IO.Compression
  $zip = [IO.Compression.ZipFile]::OpenRead($file.FullName)
  try {
    foreach ($entry in $zip.Entries) {
      $entryRecords += [pscustomobject]@{
        Archive=$file.Name; Path=$entry.FullName; SizeBytes=$entry.Length;
        CompressedBytes=$entry.CompressedLength
      }
    }
  } finally { $zip.Dispose() }
  if ($Extract) {
    # Separate destination per archive prevents name collisions.
    $destination = Join-Path $extractRoot ([IO.Path]::GetFileNameWithoutExtension($file.Name))
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    $base = [IO.Path]::GetFullPath($destination).TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    $zip = [IO.Compression.ZipFile]::OpenRead($file.FullName)
    try {
      foreach ($entry in $zip.Entries) {
        $target = [IO.Path]::GetFullPath((Join-Path $destination $entry.FullName))
        if (-not $target.StartsWith($base,[StringComparison]::OrdinalIgnoreCase)) {
          throw "Unsafe archive entry path: $($entry.FullName)"
        }
        if ($entry.FullName.EndsWith("/")) {
          New-Item -ItemType Directory -Force -Path $target | Out-Null
          continue
        }
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        if (Test-Path -LiteralPath $target) {
          throw "Destination already exists; refusing to overwrite: $target"
        }
        $inputStream = $entry.Open()
        try {
          $outputStream = [IO.File]::Open($target,[IO.FileMode]::CreateNew)
          try { $inputStream.CopyTo($outputStream) }
          finally { $outputStream.Dispose() }
        } finally { $inputStream.Dispose() }
      }
    } finally { $zip.Dispose() }
  }
}
$archiveRecords | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $OutputDirectory "archives.json")
$entryRecords | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutputDirectory "zip-contents.csv")
if ($Extract) {
  python (Join-Path $repoRoot "tools\hash_inventory.py") $extractRoot --json (Join-Path $OutputDirectory "extracted-hashes.json")
  if ($LASTEXITCODE -ne 0) { throw "Hash inventory failed" }
}
if ($ScanFirmware) {
  if (-not $Extract) { throw "-ScanFirmware requires -Extract" }
  $scanDir = Join-Path $OutputDirectory "scans"
  New-Item -ItemType Directory -Force -Path $scanDir | Out-Null
  $files = Get-ChildItem -LiteralPath $extractRoot -Recurse -File |
    Where-Object { $_.Extension -in @(".bin",".img",".dump",".ubi",".squashfs") }
  $index = 0
  foreach ($item in $files) {
    $index++
    python (Join-Path $repoRoot "tools\firmware_scan.py") $item.FullName --json (Join-Path $scanDir ("scan-{0:D4}.json" -f $index)) | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Firmware scan failed: $($item.FullName)" }
  }
}
Write-Host "Completed. Reports: $OutputDirectory"
Write-Host "Archive count: $($archiveRecords.Count); ZIP entries: $($entryRecords.Count)"
Write-Host "Share only the generated reports after reviewing for private data."
