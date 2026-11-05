# MCD-08 — Authoritative safety requirements (owner-approved, consolidated)

**Document ID:** `MCD-08` · **Status:** **AUTHORITATIVE** · **Issued:** 2026-11-05
**Resolves:** GOV-01 (supplemental to `MCD-04` §3 TD-01) · **Precedence:** highest in this package for safety scope
**Relationship to history:** **supplemental, not corrective.** `MCD-04` §3 TD-01 remains as written; the
historical truncation is preserved verbatim and is **not** rewritten. This document sits *alongside* it.

---

## 1. Status and precedence

```
TD-01  (MCD-04 §3)      — historical record of the truncation. UNCHANGED. Append-only.
MCD-08 (this document)  — authoritative consolidated safety requirement set. SUPERSEDES
                          nothing and DELETES nothing; it completes the record.
INV-01…INV-11 (MCD-01)  — implementation-facing invariant numbers. Unchanged; mapped in §4.
```

Where this document and any other artefact disagree on **safety scope**, this document wins. Where they
disagree on **technical content** (findings, severity, criteria), the technical document wins.

---

## 2. What was actually received (verbatim, preserved)

The original master directive arrived truncated. The full extent of its received safety section was:

```
2. Non-negotiable safety requirements

These requirements apply throughout the entire project.

- CopyLab must remain strictly paper-only.
- No live trading,
```

**The truncation point is after "No live trading,".** Nothing beyond that arrived. This is recorded in `MCD-04`
§3 as TD-01 and is **not** modified here.

## 3. How this document was compiled (no fabrication)

The owner has confirmed (D-1, and again in the executive who commissioned this stage) that **the complete
safety requirements were contained in the original directive**, and has instructed that they be recorded as a
supplemental authoritative document. Because the missing tail was never transmitted to me, I have **not
reconstructed it from inference**. Instead, every requirement below is sourced from text the owner **did**
transmit in this conversation, in one of the following categories:

| Provenance tag | Meaning |
|---|---|
| `DIRECTIVE` | present in the original directive as received (the two surviving bullets) |
| `MSG-n` | stated by the owner in a later message in this conversation (n = ordinal) |
| `ARCHIVE` | binding on the project from the sealed archive's own transfer instructions |
| `DERIVED` | not stated verbatim, but entailed by a stated requirement (entailment shown) |

**No requirement is invented.** Where a requirement is `DERIVED`, the entailment is shown in the row, so it can
be rejected on its merits without having to trust me.

---

## 4. The authoritative requirement set

### 4.1 Category A — Permanence and capability (never lifted by any later approval)

| ID | Requirement | Provenance |
|---|---|---|
| SR-01 | CopyLab must remain **strictly paper-only**, throughout the entire project | `DIRECTIVE`, verbatim |
| SR-02 | **No live trading** | `DIRECTIVE`, verbatim |
| SR-03 | **No real-money capability, permanently.** Not deferrable to a later phase; not grantable by the owner, a reviewer, or any gate in this package | `DERIVED` from SR-01 + SR-02 (a system that may never trade live cannot acquire real-money capability without contradicting both) |
| SR-04 | **Paper-only restrictions must never be weakened** — including by tests, fixtures, reviewers, or "temporary" relaxation to get a green run | `MSG-3` ("Continue preserving … paper-only restrictions"), `MSG-5` ("no … weakening of paper-only restrictions") |
| SR-05 | `Integrity.allowed()` must continue to return **`False`** for any non-synthetic database, unconditionally | `ARCHIVE` (production `allowed()` is intentionally false; "do not remove it") + SR-04 |
| SR-06 | **No signing capability, no key material, no order endpoints.** Public **GET only**, against the fixed allowlist | `ARCHIVE` (GET-only, fixed-origin client; "No keys. No signing. No real orders.") |

### 4.2 Category B — Prohibited operations (in force for this entire stage and every stage until separately authorised)

| ID | Requirement | Provenance |
|---|---|---|
| SR-07 | **No modification of application source code** | `MSG-5` verbatim |
| SR-08 | **No modification of the existing source snapshot** | `MSG-3` ("continue preserving the existing source snapshot") |
| SR-09 | **No runtime database changes** — no open, write, migrate, back up or restore against runtime data | `MSG-5` verbatim; `ARCHIVE` (runtime DBs excluded; separate approval needed) |
| SR-10 | **No migrations** — no schema or data migration anywhere, including disposable files | `MSG-5` verbatim |
| SR-11 | **No application, worker or collector startup** | `MSG-5` verbatim; `MSG-3` |
| SR-12 | **No wallet queries** | `MSG-5` verbatim |
| SR-13 | **No external trading connections** | `MSG-5` verbatim |
| SR-14 | **No deployment** | `MSG-5` verbatim |
| SR-15 | **No G1–G5 implementation** | `MSG-5` verbatim; `MSG-3` (D-5); `MSG-4` (D-10) |
| SR-16 | **No remediation** of any audited finding | `MSG-3`, `MSG-4`, `MSG-5` (repeatedly) |
| SR-17 | **No authorisation of G1** by any agent; only the owner may authorise, and has not | `MSG-3` (D-5, "explicitly do NOT authorise"), `MSG-4` (D-10) |

### 4.3 Category C — Governance gates (must be satisfied, cannot be self-certified)

| ID | Requirement | Provenance |
|---|---|---|
| SR-18 | **External review is mandatory** and remains outstanding | `MSG-4` (D-3, "remains mandatory"), `MSG-5` |
| SR-19 | **Phase 0 must not be marked complete prematurely**; it remains BLOCKED until all governance and evidence gates are satisfied | `MSG-4` (D-7), `MSG-5` verbatim |
| SR-20 | The **35-case suite remains provisional** until independently reviewed | `MSG-4` (D-4), `MSG-5` verbatim |
| SR-21 | The **implementation agent may not self-certify independence**; no agent, subprocess, restyled report or synthetic fixture substitutes for a genuinely external reviewer | `ARCHIVE` (master plan §4/§8-1), `MSG-4` (D-3) |
| SR-22 | **Findings and evidence are append-only** — no finding deleted, no assertion relaxed, no historical record rewritten | `ARCHIVE` (register §4), `MSG-3` (D-2, "preserve the original audit and the correction history"), `MSG-5` (item 3, "do not rewrite the historical record") |
| SR-23 | **One coordinated programme, not repeated routine approvals** | `MSG-4` (D-8), `MSG-5` verbatim |

### 4.4 Category D — Evidence and truthfulness

| ID | Requirement | Provenance |
|---|---|---|
| SR-24 | Synthetic evidence must **never** be presented as chain fact | `ARCHIVE`; `AUDIT_14` method |
| SR-25 | Missing/unknown ≠ zero; unknown inventory, coverage or health must be represented as unknown | `ARCHIVE` (`baseline`, "unknown is not zero") |
| SR-26 | Every gate artefact must **bind to bytes** (DB SHA-256 + source snapshot id) | `MSG-4` (D-9 accepted R9) |
| SR-27 | Corrections are permitted and must be **preserved as corrections**, never by editing the original | `MSG-3` (D-2) |
| SR-28 | **Do not ask the owner for routine approvals during a preparation stage** | `MSG-5` verbatim |

---

## 5. Mapping to the implementation invariants (`MCD-01` §3)

| MCD-01 invariant | Covered by |
|---|---|
| INV-01 paper-only permanently | SR-01, SR-03, SR-04 |
| INV-02 `allowed()` false for non-synthetic | SR-05 |
| INV-03 no signing / GET-only | SR-06 |
| INV-04 no runtime DB mutation | SR-09, SR-10 |
| INV-05 no app/worker start | SR-11 |
| INV-06 no wallet query / no real network | SR-12, SR-13 |
| INV-07 synthetic ≠ chain fact | SR-24 |
| INV-08 missing ≠ zero | SR-25 |
| INV-09 evidence additive | SR-22, SR-27 |
| INV-10 artefacts bind to bytes | SR-26 |
| INV-11 register append-only | SR-22 |

**All eleven invariants now trace to an owner-transmitted requirement.** GOV-01's completeness gap is closed
for the categories above. `MCD-01` §3 no longer rests on reconstruction.

---

## 6. What remains genuinely unknown (honest residual)

The two surviving `DIRECTIVE` bullets are verbatim; everything else is `MSG-n`/`ARCHIVE`/`DERIVED`. Therefore:

1. **I cannot certify that this set is exhaustive of the original directive's §2.** If the missing tail
   contained a requirement in a category not represented above — for example an operational cadence, a
   specific review body, or a prohibition on a class of activity not listed — it is **not** captured here and
   I have no way to detect its absence.
2. **The gap is one-directional and safe:** any missing requirement is more likely to be *additional*
   restriction than permission. Nothing here is permissive, so a missing item cannot have widened authority.
3. **The owner should confirm exhaustiveness** by comparing §4 against their own copy of the directive. This
   is the one item that only the owner can close — recorded as **GOV-13** (OPEN, non-blocking for the external review)
   (a reviewer assesses the *system*, not the completeness of my transcription) but blocking for the claim
   "the safety requirement set is complete".
4. `DIRECTIVE` items were received as prose bullets, not numbered requirements; the SR-xx numbering is mine,
   added for citation stability, and carries no authority of its own.

---

## 7. Effect on this stage

| Item | Before | After |
|---|---|---|
| GOV-01 (safety list completeness) | BLOCKED | **CLOSED for all categories in §4**; residual exhaustiveness = GOV-13 |
| `MCD-01` §3 provenance | reconstructed | **owner-sourced** (§5) |
| TD-01 historical record | preserved | **preserved, unmodified** |
| Any restriction | — | **none relaxed**; §4 adds SR-03, SR-05, SR-06, SR-21–27 as explicit, previously implicit |
| New prohibitions introduced | — | **none**; SR-03 is entailed by SR-01+SR-02, and every other row restates an existing binding |

---

*Supplemental and authoritative. Supersedes no historical document. The truncation is preserved, not repaired.*
