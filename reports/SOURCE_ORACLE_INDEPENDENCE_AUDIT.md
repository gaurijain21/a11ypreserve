# Source-oracle independence audit

The source verification path is a separately implemented raw-OOXML oracle, not external expert validation. `artifact_v3/src/independent_source_oracle.py` uses only the frozen manifest for locations and expected source contracts, then reads DOCX ZIP/XML parts directly with the Python standard library. It does not import ASIR, fixture-generation, manifest-generation, or destination-comparator code.

The fresh run passed 13/13 Core contracts. The path remains same-team code and therefore is not statistically or institutionally independent. The result supports “separately implemented source oracle,” not “independent validation.”

The corruption suite `tools/test_source_oracle_corruptions.py` creates temporary DOCX mutations for headings, alternative text, document language, table headers, hyperlink targets, and footnote parts. Each mutation must be rejected by the corresponding raw-OOXML observation, without modifying frozen sources.
