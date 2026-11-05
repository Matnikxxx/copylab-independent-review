# MCD-06 — Plan revision disposition register (R1–R10)

**Document ID:** `MCD-06` · **Status:** ACTIVE · **Append-only**
**Authority:** owner dispositions, 2026-11-05 (decision **D-9**, `MCD-04.md` §2)
**Subject:** the ten blocking plan revisions from `MCD-01.md` §2.2 / `INDEP-AUDIT-01` §8.2
**Group numbering:** resolves through `MCD-07.md` (authoritative 1A–1H ↔ G1–G6 cross-reference)

---

## 1. Disposition summary

| Rev | Owner disposition | Effect on plan | Effect on acceptance criteria |
|---|---|---|---|
| R1 | **ACCEPT** | red→green artefact mandatory per group | criteria unchanged; protocol bound |
| R2 | **ACCEPT** | 119-test count demoted to regression guard | criteria unchanged; no criterion may cite it |
| R3 | **ACCEPT** | A14-05 + F-04 merged into one group (G2) | criteria #16, #17, #31 co-located |
| R4 | **AMEND** | acceptance criterion rewritten per owner text | **A14-06 criteria strengthened: 3 → 4** |
| R5 | **AMEND** | invariant must live inside `collect()` | **A14-07 criteria strengthened: 2 → 4** |
| R6 | **ACCEPT** | G1 includes lock canonicalisation + Store ownership | criteria #27, #28 unchanged |
| R7 | **ACCEPT** | G3 includes snapshot-equity + closed-cycle | criteria #1, #5 unchanged |
| R8 | **ACCEPT** | G4 includes zero-basis, n-way, negative-cash | criteria #13, #11, #14 unchanged |
| R9 | **ACCEPT** | evidence-provenance binding per artefact | criterion #29 unchanged |
| R10 | **ACCEPT** | default-deny verbs moved into G1 | criterion F-06 promoted into G1 scope |

**Amendments are not cosmetic.** Both were applied by **strengthening the executable criteria**, not by
re-wording prose. The suite grew from **32 to 35** cases; the red phase was re-run and all 35 fail.

**No revision was rejected.** No acceptance criterion was weakened by any disposition.

---

## 2. R4 — AMEND

### 2.1 Owner wording (verbatim)

> "The wording 'persists ≤1 body, possibly none' describes the existing defect. The remediation acceptance
> criterion must require preservation of every relevant HTTP attempt body and associated metadata, including a
> successful HTTP 200 response followed by a later timeout or exception."

### 2.2 Assessment of the amendment — the owner is right

My original R4 text described the *defect* ("exception path persists ≤1 body") and left it implied that the
acceptance criterion would be the negation. That is exactly the class of error R1 exists to prevent: a
criterion phrased as a description of broken behaviour can be satisfied by a fix that merely shifts the
threshold. **A criterion must state the positive obligation.** The owner's version does that, and it adds a
requirement I had under-specified: **associated metadata**, not just the body bytes.

### 2.3 Restated acceptance criterion (binding)

> **A14-06 — every relevant HTTP attempt body and its associated metadata must be durable on every exit
> path, including a successful HTTP 200 response followed by a later timeout or exception.**

Decomposed into the four obligations now enforced as executable tests:

| # | Obligation | Test |
|---|---|---|
| a | every received attempt body retained | `all_failed_attempt_bodies_retained` |
| b | per-attempt metadata retained (HTTP code, error, receipt time) | `all_failed_attempt_bodies_retained` |
| c | a **successful 200** body survives a later timeout/exception, with metadata | `successful_body_survives_later_failure` |
| d | attempts are individually distinguishable; identical bodies are **not** deduplicated | `attempt_order_and_metadata_distinguishable` *(new)* |
| e | an attempt with no `last_raw` is still durable | `attempt_without_last_raw_is_durable` |

### 2.4 Criteria added / strengthened

| Test | Change | Pre-fix result |
|---|---|---|
| `all_failed_attempt_bodies_retained` | strengthened: now asserts 3 rows, each body, its HTTP code, its error, its receipt time | **FAIL** — `1 durable rows for 3 received attempts: ['body-3']` |
| `successful_body_survives_later_failure` | strengthened: asserts both bodies **and** the 200 code + receipt time of the successful attempt | **FAIL** — `successful body destroyed; durable=['bad-504']` |
| `attempt_order_and_metadata_distinguishable` | **NEW** — three attempts with *identical body text* and distinct codes must remain three distinguishable rows | **FAIL** — `1 rows for 3 attempts with identical bodies (attempt identity lost)` |
| `attempt_without_last_raw_is_durable` | unchanged | **FAIL** — `durable bodies=[]` |

### 2.5 Why (d) was added

The owner's phrase "every relevant attempt body" implies *attempt identity*, not body identity. Without (d), a
fix could satisfy the letter of the criterion by de-duplicating identical bodies — three received 5xx responses
with the same error page would collapse to one row and pass a naive count. (d) closes that loophole and fails
today for the right reason.

### 2.6 Residual scope limit (stated, not hidden)

`transport_deliveries` currently has no per-attempt identity column
(`id, batch, page_number, received, raw, disposition`). The obligation in (b)/(d) therefore requires an
**additive schema change** in G2 (attempt ordinal or equivalent). This is recorded so G2's design doc accounts
for it before code, and so no one mistakes the criterion for something achievable without a migration.

---

## 3. R5 — AMEND

### 3.1 Owner wording (verbatim)

> "Explicitly require request-scope correctness to be enforced inside `collect()` for every invocation and
> resumed batch. The invariant must not depend solely on `allowed()` or caller behaviour."

### 3.2 Assessment of the amendment — the owner is right, and this was the sharper of the two

My original R5 said containment is "of the instance, not the class" and that the invariant should be stated on
`collect()`. But I left the *mechanism* to the implementer, and `collect()` currently delegates safety to
`allowed()` (a global production kill-switch) and to callers like `Collector.baseline`. **That is a
defence-in-depth inversion:** the component that forms and resumes HTTP requests must not depend on a policy
switch three layers away, nor on every caller remembering to check. If `allowed()` ever returns `True` — which
is precisely what Phase 2 exists to enable — the defect becomes live with no further change.

### 3.3 Restated acceptance criterion (binding)

> **A14-07 — request-scope correctness is enforced inside `collect()` on every invocation, including resumed
> batches. A scope mismatch is either rejected or isolated into an independent batch. The invariant must hold
> without any contribution from `allowed()` or from caller-side checks.**

### 3.4 Criteria added / strengthened

| Test | Change | Pre-fix result |
|---|---|---|
| `scope_substitution_rejected` | unchanged | **FAIL** — `OPEN request was sent as status=CLOSED` |
| `frontier_not_published_for_wrong_scope` | unchanged | **FAIL** — frontier published for a CLOSED walk |
| `collect_enforces_scope_without_allowed` | **NEW** — encodes the owner's constraint structurally: no `allowed()` call, no caller check; only two acceptable outcomes (reject or fork) | **FAIL** — `scope mismatch neither rejected nor forked: reused pending batch, sent status='CLOSED' for a requested OPEN scope` |
| `scope_identity_persisted_per_batch` | **NEW** — resume validity must never rest on `wallet+endpoint` alone; an explicit scope-identity field must exist and be populated | **FAIL** — `collection_batches has no explicit scope-identity column (columns=['id','wallet','endpoint','params','started','finished','status','next_cursor','page_number','error','coverage'])` |

### 3.5 Why the two new criteria

- `collect_enforces_scope_without_allowed` makes the owner's constraint **testable rather than aspirational**.
  It never calls `allowed()` and performs no caller-side scope check, so a fix that works only because
  production admission is globally false cannot pass it.
- `scope_identity_persisted_per_batch` attacks the *root cause* rather than the symptom. The reason mismatch
  is possible at all is that `collect()` looks up resumable work by `(wallet, endpoint)` — the concept "which
  scope does this batch belong to" does not exist in the schema. Adding a hash and still looking up by
  `wallet+endpoint` would leave the defect intact; the test demands the identity be both **present and
  populated**, and `collect_enforces_scope_without_allowed` demands it be **used**.

### 3.6 Residual scope limit

Both new criteria are satisfiable only with an **additive schema change** (scope identity column) plus a change
to the resume lookup inside `collect()`. Recorded for G2's design doc. Neither is achievable by callers.

---

## 4. Consequences for the plan (binding on G2)

| Change | Consequence |
|---|---|
| A14-06 now 4 criteria, needs attempt identity | G2 design doc must specify the attempt-identity column **before code** |
| A14-07 now 4 criteria, needs scope identity | G2 design doc must specify scope hash + resume lookup change **before code** |
| R3 already merged A14-05 + F-04 into G2 | G2 now carries **9 criteria** across 4 findings + 1 new finding (F-04/F-05) |
| Schema changes in G2 | must be **additive/versioned** with compatibility tests; **no runtime migration** (INV-04) |

**G2 entry condition is unchanged:** it may not begin. Nothing here authorises it.

---

## 5. What these dispositions do *not* change

- **Governance state.** Phase 0 **NOT SATISFIED**; Phase 1A and **G1–G5 NOT AUTHORISED**.
- **The red phase.** Still RED — now 35/35 instead of 32/32.
- **Provisional status of the suite.** Still provisional and still subject to external review (D-4);
  these amendments make it *stronger*, which the owner's own asymmetry permits without further approval.
- **Snapshot and runtime.** Unmodified; no service, worker, collector or database action.

---

## 6. Open items created or closed by this document

| ID | Item | State |
|---|---|---|
| GOV-08 | R1–R10 dispositioned | **CLOSED** by D-9 |
| GOV-09 | G2 design doc must cover attempt identity + scope identity before code | OPEN (implementer, post-approval) |
| GOV-10 | External reviewer to confirm the R4/R5 restatements are correctly encoded in criteria | OPEN (reviewer) |
| GOV-11 | Criteria count 32 → 35; all package artefacts re-based on 35 | **CLOSED** this run |

---

*Append-only. Later dispositions recorded as R-notes here, never by editing the above.*
