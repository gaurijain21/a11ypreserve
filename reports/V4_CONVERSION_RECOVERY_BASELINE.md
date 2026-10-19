# V4 Conversion Recovery Baseline

Recorded before any V4 converter output was produced or inspected.

## Repository state

- Baseline Git status: clean (`## master`)
- Baseline commit: `7abddc7ee5f25c245e445fdc953ae1add83b6ef0`
- V4 protocol freeze commit: `41a7d3f8b84e98acbdafe14070f2ebe7ea6a59e1`
- Frozen V4 atomic fixture count: 65
- Frozen V4 protocol and decision rules were not modified for conversion recovery.
- No V4 converter outputs existed at baseline; no converter result was inspected before this record.

## Frozen artifact hashes

SHA-256 values are recorded exactly as present at baseline.

| Artifact | SHA-256 |
|---|---|
| `experiments/v4/V4_PROTOCOL.md` | `B4A2F974B7E14CB6C5847EB8667BF3A7E9CDF5C38C60AFE9C47391F476648556` |
| `experiments/v4/PRE_RESULT_FREEZE.json` | `14890A635455D7E73D82867A254264C4518038F1BAF6BB331B922DD70418CB36` |
| `experiments/v4/source_manifest.json` | `6D4E77423E84AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7` |
| `experiments/v4/v4_comparator.py` | `8BD28AF4E330D100290A049965834CFB47B388A89DE36E563C741CC3199F8EC4` |
| `experiments/v4/v4_source_oracle.py` | `7B5C309D80BD2DC32438A8EACE499ED145A0BF77E880616A0AA0875935EC1DE6` |
| `scripts/extract_semantics.py` | `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7` |
| `artifact/src/extract_semantics.py` | `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7` |

## Scope guard

This file is a provenance record only. It does not alter the frozen V4 protocol, contracts, taxonomy, feature families, fixtures, comparator, source oracle, or destination extractor.
