# MCD-05 — External review package and instructions

**Document ID:** `MCD-05` · **Status:** package ready, reviewer not yet engaged (GOV-02 BLOCKED)
**Purpose:** let a reviewer **genuinely outside** the Arena.ai Agent Mode stack reach an independent
conclusion about CopyLab's Phase 0 in a few hours, not weeks.
**This document is not a substitute for that review.** `INDEP-AUDIT-01` §2 explains why my own work cannot
close it.

---

## 1. Why an outside reviewer is mandatory (not a formality)

Three independent reasons, any one of which would suffice:

1. **Structural.** `INDEP-AUDIT-01` was produced in the same harness that produced Audit 14. The project's own
   master plan (§4, §8-1) forbids self-certification and forbids substituting "an agent, a subprocess, a
   locally written verifier, a synthetic fixture or a different speaking style" for independence.
2. **Demonstrated fallibility.** I overstated a LOW finding in my own report (`MCD-03`). If I can inflate one
   finding in the direction that sounds more serious, a reviewer must assume I may have done so in the other
   48 cases.
3. **Adversarial value.** A reviewer trying to *break* my findings is worth more than one confirming them. The
   single most useful output of this review is a case I got wrong.

---

## 2. The package (what to hand over)

Everything is in this repository. **Nothing needs to be assembled.**

| # | Artefact | Path | Why the reviewer needs it |
|---|---|---|---|
| 1 | Sealed source under review | `copylab-external-review (1).zip` + `-SHA256.txt` | the artefact itself; nothing else is authoritative |
| 2 | Transfer instructions | `copylab-external-review-INSTRUCTIONS.md` | safe extraction script, exclusion list, known limits |
| 3 | Independent audit | `AUDIT_REPORT_INDEP-AUDIT-01.md` | 49 reproduced cases, new findings, H01–H05 assessment |
| 4 | Coordination dossier | `MASTER_COMPLETION/MCD-01.md` | consolidated plan, 6 groups, G6 external programme, blockers |
| 5 | **35 acceptance criteria** | `MASTER_COMPLETION/MCD-02.md` | per-test root cause, pre-fix result, post-fix condition |
| 5b | **R1–R10 disposition register** | `MASTER_COMPLETION/MCD-06.md` | what was accepted/amended, incl. R4/R5 restatements |
| 5c | **Group cross-reference** | `MASTER_COMPLETION/MCD-07.md` | resolves 1A–1H ↔ G1–G6 (read this before assessing ordering) |
| 6 | **A14-08 correction record** | `MASTER_COMPLETION/MCD-03.md` | the claim I withdrew, and why |
| 7 | Decisions ledger | `MASTER_COMPLETION/MCD-04.md` | gate state, TD-01, what counts as Phase 0 satisfied |
| 8 | **Executable red suite** | `MASTER_COMPLETION/tools/acceptance_suite.py` | 32 tests, each asserting a safe invariant |
| 9 | **Red-phase result** | `MASTER_COMPLETION/evidence/red-phase-results.json` | 35/35 FAIL, with per-case detail |
| 10 | Probe corpus (49 cases) | `MASTER_COMPLETION/evidence/probes/` | my reproduction scripts |
| 11 | Probe outputs | `MASTER_COMPLETION/evidence/results/` | hashed, as run |
| 12 | **Reproduction guide** | `MASTER_COMPLETION/tools/REPRODUCE.md` | exact commands, isolation, expected output |
| 13 | Artefact hashes | `MASTER_COMPLETION/evidence/ARTEFACT_MANIFEST.json` | integrity of the package itself |

**Deliberately absent** (do not ask the reviewer to work around this): runtime databases, `.git`, wallet
addresses, chain identifiers, real market data, Playwright binaries. Runtime DB export requires **separate
owner approval** per the archive's own instruction. The reviewer must **not** substitute the live runtime DB.

---

## 3. Reviewer task list (≈ half a day, mostly mechanical)

Ordered so each step is cheap and falsifiable. Steps 1–4 are essential; 5–7 are judgement.

### Step 1 — Verify the artefact (2 min)

```bash
sha256sum copylab-external-review.zip
# expect f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23
```
Extract with the archive's own script (`INSTRUCTIONS.md` §2; it validates paths, duplicates, symlinks and
re-verifies all 157 members). Then make a **second** disposable copy for execution.

*Report:* hash match yes/no; member count; anything that surprised you.

### Step 2 — Run the project's own test suite (2 min)

```bash
cd <work-copy> && python3 -m unittest discover -s tests -q     # expect 119 tests, OK
```

*Report:* the count you observed. **Then read `F-01` in `INDEP-AUDIT-01` §7 and decide whether a 119/119
pass is evidence of anything relevant.** This is the single most consequential judgement in the review, because
every gate in the existing plan cites it.

### Step 3 — Run the red suite (5 min)

Follow `tools/REPRODUCE.md` §3–§5 (offline isolation first, then the suite).

```
EXPECTED: TOTAL 35  PASS 0  FAIL 35  -> phase=RED
```

Exit code **1** is correct and expected. **If any test passes, stop and report:** either the snapshot drifted
or the test is defective. A test that passes pre-fix is a suite defect, not good news.

*Report:* your counts and phase. Diff against `evidence/red-phase-results.json`.

### Step 4 — Attempt to falsify the 49 probe cases (30–60 min)

Run the three probe scripts (`REPRODUCE.md` §7). Then pick the cases you find least convincing and try to
break them — especially:
- cases where my probe writes directly into tables rather than through the application API (is the tamper
  even reachable in practice?);
- `A14-06` variants that depend on how I modelled `PublicClient.get`'s contract;
- `A14-09`, where I substituted jsdom for Chromium (**I did not run Playwright**; this is my weakest
  substitution).

*Report:* cases you could break, and whether the *finding* survives or the *demonstration* failed. These are
different outcomes and both matter.

### Step 5 — Adjudicate the A14-08 correction (15 min)

Run the script in `MCD-03` §5(b). Decide: is the corrected finding (BLOB-vs-repr-text only, numeric claim
withdrawn) **right**, or did I over-correct? Note that `MCD-03` §5(c) preserves the *wrong* version so you can
see exactly how the error arose.

*Report:* confirm, or reject with the measurement that shows otherwise.

### Step 6 — Assess H01–H05 and the G1–G6 ordering (30 min)

| Question | Where |
|---|---|
| Are H01–H05 correctly **BLOCKED** (i.e. not closable with local evidence)? | `AUDIT_REPORT_INDEP-AUDIT-01.md` §8.1 |
| Is G1→G2→G3 ordering right? Specifically: is it correct that the digest (G1) and lock (G1) must be fixed before the evidence instruments (G2)? | `MCD-01` §4 |
| Is it correct that G4 (synthetic semantics) comes *after* groups with production reach? | `MCD-01` §4 |
| Are R1–R10 the right ten plan revisions? Is any unnecessary, or is one missing? | `MCD-01` §2.2 |
| Is G6 genuinely external, or is anything in it locally obtainable? | `MCD-01` §4 G6 |

### Step 7 — Sign (5 min)

One of exactly three, in `§4` below. No conditional "looks fine" — the project needs a decision it can gate on.

---

## 4. Signature block

```
Reviewer / organisation : ______________________________________
Relationship to CopyLab : [ ] never involved  [ ] previously consulted  [ ] other: __________
Independence basis      : [ ] outside Arena.ai Agent Mode  [ ] other: __________
Date                    : ______________
Snapshot verified       : [ ] SHA-256 matched   Member count: ______
Own test run 119/119?   : observed count ______  Assessment of F-01: ____________________
Red suite result        : PASS ____  FAIL ____   Phase: ______   (expected 0 / 35 / RED)
Probe cases falsified   : ______________________________________________
A14-08 correction       : [ ] CONFIRMED  [ ] REJECTED (evidence attached)
H01-H05 BLOCKED         : [ ] AGREE  [ ] DISAGREE (which: ______ )
G1-G6 ordering          : [ ] AGREE  [ ] REVISE (which: ______ )
R1-R10                  : [ ] AGREE  [ ] REVISE (which: ______ )

DECISION (exactly one):
  [ ] APPROVE FOR BOUNDED PHASE 1A
  [ ] REVISE PLAN  — required changes: ______________________________________
  [ ] BLOCK        — reasons: _______________________________________________

Signature: ______________________
```

**What each decision means operationally:**

- **APPROVE FOR BOUNDED PHASE 1A** — Phase 0 is satisfied; the owner may then grant the single programme
  authorisation in `MCD-04` §7. It does **not** authorise runtime activation, wallets or real money.
- **REVISE PLAN** — Phase 0 not satisfied; the specific revisions are binding inputs to a re-review.
- **BLOCK** — Phase 0 not satisfied and the reviewer believes the plan or the findings are unsound in a way
  that revision cannot fix.

---

## 5. What the reviewer must NOT be asked to do

Stated so nobody pressures them later:

- **Do not** accept `INDEP-AUDIT-01` or `MCD-01` as evidence. They are the *thing under review*.
- **Do not** treat the 35/35 red result as a pass — it is a demonstration that the system is currently unsafe.
- **Do not** rely on the archived `adversarial-results.json` without re-running; it is the implementation
  authors' own script.
- **Do not** open the runtime databases. If the review needs them, escalate for separate approval.
- **Do not** start the application, worker, server or collector to "see it work".
- **Do not** accept a substituted signature (another agent, a subprocess, a restyled report). This is the one
  requirement the entire gate exists for.
- **Do not** sign `APPROVE` to unblock a schedule. `REVISE PLAN` and `BLOCK` are legitimate, expected outcomes.

---

## 6. Known limitations the reviewer should not have to discover alone

| # | Limitation | Impact on the review | Disclosed at |
|---|---|---|---|
| L1 | A14-09 reproduced in **jsdom**, not Chromium (Playwright absent, not installed) | evidence about rendering *logic*, not browser behaviour | `INDEP-AUDIT-01` §3 |
| L2 | Environment divergence: I ran Python 3.11.2 / SQLite 3.40.1 vs documented 3.13.16 / 3.46.1; no requirements file | cross-version parity unpinned | `MCD-01` App. B |
| L3 | Runtime DBs never inspected (by design) | their integrity is an **unverified claim** from my position | `INDEP-AUDIT-01` §10 |
| L4 | Git state unverifiable — no `.git` in the archive | HEAD/working-tree claims are internal-consistency only | `INDEP-AUDIT-01` §10 |
| L5 | I corrected one of my own findings (A14-08) | other findings deserve the same scepticism | `MCD-03` |
| L6 | Suite found 6 defects in itself (3 false green, 1 false red) | the harness is now validated, but a new case could still be wrong | `MCD-01` §5.3 |
| L7 | Directive §2 truncated (TD-01) | invariant set is reconstructed, possibly incomplete | `MCD-04` §3 |

---

## 7. After the signature

| Reviewer decision | Next action | Authority |
|---|---|---|
| APPROVE | Owner may grant the single programme authorisation (`MCD-04` §7) | owner |
| REVISE PLAN | Revisions become binding inputs; re-review only the changed parts | owner + implementer |
| BLOCK | Findings/plan reworked; no implementation; re-review from scratch | implementer |

**In all three cases:** no runtime migration, no app/worker start, no wallet query, no real-money capability.
Those remain separately gated no matter what the reviewer signs (`INV-01`, `INV-04`, `INV-05`).

---

## 8. Current package readiness

| Requirement | State |
|---|---|
| Sealed artefact hash-verifiable | ✔ |
| Reproduction path documented and tested | ✔ (35/35 red reproduced) |
| Per-test root cause + acceptance condition | ✔ 35/35 (`MCD-02`) |
| Own correction disclosed and reproducible | ✔ (`MCD-03`) |
| Limitations disclosed | ✔ 7 items above |
| Signature block with defined decisions | ✔ §4 |
| Reviewer engaged | **✘ GOV-02 BLOCKED — owner action** |
| Phase 0 satisfied | **✘ NOT SATISFIED** |

**Package is ready. The gate is not.**
