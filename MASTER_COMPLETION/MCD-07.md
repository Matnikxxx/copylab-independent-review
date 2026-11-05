# MCD-07 — Group numbering cross-reference (authoritative)

**Document ID:** `MCD-07` · **Status:** AUTHORITATIVE in this package · **Append-only**
**Resolves:** GOV-12 — the 1A–1H / G1–G6 numbering ambiguity
**Rule:** **both numbering schemes remain valid and neither is renumbered.** The project's
`MASTER_REMEDIATION_PLAN.md` owns `1A–1H`; this package owns `G1–G6`. This table is the single mapping. Any
document in this package that names a group **must** resolve through this table.

---

## 1. Why there are two schemes (so no one "fixes" it)

| Scheme | Owner | Scope | Why it exists |
|---|---|---|---|
| **1A–1H** | the project (`MASTER_REMEDIATION_PLAN.md` §6) | eight engineering groups | the project's own plan predates this audit; renumbering it would break every cross-reference in its register and evidence |
| **G1–G6** | this package (`MCD-01.md` §4) | six groups, incl. a non-local one | the audit found that the 1A–1H set needs reordering (R6/R7) and a distinct external group (G6) that 1A–1H does not have |

**Deliberate choice:** I did **not** renumber the project's plan. Doing so would have silently rewritten an
artefact under review — a violation of `INV-09`/`INV-11` (evidence and register are append-only). Instead both
schemes coexist and this table binds them. The cost is one extra lookup; the benefit is that the project's own
plan stays auditable in its original numbering.

---

## 2. The mapping (authoritative)

| G-group (this package) | Plan group (project) | Findings | Criteria | Depends on | Local? |
|---|---|---|---|---|---|
| **G1** | **1A** — SQLite digest & startup ownership | A14-08, A14-10, F-06, F-03* | #23 #24 #26 #27 #28 (+F-06 new) | — | yes |
| **G2** | **1B** + **1E** + **1F** + **1G** | A14-02, A14-05, A14-06, A14-07, F-04, F-05 | #7–#10 #16 #17 #18–#21(+2) #31 #32 | G1 | yes |
| **G3** | **1C** | A14-01, F-02, F-03 | #1–#6 #29 #30 | G2 | yes |
| **G4** | **1D** | A14-03, A14-04 | #11–#15 | G3 | yes (synthetic only) |
| **G5** | **1H** | A14-09, F-06† | #25 (+F-06) | G4 | yes |
| **G6** | *(none — no plan equivalent)* | H01–H05, GOV-00, SAFE-02, SRC-01…03, LIFE-01…03, GAP-01, COPY-01/02, EXEC-01/02, STRAT-01…03, RISK-01, UI-01, SEC-01, OPS-01…03, FINAL-01/02, DOC-01, GOV-01/02 | n/a — no local test | G1–G5 + external evidence | **NO** |

\* **F-03** appears in G1 and G3 because it is a *tooling* defect (`audit.py` fails open) whose fix is trivial
and whose absence undermines every artefact G3 produces. It is repaired early (G1) and *verified* in G3.
† **F-06** (default-deny HTTP verbs) appears in G1 and G5 for the same reason: hardened early, verified with the
UI work.

**Deliberate one-to-many cases are flagged, not hidden.** A finding appearing in two groups is a *scheduling*
decision (fix early, verify late), not double-counting. Each criterion still has exactly one owning group in
`MCD-02`'s Group column.

---

## 3. Expanded view: plan groups in their own numbering

| Plan group | Title (from `MASTER_REMEDIATION_PLAN.md` §6) | Maps to | Notes |
|---|---|---|---|
| 1A | SQLite digest and startup ownership | **G1** | absorbs R6 (lock canonicalisation, Store-level ownership) and R10 (default-deny verbs) |
| 1B | Complete source-journal coverage | **G2** | A14-02; needs bidirectional row/effect coverage |
| 1C | Full paper accounting invariants | **G3** | A14-01; absorbs R7 (snapshot equity, closed cycles) |
| 1D | Synthetic SPLIT/REDEEM semantics | **G4** | A14-03/04; absorbs R8 (zero-basis, n-way, negative cash) |
| 1E | Append-only certificate conflicts | **G2** | merged per R3 — same append-only evidence table as F-04 |
| 1F | Durable per-attempt transport evidence | **G2** | A14-06; **restated per R4** (see `MCD-06` §2) |
| 1G | Immutable collection scope | **G2** | A14-07; **restated per R5** (see `MCD-06` §3) |
| 1H | Honest health state | **G5** | A14-09 |

**Note the collapse:** plan groups 1B, 1E, 1F, 1G all map into **G2**. That is the consequence of R3 plus the
observation that A14-05/06/07 are one problem class — *evidence fidelity in the collection layer* — and share a
schema. Splitting them across four plan groups would have invited four migrations to the same tables.

---

## 4. Execution order (authoritative)

```
G1  (=1A)                      foundations: instruments must be trustworthy
 │
G2  (=1B+1E+1F+1G)             evidence fidelity: every byte durable, every scope immutable
 │
G3  (=1C)                      accounting proof: verifier authority over the full ledger
 │
G4  (=1D)                      semantic proof: operation-complete lifecycle (synthetic only)
 │
G5  (=1H)                      truthful UI
 │
G6  (no equivalent)            EXTERNAL evidence programme — not schedulable locally
```

**All groups NOT AUTHORISED.** G1 explicitly withheld (`MCD-04` D-5); G1–G5 withheld (D-10, this run).

---

## 5. Terminology discipline (how to avoid reintroducing the ambiguity)

| When you mean… | Write | Never write |
|---|---|---|
| a group in this package | `G2` | "1G" (that is one *component* of G2) |
| a group in the project's plan | `plan 1A` or `1A` with the word *plan* | "G1" when you mean plan 1A |
| a group cited inside another group | `G2 (plan 1F)` | bare `1F` |

**Practical rule for the external reviewer:** if you see `1X`, it is the project's numbering and this table gives
you the G-equivalent. If you see `GX`, it is this package's. No document in this package uses `1X` without the
word *plan* nearby, except in direct quotations.

---

## 6. Where each scheme is defined

| Scheme | Definition | Status |
|---|---|---|
| 1A–1H | `MASTER_REMEDIATION_PLAN.md` §6 (inside the sealed archive) | project's own; **not modified** |
| G1–G6 | `MCD-01.md` §4 | this package's |
| mapping | **this document** | authoritative |
| criteria ownership | `MCD-02.md` Group column | one group per criterion |

---

*Append-only. If a future reorganisation changes either scheme, it is recorded here as a new section rather
than by editing the tables above.*
