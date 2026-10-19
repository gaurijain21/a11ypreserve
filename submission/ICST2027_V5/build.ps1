Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$paperDir = $PSScriptRoot
$tex = (Get-Command pdflatex -ErrorAction Stop).Source
$bib = (Get-Command bibtex -ErrorAction Stop).Source

Push-Location $paperDir
try {
    for ($pass = 1; $pass -le 3; $pass++) {
        & $tex '--enable-installer=no' '-interaction=nonstopmode' '-halt-on-error' '-file-line-error' 'main.tex'
        if ($LASTEXITCODE -ne 0) { throw "pdflatex pass $pass failed with exit code $LASTEXITCODE" }
        if ($pass -eq 1) {
            & $bib 'main'
            if ($LASTEXITCODE -ne 0) { throw "bibtex failed with exit code $LASTEXITCODE" }
        }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $paperDir 'main.pdf'))) {
        throw 'main.pdf was not produced'
    }
    Write-Output "Built $((Join-Path $paperDir 'main.pdf'))"
}
finally {
    Pop-Location
}
