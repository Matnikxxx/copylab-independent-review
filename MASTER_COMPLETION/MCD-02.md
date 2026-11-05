# MCD-02 — The 35 acceptance criteria, individually specified

**Document ID:** `MCD-02` · **Parent:** `MCD-01.md` · **Status:** proposed acceptance baseline, **provisional**
**Adopted:** 2026-11-05 by owner decision **D-4**, "provisionally … subject to independent review".
**Revised:** 2026-11-05 by **D-9** — R4 and R5 amended; criteria **32 → 35** (see `MCD-06.md`).
**Snapshot:** HEAD `288a69f64c24438cfe69ea176e6f3d6ce7333499` · archive `f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23`
**Machine-readable source of truth:** `evidence/red-phase-results.json`
**Executable definition:** `tools/acceptance_suite.py`
**Group numbering:** resolves through `MCD-07.md` (authoritative cross-reference).

## How to read this document

Each criterion states five things and is falsifiable without reference to my opinion:

| Field | Meaning |
|---|---|
| **Intended failure reason** | the *mechanism* in the current code that makes the invariant fail — the thing remediation must change |
| **Pre-fix result** | what the suite actually observed on the frozen snapshot (reproducible per `tools/REPRODUCE.md`) |
| **Post-fix acceptance condition** | what "green" must mean, stated so it cannot be satisfied by weakening the test |
| **Regression guard** | what must *stay* true, so a fix cannot trade one defect for another |
| **Group** | owning group, with the project plan group in parentheses (see `MCD-07`) |

**Provisional status is load-bearing.** These criteria encode *my* reading of the desired invariants. An
independent reviewer may rule that a criterion is wrong, too strong, or too weak. Criteria may be
**strengthened** without further approval; **weakening** one requires written rationale in the open items.

**Two criteria were strengthened by owner amendment (D-9):** A14-06 is restated as a positive obligation
covering *every* attempt body **and its metadata**, including a successful HTTP 200 followed by a later
timeout; A14-07 must be enforced *inside `collect()`* for every invocation and resumed batch, independent of
`allowed()` and caller behaviour. Both are now encoded as executable tests — see `MCD-06.md`.

**Current phase: RED.** All 35 fail. That is the expected and required state before any fix.


## Summary

| # | Finding | Test | Severity | Group | Pre-fix |
|---|---|---|---|---|---|
| 1 | A14-01 | `closed_position_cycle_corruption_detected` | MEDIUM | G3 (plan 1C) | **FAIL** |
| 2 | A14-01 | `ledger_cost_delta_corruption_detected` | MEDIUM | G3 (plan 1C) | **FAIL** |
| 3 | A14-01 | `ledger_fee_corruption_detected` | MEDIUM | G3 (plan 1C) | **FAIL** |
| 4 | A14-01 | `ledger_realized_corruption_detected` | HIGH | G3 (plan 1C) | **FAIL** |
| 5 | A14-01 | `snapshot_equity_corruption_detected` | MEDIUM | G3 (plan 1C) | **FAIL** |
| 6 | A14-01 | `verifier_does_not_hardcode_integrity_ok` | MEDIUM | G3 (plan 1C) | **FAIL** |
| 7 | A14-02 | `dangling_event_movement_detected` | HIGH | G2 (plan 1B) | **FAIL** |
| 8 | A14-02 | `extra_leg_on_valid_event_detected` | HIGH | G2 (plan 1B) | **FAIL** |
| 9 | A14-02 | `orphan_effect_detected` | HIGH | G2 (plan 1B) | **FAIL** |
| 10 | A14-02 | `orphan_movement_detected` | HIGH | G2 (plan 1B) | **FAIL** |
| 11 | A14-03 | `nway_split_requires_operation_spec` | HIGH | G4 (plan 1D) | **FAIL** |
| 12 | A14-03 | `single_sided_split_quarantined` | HIGH | G4 (plan 1D) | **FAIL** |
| 13 | A14-03 | `zero_basis_split_quarantined` | HIGH | G4 (plan 1D) | **FAIL** |
| 14 | A14-04 | `negative_cash_redemption_rejected` | MEDIUM | G4 (plan 1D) | **FAIL** |
| 15 | A14-04 | `unproved_out_of_range_redemption_quarantined` | HIGH | G4 (plan 1D) | **FAIL** |
| 16 | A14-05 | `conflict_record_is_append_only` | MEDIUM | G2 (plan 1E) | **FAIL** |
| 17 | A14-05 | `conflicting_payload_retained` | MEDIUM | G2 (plan 1E) | **FAIL** |
| 18 | A14-06 | `all_failed_attempt_bodies_retained` | MEDIUM | G2 (plan 1F) | **FAIL** |
| 19 | A14-06 | `attempt_order_and_metadata_distinguishable` | MEDIUM | G2 (plan 1F) | **FAIL** |
| 20 | A14-06 | `attempt_without_last_raw_is_durable` | MEDIUM | G2 (plan 1F) | **FAIL** |
| 21 | A14-06 | `successful_body_survives_later_failure` | MEDIUM | G2 (plan 1F) | **FAIL** |
| 22 | A14-07 | `collect_enforces_scope_without_allowed` | MEDIUM | G2 (plan 1G) | **FAIL** |
| 23 | A14-07 | `frontier_not_published_for_wrong_scope` | MEDIUM | G2 (plan 1G) | **FAIL** |
| 24 | A14-07 | `scope_identity_persisted_per_batch` | MEDIUM | G2 (plan 1G) | **FAIL** |
| 25 | A14-07 | `scope_substitution_rejected` | MEDIUM | G2 (plan 1G) | **FAIL** |
| 26 | A14-08 | `digest_distinguishes_blob_from_its_repr_text` | LOW | G1 (plan 1A) | **FAIL** |
| 27 | A14-08 | `digest_distinguishes_blob_from_text` | LOW | G1 (plan 1A) | **FAIL** |
| 28 | A14-09 | `stale_health_not_green` | MEDIUM | G5 (plan 1H) | **FAIL** |
| 29 | A14-10 | `backup_requires_ownership` | LOW | G1 (plan 1A) | **FAIL** |
| 30 | A14-10 | `lock_identity_is_canonical` | MEDIUM | G1 (plan 1A) | **FAIL** |
| 31 | A14-10 | `store_requires_ownership_before_write` | MEDIUM | G1 (plan 1A) | **FAIL** |
| 32 | F-02 | `verifier_binds_database_identity` | MEDIUM | G3 (plan 1C) | **FAIL** |
| 33 | F-03 | `signing_scan_fails_closed` | MEDIUM | G1 fix / G3 verify | **FAIL** |
| 34 | F-04 | `hold_history_is_append_only` | MEDIUM | G2 (R3 merge) | **FAIL** |
| 35 | F-05 | `hold_release_is_attributable` | MEDIUM | G2 (R3 merge) | **FAIL** |

**Total 35** · HIGH 9 · MEDIUM 23 · LOW 3 · all currently `FAIL` · phase `RED`

**Amended by D-9 (R4/R5):** #18, #21 strengthened; #19, #22, #24 **new**. 
**Unchanged, ACCEPT dispositions:** #26/#27 (R6), #1/#5 (R7), #11/#13/#14 (R8), #29 (R9), #16/#17/#31 (R3), #30 (R2/R1 protocol).

---


## A14-01

### 1. `closed_position_cycle_corruption_detected` — MEDIUM

- **Invariant demanded:** A tampered closed_positions.proceeds must be detected
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** closed_positions.proceeds/realized drive win_rate and cycle reporting but are outside the replay scope.
- **Pre-fix result:** `FAIL` — observed: verifier exit=0 errors=[] (closed cycle unverified)
- **Post-fix acceptance condition:** Every closed-position cycle reconciled (cost, proceeds, realized) against the fill sequence.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 2. `ledger_cost_delta_corruption_detected` — MEDIUM

- **Invariant demanded:** A tampered ledger.cost_delta must be detected
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** ledger.cost_delta is not read by the replay at all; positions are reconstructed from fills only, so a corrupted cost basis is invisible.
- **Pre-fix result:** `FAIL` — observed: verifier exit=0 errors=[]
- **Post-fix acceptance condition:** ledger.cost_delta reconciled bidirectionally against independently derived basis.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 3. `ledger_fee_corruption_detected` — MEDIUM

- **Invariant demanded:** A tampered ledger.fee must be detected against fills.fee
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** ledger.fee is read by Accounting.metrics (reported as fees) but no verifier compares it with fills.fee.
- **Pre-fix result:** `FAIL` — observed: verifier exit=0 errors=[] (fee not reconciled)
- **Post-fix acceptance condition:** ledger.fee reconciled per fill against fills.fee; mismatch reported by row id.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 4. `ledger_realized_corruption_detected` — HIGH

- **Invariant demanded:** A tampered ledger.realized must make the verifier exit non-zero
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** tools/audit.py replays fills and checks ledger.cash_delta plus fills.realized, but never reconciles ledger.realized. lab/accounting.py:22 sums ledger.realized directly, so the app and the verifier can disagree without bound.
- **Pre-fix result:** `FAIL` — observed: verifier exit=0 errors=[] while total_pnl=999.00000000
- **Post-fix acceptance condition:** Verifier exits non-zero naming the exact ledger row id and field, AND a pristine ledger still passes (no false positive).
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 5. `snapshot_equity_corruption_detected` — MEDIUM

- **Invariant demanded:** A tampered snapshots.equity must be detected or the curve marked unverified
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** snapshots.equity and snapshots.metrics feed peak_equity and maximum_drawdown but are never verified or marked unverified.
- **Pre-fix result:** `FAIL` — observed: verifier exit=0 errors=[] (equity curve unverified)
- **Post-fix acceptance condition:** Snapshot equity recomputed from time-appropriate marks, or explicitly flagged UNVERIFIED; tamper detected.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 6. `verifier_does_not_hardcode_integrity_ok` — MEDIUM

- **Invariant demanded:** An empty database must not be reported as 10 verified portfolios
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** audit.py writes portfolios_checked=10 and integrity='ok' as literals; an empty database still reports success.
- **Pre-fix result:** `FAIL` — observed: hardcoded portfolios_checked=10 on an empty DB
- **Post-fix acceptance condition:** Fields are measured, not literal; an empty DB reports zero portfolios and is distinguishable from a verified one.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-02

### 7. `dangling_event_movement_detected` — HIGH

- **Invariant demanded:** A movement referencing a nonexistent event must be reported
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Same root cause: traversal starts from events, so a movement pointing at a nonexistent event id is never visited.
- **Pre-fix result:** `FAIL` — observed: errors=[] (dangling FK invisible; schema has no FK)
- **Post-fix acceptance condition:** Dangling reference reported by row id; absence of FKs is compensated by explicit referential checks.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1B) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 8. `extra_leg_on_valid_event_detected` — HIGH

- **Invariant demanded:** A movement whose leg is absent from its event payload must be reported
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** The verifier checks rows it finds by expected leg identity; surplus stored movements on a valid event are never enumerated.
- **Pre-fix result:** `FAIL` — observed: errors=[] (extra leg invisible)
- **Post-fix acceptance condition:** Expected-versus-stored leg sets compared both ways; surplus leg reported.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1B) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 9. `orphan_effect_detected` — HIGH

- **Invariant demanded:** A source_effects row pointing at a nonexistent event must be reported
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** source_effects is never enumerated independently; only payload-declared effects are checked for duplicates.
- **Pre-fix result:** `FAIL` — observed: errors=[] (orphan effect invisible)
- **Post-fix acceptance condition:** All source_effects rows verified for parent existence and single-use.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1B) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 10. `orphan_movement_detected` — HIGH

- **Invariant demanded:** A movement with no reachable event must be reported by row identity
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** tools/source_verify.py iterates verified_events and walks forward to movements. Rows with no reachable event are structurally invisible; the schema declares no foreign keys.
- **Pre-fix result:** `FAIL` — observed: errors=[] source_cash=0 (orphan invisible)
- **Post-fix acceptance condition:** Every source_movements row accounted for exactly once; orphan reported with row id and reason.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1B) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-03

### 11. `nway_split_requires_operation_spec` — HIGH

- **Invariant demanded:** A 3-way fan-out with no condition/outcome mapping must be quarantined
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** No condition id, outcome set, collateral or denominator is required; an arbitrary n-way fan-out is accepted as a split.
- **Pre-fix result:** `FAIL` — observed: unspecified 3-way split state=applied
- **Post-fix acceptance condition:** Operation-specific outcome set and collateral required; unspecified fan-out quarantined.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G4 (plan 1D) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 12. `single_sided_split_quarantined` — HIGH

- **Invariant demanded:** A split with no complementary outcome must be quarantined, not applied
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** lab/integrity.py:161-199 only asserts all deltas>0 and sum(cash)==-sum(cost_delta). One positive leg with balanced paid basis satisfies both.
- **Pre-fix result:** `FAIL` — observed: single-sided split state=applied
- **Post-fix acceptance condition:** A split without a complementary outcome mapping is quarantined with zero partial journal effects.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G4 (plan 1D) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 13. `zero_basis_split_quarantined` — HIGH

- **Invariant demanded:** A split consuming no paid basis must be quarantined (cannot mint inventory)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** The paid-basis identity is trivially satisfied when both sides are zero, so a split can mint inventory from nothing.
- **Pre-fix result:** `FAIL` — observed: zero-basis split state=applied; 0 == 0 satisfies the paid-basis identity
- **Post-fix acceptance condition:** Non-zero paid basis required; zero-basis split quarantined.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G4 (plan 1D) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-04

### 14. `negative_cash_redemption_rejected` — MEDIUM

- **Invariant demanded:** A redemption leg paying negative cash must not be applied as a payout
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** A negative cash leg is accepted on REDEEM because only the delta sign is checked, not the cash direction.
- **Pre-fix result:** `FAIL` — observed: negative-cash redemption state=applied
- **Post-fix acceptance condition:** Negative-cash redemption rejected as an invalid payout.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G4 (plan 1D) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 15. `unproved_out_of_range_redemption_quarantined` — HIGH

- **Invariant demanded:** A payout above one unit per share with no proof must be quarantined
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** The burn/debit check confirms a negative delta but never bounds payout per share or requires resolution/finality evidence.
- **Pre-fix result:** `FAIL` — observed: unproved redemption state=applied
- **Post-fix acceptance condition:** Payout numerator/denominator and finality required; per-share payout above the ceiling quarantined.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G4 (plan 1D) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-05

### 16. `conflict_record_is_append_only` — MEDIUM

- **Invariant demanded:** A conflict must leave an immutable record; state flip alone is insufficient
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** verified_events is a mutable single row, so the first payload is overwritten and no conflict evidence table exists.
- **Pre-fix result:** `FAIL` — observed: no append-only conflict evidence: the conflicting payload is absent from every non-state table (34 checked); only mutable state/review rows exist
- **Post-fix acceptance condition:** An append-only conflict record exists; both raw payloads immutable; no silent winner.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1E) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 17. `conflicting_payload_retained` — MEDIUM

- **Invariant demanded:** A conflicting certificate payload must be durably retrievable after the conflict
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** The conflict branch at integrity.py:127-143 flips verified_events.state and writes a hold; it never stores the new payload, kind or provenance.
- **Pre-fix result:** `FAIL` — observed: conflicting payload not retained in any of 36 tables
- **Post-fix acceptance condition:** Raw original and raw conflicting payloads both durably retrievable with provenance.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1E) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-06

### 18. `all_failed_attempt_bodies_retained` — MEDIUM

- **Invariant demanded:** Every received attempt body AND its metadata must be durable after total failure (R4 AMENDED)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** The success path flushes attempt_log[:-1], but the exception path persists only last_raw, discarding earlier received bodies.
- **Pre-fix result:** `FAIL` — observed: 1 durable rows for 3 received attempts: ['body-3']
- **Post-fix acceptance condition:** Every received attempt body durable on every exit path; batch remains incomplete.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1F) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 19. `attempt_order_and_metadata_distinguishable` — MEDIUM

- **Invariant demanded:** Concurrent same-body attempts must remain individually distinguishable with metadata (R4 AMENDED)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Attempts are identified by nothing at all in the schema (transport_deliveries has no attempt ordinal) and the exception path writes only last_raw, so three received attempts collapse to one row. Added by R4 AMEND: 'every relevant attempt body' implies attempt identity, not body identity.
- **Pre-fix result:** `FAIL` — observed: 1 rows for 3 attempts with identical bodies (attempt identity lost)
- **Post-fix acceptance condition:** Three attempts with identical body text and distinct HTTP codes persist as three distinguishable rows, each carrying its own code/error/receipt time; de-duplicating identical bodies fails. (Requires additive attempt-identity column.)
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1F) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 20. `attempt_without_last_raw_is_durable` — MEDIUM

- **Invariant demanded:** An attempt log with no last_raw (pre-response failure) must still be durable
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** If get() raises before assigning last_raw, the exception path persists nothing at all; only the batch error survives.
- **Pre-fix result:** `FAIL` — observed: durable bodies=[]; nothing persisted at all
- **Post-fix acceptance condition:** Attempt-level durability written before get() returns; UNKNOWN is recorded rather than nothing.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1F) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 21. `successful_body_survives_later_failure` — MEDIUM

- **Invariant demanded:** An HTTP 200 body received before a later timeout must survive WITH its success metadata (R4 AMENDED)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Same root cause, worse consequence: a successful 200 body received before a later timeout is destroyed.
- **Pre-fix result:** `FAIL` — observed: successful body destroyed; durable=['bad-504']
- **Post-fix acceptance condition:** No received body is ever lost, including successful ones preceding a failure.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1F) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-07

### 22. `collect_enforces_scope_without_allowed` — MEDIUM

- **Invariant demanded:** collect() itself must reject/isolate a scope mismatch, independent of allowed() or callers (R5 AMENDED)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** collect() looks up pending batches by wallet+endpoint and adopts stored params. Safety currently rests on Integrity.allowed() returning False for production and on callers such as Collector.baseline — a defence-in-depth inversion. Added by R5 AMEND: the invariant must hold with no contribution from allowed() or caller behaviour.
- **Pre-fix result:** `FAIL` — observed: scope mismatch neither rejected nor forked: reused pending batch, sent status='CLOSED' for a requested OPEN scope
- **Post-fix acceptance condition:** collect() itself rejects or forks on scope mismatch, provable with allowed() never consulted and no caller-side check. A fix that only works while allowed() is globally false cannot pass.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1G) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 23. `frontier_not_published_for_wrong_scope` — MEDIUM

- **Invariant demanded:** A completed walk must not be published as the requested scope's frontier
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** capture_frontiers is keyed wallet+endpoint, so a completed CLOSED walk is published as the OPEN evidence frontier.
- **Pre-fix result:** `FAIL` — observed: frontier published for a CLOSED walk under an OPEN request: [{'wallet': 'fixture-wallet', 'endpoint': '/v2/positions', 'batch': 1, 'captured_at': 1793885135.9850898, 'coverage': 'captured pages only; late inserts and source completeness unproven'}]
- **Post-fix acceptance condition:** Frontier bound to a scope hash; never published for a different requested scope.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1G) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 24. `scope_identity_persisted_per_batch` — MEDIUM

- **Invariant demanded:** Each batch must persist an explicit scope identity so resume validity never depends on wallet+endpoint (R5 AMENDED)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** collection_batches has no scope-identity column (id, wallet, endpoint, params, started, finished, status, next_cursor, page_number, error, coverage), so 'which scope is this batch' does not exist in the schema and resume validity rests on wallet+endpoint alone. Added by R5 AMEND to attack the root cause rather than the symptom.
- **Pre-fix result:** `FAIL` — observed: collection_batches has no explicit scope-identity column (columns=['id', 'wallet', 'endpoint', 'params', 'started', 'finished', 'status', 'next_cursor', 'page_number', 'error', 'coverage']); resume validity rests on wallet+endpoint alone
- **Post-fix acceptance condition:** An explicit, populated scope-identity field exists on collection_batches and is the basis of resume validity. Adding a hash while still looking up by wallet+endpoint must fail this criterion.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1G) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 25. `scope_substitution_rejected` — MEDIUM

- **Invariant demanded:** A pending CLOSED walk must not be sent as the caller's OPEN request
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** collect() looks up pending batches by wallet+endpoint only and adopts the stored params, silently discarding the caller requested scope.
- **Pre-fix result:** `FAIL` — observed: OPEN request was sent as status=CLOSED
- **Post-fix acceptance condition:** Scope identity includes all filters/window/params; mismatch rejects or forks a new batch.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (plan 1G) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-08

### 26. `digest_distinguishes_blob_from_its_repr_text` — LOW

- **Invariant demanded:** A BLOB and the TEXT of its own Python repr must not collide through default=str
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Same root cause tested on a no-affinity column, where SQLite provably preserves distinct storage types, removing any affinity artefact.
- **Pre-fix result:** `FAIL` — observed: collision: blob and text share digest fe21b3a17c7cc0eb (default=str renders bytes as the text b"..." )
- **Post-fix acceptance condition:** BLOB and the TEXT of its repr hash differently; golden vectors published.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G1 (plan 1A) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 27. `digest_distinguishes_blob_from_text` — LOW

- **Invariant demanded:** BLOB b"A" and TEXT "b'A'" must produce different digests (default=str collision)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** migrations.table_digests encodes cells with json.dumps(default=str), rendering bytes b'A' as the text "b'A'"; the TEXT row hashes identically.
- **Pre-fix result:** `FAIL` — observed: collision: blob and text(text) share digest fe21b3a17c7cc0eb
- **Post-fix acceptance condition:** Typed length-framed encoding distinguishes every genuine stored-type pair at every affinity.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G1 (plan 1A) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-09

### 28. `stale_health_not_green` — MEDIUM

- **Invariant demanded:** A ts=0 ok=1 health row must not render as Healthy
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** dashboard.html renders h.ok?'Healthy':'Attention' and displays ts without ever comparing it to now; a ts=0 row is green forever.
- **Pre-fix result:** `FAIL` — observed: stale ts=0 row rendered as 'Healthy'
- **Post-fix acceptance condition:** Health has TTL/staleness semantics; an old row cannot render Healthy.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G5 (plan 1H) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## A14-10

### 29. `backup_requires_ownership` — LOW

- **Invariant demanded:** A backup must not proceed while another process holds writer ownership
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Store.backup() performs no ownership check, and main()'s backup branch returns before the flock is taken.
- **Pre-fix result:** `FAIL` — observed: backup succeeded while another owner held the worker lock
- **Post-fix acceptance condition:** Backup requires the maintenance ownership mode.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G1 (plan 1A) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 30. `lock_identity_is_canonical` — MEDIUM

- **Invariant demanded:** A DB reached via symlink must use the same worker lock as the real path
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Every entry point opens str(db)+'.worker.lock'. A symlinked DB path yields a different lock file, so two processes lock different inodes and both become owners.
- **Pre-fix result:** `FAIL` — observed: symlinked path acquired a SECOND exclusive lock: two owners possible
- **Post-fix acceptance condition:** Lock identity derived from realpath of the DB; aliases resolve to one lock.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G1 (plan 1A) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

### 31. `store_requires_ownership_before_write` — MEDIUM

- **Invariant demanded:** While another owner holds the worker lock, a second Store must refuse or be read-only
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** Store.__init__ never consults the worker lock; only main()/configure.py/upgrade_existing do. A library caller silently becomes a second writer.
- **Pre-fix result:** `FAIL` — observed: a second Store() became a WRITER while the owner held the worker lock; Store() itself is not ownership-aware, so safety depends on every caller remembering to flock
- **Post-fix acceptance condition:** Store is mode-aware: refuses or is read-only without ownership.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G1 (plan 1A) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## F-02

### 32. `verifier_binds_database_identity` — MEDIUM

- **Invariant demanded:** The verifier report must identify the database it verified (hash)
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** audit.py reports only the database path; nothing binds the report to the verified bytes, so findings cannot be attributed to a snapshot.
- **Pre-fix result:** `FAIL` — observed: verifier report does not bind the verified database bytes (no sha256 44e9b382070d...); findings cannot be attributed to a snapshot
- **Post-fix acceptance condition:** Report embeds the SHA-256 of the verified database and the source snapshot id.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G3 (plan 1C) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## F-03

### 33. `signing_scan_fails_closed` — MEDIUM

- **Invariant demanded:** If the signing-code scan finds no source files it must error, not silently pass
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** audit.py builds its signing-code scan from Path('lab').glob relative to CWD; run elsewhere the glob is empty, the scan finds nothing, and the report still exits 0.
- **Pre-fix result:** `FAIL` — observed: exit=0 errors=[] - scan silently empty when cwd has no lab/
- **Post-fix acceptance condition:** Scan resolves paths from the module and errors if its target set is empty.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G1 fix / G3 verify · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## F-04

### 34. `hold_history_is_append_only` — MEDIUM

- **Invariant demanded:** Two successive holds must leave both reasons retrievable
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** integrity.py:25 uses INSERT OR REPLACE keyed on (model,track,wallet,token), so a second hold overwrites the first reason and reconciliation id.
- **Pre-fix result:** `FAIL` — observed: hold history overwritten: final visible reasons={'gap B'}
- **Post-fix acceptance condition:** Holds are append-only events; both reasons retrievable; release recorded separately.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (R3 merge) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)


## F-05

### 35. `hold_release_is_attributable` — MEDIUM

- **Invariant demanded:** There must be a release path that records who released and on what evidence
- **What the test does:** drives the shipped code with a disposable symbolic fixture and asserts the invariant above. No application, worker, server, network or runtime database.
- **Intended failure reason (root cause):** paper_holds rows are only ever inserted. No release path exists in code or schema; clearing a hold requires direct SQL.
- **Pre-fix result:** `FAIL` — observed: no hold-release mechanism or release record exists in code or schema
- **Post-fix acceptance condition:** Attributable release record with actor, evidence and timestamp; re-enable requires it.
- **Regression guard:** the whole suite must remain green, no assertion may be relaxed, and a pristine fixture must still pass (no false positive introduced).
- **Group:** G2 (R3 merge) · **Provenance:** reproduced by `INDEP-AUDIT-01` (probe case in `evidence/probes/`)

---

## Suite self-validation (why these 35 can be trusted at all)

A red suite that has never been validated is worthless, and a test that passes pre-fix is a defect in the test.
Five were found and fixed during construction (`MCD-01` §5.3). The D-9 amendments were validated the same way:
after strengthening #18/#21 and adding #19/#22/#24, the red phase was **re-run and all 35 fail** — confirming
the new criteria genuinely detect the current behaviour rather than passing on a technicality.

| # | Self-defect | Consequence if shipped | Resolution |
|---|---|---|---|
| 1 | helper bound a `sqlite3.Cursor` instead of `.lastrowid` | 4 tests ERROR instead of measuring | fixed |
| 2 | F-02 accepted the `database` **path echo** as identity binding | **false green** | now demands actual SHA-256 of the bytes |
| 3 | F-04 unioned an earlier and a later sample | **false green** — hid the overwrite it tests | now samples final state only |
| 4 | A14-10 asserted "DB bytes unchanged"; a second `Store()` on a migrated DB writes nothing yet still becomes a writer | **false green** | now asserts refuse-or-read-only |
| 5 | A14-08 numeric-collision claim contradicted by re-measurement | report overstated the finding | finding corrected (`MCD-03`) |
| 6 | A14-09 probe silently reported FAIL when its Node dependency was missing | **false red** (wrong reason) — caught during the D-9 re-run | it now errors loudly; dependency restored and re-measured |

Three of the six were **false greens**, one a **false red**. Both directions are failures and both were found by
re-running rather than by reading.

## Conditions the owner attached to provisional adoption

| Owner condition | Satisfied by |
|---|---|
| Must remain subject to independent review | this header; "Provisional status is load-bearing"; GOV-02 |
| Every test has a documented intended failure reason | the 35 blocks above |
| Every test has a reproducible pre-fix result | `evidence/red-phase-results.json` + `tools/REPRODUCE.md` |
| Every test has a corresponding post-fix acceptance condition | the 35 blocks above |
| (D-9) R4: every attempt body **and metadata**, incl. 200-then-timeout | #18, #19, #21 |
| (D-9) R5: scope correctness **inside `collect()`**, not `allowed()`/callers | #22, #24 |

## Limits of this baseline (stated, not hidden)

1. It tests **local** properties only. It says nothing about H01–H05, which cannot be closed locally.
2. It is **author-written**. `INDEP-AUDIT-01` §2 applies: same harness as the implementation agent.
3. Passing all 35 means the *instruments* are correct — not that CopyLab would copy a real wallet correctly.
4. It cannot detect defects no one has thought of. A reviewer should be asked to add cases, not merely check mine.
5. A14-08 remains **LOW**; numeric-collision claim withdrawn (`MCD-03`).
6. #19, #22 and #24 require **additive schema changes** to satisfy (attempt identity; scope identity). No
   runtime migration is authorised; they are disposable-file changes only (`INV-04`).
