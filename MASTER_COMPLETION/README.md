# MASTER_COMPLETION — CopyLab Phase-0 coordination package

**Phase 0: NOT SATISFIED · Phase 1A: NOT AUTHORISED · G1: NOT AUTHORISED · no fix performed.**

Owner decisions of 2026-11-05 are recorded in **`MCD-04.md`** (D-1…D-8). The only state change this run
makes is that the 32-case suite is now the **provisional** acceptance baseline (D-4). No gate was advanced.

## Read in this order

| # | Document | What it answers |
|---|---|---|
| 1 | **`MCD-04.md`** — decisions ledger | what the owner decided, TD-01 transmission record, what would satisfy Phase 0 |
| 2 | **`MCD-01.md`** — coordination dossier | state, reconciliation, 6-group plan, blockers, armed sequence |
| 3 | **`MCD-02.md`** — the 32 criteria | per-test root cause, pre-fix result, post-fix acceptance condition |
| 4 | **`MCD-03.md`** — A14-08 correction | the claim I withdrew, the corrected finding, reproducible evidence |
| 5 | **`MCD-05.md`** — external review package | reviewer instructions, task list, signature block |
| — | `../AUDIT_REPORT_INDEP-AUDIT-01.md` | the independent audit (49 cases); **unedited**, correction appended |

## The 32 acceptance criteria — individual results

Executable: `tools/acceptance_suite.py` · Machine-readable: `evidence/red-phase-results.json`
Run against the pristine snapshot: **32 tested, 0 pass, 32 fail, phase RED.**
Exit code 1 is the expected and correct result.

| # | Finding | Test | Sev | Result | Observed |
|---|---|---|---|---|---|
| 1 | A14-01 | `closed_position_cycle_corruption_detected` | MEDIUM | **FAIL** | verifier exit=0 errors=[] (closed cycle unverified) |
| 2 | A14-01 | `ledger_cost_delta_corruption_detected` | MEDIUM | **FAIL** | verifier exit=0 errors=[] |
| 3 | A14-01 | `ledger_fee_corruption_detected` | MEDIUM | **FAIL** | verifier exit=0 errors=[] (fee not reconciled) |
| 4 | A14-01 | `ledger_realized_corruption_detected` | HIGH | **FAIL** | verifier exit=0 errors=[] while total_pnl=999.00000000 |
| 5 | A14-01 | `snapshot_equity_corruption_detected` | MEDIUM | **FAIL** | verifier exit=0 errors=[] (equity curve unverified) |
| 6 | A14-01 | `verifier_does_not_hardcode_integrity_ok` | MEDIUM | **FAIL** | hardcoded portfolios_checked=10 on an empty DB |
| 7 | A14-02 | `dangling_event_movement_detected` | HIGH | **FAIL** | errors=[] (dangling FK invisible; schema has no FK) |
| 8 | A14-02 | `extra_leg_on_valid_event_detected` | HIGH | **FAIL** | errors=[] (extra leg invisible) |
| 9 | A14-02 | `orphan_effect_detected` | HIGH | **FAIL** | errors=[] (orphan effect invisible) |
| 10 | A14-02 | `orphan_movement_detected` | HIGH | **FAIL** | errors=[] source_cash=0 (orphan invisible) |
| 11 | A14-03 | `nway_split_requires_operation_spec` | HIGH | **FAIL** | unspecified 3-way split state=applied |
| 12 | A14-03 | `single_sided_split_quarantined` | HIGH | **FAIL** | single-sided split state=applied |
| 13 | A14-03 | `zero_basis_split_quarantined` | HIGH | **FAIL** | zero-basis split state=applied; 0 == 0 satisfies the paid-basis identity |
| 14 | A14-04 | `negative_cash_redemption_rejected` | MEDIUM | **FAIL** | negative-cash redemption state=applied |
| 15 | A14-04 | `unproved_out_of_range_redemption_quarantined` | HIGH | **FAIL** | unproved redemption state=applied |
| 16 | A14-05 | `conflict_record_is_append_only` | MEDIUM | **FAIL** | no append-only conflict evidence: the conflicting payload is absent from every non-state table (34 checked); o |
| 17 | A14-05 | `conflicting_payload_retained` | MEDIUM | **FAIL** | conflicting payload not retained in any of 36 tables |
| 18 | A14-06 | `all_failed_attempt_bodies_retained` | MEDIUM | **FAIL** | durable bodies=['body-3'] (expected all 3) |
| 19 | A14-06 | `attempt_without_last_raw_is_durable` | MEDIUM | **FAIL** | durable bodies=[]; nothing persisted at all |
| 20 | A14-06 | `successful_body_survives_later_failure` | MEDIUM | **FAIL** | durable bodies=['bad-504']; the successful body was destroyed |
| 21 | A14-07 | `frontier_not_published_for_wrong_scope` | MEDIUM | **FAIL** | frontier published for a CLOSED walk under an OPEN request: [{'wallet': 'fixture-wallet', 'endpoint': '/v2/pos |
| 22 | A14-07 | `scope_substitution_rejected` | MEDIUM | **FAIL** | OPEN request was sent as status=CLOSED |
| 23 | A14-08 | `digest_distinguishes_blob_from_its_repr_text` | LOW | **FAIL** | collision: blob and text share digest fe21b3a17c7cc0eb (default=str renders bytes as the text b"..." ) |
| 24 | A14-08 | `digest_distinguishes_blob_from_text` | LOW | **FAIL** | collision: blob and text(text) share digest fe21b3a17c7cc0eb |
| 25 | A14-09 | `stale_health_not_green` | MEDIUM | **FAIL** | stale ts=0 row rendered as 'Healthy' |
| 26 | A14-10 | `backup_requires_ownership` | LOW | **FAIL** | backup succeeded while another owner held the worker lock |
| 27 | A14-10 | `lock_identity_is_canonical` | MEDIUM | **FAIL** | symlinked path acquired a SECOND exclusive lock: two owners possible |
| 28 | A14-10 | `store_requires_ownership_before_write` | MEDIUM | **FAIL** | a second Store() became a WRITER while the owner held the worker lock; Store() itself is not ownership-aware,  |
| 29 | F-02 | `verifier_binds_database_identity` | MEDIUM | **FAIL** | verifier report does not bind the verified database bytes (no sha256 44e9b382070d...); findings cannot be attr |
| 30 | F-03 | `signing_scan_fails_closed` | MEDIUM | **FAIL** | exit=0 errors=[] - scan silently empty when cwd has no lab/ |
| 31 | F-04 | `hold_history_is_append_only` | MEDIUM | **FAIL** | hold history overwritten: final visible reasons={'gap B'} |
| 32 | F-05 | `hold_release_is_attributable` | MEDIUM | **FAIL** | no hold-release mechanism or release record exists in code or schema |

**All 32 currently FAIL.** That is the required state before any fix. A future green run is meaningful only
because these same tests are known red today.

## Gate state (authoritative — see `MCD-04.md` §1)

| Gate | State |
|---|---|
| Phase 0 — independent review satisfied | **NOT SATISFIED** |
| Phase 1A / G1 … G5 implementation | **NOT AUTHORISED** (owner decision D-5 is explicit) |
| Red-phase suite | **ADOPTED, PROVISIONAL** (D-4) — subject to independent review |
| External review | **MANDATORY, OUTSTANDING** (D-3) — GOV-02 BLOCKED |
| A14-08 numeric-collision claim | **WITHDRAWN**; corrected finding accepted (D-2) |
| Paper-only, snapshot, databases | **PRESERVED, unchanged** (D-6) |

## The 11 blockers

| # | Blocker | Class | Clears when |
|---|---|---|---|
| 1 | **GOV-01 / TD-01** directive §2 truncated | governance | owner re-sends full safety list |
| 2 | **GOV-02** no genuinely external reviewer | governance | reviewer engaged and signed (`MCD-05` §4) |
| 3 | No authorisation of a bounded scope | governance | owner grants after §1–2 clear |
| 4 | **GOV-08** plan revisions R1–R10 not dispositioned | process | owner/implementer disposition |
| 5 | **H01** no authoritative source checkpoint | evidence | upstream/provider capability proof |
| 6 | **H02** no canonical identity/finality | evidence | real chain identity evidence |
| 7 | **H03** no real decoder evidence | evidence | version-specific operation data |
| 8 | **H04** no historical gap reconstruction | evidence | history that does not currently exist |
| 9 | **H05** no forward / calibration / performance evidence | evidence | approved wallets + time |
| 10 | Runtime DB state unverified (excluded by design) | evidence | separate explicit approval |
| 11 | Cross-version reproducibility unpinned | technical | pin versions + parity evidence |

Blockers 5–9 mean CopyLab **cannot currently demonstrate it would copy a real wallet correctly even if every
A14 defect were fixed.** Fixing A14 improves the instruments; it does not supply the measurements.

## Package contents

```
MCD-01.md                          coordination dossier (plan, blockers, sequence)
MCD-02.md                          32 criteria, individually specified
MCD-03.md                          A14-08 correction record + reproducible evidence
MCD-04.md                          owner decisions, TD-01, gate state, open items
MCD-05.md                          external review package + signature block
README.md                          this file
tools/acceptance_suite.py          the 32 executable criteria
tools/REPRODUCE.md                 exact reproduction commands + isolation
tools/package.json                 jsdom dependency for the A14-09 probe only
evidence/red-phase-results.json    32/32 FAIL, per-case detail
evidence/probes/                   49-case probe corpus (5 files)
evidence/results/                  probe outputs, hashed
evidence/ARTEFACT_MANIFEST.json    hashes of this package
```

**Not present, by design:** runtime databases, `.git`, wallet addresses, chain identifiers, real market data,
synthetic data dressed as real. `node_modules` is git-ignored (`.gitignore` at repo root).

## Next objective (owner D-7)

Obtain a genuinely external review; establish whether Phase 0 can be satisfied. **Do not mark it complete
prematurely.** The package is ready in `MCD-05.md`; the gate is not.
