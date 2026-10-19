# Google route audit

Core and Core repeatability used the recorded visible Google Docs download workflow. Variant B used the authenticated in-session export backend after the visible download action did not register despite retries. The deviation is recorded in `v3/variant_set_b/google/CONVERSION_REPORT.json`; no print-to-PDF, screenshot, or manual repair was used.

The three-run Core arm produced stable classifications and byte-identical files for all 13 fixtures under the recorded workflow. This supports workflow repeatability for the dated run, not backend invariance or future-service reproducibility. The route difference is a threat to direct Core/Variant B comparison and is retained rather than normalized post hoc.
