# MCD-04 — Owner decisions ledger and directive transmission record

**Document ID:** `MCD-04` · **Status:** active · **Append-only**
**Purpose:** record the owner's decisions verbatim-in-intent, the transmission discrepancy required by
decision #1, and the standing authorisation state. Everything here is citable by later phases.

---

## 1. Governor state (as of 2026-11-05)

| Gate | State | Set by |
|---|---|---|
| Phase 0 — independent review satisfied | **NOT SATISFIED** | owner, this message |
| Phase 1A — implementation authorised | **NOT AUTHORISED** (explicit) | owner, decision #5 |
| G1 — implementation authorised | **NOT AUTHORISED** (explicit) | owner, decision #5 |
| Red-phase suite — acceptance baseline | **ADOPTED, PROVISIONAL** | owner, decision #4 |
| External review — mandatory | **YES, MANDATORY, OUTSTANDING** | owner, decision #3 |
| A14-08 numeric-collision claim | **WITHDRAWN**, corrected finding accepted | owner, decision #2 |
| Paper-only restriction | **IN FORCE, unchanged** | standing |
| Source snapshot / databases | **PRESERVED, unchanged** | standing |

**No gate was advanced by this run.** The only state change is that the red-phase suite is now *adopted as a
proposed baseline* — which is a statement about what will count as evidence later, not authority to act now.

---

## 2. Decision record

Each decision is transcribed in intent, with the operational consequence I have implemented. Where a decision
implies an obligation on me, it is listed so it cannot be quietly dropped.

### D-1 · GOV-01 — transmission discrepancy

> *Owner:* "The original master directive contained the complete safety requirements. Please compare the
> actual received prompt against the full directive and record this as a transmission discrepancy. Do not
> interpret missing text as permission to relax any restrictions."

**Implemented:**
- Recorded as **TD-01** in §3 below.
- The received text is preserved verbatim for comparison; the *full* directive text is **not in my
  possession** and I have not reconstructed it from memory or inference — doing so would fabricate the
  evidence the record is supposed to establish.
- No restriction was relaxed. §4 shows the operative invariant set and its source for each item; every item
  traces to a source that *is* in my possession, none of which depends on the missing lines.
- **Obligation created:** when the full text arrives, I must diff it against §3 and reconcile any invariant
  I could not derive — upward only, per D-2's logic that corrections may tighten.

### D-2 · A14-08 — correction accepted, conditional on reproducible evidence

> *Owner:* "I accept withdrawing the numerical collision claim, provided the corrected finding is supported
> by reproducible evidence. Preserve the original audit and the correction history."

**Implemented:**
- `MCD-03.md` is the correction record: original claim quoted verbatim, error identified, corrected finding
  stated, severity/scope table, **and a runnable script whose output supports it**.
- I re-ran that script during this run; output is in `MCD-03` §5(b) and reproduced in this package.
- `AUDIT_REPORT_INDEP-AUDIT-01.md` is **unedited**. The correction is appended, never substituted.
- A14-08 status unchanged: **OPEN, LOW, Group G1**. Two criteria (#23, #24) assert only the corrected family.
- **Obligation created:** GOV-05 (acknowledge in the audit record), GOV-07 (reviewer re-derives §3).

### D-3 · External review — mandatory

> *Owner:* "Agreed. The external-review requirement remains mandatory."

**Implemented:** package staged (`MCD-05.md`), reviewer instructions (`tools/EXTERNAL_REVIEW_INSTRUCTIONS.md`),
reproduction guide (`tools/REPRODUCE.md`). GOV-02 remains **BLOCKED**. Nothing in this package is a
substitute for that sign-off.

### D-4 · Red-phase suite — provisional adoption with four conditions

> *Owner:* "Adopt the 32-case suite provisionally as the proposed acceptance baseline. It must remain subject
> to independent review. Every test must have a documented intended failure reason, reproducible pre-fix
> result and corresponding post-fix acceptance condition."

**Implemented — condition by condition:**

| Owner condition | Where satisfied | Verified |
|---|---|---|
| provisional / subject to independent review | `MCD-02` header + "Provisional status is load-bearing" | ✔ |
| documented intended failure reason | `MCD-02` §1–32, "Intended failure reason (root cause)" per test | ✔ 32/32 |
| reproducible pre-fix result | `MCD-02` per test + `evidence/red-phase-results.json` + `REPRODUCE.md` | ✔ 32/32 |
| corresponding post-fix acceptance condition | `MCD-02` §1–32, "Post-fix acceptance condition" per test | ✔ 32/32 |

- Adoption is **provisional**, and I have recorded the asymmetry: criteria may be **strengthened** by a
  reviewer without further approval; **weakening** one requires written rationale in the open items.
- **Obligation created:** the suite is now the proposed acceptance instrument, so any future change to it is
  itself a governance event (version bump + rationale), not a routine edit.

### D-5 · G1 withheld

> *Owner:* "I explicitly do NOT authorise G1 implementation at this stage."

**Implemented:** G1 is marked **NOT AUTHORISED** in §1 and in `MCD-01` §7 (S1 gate remains closed). No code
was written, no design doc for G1 was produced beyond the *scope statement* already in `MCD-01` §4, and no G1
red case was "pre-fixed". I did not treat the plan's existence as authority.

### D-6 · Preservation and prohibition (standing)

> *Owner:* "Continue preserving the existing source snapshot, databases and paper-only restrictions."

**Implemented:** snapshot re-verified pristine before and after this run (§5). No runtime DB touched, no
app/worker/collector started, no network used for project code, no wallet queried. `MCD-01` §3 `INV-01…INV-11`
remain in force.

### D-7 · Next objective

> *Owner:* "The next objective is to obtain a genuinely external review and establish whether Phase 0 can be
> satisfied. Do not mark it complete prematurely."

**Implemented:** this run is scoped entirely to making external review *possible and cheap*. Phase 0 is
recorded as **NOT SATISFIED** in every document. §6 lists the exact evidence a reviewer may accept or reject —
I have deliberately not pre-judged it.

### D-8 · One coordinated programme

> *Owner:* "I want one coordinated project, not repeated small approval requests. Once the mandatory external
> review is complete and the implementation plan is approved, we can authorise the approved remediation work
> as one coordinated programme."

**Implemented:** `MCD-01` §7 already sequences G1→G5 as a single cycle; this run adds the programme-level
authorisation record in §7 below, so that the *one* approval event the owner wants is a single pre-specified
object rather than five separate asks.

---

## 3. TD-01 · Transmission discrepancy record

| Field | Value |
|---|---|
| **ID** | TD-01 |
| **Detected** | 2026-11-05, during `MCD-01` preparation |
| **Class** | transmission truncation (not a content dispute) |
| **Owner's statement** | the original directive contained the complete safety requirements |
| **Observed** | the received directive ends mid-sentence at: `- No live trading,` |
| **Missing** | the remainder of §2 "Non-negotiable safety requirements" and, by inference, all subsequent sections |
| **My treatment** | strictest-reading reconstruction; **no relaxation**; no reconstruction of the missing text |

**Verbatim tail of the received directive**, preserved so the truncation point is provable rather than
asserted:

```
2. Non-negotiable safety requirements

These requirements apply throughout the entire project.

- CopyLab must remain strictly paper-only.
- No live trading,
```

**What I explicitly did NOT do:**

- I did not invent the missing bullets.
- I did not treat "no live trading" as the last requirement.
- I did not lower any restriction because a restriction was absent from the received text.
- I did not assume the missing text was permissive — a reasonable reading is that it contained *more*
  prohibitions (no wallets, no network, no secrets, no deployment), all of which I applied anyway.

**Reconstruction basis for §4** — every operative invariant traces to a source I hold:

| Source | Type | Available? |
|---|---|---|
| `copylab-external-review-INSTRUCTIONS.md` | sealed transfer instructions in the archive | ✔ |
| `docs/phase0-audit14/AUDIT_14.md` method section | the project's own audit constraints | ✔ |
| `MASTER_REMEDIATION_PLAN.md` §5 protocol | the project's own engineering discipline | ✔ |
| `INDEP-AUDIT-01` §3 isolation envelope | my own audit constraints | ✔ |
| Owner's decision #6 this message | explicit standing preservation order | ✔ |
| **Original directive §2 (complete)** | **owner's primary safety list** | **✘ — MISSING** |

The last row is the gap. **GOV-01 stays BLOCKED until it is supplied**, and `MCD-01`/`MCD-02` remain labelled
as operating on a reconstructed set. This is recorded, not worked around.

---

## 4. Operative invariants and their provenance (no item depends on missing text)

| ID | Invariant | Source (all in my possession) |
|---|---|---|
| INV-01 | Paper-only permanently; `paper_only` must be `true` | directive (received line) + `config.validate` |
| INV-02 | `allowed()` returns `False` for non-synthetic DBs unconditionally | code + `SAFE-01`; re-verified by INDEP-AUDIT-01 |
| INV-03 | No signing, no keys, no order endpoints; GET allowlist only | code + `AUDIT_14` + archive instructions |
| INV-04 | No runtime DB mutation without separate approval + verified backup | archive instructions + `SAFE-02`/`OPS-03` |
| INV-05 | No app/worker/server start during review/engineering | archive instructions + `AUDIT_14` method |
| INV-06 | No wallet query, no real network source call in tests | archive instructions + `AUDIT_14` method |
| INV-07 | Synthetic evidence never presented as chain fact | code (`provenance`) + `AUDIT_14` |
| INV-08 | Missing ≠ zero | code (`baseline`) + `AUDIT_14` |
| INV-09 | Evidence additive; failures preserved; no relaxed assertions | `MASTER_REMEDIATION_PLAN` §5.7 |
| INV-10 | Every gate artefact binds to bytes (DB SHA-256 + snapshot id) | `INDEP-AUDIT-01` F-02 / plan R9 |
| INV-11 | Register append-only; findings never deleted | `MASTER_DEFECT_REGISTER` §4 |

**None of the eleven depends on the missing §2 lines.** The truncation therefore reduces *completeness* of
the safety list, not *strength* of what is enforced — which is why work could proceed without relaxation.

---

## 5. Preservation evidence for this run

| Check | Result |
|---|---|
| Archive SHA-256 | `f1943…b11c23` — identical, before and after |
| Snapshot manifest | **156/156 files, 0 mismatches** — pristine |
| Project source tree in version control | **none** — source remains sealed in the ZIP |
| Runtime databases | **not read, copied, hashed or opened** |
| App / worker / server / collector | **not started** |
| Migrations | **not run** |
| Wallet / network / signing | **none** |
| Files added to `MASTER_COMPLETION/` | documentation, harness, evidence only |

---

## 6. What constitutes Phase 0 satisfaction (not pre-judged by me)

Recorded so the owner and reviewer share one definition, and so I cannot later claim a pass on my own terms.

Phase 0 is satisfied **only** when all of the following exist:

1. A reviewer **outside this tooling stack**, named and accountable (§ `MCD-05` §4), has:
   - verified the archive hash independently;
   - re-run the 32-case red suite and obtained **32/32 FAIL**;
   - attempted to falsify the 49 probe cases and reported the outcome, including any they could break;
   - independently assessed the A14-08 correction (`MCD-03` §3) — confirm or reject;
   - assessed the H01–H05 BLOCKED classifications and the G1–G6 ordering;
   - **signed** with `APPROVE FOR BOUNDED PHASE 1A`, `REVISE PLAN`, or `BLOCK`.
2. GOV-01 (full directive §2) is supplied and any resulting invariant gap is reconciled upward.
3. R1–R10 plan revisions are applied or explicitly rejected with reasoning.
4. The owner explicitly authorises the bounded scope (currently withheld, D-5).

**My contribution satisfies items 1's *inputs* and nothing more.** Items 1 (the signature), 2, 3 and 4 are
not mine to close. Phase 0 will therefore be reported as **NOT SATISFIED** in every artefact until those
exist, regardless of how complete the preparation becomes.

---

## 7. Programme authorisation record (the single approval event the owner asked for)

Per D-8, the owner wants **one** authorisation, not five. The object of that single approval is defined here
in advance so it can be granted once, cleanly, after external review.

**Proposed single authorisation: "CopyLab Remediation Programme, G1–G5, bounded."**

| Attribute | Value |
|---|---|
| **Scope** | Groups G1–G5 exactly as specified in `MCD-01` §4; 32 criteria in `MCD-02` as acceptance |
| **Explicitly excluded** | G6 (external evidence programme), any runtime activation, any wallet onboarding, any real-money capability (permanent, INV-01) |
| **Entry conditions** | external review signed; GOV-01 closed; R1–R10 dispositioned |
| **Per-group discipline** | red re-confirm → fix → green → independent re-run → STOP; unchanged from `MCD-01` §5.4 |
| **Authorisation is NOT** | permission to skip a group's stop gate, to weaken a criterion, or to touch runtime data |
| **Duration** | until G5 is green and reviewed, or the owner revokes |

**Why this is safe to grant as one event:** the stop-gate discipline is *inside* the programme, so a single
authorisation does not skip the per-group evidence requirements. The owner authorises the *programme*; each
group still has to earn its own green.

**Current state of this object: NOT GRANTED.** G1 explicitly withheld (D-5), and entry conditions unmet.

---

## 8. Open items (current, complete)

| ID | Item | Severity | Status | Owner |
|---|---|---|---|---|
| GOV-01 | Full directive §2 not received (TD-01) | HIGH | **BLOCKED on owner** | owner |
| GOV-02 | No genuinely external reviewer engaged | HIGH | **BLOCKED** | owner |
| GOV-03 | Red suite adopted provisionally; needs independent validation | HIGH | OPEN (provisional per D-4) | external reviewer |
| GOV-04 | F-01…F-09 not yet in `MASTER_DEFECT_REGISTER.md` | MEDIUM | OPEN | implementer, post-approval |
| GOV-05 | A14-08 correction not yet acknowledged in audit record | MEDIUM | OPEN | owner + reviewer |
| GOV-06 | Evidence provenance binding (R9/F-02) unimplemented | MEDIUM | OPEN | implementer, in G1/G3 |
| GOV-07 | Reviewer to re-derive A14-08 corrected scope | MEDIUM | OPEN | external reviewer |
| GOV-08 | R1–R10 plan revisions not dispositioned | HIGH | OPEN | owner + implementer |
| — | 32 criteria provisional acceptance | — | **CLOSED** by D-4 | owner |

---

*Append-only. Superseding decisions will be added as D-9, D-10 … rather than editing the above.*
