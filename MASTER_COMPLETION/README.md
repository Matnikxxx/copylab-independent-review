# MASTER_COMPLETION — CopyLab Phase-0 coordination package

**Status: Phase 0 NOT SATISFIED · Phase 1A NOT AUTHORISED · no fix performed.**

Start with [`MCD-01.md`](MCD-01.md). It is the consolidated dossier: state, reconciliation with the
existing master plan/register, the six-group remediation plan, 32 acceptance criteria, the red-phase
result, the external-review package, 11 blockers, and the armed implementation sequence.

| What | Where |
|---|---|
| Consolidated dossier | `MCD-01.md` |
| Red-phase acceptance suite (32 tests) | `tools/acceptance_suite.py` |
| Reproduction guide for outside reviewers | `tools/REPRODUCE.md` |
| Red-phase result (**32/32 fail**) | `evidence/red-phase-results.json` |
| My 49 reproduction probes | `evidence/probes/` |
| Probe outputs | `evidence/results/` |
| Artefact hashes | `evidence/ARTEFACT_MANIFEST.json` |

**Read `MCD-01.md` §0.1 first:** the master directive arrived truncated at "No live trading," so the
safety list was reconstructed from the strictest available sources. That is open item GOV-01.

**Read `MCD-01.md` §0.4 second:** it corrects an overstatement in `AUDIT_REPORT_INDEP-AUDIT-01.md` (A14-08
numeric-type collisions do not exist; the BLOB-repr collision does).

Nothing here modifies the audited snapshot. The CopyLab source remains sealed in the ZIP.
