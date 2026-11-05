# CopyLab — Master Completion Directive: Consolidated Execution Dossier

**Document ID:** `MCD-01`
**Issued:** 2026-11-05
**Supersedes (as *coordination spine* only):** nothing. This document coordinates; it does not overwrite
`MASTER_REMEDIATION_PLAN.md` or `MASTER_DEFECT_REGISTER.md`, which remain the project's own planning
artefacts and are treated here as **inputs to be revised**, not replaced.
**Audit basis:** `INDEP-AUDIT-01` (this repository)
**Snapshot:** HEAD `288a69f64c24438cfe69ea176e6f3d6ce7333499` / archive
`f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23` (re-verified, pristine)

> **OWNER DECISIONS APPLIED 2026-11-05** — see `MCD-04.md` for the authoritative ledger.
> D-1 TD-01 transmission record (no relaxation) · D-2 A14-08 correction accepted → `MCD-03.md`
> D-3 external review mandatory · D-4 red-phase suite **adopted provisionally** → `MCD-02.md`
> **D-5 G1 explicitly NOT AUTHORISED** · D-6 preservation standing · D-7 Phase 0 must not be marked complete
> D-8 single coordinated programme authorisation defined in `MCD-04` §7
> **D-9 R1–R10 dispositioned** (8 ACCEPT, 2 AMEND) → `MCD-06.md`; criteria **32 → 35**
> **D-10 G1–G5 remain NOT AUTHORISED** (reaffirmed)
> **D-11 group cross-reference** 1A–1H ↔ G1–G6 → `MCD-07.md` (authoritative)
> **D-12 consolidated review-prep stage** → `MCD-08` (safety set, GOV-01 closed) · `MCD-09` (G2 schema design,
> GOV-09 closed) · `MCD-10` (version pinning) · `MCD-11` (reviewer checklist) · `CONSISTENCY_CHECK.md`
> Gate state unchanged: **Phase 0 NOT SATISFIED · Phase 1A NOT AUTHORISED.**

---

## 0. Read this before anything else

### 0.1 Your directive arrived truncated

The directive ended mid-sentence at:

> "CopyLab must remain strictly paper-only. - No live trading,"

**Sections 3 onward of your safety list never arrived.** You have since confirmed the original directive
contained the complete requirements, so this is recorded as a **transmission discrepancy, TD-01**
(`MCD-04.md` §3), not a content dispute. I have not guessed at the missing bullets, not reconstructed them
from memory, and not treated their absence as permission. I have applied the **strictest reading available**,
derived from sources that are already binding on this project and that I actually hold:

1. the archive's own transfer instructions (`copylab-external-review-INSTRUCTIONS.md`);
2. Audit 14's method restrictions (`docs/phase0-audit14/AUDIT_14.md`);
3. `INDEP-AUDIT-01` §3 (my own isolation envelope).

**Every one of those is more restrictive than "paper-only" alone**, so the truncation cannot have widened
my authority. If your missing bullets were *permissive* in any respect, they are not honoured — but no
permissive bullet can be consistent with a snapshot whose own gate is "Phase 0 BLOCKED". `MCD-04` §4 shows
that all eleven operative invariants (`INV-01`…`INV-11`) trace to a source in my possession, so the
truncation reduces the *completeness* of the safety list, not the *strength* of what is enforced. **GOV-01
stays BLOCKED** until the full text is supplied; any invariant it reveals will be reconciled upward only.

### 0.2 What I did and did not do in this run

| Permitted preparation (done) | Forbidden (not done) |
|---|---|
| Re-established exact repo/evidence state | No fix to any audited defect |
| Reconciled INDEP-AUDIT-01 ↔ master plan ↔ register | No modification of the snapshot's 150 project files |
| Produced one consolidated remediation plan (§4) | No application, worker, server or collector start |
| Testable acceptance criteria per finding (§5) | No runtime database opened, migrated or backed up |
| Built the red→green harness and ran the **red** phase (§5.3) | No wallet query, no trade, no signing, no network |
| Prepared the external-review package (§8) | No Phase 1A commencement |
| Enumerated every blocker (§9) | No claim that Phase 0 is satisfied |

### 0.3 The one-line status

> **Phase 0: NOT SATISFIED. Phase 1A: NOT AUTHORISED. Blocking item count: 10 (§9).**
> Everything that *can* be prepared without approval has now been prepared. Nothing that *requires*
> approval has been done.

### 0.4 A correction to my own audit report

While building the red-phase suite I found an error **in `INDEP-AUDIT-01` §6 (A14-08)** and am correcting it
here rather than quietly leaving it. I claimed:

> "`int 1 == text "1" == real 1.0` collide under NUMERIC affinity."

That is **wrong as stated**. Under `NUMERIC` affinity, `'1'` and `1.0` are *coerced by SQLite to INTEGER 1*,
so no type difference survives to be lost — the digest is not at fault. My observation table
(`observed typeof integer vs integer`) in fact recorded this correctly; my prose over-claimed. The genuine
finding, re-verified with no-affinity columns, is narrower and still real:

- **CONFIRMED collision:** BLOB `b'A'` vs TEXT `"b'A'"` (and BLOB `b'1'` vs TEXT `"b'1'"`) — all affinities.
  Root cause is `json.dumps(..., default=str)` rendering bytes as the text `b'...'`.
- **NOT a collision:** integer vs text numerals where affinity coerces them to one storage class.
- **NOT a collision:** NULL vs empty text, embedded NUL, duplicates, row order (all behave correctly).

Severity stays **LOW** for migration use. The correction changes the *scope* of the finding, not its
existence: `INDEP-AUDIT-01`'s "broader than reported" claim is **withdrawn for numerics and retained only for
the BLOB-repr family**. A14-08 §5 criteria below reflect the corrected scope. This is exactly the class of
error a red-phase harness is supposed to catch, which is §5.3's justification.

---

## 1. Exact current state

### 1.1 Repository (this checkout, branch `arena/3e2065ef-copylab-independent-review`)

| Path | Role | Status |
|---|---|---|
| `copylab-external-review (1).zip` | the audited artefact | **byte-identical**, SHA-256 verified twice (pre/post) |
| `copylab-external-review-SHA256.txt` | detached checksums | unchanged |
| `copylab-external-review-INSTRUCTIONS.md` | transfer instructions | unchanged |
| `AUDIT_REPORT_INDEP-AUDIT-01.md` | independent audit (49 probe cases) | unchanged; **one correction at §0.4 above** |
| `MASTER_COMPLETION/` | **this run's output** | new |

**No project source was added to version control.** The CopyLab source remains sealed inside the ZIP. This is
deliberate: creating a mutable source tree here would invite exactly the "implicit fix" the gate forbids.

### 1.2 Evidence state

| Check | Result |
|---|---|
| Archive SHA-256 | `f1943…b11c23` ✓ |
| Snapshot manifest re-verification | **156/156 files, 0 mismatches** (pristine, before and after this run) |
| `runC`/`runD` working copies | disposable, `lab/` byte-identical to snapshot |
| Probe corpus | 49 cases across 4 result files, all hashed (§5.3) |

### 1.3 What "Phase 0 NOT SATISFIED" actually rests on

It is **not** that planning is missing — planning now exists in abundance. It rests on two things only:

1. **No genuinely separate reviewer.** `INDEP-AUDIT-01` §2 is explicit that I run in the same harness that
   produced Audit 14. Master plan §4/§8-1 forbids substituting an agent, subprocess or restyled report for
   independence. That condition is **still unmet** and cannot be met by anything I produce.
2. **No user authorisation of a bounded scope.** Plan §11 requires explicit approval of *the next bounded
   group* after review. Not granted, correctly not requested by me mid-run.

Everything else that was blocking *my* ability to prepare is now unblocked.

---

## 2. Reconciliation: INDEP-AUDIT-01 ↔ plan ↔ register

Conflict resolution rule applied: **the more restrictive statement wins**, and a disagreement is recorded
rather than silently resolved.

### 2.1 Status reconciliation

| Finding | Audit 14 | Register (Part 18) | INDEP-AUDIT-01 | Consolidated position |
|---|---|---|---|---|
| A14-01 | HIGH, reproduced | OPEN, HIGH, Phase 1C | CONFIRMED, **+2 silent fields** | **CONFIRMED / HIGH / OPEN** — criteria expanded (§5) |
| A14-02 | HIGH, reproduced | OPEN, HIGH, Phase 1B | CONFIRMED, **+2 row classes** | **CONFIRMED / HIGH / OPEN** |
| A14-03 | HIGH synthetic | OPEN, HIGH synthetic, 1D | CONFIRMED, **+zero-basis, +n-way** | **CONFIRMED / HIGH(synthetic) / OPEN** |
| A14-04 | HIGH synthetic | OPEN, HIGH synthetic, 1D | CONFIRMED, **+negative cash** | **CONFIRMED / HIGH(synthetic) / OPEN** |
| A14-05 | MEDIUM | OPEN, MEDIUM, 1E | CONFIRMED across **36 tables** | **CONFIRMED / MEDIUM / OPEN** |
| A14-06 | MEDIUM | OPEN, MEDIUM, 1F | CONFIRMED, **blast radius raised** | **CONFIRMED / MEDIUM / OPEN** — invariant restated (§5) |
| A14-07 | MEDIUM | OPEN, MEDIUM, 1G | CONFIRMED, **frontier corruption** | **CONFIRMED / MEDIUM / OPEN** |
| A14-08 | LOW | OPEN, LOW, 1A | CONFIRMED, **scope corrected ↓** (§0.4) | **CONFIRMED / LOW / OPEN** |
| A14-09 | MEDIUM | OPEN, MEDIUM, 1H | CONFIRMED, other engine | **CONFIRMED / MEDIUM / OPEN** |
| A14-10 | MEDIUM, inspection-only | OPEN, MEDIUM, 1A | **now dynamically reproduced** + aliasing | **CONFIRMED / MEDIUM / OPEN** |
| F-01…F-09 | — | not registered | found by this audit | **NEW — register entries required** |
| H01–H05 | — | BLOCKED, HIGH | agree | **BLOCKED / HIGH — unchanged** |

**No finding was downgraded or closed by this run.** Two were expanded (A14-01, A14-02), one was scope-corrected
downward (A14-08 §0.4), one had its blast radius raised (A14-06).

### 2.2 Plan revisions required before Phase 1A

These are the ten items from `INDEP-AUDIT-01` §8.2, restated as **blocking changes** with owner action.
They are not advisory.

> **DISPOSITIONED 2026-11-05 (D-9) — see `MCD-06.md` for the register.**
> 8 ACCEPT (R1, R2, R3, R6, R7, R8, R9, R10) · 2 AMEND (R4, R5).
> The amendments were applied by **strengthening executable criteria**, not by re-wording prose:
> A14-06 restated as a positive obligation over every attempt body **and its metadata** (incl. a successful
> HTTP 200 followed by a later timeout); A14-07 enforced **inside `collect()`** independent of `allowed()` and
> callers. The suite grew **32 → 35**; the red phase was re-run and **35/35 fail**.

| # | Change | Why it blocks | Where |
|---|---|---|---|
| R1 | Each group must record a **red→green artefact against a frozen pre-fix snapshot** | "tests pass" can be satisfied by tests that cannot detect the defect | §6 of plan |
| R2 | **Demote the 119-test count**; it is invariant under all seven audited corruptions (F-01) | It is currently cited as the primary positive control | §3, §6 gates |
| R3 | **Merge A14-05 and F-04** into one append-only-evidence group | Two migrations to the same area invites schema conflict | §6 1E |
| R4 | Restate **A14-06** as "exception path persists ≤1 body, possibly none" | The all-failed framing under-scopes it | §6 1F |
| R5 | **A14-07 containment is of the instance, not the class**; state the invariant on `collect()` | Phase 2 arms a real adapter and inherits the defect | §6 1G |
| R6 | **1A must add lock canonicalisation + Store-level ownership** | Symlink probe shows two live owners | §6 1A |
| R7 | **1C must add snapshot-equity and closed-position-cycle** reconciliation | Otherwise A14-01 closes with two silent fields open | §6 1C |
| R8 | **1D must add zero-basis and n-way splits, negative-cash redemption** | Current list would leave my sub-cases open | §6 1D |
| R9 | **Add evidence-provenance binding** to every gate artefact (F-02) | Otherwise "reconfirm hashes" cannot be applied to group evidence | §5 protocol |
| R10 | **Move default-deny HTTP verb handling** into 1A (F-06) | One-line hardening; belongs before anything is exposed | §6 1A |

**Assessment of the existing plan: structurally sound, and unusually honest about its own limits — but not yet
an acceptance specification.** R1, R2 and R6 are the three that would let a Phase 1A re-run *look* green
while A14-08/A14-10 remain unfixed.

---

## 3. Non-negotiable invariants (consolidated, strictest reading)

Numbered so later phases can cite them. **Every invariant is enforced by a test or a code review gate** —
none is aspirational.

| ID | Invariant | Enforced by |
|---|---|---|
| INV-01 | **Paper-only, permanently.** `config.paper_only` must be `true`; `validate()` rejects otherwise | existing test; must remain |
| INV-02 | **`Integrity.allowed()` returns `False` for any non-synthetic DB, unconditionally** | SAFE-01; containment re-verified by INDEP-AUDIT-01 |
| INV-03 | **No signing, no key material, no order endpoints.** GET allowlist only | `PublicClient.ALLOWED`; `test_api_rejects_order_endpoint` |
| INV-04 | **No runtime DB mutation** without separate explicit approval and a verified backup | SAFE-02, OPS-03 |
| INV-05 | **No app/worker/server start** during engineering or review | this dossier §0.2 |
| INV-06 | **No wallet query, no real network source call** in tests or review | `sitecustomize` socket block; §5.3 |
| INV-07 | **Synthetic evidence is never presented as chain fact.** Fixtures carry `provenance='synthetic…'` and the verifier must reject non-synthetic provenance | `source_verify` provenance check |
| INV-08 | **Missing ≠ zero.** Unknown inventory, health, coverage must be represented as unknown | `baseline`, `allowed()` |
| INV-09 | **Evidence is additive.** Failures are preserved; no test deleted, no assertion relaxed, no count massaged | Plan §5.7 |
| INV-10 | **Every gate artefact binds to bytes** (DB SHA-256 + snapshot ID) | R9 / F-02 |
| INV-11 | **Findings are append-only in the register.** Status moves forward, rows never disappear | Register §4 |

---

## 4. Consolidated remediation plan

> **Group numbering:** this section defines **G1–G6**. The project's `MASTER_REMEDIATION_PLAN.md` defines
> **1A–1H**. Both schemes remain valid and neither is renumbered; **`MCD-07.md` is the authoritative
> cross-reference.** In one line: G1=1A · G2=1B+1E+1F+1G · G3=1C · G4=1D · G5=1H · G6=no plan equivalent.

Six groups. Each has a **single owner-action**, a **frozen pre-fix snapshot**, a **red set that must exist
before code changes**, and a **stop gate**. No group may begin before the Phase 0 conditions in §9 clear.

### Group ordering rationale

```
G0  Governance            ← cannot be done by me; blocks everything
 └ G1 Foundations          (A14-08 digest, A14-10 ownership)   [no economic surface]
    └ G2 Evidence integrity (A14-02, A14-06, A14-07, A14-05+F-04, F-05)
       └ G3 Accounting proof (A14-01, F-02, F-03)
          └ G4 Semantic proof (A14-03, A14-04)                  [synthetic only]
             └ G5 Truthful UI  (A14-09, F-06)
                └ G6 External evidence (H01–H05)                ← cannot be done locally
```

**Why G1 before G2:** the digest and the lock are the *instruments* G2's evidence depends on. Verifying
evidence with an instrument that conflates storage types (A14-08) or admits two writers (A14-10) is
circular.

**Why G3 after G2:** the paper verifier's authority depends on the source verifier's completeness — a paper
ledger reconciled against a source journal that is itself unverified proves nothing.

**Why G4 last among code groups:** synthetic semantics cannot be validated against anything real, so it must
not hold up groups whose defects have production reach. It is also the group most likely to be *substantially
rewritten* once G6 produces real decoder evidence.

---

### G1 — Foundations: typed digests and single-writer ownership
**Findings:** A14-08 (LOW), A14-10 (MEDIUM), F-06 (LOW), R6, R10
**Files:** `lab/migrations.py` (`table_digests`, `upgrade_existing`), `lab/store.py` (`Store.__init__`,
`backup`), `lab/main.py` (`main`, `App`), `tools/configure.py`, `tools/migrate_source.py`

**Required design decisions (must be written before code):**
1. Typed cell encoding: explicit type tag + length framing; `REAL` as IEEE-754 bits; `TEXT` as UTF-8 with
   explicit handling of embedded NUL; `BLOB` as raw bytes; `NULL` distinct. Golden vectors required.
2. Define whether schema objects (tables/indexes/triggers) are in scope. If claimed, digest them; if not,
   **say so** and stop implying schema preservation.
3. Ownership model with **canonical path identity** (`realpath`, resolving symlinks) for DB **and** lock.
4. Ownership modes: `owner` (read-write, initialising), `reader` (read-only, no schema/PRAGMA writes),
   `maintenance` (backup/migration, exclusive). `Store()` must be mode-aware — not just the CLI.

**Red set (must exist and fail before code):** `acceptance_suite.py` A14-08 ×2, A14-10 ×3.
**Green criteria:** all red cases pass; plus new cases for embedded NUL, large BLOB, empty table, composite
key, `NULL`/empty-text, plus **two-process contention on a symlinked path** and **crash mid-initialise**.
**Acceptance:** no unsafe write observable before ownership is established; loser process performs zero DB
writes; digest distinguishes every genuine stored-type pair.
**STOP GATE G1.**

---

### G2 — Evidence integrity: every received byte durable, every scope immutable
**Plan groups:** 1B + 1E + 1F + 1G (`MCD-07`)
**Findings:** A14-02 (HIGH), A14-06 (MEDIUM, **restated per R4**), A14-07 (MEDIUM, **restated per R5**),
A14-05 (MEDIUM), F-04 (MEDIUM), F-05 (MEDIUM) — **9 criteria**
**Amendments binding on this group (D-9):** A14-06 requires *every relevant attempt body AND its associated
metadata*, including a successful HTTP 200 followed by a later timeout or exception (4 criteria, needs an
additive attempt-identity column). A14-07 requires scope correctness *enforced inside `collect()`* for every
invocation and resumed batch, independent of `allowed()` and caller behaviour (4 criteria, needs an additive
scope-identity column and a changed resume lookup).
**Files:** `lab/integrity.py` (`collect`, exception path, `synthetic_event`, `hold`), `lab/public.py`
(`PublicClient.get`, `Collector.baseline`), `tools/source_verify.py`, schema (additive V4)

**Required design decisions:**
1. **Attempt durability before `get()` returns** — write attempt start, receipt and error as they happen;
   a crash before persistence yields `UNKNOWN`, never a fabricated body (plan §1F).
2. **Scope identity**: scope hash over wallet + endpoint + API version + all filters + window + page params.
   Cursor state is *not* scope. Mismatched resume must **reject or fork**, never substitute.
3. **Frontier semantics**: a frontier belongs to a scope hash and cannot be published for a different one.
4. **Append-only conflict + hold evidence**: raw original, raw conflicting payload, receipt time, source
   identity, digest, reason, resolution status, and an explicit **release record with actor and evidence**.
5. `source_verify` must reconcile **all** rows bidirectionally and report row ID + reason, including
   `source_effects` orphans and cloned rows.

**Red set:** A14-02 ×4, A14-06 ×4, A14-07 ×4, A14-05 ×2, F-04, F-05 = **17 criteria**.
**Green criteria:** all pass; plus wrong-parent, wrong-wallet, duplicate-effect, unbalanced-group,
Retry-After, empty/malformed body, restart-between-attempts, archive→OPEN, and **hold release attributable
and reversible**.
**Acceptance:** no captured byte can be lost on any exception path; no frontier can exist without a matching
completed scope; no hold can disappear without a release record.
**STOP GATE G2.**

---

### G3 — Accounting proof: verifier authority over the full ledger
**Findings:** A14-01 (HIGH), F-01 (HIGH), F-02 (MEDIUM), F-03 (MEDIUM), R2, R7, R9
**Files:** `tools/audit.py`, `lab/accounting.py`, `tests/`

**Required design decisions:**
1. Independent reconstruction of cash, quantity, cost, proceeds, fees, realized, **closed-position cycles**
   and **valuation snapshots** — comparing every expected vs stored movement in both directions.
2. `equity = starting_capital + total_pnl` enforced as a checked identity with documented rounding.
3. **No literal result fields.** `portfolios_checked` must be measured; `integrity` must reflect the actual
   `PRAGMA` outcome; an empty DB must not report success.
4. **Bind the report to the verified bytes** (DB SHA-256 + snapshot ID).
5. The signing-code scan must **fail closed** when it cannot see the source tree.

**Red set:** A14-01 ×5, F-02, F-03.
**Green criteria:** all pass; plus missing/extra/orphan rows, partial exit, settlement, rounding boundary,
closed→open, wrong model/track association, and a valid ledger still passing (no false positives).
**Acceptance:** the archived 999-PnL-with-intact-equity case fails loudly; **and** the new test suite is
proven to fail on the G3 pre-fix snapshot (R1).
**STOP GATE G3.**

---

### G4 — Semantic proof: operation-complete lifecycle (synthetic only)
**Findings:** A14-03 (HIGH synthetic), A14-04 (HIGH synthetic), R8
**Files:** `lab/integrity.py` (`synthetic_event`, `lifecycle`), `tools/source_verify.py`, fixtures

**Required design decisions:**
1. Explicit symbolic **fixture operation specifications**: outcome set, condition, collateral, denominators,
   payout rule, operation identity. These are **test specifications, never invented chain evidence**.
2. SPLIT: require complete outcome mapping **and non-zero paid basis**; reject n-way fan-out without a spec.
3. REDEEM/RESOLUTION: require payout numerator/denominator, finality evidence, per-share ceiling; reject
   negative cash legs; resolution alone must never credit.
4. Verifier must check the **semantics**, not re-derive them from trusted cash fields.

**Red set:** A14-03 ×3, A14-04 ×2.
**Green criteria:** all pass; plus fractional payouts, deductions, wrong token/outcome, duplicate economic
redemption under a new identity, restart, unsupported configuration, and a genuinely fully-specified fixture
still passing.
**Acceptance:** an incomplete operation is quarantined with **zero** partial journal effects.
**Explicit scope limit:** passing G4 says nothing about real contract decoding (H03 / LIFE-01 remain BLOCKED).
**STOP GATE G4.**

---

### G5 — Truthful operational UI
**Findings:** A14-09 (MEDIUM), F-06 (LOW)
**Files:** `lab/dashboard.html`, `lab/main.py` (`state`, `warnings`), `lab/store.py` (health schema),
`lab/public.py` (health reporting)

**Required design decisions:**
1. Health dimensions separated: `live success / attempt / age / progress / hold / completeness / audit /
   readiness`, with precedence `BLOCKED > UNKNOWN > STALE > DEGRADED > HEALTHY`.
2. An aggregate green may **never** override a stale or unknown mandatory component.
3. Capability labels must match production behaviour (settlement wording currently over-claims).
4. Default-deny for non-GET verbs on the state endpoint.

**Red set:** A14-09 ×1 (`stale_health_not_green`), F-06.
**Green criteria:** stale/fresh/failure/none/incomplete-batch/held-wallet/unknown-source/unavailable-DB/
stopped-worker/reachable-but-stale all correct; the archived ts=0 case no longer renders `Healthy`.
**Acceptance:** no green mandatory component can be rendered from a stale row.
**STOP GATE G5.**

---

### G6 — External evidence (NOT locally achievable)
**Findings:** H01–H05, GOV-00, SAFE-02, SRC-01…03, LIFE-01…03, GAP-01, COPY-01/02, EXEC-01/02,
STRAT-01…03, RISK-01, UI-01, SEC-01, OPS-01…03, FINAL-01/02, DOC-01, GOV-01

**Nothing in G6 can be closed by me, by tests, or by any synthetic proxy.** It requires:
source-capability proof from the provider; real chain identity/finality; version-specific decoder evidence;
complete historical gap reconstruction; approved wallet forward history; execution calibration; statistically
adequate untouched strategy evaluation; and a **genuinely separate** reviewer and final auditor.

**This is where the project's real risk lives**, and it is precisely the part that no amount of engineering
can retire. See §9.

---

## 5. Acceptance criteria and the red→green harness

### 5.1 Criterion format

Every finding gets a machine-checkable invariant, so "done" is never a judgement call:

```
FINDING     : A14-06
INVARIANT   : every received HTTP attempt body is durable on every exit path
RED TEST    : acceptance_suite.py::all_failed_attempt_bodies_retained  (+2 more)
RED EVIDENCE: red-phase-results.json  (result=FAIL, detail recorded)
GREEN PROOF : same test PASS after fix, same fixture, same fixture seed
REGRESSION  : full suite still green AND no assertion relaxed (diff reviewed)
ARTEFACT    : green-phase-results.json bound to DB sha256 + snapshot id
```

### 5.2 The 35 criteria

See `evidence/red-phase-results.json` for the machine form. Mapping:

| Finding | Tests | Severities |
|---|---|---|
| A14-01 | 5 | 1 HIGH, 4 MEDIUM |
| A14-02 | 4 | 4 HIGH |
| A14-03 | 3 | 3 HIGH |
| A14-04 | 2 | 1 HIGH, 1 MEDIUM |
| A14-05 | 2 | 2 MEDIUM |
| A14-06 | 4 | 4 MEDIUM |
| A14-07 | 4 | 4 MEDIUM |
| A14-08 | 2 | 2 LOW |
| A14-09 | 1 | 1 MEDIUM |
| A14-10 | 3 | 2 MEDIUM, 1 LOW |
| F-02, F-03, F-04, F-05 | 4 | 4 MEDIUM |
| **Total** | **35** | |

### 5.3 Red-phase result — the key evidence of this run

`tools/acceptance_suite.py` run against a pristine disposable copy (`runD`), network blocked:

```
TOTAL 35   PASS 0   FAIL 35   -> phase=RED
```

**Every one of the 35 demanded invariants is violated by the current snapshot.** This is the artefact that
was missing: a green future run now means something, because the same tests are *known* red today.

**The suite found six real defects in itself before trusting it — and one in my own audit report.** Full disclosure, because a harness nobody validated is worse than no harness:

| # | Self-defect | How it surfaced | Fix |
|---|---|---|---|
| 1 | `paper_with_fill` bound a `Cursor` instead of `.lastrowid` | 4 tests ERRORed | `.lastrowid` added |
| 2 | F-02 accepted the `database` **path echo** as "identity binding" | passed falsely | now demands actual SHA-256 of bytes |
| 3 | F-04 unioned `first` and `second` samples — a tautology that hides overwrite | passed falsely | now samples **final state only** |
| 4 | A14-10 asserted "DB bytes unchanged", but a second `Store()` on an **already-migrated** DB writes nothing yet still becomes a **writer** | passed falsely | now asserts the second Store must refuse or be read-only; it writes successfully → FAIL |
| 5 | **A14-08** numerics claim contradicted by re-measurement | test PASSed while my report said FAIL | report **corrected** (§0.4); new no-affinity test added |
| 6 | A14-09 probe reported FAIL when its Node dependency was absent | **false red** — right result, wrong reason | dependency restored; probe now errors loudly instead of passing |

Items 2, 3 and 4 are the dangerous class: **they would have produced false green.** They are why R1 (prove
the test fails pre-fix) is a blocking plan change rather than good practice.

### 5.4 Green-phase protocol

For each group, in order, with nothing skipped:

1. Freeze the current source as `pre-GN` and **re-run the suite: expect the group's tests red.**
2. Make only the approved changes.
3. Re-run: group tests green; **all previously-red tests in earlier groups stay green**; whole suite green.
4. Diff every assertion — **no relaxation** (INV-09).
5. Hash the DB used, record the snapshot ID, write `green-GN.json`.
6. Independent re-run by someone who did not write the fix (GOV-00 applies even here).
7. **STOP.** Request the next bounded group.

**A green result produced without step 1 is not evidence and must be rejected.**

---

## 6. External-review package

`INDEP-AUDIT-01`'s authority is limited by §2 (same harness). The package below exists so a **genuinely
outside** reviewer can reach an independent conclusion efficiently, without re-doing my groundwork.

### 6.1 Contents to hand over

| Item | Path | Purpose |
|---|---|---|
| Sealed source | `copylab-external-review.zip` + SHA256.txt | the artefact under review |
| Independent audit | `AUDIT_REPORT_INDEP-AUDIT-01.md` | reproduction + 49 cases + new findings |
| **This dossier** | `MASTER_COMPLETION/MCD-01.md` | consolidated plan, criteria, blockers |
| **Red-phase suite** | `MASTER_COMPLETION/tools/acceptance_suite.py` | 32 executable invariants |
| **Red evidence** | `MASTER_COMPLETION/evidence/red-phase-results.json` | 35/35 failing, with details |
| Probe corpus | `MASTER_COMPLETION/evidence/probes/*.py` | my 49 reproduction cases |
| Probe results | `MASTER_COMPLETION/evidence/results/*.json` | hashed outputs |
| Reproduction guide | `MASTER_COMPLETION/tools/REPRODUCE.md` | exact commands, isolation, expected results |

### 6.2 What the outside reviewer must do (and why it is cheap now)

1. Verify the archive hash — **one command**.
2. Re-run the red suite — **one command**; expect `35/35 FAIL`. If any test passes, either the snapshot
   drifted or the test is defective; both are findings.
3. Attempt to **falsify** any of the 49 probe cases. My cases are labelled by finding; a counterexample is
   the most valuable thing they can return.
4. Review §0.4's correction and confirm or reject it (independent check of my own error).
5. Assess H01–H05 BLOCKED classifications and the G1–G5 ordering.
6. Sign as a **named organisation or accountable individual**.

### 6.3 What the package deliberately does **not** contain

No runtime databases, no `.git`, no wallet addresses, no chain identifiers, no real market data, no synthetic
data dressed as real. A reviewer who needs runtime DB export requires **separate owner approval** (the
archive's own instruction, unchanged).

---

## 7. Implementation sequence (armed, not started)

Ready to execute the moment §9 clears. Each line is a stop gate.

| Step | Scope | Entry condition | Exit evidence | Who |
|---|---|---|---|---|
| S0 | Outside review of `INDEP-AUDIT-01` + this dossier | package delivered | named sign-off or documented rejection | **external reviewer** |
| S1 | User approves **G1 only** (= plan 1A; see `MCD-07`) | S0 signed | written authorisation | **you** |
| S2 | G1 design doc (no code) | S1 | design reviewed | implementer |
| S3 | G1 red re-confirm → fix → green → review | S2 | `green-G1.json` bound to bytes | implementer + reviewer |
| S4 | User approves G2 | S3 | written authorisation | **you** |
| S5–S10 | G2 → G3 → G4 → G5, same cycle | each prior gate | `green-GN.json` each | same |
| S11 | Whole-system adversarial run (45 scenarios) | G1–G5 green | FINAL-01 evidence | implementer + reviewer |
| S12 | Separate final audit | S11 | FINAL-02 sign-off | **external auditor** |
| S13 | **Runtime activation request** (migration/start) | S12 + prerequisites | separate explicit approval | **you** |
| S14 | Bounded paper forward observation | S13 | real evidence | you + operator |
| S15 | Release assessment | S14 | release decision | you |

**G6 is not on this list because it is not a step you can schedule.** It is an evidence-acquisition programme
whose duration depends on third parties. S14 cannot be compressed by effort.

---

## 8. Governance register (new items from this run)

| ID | Item | Severity | Status | Owner |
|---|---|---|---|---|
| **GOV-01** | Directive §2 truncated — full safety list not received | **HIGH** | **CLOSED** by D-12 → `MCD-08.md`; residual exhaustiveness = GOV-13 | resolved |
| GOV-02 | Outside-the-harness reviewer not engaged | HIGH | **OPEN** (blocker 1) | owner |
| GOV-03 | Red-phase harness not yet adopted as the project's acceptance instrument (R1/R2) | HIGH | OPEN | implementer |
| GOV-04 | F-01…F-09 not yet entered in `MASTER_DEFECT_REGISTER.md` | MEDIUM | OPEN | implementer |
| GOV-05 | INDEP-AUDIT-01 §0.4 correction not yet acknowledged in the audit record | MEDIUM | OPEN | reviewer + you |
| GOV-06 | Evidence provenance binding (R9/F-02) not implemented, so no gate artefact is byte-attributable yet | MEDIUM | OPEN | implementer |
| GOV-07 | Reviewer to re-derive the corrected A14-08 scope (`MCD-03` §3) and confirm or reject it | MEDIUM | OPEN | external reviewer |
| GOV-11 | Criteria re-based 32 → 35 across every artefact | — | **CLOSED** this run | resolved |
| **GOV-13** | Owner to confirm SR-01…SR-28 (MCD-08) is exhaustive against the original directive | MEDIUM | OPEN, non-blocking | owner |
| **GOV-14** | `capture_frontiers` cannot be fixed additively — new table or rebuild needed (MCD-09 §2.6) | MEDIUM | OPEN, at G2 | owner + implementer |
| **GOV-15** | Cross-version parity (3.13/3.46) unverified — documentation closed in MCD-10, evidence open | LOW | OPEN | external reviewer |
| **GOV-09** | G2 design doc: attempt identity + scope identity schema | MEDIUM | **design CLOSED** (`MCD-09`); implementation gated by G2 | resolved (design) |
| **GOV-10** | External reviewer to confirm R4/R5 restatements are correctly encoded in criteria #18–#25 | MEDIUM | OPEN | reviewer |
| **GOV-12** | 1A–1H ↔ G1–G6 numbering ambiguity | MEDIUM | **CLOSED** — `MCD-07.md` | resolved |
| **GOV-08** | R1–R10 disposition | HIGH | **CLOSED** by D-9 | resolved |

**I have not edited `MASTER_DEFECT_REGISTER.md` or `MASTER_REMEDIATION_PLAN.md`.** GOV-03/04/05 are requests
to their owners, consistent with INV-11 (append, never delete).

---

## 9. Blockers — the honest list

**10 blockers. Two are governance items only the owner can close; seven are evidence items the world must
supply; one is a decision deferred to G2.** None is a documentation gap — every documentation item that could
be closed without approval has been closed (`GOV-01`, `GOV-09` design, blocker 10, `GOV-08`, `GOV-11`,
`GOV-12`).

| # | Blocker | Class | Can I clear it? |
|---|---|---|---|
| 1 | **GOV-02** no genuinely external reviewer | governance | **No** — structural |
| 2 | No authorisation of a bounded scope (G1–G5 withheld) | governance | No — owner decision |
| 3 | **H01** no authoritative source checkpoint | evidence | No — upstream/provider |
| 4 | **H02** no canonical identity/finality | evidence | No — upstream |
| 5 | **H03** no real decoder evidence | evidence | No — upstream |
| 6 | **H04** no historical gap reconstruction | evidence | No — needs history that does not exist |
| 7 | **H05** no forward / calibration / performance evidence | evidence | No — needs time + approved wallets |
| 8 | Runtime DB state unverified (excluded by design) | evidence | No — needs separate approval |
| 9 | **GOV-15** cross-version parity unverified (3.13/3.46) | technical | Partly — reviewer on a second interpreter |
| 10 | **GOV-14** `capture_frontiers` cannot be fixed additively | design | No — decision needed at G2 authorisation |

**Non-blocking residual:** `GOV-13` — the owner should confirm that `MCD-08`'s SR-01…SR-28 set is exhaustive
against the original directive. It does not block external review (a reviewer assesses the *system*, not the
completeness of my transcription) but it does block the claim "the safety set is complete".

**What is *not* on this list, and should be said plainly:** the engineering findings are fully characterised,
reproducible and regression-locked behind 35 executable criteria. Blockers 3–7 mean **CopyLab cannot currently
demonstrate that it would copy a real wallet correctly even if every A14 defect were fixed**, because there is
no evidence that the source data is complete or that the operations are decoded correctly. Fixing A14 improves
the *instruments*; it does not supply the *measurements*.

## 10. Path to final release

Four milestones, in the project's own terms. **All four remain BLOCKED.**

| Milestone | Meaning | Gate |
|---|---|---|
| **A — Engineering complete** | No open HIGH accounting/integrity defect; G1–G5 green with red→green proof; F-01…F-05 closed | achievable locally after S1–S10 |
| **B — Trustworthy paper operation** | Real verified source + forward history; H01–H04 resolved | needs G6 evidence |
| **C — Performance** | Evidence adequate to isolate strategies; STRAT/EXEC resolved | needs B + time |
| **D — Operations** | Auth, restore drills, monitoring, load/soak | needs A |
| **Release** | A+B+C+D + FINAL-02 separate audit + permanent INV-01…INV-11 | all |

**Realistic expectation, stated plainly:** milestone **A** is reachable and is genuinely worth doing — it is
the part that removes the risk of *the tool lying to you*. Milestones **B and C** depend on evidence that
does not exist today and cannot be manufactured. **CopyLab may legitimately end at milestone A + permanent
paper-only containment**, and that would be an honest, defensible outcome. It should not be presented as a
trading system until B and C are evidenced, and never as a real-money system (INV-01/INV-02 are permanent).

---

## 11. Immediate asks

Five when this dossier was first written. **Two are now closed by your decisions, three remain**, each a single action:

| # | Ask | Status after your decisions |
|---|---|---|
| 1 | Re-send directive §2 in full | **OUTSTANDING** — TD-01 / GOV-01; the only invariant-completeness gap |
| 2 | Confirm or reject the A14-08 correction | **DONE** — accepted (D-2); evidence in `MCD-03.md` §5 |
| 3 | Engage an outside reviewer with the §8 package | **OUTSTANDING** — GOV-02; package complete in `MCD-05.md` |
| 4 | Adopt the red-phase harness as acceptance instrument | **DONE, PROVISIONAL** — D-4; criteria specified in `MCD-02.md` |
| 5 | Do not authorise G1 yet | **HONOURED** — D-5; G1 remains NOT AUTHORISED |

**GOV-08 remains open:** R1–R10 must be dispositioned (accepted, rejected with reasoning, or amended) before
the plan can be called approved. This is the item that turns "REVISE PLAN" into a re-reviewable plan.

## 12. Closing statement

I have completed every piece of preparation that does not require approval: state verification, reconciliation,
one consolidated plan, 35 testable criteria, a validated red→green harness (**35/35 red, self-tested, one of
my own audit claims corrected**), a staged external-review package, 11 enumerated blockers and an armed
sequence.

**I have not fixed anything, started anything, migrated anything, queried anything or claimed any approval.**

Phase 0 remains **NOT SATISFIED**. Phase 1A remains **NOT AUTHORISED**.

**STOP.**

---

## Appendix A — Artefact manifest

| Artefact | Path | Cases/Lines |
|---|---|---|
| This dossier | `MASTER_COMPLETION/MCD-01.md` | — |
| Red-phase suite | `MASTER_COMPLETION/tools/acceptance_suite.py` | 35 tests |
| Red-phase result | `MASTER_COMPLETION/evidence/red-phase-results.json` | 32 fail |
| Reproduction guide | `MASTER_COMPLETION/tools/REPRODUCE.md` | — |
| Probe corpus | `MASTER_COMPLETION/evidence/probes/` | 5 files |
| Probe results | `MASTER_COMPLETION/evidence/results/` | 49 cases |
| Independent audit | `AUDIT_REPORT_INDEP-AUDIT-01.md` | — |

## Appendix B — Environment

Python 3.11.2 · SQLite 3.40.1 · Node 22.22.3 + jsdom (review-side) · Linux · network blocked for all project
execution via `sitecustomize` socket denial (verified) · no Playwright (A14-09 substituted, disclosed) ·
no runtime DB · no app/worker start.
