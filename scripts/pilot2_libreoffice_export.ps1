param(
    [string]$RuntimeRoot = (Join-Path $PSScriptRoot '..\pilot2\libreoffice_runtime'),
    [string]$FixtureRoot = (Join-Path $PSScriptRoot '..\pilot\fixtures'),
    [string]$OutputRoot = (Join-Path $PSScriptRoot '..\pilot2\outputs\libreoffice_pdf'),
    [string]$StagingRoot = (Join-Path $PSScriptRoot '..\pilot2\lo_inputs'),
    [string]$ProfileRoot = (Join-Path $PSScriptRoot '..\pilot2\lo_profiles')
)

$ErrorActionPreference = 'Stop'
$runtime = (Resolve-Path -LiteralPath $RuntimeRoot).Path
$fixtures = (Resolve-Path -LiteralPath $FixtureRoot).Path
New-Item -ItemType Directory -Force -Path $OutputRoot, $StagingRoot, $ProfileRoot | Out-Null

$fixtureNames = @(
    'F01_HEADINGS',
    'F02_ALT_TEXT',
    'F03_LISTS',
    'F04_TABLE'
)

$records = @()
foreach ($fixtureName in $fixtureNames) {
    $source = Join-Path $fixtures ($fixtureName + '.docx')
    $staging = Join-Path $StagingRoot ($fixtureName + '__LIBREOFFICE.docx')
    $profile = Join-Path $ProfileRoot $fixtureName
    $converted = Join-Path $OutputRoot ($fixtureName + '__LIBREOFFICE.pdf')
    $temporaryOutput = Join-Path $OutputRoot ($fixtureName + '__LIBREOFFICE.pdf')

    Copy-Item -LiteralPath $source -Destination $staging -Force
    New-Item -ItemType Directory -Force -Path $profile | Out-Null
    if (Test-Path -LiteralPath $temporaryOutput) {
        Remove-Item -LiteralPath $temporaryOutput -Force
    }

    $profileUri = 'file:///' + ((Resolve-Path -LiteralPath $profile).Path.Replace('\', '/'))
    $outputPath = (Resolve-Path -LiteralPath $OutputRoot).Path
    $stagingPath = (Resolve-Path -LiteralPath $staging).Path
    $argumentString = '-env:UserInstallation=' + $profileUri +
        ' --headless --invisible --nodefault --nologo --nolockcheck --norestore --nofirststartwizard' +
        ' --convert-to "pdf:writer_pdf_Export:UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1"' +
        ' --outdir "' + $outputPath + '" "' + $stagingPath + '"'

    $started = Get-Date
    $process = Start-Process -FilePath (Join-Path $runtime 'program\soffice.com') `
        -ArgumentList $argumentString `
        -WorkingDirectory (Join-Path $runtime 'program') `
        -PassThru

    $deadline = (Get-Date).AddSeconds(120)
    do {
        Start-Sleep -Milliseconds 500
        $exists = Test-Path -LiteralPath $converted
        $running = Get-Process -Id $process.Id -ErrorAction SilentlyContinue
    } while (-not $exists -and $running -and (Get-Date) -lt $deadline)

    $result = 'SUCCESS'
    $errorText = $null
    if (-not (Test-Path -LiteralPath $converted)) {
        $result = 'FAILED'
        $errorText = 'LibreOffice did not produce the expected PDF within 120 seconds.'
        if ($running) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    }

    $records += [ordered]@{
        fixture = $fixtureName
        source = $source
        staging_source = $staging
        destination = $converted
        method = 'LibreOffice soffice.com headless conversion using writer_pdf_Export'
        settings = 'UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1'
        started_at = $started.ToString('o')
        completed_at = (Get-Date).ToString('o')
        result = $result
        error = $errorText
        process_id = $process.Id
    }
}

$records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot '..\pilot2\logs\libreoffice_export_attempt.json') -Encoding UTF8
$records | Format-Table fixture,result,destination,process_id -AutoSize
