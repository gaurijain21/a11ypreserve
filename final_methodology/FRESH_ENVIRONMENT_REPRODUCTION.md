# Fresh-environment reproduction audit

## Level 1 verification

In the current project environment, the V3 classification runner reproduced all 26 Core decisions and the V3 Variant Set B source oracle passed 13/13. The local LibreOffice variant converter produced 13/13 parseable tagged PDFs.

## Clean-environment attempt

A new Python virtual environment was created under a V3-only temporary path. Installing the artifact requirements failed because the sandbox could not reach the package index (`WinError 10013`, no permitted socket access). The environment was removed after the failed attempt. No claim of full clean-environment reproduction is made.

## Reproducibility consequence

The artifact supports evidence verification and local reruns when its documented Python dependencies are available. A true fresh-machine reproduction still requires a dependency source or prebuilt environment. Google Docs additionally requires an authenticated cloud workflow and cannot be perfectly reproduced from a local package.

