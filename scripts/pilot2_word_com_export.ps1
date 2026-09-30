$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$pilot2 = Join-Path $root 'pilot2'
$outDir = Join-Path $pilot2 'outputs\word_pdf'
$logDir = Join-Path $pilot2 'logs'
New-Item -ItemType Directory -Force -Path $outDir,$logDir | Out-Null
$fixtures = @('F01_HEADINGS','F02_ALT_TEXT','F03_LISTS','F04_TABLE')
$records = @()
$word = $null
$version = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $version = [string]$word.Version
  foreach($fixture in $fixtures) {
    $src = Join-Path $root ("pilot\fixtures\{0}.docx" -f $fixture)
    $dst = Join-Path $outDir ("{0}__WORD.pdf" -f $fixture)
    $doc = $null
    $row = [ordered]@{fixture=$fixture; source=$src; destination=$dst; converter='Microsoft Word'; version=$version; method='Word.Application Documents.Open + ExportAsFixedFormat'; settings=[ordered]@{ExportFormat='wdExportFormatPDF (17)'; OpenAfterExport=$false; OptimizeFor='wdExportOptimizeForPrint (0)'; Range='wdExportAllDocument (0)'; Item='wdExportDocumentContent (0)'; IncludeDocProps=$true; KeepIRM=$true; CreateBookmarks='wdExportCreateHeadingBookmarks (1)'; DocStructureTags=$true; BitmapMissingFonts=$true; UseISO19005_1=$true}; status='failed'; error=$null}
    try {
      $doc = $word.Documents.Open($src, $false, $true, $false)
      $doc.ExportAsFixedFormat($dst, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $true)
      $row.status='ok'
      $row.output_size=(Get-Item -LiteralPath $dst).Length
    } catch { $row.error=$_.Exception.ToString() }
    finally { if($null -ne $doc){ try{$doc.Close($false)}catch{} } }
    $records += [pscustomobject]$row
  }
} catch {
  $records += [pscustomobject][ordered]@{fixture=$null; converter='Microsoft Word'; version=$version; method='Word.Application COM activation'; status='blocked'; error=$_.Exception.ToString()}
} finally { if($null -ne $word){ try{$word.Quit()}catch{} } }
$result = [ordered]@{timestamp_utc=(Get-Date).ToUniversalTime().ToString('o'); os="Windows $([System.Environment]::OSVersion.Version)"; word_version=$version; records=$records}
$result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $logDir 'word_com_attempt.json') -Encoding UTF8
$result | ConvertTo-Json -Depth 10
