# Consistency and Integrity Check — Final Package (D-12)

**Purpose.** Evidence that the external-review package agrees with itself, that its
numbers are reproducible, and that no document overstates the governance state.
This document records **measured output**, not assertions. Every figure below was
produced by a script run against the files in this directory and against a fresh
execution of the acceptance suite; nothing is copied from an earlier claim.

**Run date:** 2026-11-05 · **Stage:** D-12 (consolidated external-review preparation)
**Governance state at time of check:** Phase 0 **NOT SATISFIED** · Phase 1A / G1–G5 **NOT AUTHORISED** · suite **PROVISIONAL** · **no source, DB, or migration action taken.**

---

## 0. Defects found by this check, and their disposition

A consistency check is only worth publishing if it reports what it caught. Seven
inconsistencies were found in this stage and all seven were corrected as they were
found, so that this document describes a package that no longer contains them. The reader should treat the counts in §1–§9 as the post-fix
state, and should be able to re-derive each one.

| # | Defect found | Where | Fix applied |
|---|---|---|---|
| C-1 | `CONSISTENCY_CHECK.md` referenced by three documents but never written | `MCD-01` §, `MCD-04`, `MCD-05` §5h | this document created |
| C-2 | `GOV-01` still rendered **BLOCKED on owner** after D-12 closed it | `MCD-01` §8, `MCD-04` §8 | both rows rewritten to **CLOSED** by D-12 → `MCD-08`, residual = GOV-13 |
| C-3 | `GOV-09` still rendered **OPEN** although D-12 closed the design portion | `MCD-01` §8, `MCD-04` §8, `MCD-06` | split into **design CLOSED** (`MCD-09`) / implementation gated by G2 |
| C-4 | `GOV-02` status word inconsistent between registers (`BLOCKED` vs `OPEN`) | `MCD-01` §8 | normalised to **OPEN (blocker 1)** |
| C-5 | `MCD-08` §"residual" sentence opened a parenthetical it did not close | `MCD-08` | corrected to **GOV-13 (OPEN, non-blocking)** |
| C-6 | `MCD-02` legend row could be miscounted as a 36th criterion | `MCD-02` | explicit count note added beside the legend |
| C-7 | `MCD-01` §8 register omitted `GOV-07` and `GOV-11` while calling itself the governance register | `MCD-01` §8 | both rows added; all 15 GOV IDs (01–15) now enumerated in one place |

**Two apparent defects were investigated and found to be artefacts of the checking
script, not of the package** — recorded here so a reviewer running a similar grep
does not chase them:

- `GOV-13` appearing to read "CLOSED". It is genuinely **OPEN**. The false reading came
  from a naive adjacent-line grep: the `GOV-01` row two lines earlier ends with the
  words "residual exhaustiveness = GOV-13", and a line-oriented matcher associated the
  `CLOSED` on that row with the `GOV-13` token. Confirmed by per-row enumeration (§5).
- `MCD-02` appearing to hold 31 criteria. It holds **35**. An early pattern required a
  backticked test name and silently skipped the four `F-xx` rows written in a slightly
  different cell style. Fixed pattern → exact 35/35 match with the suite (§2).

---

## 1. Document inventory

Thirteen Markdown files, all present, all non-empty:

| Document | Lines | Bytes | Role |
|---|---:|---:|---|
| `README.md` | 140 | 11 119 | entry point |
| `MCD-01.md` | 631 | 38 826 | dossier, gate state, blocker register |
| `MCD-02.md` | 516 | 45 492 | the 35 criteria |
| `MCD-03.md` | 170 | 8 490 | A14-08 correction record |
| `MCD-04.md` | 340 | 20 023 | decision register D-1…D-12, TD-01 |
| `MCD-05.md` | 229 | 12 789 | external-review handover package |
| `MCD-06.md` | 171 | 10 500 | R1–R10 disposition register |
| `MCD-07.md` | 112 | 6 097 | authoritative 1A–1H ↔ G1–G6 cross-reference |
| `MCD-08.md` | 164 | 10 004 | **authoritative** safety requirements SR-01…SR-28 |
| `MCD-09.md` | 317 | 17 185 | G2 additive schema design (design only) |
| `MCD-10.md` | 108 | 5 987 | environment / version pinning |
| `MCD-11.md` | 129 | 7 894 | reviewer checklist A–I |
| `CONSISTENCY_CHECK.md` | 206 | 10 667 | this document |

## 2. Criteria: the 35 are the same 35 everywhere

| Check | Result |
|---|---|
| Rows in the `MCD-02` numbered register, numbered 1…35 | **35**, contiguous |
| Distinct test names in that register | **35** (no duplicates) |
| Cases executed by the suite | **35** |
| Register names ≡ suite names (set equality) | **True** |
| Finding ID agrees per test name | **True**, for all 35 |
| Distribution by finding | A14-01 ×6, A14-02 ×4, A14-03 ×3, A14-04 ×2, A14-05 ×2, A14-06 ×4, A14-07 ×4, A14-08 ×2, A14-09 ×1, A14-10 ×3, F-02 ×1, F-03 ×1, F-04 ×1, F-05 ×1 |

The count is therefore not merely asserted in prose: the criterion register, the
executed suite, and the results JSON are the same 35 items in the same order.

## 3. Red-phase execution (re-run for this check)

Executed against the pre-fix snapshot, under a socket-blocking harness, in the
writable copy (`runE`) — never against the immutable input.

| Measure | Value |
|---|---|
| `TOTAL` | **35** |
| `PASS` | **0** |
| `FAIL` | **35** |
| `phase` | **RED** |
| Distinct case results | `{FAIL}` only — no ERROR, no accidental PASS |
| Exit code | non-zero (expected) |

`phase=RED` with `PASS 0 / FAIL 35` is the **required** outcome for a pre-fix
snapshot. A green run here would mean the suite does not test the findings.

## 4. Immutable input integrity

| Measure | Value |
|---|---|
| Archive SHA-256 | `f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23` |
| Files in extraction manifest | **156** |
| Hash mismatches against manifest | **0** |
| Files written inside the extraction tree | none |

The reviewed snapshot is unmodified. All execution occurred in the separate
writable copy.

## 5. Governance register — per-row enumeration

Status derived per row, not by adjacency:

| ID | Status |
|---|---|
| GOV-00 | external-review blocker (G6 scope; not a package defect) |
| GOV-01 | **CLOSED** by D-12 → `MCD-08` |
| GOV-02 | **OPEN** — blocker 1 |
| GOV-03 … GOV-07 | **OPEN** |
| GOV-08 | **CLOSED** (D-9) |
| GOV-09 | **design CLOSED** (`MCD-09`) · implementation OPEN, gated by G2 |
| GOV-10 | **OPEN** |
| GOV-11 | **CLOSED** (32→35) |
| GOV-12 | **CLOSED** (D-11) |
| GOV-13 | **OPEN**, non-blocking (owner: confirm SR exhaustiveness) |
| GOV-14 | **OPEN**, decision required at G2 (`capture_frontiers` PK) |
| GOV-15 | **OPEN** (cross-version parity unverified) |

No row claims a closure that another document contradicts. `GOV-00` is tabulated
only in the findings inventory (`MCD-01` §, `MCD-07` G6); it is not a governance
item requiring closure by this package.

## 6. Safety-requirement provenance (MCD-08)

| Primary tag | Count | Rows |
|---|---:|---|
| `DIRECTIVE` | 2 | SR-01, SR-02 |
| `DERIVED` | 1 | SR-03 |
| `MSG-n` | 19 | SR-04, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 26, 27, 28 |
| `ARCHIVE` | 6 | SR-05, 06, 21, 22, 24, 25 |
| **UNTAGGED** | **0** | — |

- SR identifiers are **contiguous SR-01…SR-28**, no gaps, no duplicates.
- **12 rows carry more than one distinct tag** (e.g. SR-09 `MSG-5` + `ARCHIVE`,
  SR-15 `MSG-3` + `MSG-4` + `MSG-5`). These are counted once, under the strongest
  applicable tag, in the table above; the full multi-tag provenance is preserved
  in each row. A reviewer should read the table as *primary* attribution.
- **0 untagged rows.** Every requirement traces to owner-transmitted text or the
  sealed archive; nothing was reconstructed from memory or inference.

## 7. Historical record preserved (TD-01)

| Check | Result |
|---|---|
| `AUDIT_REPORT_INDEP-AUDIT-01.md` unmodified vs Git HEAD | **yes** (no diff) |
| Directive §2 truncation still present as transmitted | **yes** — quoted verbatim, ending at "No live trading," |
| Truncation explained rather than silently completed | **yes** — `MCD-04` TD-01; `MCD-08` §provenance |
| Missing text reconstructed or inferred anywhere | **no** |
| Missing text used to relax any restriction | **no** |

`MCD-08` expands the safety set **only** from owner-transmitted text and the
archive. Where the original directive was longer than what was transmitted, that
gap is stated as a gap (GOV-13), not filled.

## 8. No document overstates the governance state

All 25 statements in the package that mention authorisation or gate state were
enumerated. Every one reads **NOT SATISFIED** / **NOT AUTHORISED**, or describes a
hypothetical future state ("Phase 0 is satisfied **only** when…", "**APPROVE** would
mean…"). Three lines use the phrase "Phase 0 is satisfied" and all three were
inspected in context:

| Location | Verdict |
|---|---|
| `MCD-04` §6 | conditional — lists what *would* have to exist; not a claim |
| `MCD-05` §verdict options | reviewer-facing definition of what an APPROVE verdict *would* mean |
| `MCD-11` §I | same, in the checklist's sign-off guidance |

None asserts a satisfied gate. Decision register spans **D-1…D-12**, contiguous.

## 9. Claimed-but-not-performed — declared limitations

Stated so the reviewer does not have to discover them:

| Item | Status |
|---|---|
| Migration written, run, or tested | **No** — `MCD-09` is design only; no DDL executed |
| Runtime database opened, written, migrated, backed up | **No** |
| Application, worker, or collector started | **No** |
| Wallet queried; external trading connection opened | **No** |
| Patch authored or applied to product source | **No** — suite is red-phase against the pre-fix snapshot |
| G1–G5 implemented | **No** — all five NOT AUTHORISED |
| Cross-version parity (Python 3.13.16 / SQLite 3.46.1 vs measured 3.11.2 / 3.40.1) | **Not proven** — reasoned unlikely to change results; GOV-15 |
| `capture_frontiers` primary-key defect resolved | **No** — cannot be fixed additively; GOV-14 |
| SR-set exhaustiveness against the original directive | **Not confirmed** — only the owner can; GOV-13 |
| Authors' environment reproduced exactly | **No** — versions differ; `MCD-10` documents the divergence |

## 10. Verdict of this check

**The package is internally consistent in every dimension measured above**, after
seven corrections (C-1…C-7). No contradiction remains between the criterion count,
the executed suite, the results file, the governance registers, the decision
register, and the safety-requirement set.

**This is a consistency result, not an approval.** It says the package does not
contradict itself. It does **not** say the criteria are correct, sufficient, or
independent — that is the external reviewer's judgement (GOV-02), and it is
outstanding. Phase 0 remains **NOT SATISFIED**; G1–G5 remain **NOT AUTHORISED**.
