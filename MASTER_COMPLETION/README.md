# MASTER_COMPLETION — CopyLab Phase-0 coordination package

**Phase 0: NOT SATISFIED · Phase 1A: NOT AUTHORISED · G1–G5: NOT AUTHORISED · no fix performed.**

Owner decisions **D-1…D-12** are recorded in **`MCD-04.md`**. Latest: **D-12** — the owner accepted R1–R10 and the
35-case suite and ordered one consolidated external-review preparation stage, with **no routine approvals**. That
stage produced the safety-requirement set (`MCD-08`), the G2 schema design (`MCD-09`), version pinning (`MCD-10`),
the reviewer checklist (`MCD-11`) and this consistency check. **No gate advanced.**
Red-phase suite re-based **32 → 35** criteria; all **35 fail** on the current snapshot.

## Read in this order

| # | Document | What it answers |
|---|---|---|
| 1 | **`MCD-04.md`** — decisions ledger | D-1…D-12, TD-01 transmission record, gate state, Phase-0 definition |
| 2 | **`MCD-07.md`** — group cross-reference | **read before any ordering discussion**: 1A–1H ↔ G1–G6, authoritative |
| 3 | **`MCD-06.md`** — R1–R10 disposition register | what was accepted/amended; the R4/R5 restatements |
| 4 | **`MCD-01.md`** — coordination dossier | state, reconciliation, 6-group plan, 10 blockers, armed sequence |
| 5 | **`MCD-02.md`** — the 35 criteria | per-test root cause, pre-fix result, post-fix acceptance condition |
| 6 | **`MCD-03.md`** — A14-08 correction | the claim withdrawn, corrected finding, reproducible evidence |
| 7 | **`MCD-05.md`** — external review package | reviewer instructions, task list, signature block |
| 8 | **`MCD-08.md`** — **safety requirements SR-01…SR-28** | authoritative, provenance-tagged; closes GOV-01 |
| 9 | **`MCD-09.md`** — G2 schema design | attempt + scope identity; **design only, no migration** |
| 10 | **`MCD-10.md`** — version pinning | exact versions, divergence, reproducibility limits |
| 11 | **`MCD-11.md`** — reviewer checklist A–I | what must be reproduced, inspected, and signed off |
| 12 | **`CONSISTENCY_CHECK.md`** | measured evidence that the package agrees with itself |
| — | `../AUDIT_REPORT_INDEP-AUDIT-01.md` | the independent audit (49 cases); **unedited**, correction appended |

## Group numbering (one line — full table in `MCD-07.md`)

`G1 = plan 1A` · `G2 = plan 1B + 1E + 1F + 1G` · `G3 = plan 1C` · `G4 = plan 1D` · `G5 = plan 1H` ·
`G6 = no plan equivalent` (external evidence programme).

**Neither scheme was renumbered.** The project's plan keeps 1A–1H; this package uses G1–G6; `MCD-07` binds them.

## The 35 acceptance criteria — individual results

Executable: `tools/acceptance_suite.py` · Machine-readable: `evidence/red-phase-results.json`
Run against the pristine snapshot: **35 tested, 0 pass, 35 fail, phase RED.**
Exit code 1 is the expected and correct result.

| # | Finding | Test | Sev | Grp | Result | Observed |
|---|---|---|---|---|---|---|
| 1 | A14-01 | `closed_position_cycle_corruption_detected` | MEDIUM | G3 | **FAIL** | verifier exit=0 errors=[] (closed cycle unverified) |
| 2 | A14-01 | `ledger_cost_delta_corruption_detected` | MEDIUM | G3 | **FAIL** | verifier exit=0 errors=[] |
| 3 | A14-01 | `ledger_fee_corruption_detected` | MEDIUM | G3 | **FAIL** | verifier exit=0 errors=[] (fee not reconciled) |
| 4 | A14-01 | `ledger_realized_corruption_detected` | HIGH | G3 | **FAIL** | verifier exit=0 errors=[] while total_pnl=999.00000000 |
| 5 | A14-01 | `snapshot_equity_corruption_detected` | MEDIUM | G3 | **FAIL** | verifier exit=0 errors=[] (equity curve unverified) |
| 6 | A14-01 | `verifier_does_not_hardcode_integrity_ok` | MEDIUM | G3 | **FAIL** | hardcoded portfolios_checked=10 on an empty DB |
| 7 | A14-02 | `dangling_event_movement_detected` | HIGH | G2 | **FAIL** | errors=[] (dangling FK invisible; schema has no FK) |
| 8 | A14-02 | `extra_leg_on_valid_event_detected` | HIGH | G2 | **FAIL** | errors=[] (extra leg invisible) |
| 9 | A14-02 | `orphan_effect_detected` | HIGH | G2 | **FAIL** | errors=[] (orphan effect invisible) |
| 10 | A14-02 | `orphan_movement_detected` | HIGH | G2 | **FAIL** | errors=[] source_cash=0 (orphan invisible) |
| 11 | A14-03 | `nway_split_requires_operation_spec` | HIGH | G4 | **FAIL** | unspecified 3-way split state=applied |
| 12 | A14-03 | `single_sided_split_quarantined` | HIGH | G4 | **FAIL** | single-sided split state=applied |
| 13 | A14-03 | `zero_basis_split_quarantined` | HIGH | G4 | **FAIL** | zero-basis split state=applied; 0 == 0 satisfies the paid-basis identity |
| 14 | A14-04 | `negative_cash_redemption_rejected` | MEDIUM | G4 | **FAIL** | negative-cash redemption state=applied |
| 15 | A14-04 | `unproved_out_of_range_redemption_quarantined` | HIGH | G4 | **FAIL** | unproved redemption state=applied |
| 16 | A14-05 | `conflict_record_is_append_only` | MEDIUM | G2 | **FAIL** | no append-only conflict evidence: the conflicting payload is absent from every non-state table (34 c |
| 17 | A14-05 | `conflicting_payload_retained` | MEDIUM | G2 | **FAIL** | conflicting payload not retained in any of 36 tables |
| 18 | A14-06 | `all_failed_attempt_bodies_retained` | MEDIUM | G2 | **FAIL** | 1 durable rows for 3 received attempts: ['body-3'] |
| 19 | A14-06 | `attempt_order_and_metadata_distinguishable` | MEDIUM | G2 | **FAIL** | 1 rows for 3 attempts with identical bodies (attempt identity lost) |
| 20 | A14-06 | `attempt_without_last_raw_is_durable` | MEDIUM | G2 | **FAIL** | durable bodies=[]; nothing persisted at all |
| 21 | A14-06 | `successful_body_survives_later_failure` | MEDIUM | G2 | **FAIL** | successful body destroyed; durable=['bad-504'] |
| 22 | A14-07 | `collect_enforces_scope_without_allowed` | MEDIUM | G2 | **FAIL** | scope mismatch neither rejected nor forked: reused pending batch, sent status='CLOSED' for a request |
| 23 | A14-07 | `frontier_not_published_for_wrong_scope` | MEDIUM | G2 | **FAIL** | frontier published for a CLOSED walk under an OPEN request: [{'wallet': 'fixture-wallet', 'endpoint' |
| 24 | A14-07 | `scope_identity_persisted_per_batch` | MEDIUM | G2 | **FAIL** | collection_batches has no explicit scope-identity column (columns=['id', 'wallet', 'endpoint', 'para |
| 25 | A14-07 | `scope_substitution_rejected` | MEDIUM | G2 | **FAIL** | OPEN request was sent as status=CLOSED |
| 26 | A14-08 | `digest_distinguishes_blob_from_its_repr_text` | LOW | G1 | **FAIL** | collision: blob and text share digest fe21b3a17c7cc0eb (default=str renders bytes as the text b"..." |
| 27 | A14-08 | `digest_distinguishes_blob_from_text` | LOW | G1 | **FAIL** | collision: blob and text(text) share digest fe21b3a17c7cc0eb |
| 28 | A14-09 | `stale_health_not_green` | MEDIUM | G5 | **FAIL** | stale ts=0 row rendered as 'Healthy' |
| 29 | A14-10 | `backup_requires_ownership` | LOW | G1 | **FAIL** | backup succeeded while another owner held the worker lock |
| 30 | A14-10 | `lock_identity_is_canonical` | MEDIUM | G1 | **FAIL** | symlinked path acquired a SECOND exclusive lock: two owners possible |
| 31 | A14-10 | `store_requires_ownership_before_write` | MEDIUM | G1 | **FAIL** | a second Store() became a WRITER while the owner held the worker lock; Store() itself is not ownersh |
| 32 | F-02 | `verifier_binds_database_identity` | MEDIUM | G3 | **FAIL** | verifier report does not bind the verified database bytes (no sha256 44e9b382070d...); findings cann |
| 33 | F-03 | `signing_scan_fails_closed` | MEDIUM | G3 | **FAIL** | exit=0 errors=[] - scan silently empty when cwd has no lab/ |
| 34 | F-04 | `hold_history_is_append_only` | MEDIUM | G2 | **FAIL** | hold history overwritten: final visible reasons={'gap B'} |
| 35 | F-05 | `hold_release_is_attributable` | MEDIUM | G2 | **FAIL** | no hold-release mechanism or release record exists in code or schema |

**All 35 currently FAIL.** That is the required state before any fix. A future green run is meaningful
only because these same tests are known red today.

**Changed by D-9 (R4/R5 amendments):** #18 and #21 strengthened; **#19, #22, #24 are new**.
#19 closes a de-duplication loophole in the R4 obligation; #22 encodes R5's "no dependence on `allowed()` or
callers" structurally; #24 requires a persisted scope identity rather than a symptom fix.

## Gate state (authoritative — see `MCD-04.md` §1)

| Gate | State |
|---|---|
| Phase 0 — independent review satisfied | **NOT SATISFIED** |
| Phase 1A / G1 … G5 implementation | **NOT AUTHORISED** (D-5, D-10) |
| Red-phase suite | **ADOPTED, PROVISIONAL** (D-4), now 35 criteria, subject to external review |
| R1–R10 plan revisions | **DISPOSITIONED** — 8 ACCEPT, 2 AMEND, applied (D-9) |
| 1A–1H ↔ G1–G6 numbering | **RESOLVED** (D-11 → `MCD-07.md`) |
| External review | **MANDATORY, OUTSTANDING** (D-3) — GOV-02 BLOCKED |
| A14-08 numeric-collision claim | **WITHDRAWN**; corrected finding accepted (D-2) |
| Paper-only, snapshot, databases | **PRESERVED, unchanged** (D-6) |

## The 10 blockers

| # | Blocker | Class | Clears when |
|---|---|---|---|
| 1 | **GOV-02** no genuinely external reviewer | governance | reviewer engaged and signed (`MCD-05` §4) |
| 2 | No authorisation of a bounded scope | governance | owner grants after §1–2 clear |
| 3 | **H01** no authoritative source checkpoint | evidence | upstream/provider capability proof |
| 4 | **H02** no canonical identity/finality | evidence | real chain identity evidence |
| 5 | **H03** no real decoder evidence | evidence | version-specific operation data |
| 6 | **H04** no historical gap reconstruction | evidence | history that does not currently exist |
| 7 | **H05** no forward / calibration / performance evidence | evidence | approved wallets + time |
| 8 | Runtime DB state unverified (excluded by design) | evidence | separate explicit approval |
| 9 | **GOV-15** cross-version reproducibility unpinned | technical | parity evidence (`MCD-10`) |
| 10 | **GOV-14** `capture_frontiers` key `(wallet, endpoint)` cannot be fixed additively | technical | new table or rebuild, decided at G2 (`MCD-09`) |

Blockers 3–7 mean CopyLab **cannot currently demonstrate it would copy a real wallet correctly even if every
A14 defect were fixed.** Fixing A14 improves the instruments; it does not supply the measurements.

*(Closed since the previous edition: **GOV-01** (D-12 → `MCD-08`), **GOV-08** (D-9), **GOV-09 design** (D-12 → `MCD-09`), **GOV-11**, **GOV-12** (D-11), and the version-documentation portion of the cross-version blocker (now `MCD-10`; parity itself is GOV-15). GOV-01 also removes TD-01 from the blocker list — the transmission discrepancy remains on the record, but its safety content is now captured in `MCD-08`.)*

## Package contents

```
MCD-01.md                          coordination dossier (plan, blockers, sequence)
MCD-02.md                          35 criteria, individually specified
MCD-03.md                          A14-08 correction record + reproducible evidence
MCD-04.md                          owner decisions D-1..D-12, TD-01, gate state
MCD-05.md                          external review package + signature block
MCD-06.md                          R1-R10 disposition register (D-9)
MCD-07.md                          group cross-reference 1A-1H <-> G1-G6 (D-11)
MCD-08.md                          safety requirements SR-01..SR-28 (authoritative, D-12)
MCD-09.md                          G2 schema design: attempt + scope identity (design only)
MCD-10.md                          environment and version pinning
MCD-11.md                          reviewer checklist A-I
CONSISTENCY_CHECK.md               measured package self-consistency evidence
README.md                          this file
tools/acceptance_suite.py          the 35 executable criteria
tools/REPRODUCE.md                 exact reproduction commands + isolation
tools/package.json                 jsdom dependency for the A14-09 probe only
evidence/red-phase-results.json    35/35 FAIL, per-case detail
evidence/probes/                   49-case probe corpus (5 files)
evidence/results/                  probe outputs, hashed
evidence/ARTEFACT_MANIFEST.json    hashes of this package
```

**Not present, by design:** runtime databases, `.git`, wallet addresses, chain identifiers, real market data,
synthetic data dressed as real. `node_modules` and `__pycache__` are git-ignored.

## Next objective (owner D-7)

Obtain a genuinely external review; establish whether Phase 0 can be satisfied. **Do not mark it complete
prematurely.** The package is ready in `MCD-05.md`; the gate is not.
