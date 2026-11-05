# MCD-11 — External review checklist

**Document ID:** `MCD-11` · **For:** the reviewer · **Package:** `MASTER_COMPLETION/` + `AUDIT_REPORT_INDEP-AUDIT-01.md`
**Rule:** each box is either **ticked with your own observed output** or **explicitly not done, with a reason**.
Unticked-and-unexplained is not acceptable; ticked-without-output is not acceptable.

---

## A. Artefact integrity — must be reproduced (≈3 min)

- [ ] **A1** Archive SHA-256 = `f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23`
      → your command, your output: ____________________
- [ ] **A2** Extraction yields **157** members; the archive's own script reports
      `Verified 157 archive members; no application code executed.`
- [ ] **A3** Post-extraction manifest re-verification: **156/156, 0 mismatches**
- [ ] **A4** `MASTER_COMPLETION/evidence/ARTEFACT_MANIFEST.json` hashes match the files you received (22 artefacts)
- [ ] **A5** Record any file whose hash does **not** match — do not proceed silently past a mismatch

## B. The project's own baseline — must be reproduced (≈3 min)

- [ ] **B1** `python3 -m unittest discover -s tests -q` → record exact count: ______ (expected 119)
- [ ] **B2** Run it again with outbound sockets blocked; record count: ______
- [ ] **B3** **Judge F-01** (`INDEP-AUDIT-01` §7): is a 119/119 pass evidence for any of the 35 audited
      properties? Your position, with reasoning: ______________________________

## C. The 35 criteria — must be reproduced (≈10 min)

- [ ] **C1** Run `tools/acceptance_suite.py` per `tools/REPRODUCE.md` §3–§5
      → `TOTAL ____ PASS ____ FAIL ____ phase ______` (expected 0 / 35 / RED, exit code 1)
- [ ] **C2** Diff your results against `evidence/red-phase-results.json`; report any case where you differ
- [ ] **C3** For **any test that PASSES**, stop and report it as a **suite defect** — a criterion must not pass
      pre-fix
- [ ] **C4** Distinguish `ERROR` from `FAIL` in your report (an ERROR can be a *false red*, e.g. missing jsdom)
- [ ] **C5** Confirm the two R4 codes are real: #19 (identical bodies not deduplicated) and #21 (200-then-timeout
      keeps the 200)
- [ ] **C6** Confirm the two R5 codes are real: #22 (reject-or-fork with `allowed()` never called) and #24
      (explicit populated scope identity)

## D. Falsification — the most valuable part (≈60 min)

- [ ] **D1** Run the three probe scripts (49 cases); record your counts: ______
- [ ] **D2** Attempt to **break** at least these three, and report honestly:
      - `A14-06` — my model of `PublicClient.get`'s contract (is the exception path reachable as I model it?)
      - `A14-09` — jsdom vs Chromium (**my weakest substitution**; Playwright was never installed)
      - `A14-02` — probes insert rows directly rather than through the application API (is the tamper reachable?)
- [ ] **D3** For each case you break, state whether the **finding** survives or the **demonstration** failed
      (different outcomes, both useful)
- [ ] **D4** Report any case where my probe asserts more than the evidence supports

## E. The audit's own correction — must be adjudicated (≈15 min)

- [ ] **E1** Run the script in `MCD-03` §5(b); confirm output matches across all five affinities
- [ ] **E2** Decide: is the corrected A14-08 finding (**BLOB-vs-repr-text only**; numeric claim **withdrawn**)
      correct, or did I over-correct? → [ ] CONFIRMED  [ ] REJECTED (attach measurement)
- [ ] **E3** Note that `AUDIT_REPORT_INDEP-AUDIT-01.md` §6/§9 were **left unedited** and the correction is
      appended. Confirm this is adequate preservation, or require more.

## F. Documents that must be inspected, not merely accepted

- [ ] **F1** `MCD-08` — are the owner-approved safety requirements (SR-01…SR-28) correctly categorised, and is
      anything **more restrictive** than the sources support (over-restriction is also a defect)?
- [ ] **F2** `MCD-09` — assess the proposed additive schema. Specifically:
      - is `scope_hash` exclusion of `cursor`/`page_number` correct for resumability?
      - is the **partial unique index** on `(wallet, endpoint, scope_hash)` sound?
      - do you agree that `capture_frontiers` **cannot** be fixed additively (GOV-14)?
      - do you accept the §0 claim that **A14-08 blocks G2** (an added column changes the whole-row digest)?
- [ ] **F3** `MCD-10` — is the version-divergence impact analysis (§3) sound, or did I dismiss a real risk?
- [ ] **F4** `MCD-06` — are the R4/R5 amendments correctly encoded as criteria (not merely reworded)?
- [ ] **F5** `MCD-07` — does the 1A–1H ↔ G1–G6 mapping hold, and is the G1→G2→…→G6 ordering justified?
- [ ] **F6** `MCD-01` §4 — is **G6 genuinely external**, or is any part of it locally obtainable?
- [ ] **F7** `MCD-01` §10 — are milestones B and C correctly judged as **not locally achievable**?

## G. Findings and classification

- [ ] **G1** For each of A14-01…A14-10: CONFIRMED / REJECTED / RECLASSIFIED, with your own severity
- [ ] **G2** For F-01…F-05 (new findings in `INDEP-AUDIT-01` §7): accept, reject or reclassify
- [ ] **G3** Assess H01–H05 **BLOCKED** classifications: [ ] AGREE [ ] DISAGREE (which: ______)
- [ ] **G4** Add any defect **we both missed** — the package is not claimed exhaustive
- [ ] **G5** Confirm no finding in this package relies on **real wallet data or live trading** (it must not)

## H. Safety compliance of the package itself

- [ ] **H1** Confirm the snapshot was **not modified** by anyone in the chain (hash A1 + manifest A3)
- [ ] **H2** Confirm **no runtime database** is included and none was opened: [ ] verified
- [ ] **H3** Confirm **no application/worker/collector** was started to produce this evidence: [ ] verified
- [ ] **H4** Confirm `Integrity.allowed()` still returns `False` for non-synthetic DBs (re-read the code; do not
      start anything): [ ] verified
- [ ] **H5** Confirm no signing/order endpoint exists and the client is GET-only against a fixed allowlist

## I. Signature

```
Reviewer / organisation : ______________________________________
Independence basis      : [ ] outside Arena.ai Agent Mode  [ ] other: __________
Relationship to CopyLab : [ ] never involved  [ ] previously consulted  [ ] other: __________
Date                    : ______________
Snapshot SHA-256 verified: [ ] yes   Member count: ______
Environment             : Python ______  SQLite ______  OS ______  Playwright: [ ] yes [ ] no
Suite result            : PASS ____  FAIL ____  ERROR ____  phase ______
Cases I could falsify   : ______________________________________________
A14-08 correction       : [ ] CONFIRMED  [ ] REJECTED (evidence attached)
H01-H05 BLOCKED         : [ ] AGREE  [ ] DISAGREE (which: ______)
G1-G6 ordering          : [ ] AGREE  [ ] REVISE (which: ______)
R1-R10 dispositions     : [ ] AGREE  [ ] REVISE (which: ______)

DECISION (exactly one):
  [ ] APPROVE FOR BOUNDED PHASE 1A
  [ ] REVISE PLAN   — required changes: ___________________________________
  [ ] BLOCK         — reasons: ___________________________________________

Signature: ______________________
```

---

## What "APPROVE" would and would not mean

**Would mean:** Phase 0 is satisfied; the owner may then grant the single bounded programme authorisation in
`MCD-04` §7.

**Would NOT mean, in any reading:** permission to start a runtime migration, start the application, onboard a
wallet, or enable real money. `MCD-08` SR-01/SR-03/SR-09/SR-10/SR-11 are **permanent or separately gated** and
are not within a reviewer's gift.

## If you can only do part of this

Do **A, B, C, E, G1** first — that is the minimum for a defensible decision, and it is under 45 minutes.
Report plainly what you did not do. A partial review with an honest scope is worth more than a full-looking one
that was not actually performed.
