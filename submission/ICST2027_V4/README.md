# A11yPreserve V4 manuscript

This manuscript is generated from the completed frozen V4 evidence. It reports the 65-fixture corpus across LibreOffice and Google Docs, retains the 26-case holdout separation, and does not include Word in the denominator. V3 remains preserved at `submission/ICST2027_V3/`.

Primary evidence:

- `experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json`
- `experiments/v4/conversions/google/analysis/V4_GOOGLE_ANALYSIS.json`
- `experiments/v4/conversions/CROSS_PIPELINE_COMPARISON.json`
- `reports/V4_CONVERSION_RECOVERY_FINAL.md`

## Verified manuscript build

Run the following command twice from the repository root:

```text
pdflatex --enable-installer=no -interaction=nonstopmode -halt-on-error -file-line-error -output-directory submission\ICST2027_V4 submission\ICST2027_V4\main.tex
```

The first MiKTeX run on a cold package cache may take roughly two minutes while loading packages. Keep the process attached as long as output continues to advance. Subsequent runs complete in a few seconds. The verified output is `submission/ICST2027_V4/main.pdf`.
