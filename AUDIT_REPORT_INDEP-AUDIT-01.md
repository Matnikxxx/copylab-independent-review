# CopyLab — Independent Technical Audit Report

**Report ID:** `INDEP-AUDIT-01`
**Date:** 2026-11-05
**Subject:** CopyLab working-tree snapshot, reference HEAD `288a69f64c24438cfe69ea176e6f3d6ce7333499` (branch `main`)
**Archive SHA-256:** `f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23` (**verified**)
**Snapshot ID (canonical source inventory hash):** `b4159070b4ebe77a22ada54bd750ef1cd37ddbf08996778813dedfb818c21d6f`
**Report status:** FINAL for this scope. Read-only. No source modified, no fix implemented, no application/worker started.

---

## 1. Verdict

| Question | Answer |
|---|---|
| Do the nine reproduced Audit 14 defects hold up under independent reproduction? | **Yes — all nine CONFIRMED**, four of them with materially broader impact than reported. |
| Is A14-10 (inspection-only, no dynamic test) reproducible? | **Yes — now dynamically reproduced**; the finding is stronger than "static ordering only". |
| Are the H01–H05 parent findings correctly classified BLOCKED? | **Yes**, with one reclassification of A14-06 severity (upward) and one containment claim that is narrower than implied. |
| Is the master remediation plan sound enough to start Phase 1A? | **No — REVISE PLAN.** The plan's proposed test suites would pass with the defects still present. |
| Phase 0 / programme gate | **REMAINS BLOCKED.** Phase 1A is **NOT AUTHORISED** by this report. |
| Am I independent of the implementation agent? | **No, not fully — see §2.** This is a genuine limitation of this report's authority. |

**Recommendation: BLOCK** (with the specific plan revisions in §9).

---

## 2. Independence declaration (read this first)

I must be explicit rather than flattering.

- **I did not write CopyLab, Audit 14, the H01–H05 remediation, or the master plan/register.** In that narrow sense I am a separate reviewer: I found no prior authorship stake and reproduced the findings from the code, not from the authors' prose.
- **I am not an organisationally independent auditor.** I am an agent running in the same Arena.ai Agent Mode harness that the documentation says produced Audit 14 ("Prepared by the same Arena.ai assistant that authored Audit 14"). I share that infrastructure, and the master plan itself observes that no separate reviewer tool is available "in this session." **A different agent instance is not the same thing as an independent third party**, and this report must not be presented to any downstream party as third-party assurance.
- **I cannot certify my own reproducibility as proof of a clean room.** I used the authors' archived signatures as a cross-check *and* wrote my own probes; where my probes were derived from reading their harness, I say so. My probes are in `indy/probes/` (18 + 21 + 12 + 1 cases) and are not copies of `adversarial_checks.py`, but the same author-written source told me where to look.
- **No conflict of interest, no compensation, no stake** in CopyLab's approval or rejection. I was not asked to reach a particular outcome.
- **Practical consequence:** this report can discharge *"the findings were independently reproduced by a separately identifiable reviewer"*. It **cannot** discharge *"genuinely separate review"* as the master plan defines it (Plan §4, GOV-00, FINAL-02). That gate needs a reviewer outside this tooling stack, with a name/organisation accountable for the sign-off. I recommend the user obtain that before any implementation approval.

## 3. Environment and isolation

| Item | Value |
|---|---|
| OS | Linux (Debian-based sandbox), non-root user |
| Python | 3.11.2 (documented preparation environment was 3.13.16 — **version divergence**) |
| SQLite | 3.40.1 (documented: 3.46.1 — **version divergence**) |
| Playwright / Chromium | **Not installed, not installed by me.** A14-09 was reproduced with a different engine (§6, A14-09) |
| Node.js | v22.22.3, `jsdom` installed into `indy/dom/` (review-side only, not in the project) |
| Network | Denied for all project-derived execution via a `sitecustomize.py` socket block on `PYTHONPATH`; verified by an attempted connection that was refused. The single permitted network use was downloading `jsdom` into my own scratch directory, disclosed here |
| Untouched input | `audit-review/stage/copylab-external-review-extracted/` (chmod a-w after extraction); re-hashed after the audit: **0 mismatches** |
| Disposable copies | `runA` (test suite), `runB` (authors' harness), `runC` (my probes); `lab/` byte-identical to the snapshot (verified by diff) |
| Runtime data | **Never read.** No `data/` directory exists in the archive; no SQLite file in any run directory (`find` for `*.sqlite`, `*.lock`, `__pycache__` returned nothing) |
| App/worker | **Never started.** No `serve_forever`, no `App.run()`, no `Collector.cycle()` against a real client, no `main()`. `App.__init__` was constructed twice on disposable DBs solely to measure A14-10 ordering (§6) |
| Wallets/trading | No wallet queried, no key, no signature, no order. The only wallet addresses seen are documentation constants (`0x`+40 hex) and the project's own `0x111…1`/`0x222…2` fixtures |

**Test not run, and why:** the browser reproduction path as supplied (`docs/phase0-audit14/dashboard_probe.py` + `dashboard-stale-health.png`). Playwright is absent and I did not install it (it needs OS provisioning and I judged a second browser engine sufficient for the *rendering* claim). I substituted a real DOM execution of the real `dashboard.html` in jsdom. This is a **substitution, disclosed as a limitation**: it exercises the same renderer code path, but not Chromium's layout/paint, and it is not the authors' harness.

## 4. Input verification

All checks below were performed before trusting any content.

| Check | Result |
|---|---|
| Archive size | 1,239,236 bytes = byte-for-byte the documented size |
| Archive SHA-256 | `f1943…b11c23` — **matches** the checksum file and the instruction page |
| Detached inner manifest hash | `MANIFEST.json` digest `39dd64b6…21b60` — **matches** |
| Members | 157 = `included_file_count`; every member size + SHA-256 re-verified against `MANIFEST.json` |
| Path safety | No absolute paths, no `..`, no backslashes, no symlinks, no `.git` entries, no `data/` entries, no `-wal/-shm/.db/.sqlite` members |
| ZIP CRC | `testzip()` clean |
| `FILE_INVENTORY.csv` | 150 rows: 60 tracked + 90 untracked, `redaction=none` for all; `transfer_sha256`/`original_sha256`/`size` re-computed for all 150 — **0 mismatches** |
| Snapshot metadata | HEAD, branch, `Africa/Johannesburg` timezone, tool clock `2026-11-05T12:02:15Z`, `no_runtime_databases_exported` — consistent with the instruction page |
| Exclusions | 107 files: 104 `.git` internals, 2 protected runtime DBs, 1 worker lock — consistent |
| Post-audit re-hash | **0 mismatches** — the snapshot was not altered by this audit |
| Secret heuristic | Supplied scan reports none; my own independent grep found no private keys, signing libraries, or credential assignments. `tools/audit.py` contains its own `private_key`/`eth_account` string scan. See §7 F-08 for a weakness in *that* scan |

**Repackaging note (not a defect):** the archive distributed is named `copylab-external-review (1).zip`; the checksum file names `copylab-external-review.zip`. I renamed my local copy before hashing. The bytes match, so integrity is unaffected, but the filename divergence should be normalised, since "keep ZIP and checksum together, same name" is part of the documented procedure.

## 5. Reproduction summary

Legend: **CONFIRMED** = I observed the defect myself in a fresh disposable fixture. **BLOCKED** = cannot be resolved with local evidence. **FAILED TO REPRODUCE** = I attempted and did not observe it. All fixtures are symbolic (`T`, `M`, `fixture-wallet`); **no synthetic value is presented as a blockchain fact.**

### 5.1 Authors' harness, re-executed (cross-check only)

I ran `docs/phase0-audit14/adversarial_checks.py` in `runB` (exit 0) and reproduced its exact signatures, including the archived digests (`fe21b3a1…ecad` for A14-08) and the two containment controls. This confirms the archived evidence is not stale relative to the shipped code. It is **not** independent evidence — it is the authors' own script.

### 5.2 Project's own test suite, re-executed

`python3 -m unittest discover -s tests` → **119 tests, 119 pass**, also **119/119 with sockets hard-blocked**. So the 119/119 claim is true and the suite needs no network. It is also **analytically worthless as evidence of correctness for the audited properties** — see §7 F-01.

---

## 6. Findings — Audit 14, each reproduced independently

### A14-01 — Paper verifier does not detect ledger corruption — **CONFIRMED**
**Own severity: HIGH (agree).** Scope is *wider* than reported.

Code: `tools/audit.py` (whole file), `lab/accounting.py:8–36`.
Method: my own probe `indy/probes/p1_a1401_a1402.py`, 10 cases, fresh DB per case, verifier run as a separate process exactly as a reviewer would.

| Case | Tamper | Verifier exit | Verifier errors | Verdict |
|---|---|---|---|---|
| control | clean ledger, BUY+SELL | 0 | `[]` | correct |
| **archived** | `ledger.realized = 999` | **0** | **`[]`** | **CONFIRMED** — reported equity 1003, PnL 1998, identity broken by 995 |
| **new** | `ledger.fee = 55` (cash & realized untouched) | **0** | **`[]`** | **CONFIRMED** — `metrics.fees` reported as 55.00 |
| **new** | `ledger.cost_delta = 12345` | **0** | **`[]`** | **CONFIRMED** |
| **new** | `snapshots.equity = 999999` | **0** | **`[]`** | **CONFIRMED** — equity curve is unverified; it feeds `peak_equity`/drawdown |
| **new** | `closed_positions.proceeds = 99999` | **0** | **`[]`** | **CONFIRMED** — cycle `realized` is never reconciled; it drives `win_rate` |
| control | `DELETE FROM ledger` | 1 | cash mismatch + orphan | correct |
| control | `positions.qty = -5` | 1 | position mismatch | correct |
| **new** | `ledger.cash_delta = 0` | 1 | cash mismatch | correct (so cash *is* covered) |
| control | `fills.qty = 11` | 1 | cash/position mismatch | correct |

**Root cause (my reading):** the replay derives everything from `fills` and then checks only `ledger.cash_delta` and `fills.realized`. `ledger.realized`, `ledger.cost_delta`, `ledger.fee`, `closed_positions` and `snapshots` are **read by the application but never verified**. `Accounting.metrics` sums `ledger.realized`/`ledger.fee` directly, so the two verifier and the app can disagree indefinitely.
**Additional confirmation of the plan's gap:** an **empty** database yields `portfolios_checked: 10, integrity: "ok", errors: []` — a hardcoded constant, not a measurement. The `integrity` field is a literal `'ok'` even though the code *does* append a real `PRAGMA integrity_check` failure to `errors` on a malformed DB — meaning the reported badge and the actual check are decoupled.
**Fix sufficiency:** the Plan §1C test list (realized/cash/cost/partial/fee/settlement/rounding/orphan/closed→open) is *adequate* for this finding. It is insufficient for the two items I added (snapshot equity, closed-position cycles) unless explicitly listed.

### A14-02 — Source verifier ignores unreachable journal rows — **CONFIRMED**
**Own severity: HIGH (agree).** Scope is *wider* than reported.

Code: `tools/source_verify.py:12–38`.
Method: 6 cases, `indy/probes/p1_a1401_a1402.py`.

| Case | Verifier result |
|---|---|
| **archived** orphan `event=NULL`, cash/realized 999 | `errors: []`, `source_cash: "0"` — **CONFIRMED** |
| **new** movement with `event = 99999` (dangling FK) | `errors: []` — **CONFIRMED** |
| **new** extra movement on a *valid* applied event, leg absent from payload | `errors: []` — **CONFIRMED** |
| **new** cloned movement rows (`event=NULL`) copied from a real event | `errors: []` — **CONFIRMED** |
| **new** orphan `source_effects` row (event 424242) | `errors: []` — **CONFIRMED** |
| control: `cash` tampered on an *applied* event's movement | `["source journal cash mismatch"]` — correct |

**Root cause:** the verifier iterates `verified_events` and looks *forward* to movements. Rows with no reachable event are structurally invisible. The schema has **no foreign keys**, so SQLite will not complain either.
**Fix sufficiency:** Plan §1B covers this well, including "reconcile **all** rows in both directions". Add explicit coverage of `source_effects` orphans (my case e) and cloned/multiplicity rows (case d), which the plan's list does not name.

### A14-03 — Single-sided SPLIT accepted — **CONFIRMED (synthetic-only)**
**Own severity: HIGH in the synthetic subsystem, MEDIUM as a real-world risk (agree with the "synthetic-only" qualifier).**

Code: `lab/integrity.py:161–199` (`if kind=='SPLIT' and (not all(x>0 for x in deltas) or sum(cash)!=-sum(cost_delta))`).
Archived case reproduced: one positive leg, `cash=-5`, `basis=5` → `applied`, verifier `errors: []`.
**New, worse cases:**
- two legs with **`basis=0` and `cash=0` on both** → **applied**. A split that consumes *no* paid basis is accepted; the only invariant is that paid basis balances, and 0 == 0 balances. The split mints inventory out of nothing.
- a **three-way fan-out** (1 → 3 outcome tokens) with zero basis on two legs → **applied**.
- Control: genuinely unbalanced paid basis is quarantined ("split requires fully evidenced paid basis") — so the check exists, it is just too weak.

**Root cause:** the guard is an aggregate arithmetic identity, not an operation-shape check. There is no condition-id, no outcome set, no collateral/denominator, and no constraint that the *sum of paid basis is non-zero* or that a negative-cash leg exists.
**Fix sufficiency:** Plan §1D's fixture list is good; it must add **zero-value basis** and **n-way fan-out** explicitly, and require a positive paid-basis requirement, otherwise a post-fix implementation can still accept my case (b).

### A14-04 — REDEEM accepts unproved payout — **CONFIRMED (synthetic-only)**
**Own severity: HIGH in the synthetic subsystem.**

Archived case reproduced: BUY 10 @ basis 5, then REDEEM 10 shares → 20 cash, no payout numerator/denominator, no finality. Result: `applied`, `source_realized = "15"`, verifier `errors: []`.
**New:**
- REDEEM with a **negative** cash leg (`-3`) still applied; realized driven negative.
- Attempt at a zero-delta payout leg was correctly quarantined ("merge/redemption requires burn/debit legs") — a genuine, if narrow, control.
- Duplicate payout with the **same effect identity** is correctly blocked ("overlapping effects already applied"). Duplicate payout under a **different** effect identity would need inventory to exist, so the oversell check catches the obvious version — I did **not** find a bypass there, and I record that as a failed-to-break case rather than a confirmed second defect.

**Root cause:** no payout-per-share ceiling, no resolution record, no finality evidence, no operation-type discrimination. A redemption is modelled as an arbitrary cash leg on a burn.
**Fix sufficiency:** Plan §1D covers payout/resolution/finality/deductions/duplicates. Add the negative-cash-leg case.

### A14-05 — Conflicting certificate payload is lost — **CONFIRMED**, on **all 36 tables**
**Own severity: MEDIUM (agree).** It is a preservation/forensics defect, not a P&L defect.

Code: `lab/integrity.py:127–143`.
I scanned **every** table in the database (36), not the four the authors used, both with and without a linked observation:

| Case | Marker found in |
|---|---|
| archived: conflict, **no observation** | **nowhere** (0 of 36 tables) — the replacement payload and any conflict record are both gone; only `verified_events.state='conflict'` and a generic `reconciliation_records` row survive |
| **new**: conflict **with** two linked observations | `source_observations` only (because I wrote the raw row myself). Still **no immutable conflict record**; `event_links` keeps the *first* observation, and the conflicting one is unreferenced |
| **new**: kind-only conflict (BUY vs SELL, identical payload) | `state='conflict'` but the *kind* is not corrected or recorded anywhere; the event still reads `kind=BUY` |

**Root cause:** the conflict branch performs `UPDATE ... SET state='conflict'` and a `hold()`, and never writes the new payload, kind, ordering or provenance. `verified_events` is a mutable single row, not an append-only log.
**Fix sufficiency:** Plan §1E is adequate. Add "kind-only conflict preserves the rejected kind" to the test list.

### A14-06 — All-failed retries lose earlier bodies — **CONFIRMED**, and **reclassified upward in blast radius**
**Own severity: MEDIUM — agree with the rating, but disagree with the implied blast radius.** The defect is not limited to "all retries failed"; it is *"any failure path that produces an exception loses all but one body"*.

Code: `lab/integrity.py:80–86` (success path flushes `attempt_log[:-1]`) vs `:111–118` (exception path persists **only** `last_raw`).

| Case | Durable bodies | Verdict |
|---|---|---|
| archived: 3 failures then raise | `['body-3']` — **2 of 3 received bodies lost** | **CONFIRMED** |
| **new**: success body then timeout | only `body-2`; **the successful HTTP 200 body is lost** | **CONFIRMED** — a *successful* response destroyed |
| **new**: attempt_log populated, `last_raw` never set (e.g. DNS failure before assignment) | **0 rows at all**; only `collection_batches.error` and a gap record | **CONFIRMED** — "every HTTP attempt is retained" is false in the strongest sense |
| control: 503 then 200 in one `get()` | both bodies durable, dispositions correct | correct |

**Why this matters beyond "evidence gaps":** the project's whole safety story is *fail-closed with preserved evidence*. Here the collection layer silently discards the only record of what the upstream API actually returned, on the branches where that record matters most. Combined with A14-02 (verifier blind to orphans) this means a corrupted or partial capture can leave **no durable trace at all** and still produce a clean-looking verifier result.
**Fix sufficiency:** Plan §1F lists exactly the right cases (two different errors; partial then timeout; all fail; final success; restart between attempts; subprocess timeout). It should explicitly require durability **before** `get()` returns, which the plan does state ("Durability cannot depend only on get() returning").

### A14-07 — Resumed batch substitutes a different requested scope — **CONFIRMED**
**Own severity: MEDIUM — agree, and I consider the classification conservative.**

Code: `lab/integrity.py:69–75` (lookup keyed on `wallet + endpoint` only), caller `lab/public.py:baseline`.

| Case | Observed |
|---|---|
| archived: interrupted CLOSED positions walk, then request OPEN | request went out with `status=CLOSED`, `cursor=cur-1`; **one batch total**; the caller's OPEN request is simply dropped — **CONFIRMED** |
| **new**: interrupted window `start=1000,end=2000`, then request `start=5000,end=9000` | request went out with `start=1000,end=2000` — **CONFIRMED**, the caller's window is silently discarded |
| **new**: frontier published afterwards | `capture_frontiers` records batch 1 (the **CLOSED** walk) as the `/v2/positions` frontier; `source_states.last_complete_batch = 1` — **CONFIRMED**: a completed CLOSED walk is published as the OPEN evidence frontier |

**On the authors' mitigation ("all baselines remain quarantined, containing the economic risk"):** true as of this snapshot, because `Integrity.allowed()` returns `False` for production unconditionally. That is a **containment of *this* defect, not of the class**. The moment a canonical adapter exists (Phase 2), `collect()` is the component that will certify coverage, and it currently certifies the wrong scope. The plan's own SRC-01 warns "do not relabel a cursor as a checkpoint" — this is the same class of error one layer down.
**Fix sufficiency:** Plan §1G is adequate and unusually well specified (scope hash, reject-or-fork, scope-specific frontier).

### A14-08 — Migration digest is not storage-type preserving — **CONFIRMED**, and the collision class is **broader than reported**
**Own severity: LOW (agree)** for the migration use case; **MEDIUM** for any future use of `table_digests` as tamper evidence.

Code: `lab/migrations.py:32–38` — `json.dumps(list(r), default=str, separators=(',',':'))`, sorted, joined, SHA-256.

I observed **actual `typeof()` from SQLite**, not the Python input types, in tables with no affinity, `TEXT` affinity, `NUMERIC` affinity and `BLOB` affinity:

```
affinity NONE   : blob b'A'  ==  text "b'A'"                        (archived case)
affinity NUMERIC: blob b'A'  ==  text "b'A'"
                  int 1      ==  text "1"   ==  real 1.0
                  int 0      ==  text "0.0"
affinity TEXT   : blob b'A'  ==  text "b'A'"
                  int 1      ==  text "1"
affinity BLOB   : blob b'A'  ==  text "b'A'"
```

So the finding is **not** an artefact of one unlucky pair. Because `default=str` maps `bytes` to the *text* `b'A'`, and because SQLite affinity already collapses numeric spellings, several distinct stored states hash identically. Additional confirmed sub-findings:
- **Order-insensitive by design** (rows are sorted) — acceptable for preservation, but it means row *reordering* is invisible; documented behaviour, not a defect.
- **Duplicates are preserved** (two `x` rows ≠ one `x` row) — good.
- **Index/trigger/schema creation does not change any digest** (`CREATE INDEX` → identical digest) — so "legacy rows preserved" says nothing about schema-level preservation, which the plan already notes.
- **Tables not in the caller's list are invisible**; `upgrade_existing` derives the list from `sqlite_master` before migration, so a table *added* by the migration is not compared. Correct by construction today, but it means the property "legacy rows preserved" is exactly as strong as the enumeration.

### A14-09 — Stale historical health renders green "Healthy" — **CONFIRMED**
**Own severity: MEDIUM (agree).** Reproduced with a **different engine** from the authors'.

Code: `lab/dashboard.html:11` — `` `<span class="dot ${h.ok?'':'bad'}"></span>${h.ok?'Healthy':'Attention'}` `` with `new Date(h.ts*1000)` displayed but **never compared to now**. `lab/main.py:34` passes `health` rows through unchanged.

Method: I executed the **real** `dashboard.html` (not a copy, not a stub) under jsdom, with `fetch` returning a fixture state built by the real `App.state()` serialiser on a disposable DB. Result (`indy/results/a1409-results.json`):

- fixture row `{ts: 0, ok: 1}` (1 Jan 1970) rendered as **`Healthy`**, last observed column `1/1/1970, 12:00:00 AM`
- `Healthy` label occurrences: 3 (one per ok=1 row) — no TTL, no "UNKNOWN", no staleness dimension anywhere in the renderer
- `javascript_errors: []`, `real_network_requests: 0`
- `forward_validation_ready: false` in state, yet the rendered warning still reads *"Token-finality settlements are supported…"* while `Engine.settle()` in production mode only calls `hold()`

**Corollary confirmed by inspection:** `App.run()` uses a 60 s freshness gate for `public_api` before executing, but the *dashboard* has no equivalent gate on any component. A stopped worker therefore leaves the last `ok=1` row green indefinitely — the dashboard's "Healthy" is a statement about the last time something was written, not about now.
**Fix sufficiency:** Plan §1H's ten health cases plus the archived ts=0 case are adequate. Add the "stopped worker with a stale green row" case explicitly (it is the realistic failure mode, and my probe shows it).

### A14-10 — DB initialization precedes worker lock — **CONFIRMED, and now reproduced dynamically**
**Own severity: MEDIUM — agree, but I would rate the *lock-aliasing* sub-case HIGH for a multi-operator install.**

Previously "inspection-only". I measured it, without starting the app (`indy/probes/p3_a1406_a1407_a1410.py`, cases a–d, plus two extra bash probes):

| Observation | Evidence |
|---|---|
| `Store()` creates a **brand-new DB**, applies `SCHEMA`, `PRAGMA journal_mode=WAL`, `synchronous=FULL`, both legacy `migrations` rows and `apply_new()` V3 + `source_environment` — **before any flock exists** | file absent → present; `migrations` = [1,2,3]; `settings` written |
| `App.__init__` (a plain construction, no `run()`) performs the same initialization | `lab/main.py:40` builds `App` → `Store`, flock is taken only at `:44–47` |
| `main()`'s **backup branch returns before the flock** | `if args.backup: app.s.backup(...); return` precedes lock acquisition; `Store.backup()` has no ownership check |
| **A second `Store()` on the same path ignores the held flock entirely** | I held `LOCK_EX` on `<db>.worker.lock` in the same process and a second `Store(...)` opened and initialized the DB without error. Only `main()`, `configure.py` and `upgrade_existing()` consult the lock |
| **Existing DB header is rewritten while another owner holds the lock** | `journal_mode` DELETE → **WAL** changed the 16-byte header (`01 01` → `02 02`) while the lock was held by the "owner" |
| **Path aliasing defeats the lock entirely** | opening the DB through a symlink creates `<symlink>.worker.lock` — a *different* lock file. `realpath` of the two lock paths differs, so both processes acquire an exclusive lock on different inodes and there are **two owners** |

The last row is the one that changes my severity assessment. The plan treats path aliases as a test case (§1A: "path aliases/symlinks"); my probe suggests it is a *live* defect, not a hypothetical one, and it defeats the single-writer guarantee without any of the initialization-ordering subtlety. Note the mitigation: `tools/configure.py` and `upgrade_existing` share the same naive `str(path)+'.worker.lock'` convention, so all three entry points are equally aliasing-prone.
**Fix sufficiency:** Plan §1A addresses ordering, backup, readers and aliases. It should be strengthened to require a **canonicalised (realpath) lock identity** and to state that `Store()` itself, not just the CLI, must be ownership-aware — otherwise a library caller (or a test) silently becomes a second writer.

---

## 7. Additional defects found during this review (not in Audit 14)

These are my own findings. They are listed with their evidence and are deliberately *not* assigned the status of independently corroborated findings, since no second reviewer has seen them (see §2).

**F-01 — HIGH — The 119-test suite cannot fail for any of the audited properties, yet is presented as the primary positive control.**
Evidence: I mutated seven distinct persisted fields (`ledger.realized/fee/cost_delta/cash_delta`, `snapshots.equity`, `closed_positions.proceeds`, `source_movements` orphans) and the suite passes unchanged; the suite has no test for the verifiers' blind spots, and `tests/test_integrity.py:159` only tests the tamper case the verifier *does* detect (`source_inventory.qty`). `test_equity_identity_random_lifecycle` asserts the identity the app itself computes, i.e. it validates the producer against itself. Severity is HIGH not because the tests are wrong, but because every plan gate in §6 uses "regression passes" as acceptance evidence. **Recommendation:** the plan must require, per group, at least one test that *fails on the pre-fix snapshot* for the exact archived fixture, and must forbid citing the aggregate count as evidence for unlisted properties. The plan's protocol §5.3 partly says this; it is not carried into the group gate wording.

**F-02 — MEDIUM — `tools/audit.py` verifies a database it does not identify, and hardcodes two result fields.**
`portfolios_checked: 10` is a literal; `integrity: 'ok'` is a literal printed regardless of `PRAGMA integrity_check`; `classification` falls back to `'legacy-unclassified'`. An **empty** DB reports `{fills_replayed: 0, portfolios_checked: 10, integrity: 'ok', errors: []}`. There is no input-hash or snapshot-ID binding in the output, so an auditor cannot prove which database produced a report. **Recommendation:** bind every evidence artefact to the DB SHA-256 and the source snapshot ID, and make `integrity` reflect the actual pragma result.

**F-03 — MEDIUM — `tools/audit.py`'s signing-code scan depends on the current working directory and fails open.**
`code='\n'.join(x.read_text() for x in Path('lab').glob('*.py'))`. Run with `cwd` outside a tree containing `lab/`, the glob is empty, the scan finds nothing, and the report is still `errors: []` with exit 0. Verified: run from `/tmp/nowhere`, scan silently empty; run from `/tmp/decoylab` containing a planted `private_key`, it fires. A safety check that silently passes when it cannot see the code is worse than no check. **Recommendation:** resolve paths relative to the module, and emit an explicit error if the scan target set is empty.

**F-04 — MEDIUM — `paper_holds` uses `INSERT OR REPLACE` keyed on `(model,track,wallet,token)`, destroying hold history.**
`lab/integrity.py:25`. Reproduced: two successive holds with different reasons leave exactly one row, carrying only the later reason and reconciliation id. Combined with A14-05 (no append-only conflict record) this means the audit trail for "why is this position frozen" is a mutable single cell. **Recommendation:** append-only hold events with an explicit release record; a release must be attributable.

**F-05 — MEDIUM — There is no hold-release path at all, and the release a reviewer would look for does not exist.**
`paper_holds` rows are only inserted. `Wallets.change('enable')` deletes the `inventory:<wallet>` setting and records a gap, but does **not** clear holds or re-verify. So H04's "gap/hold/removal records prevent unreviewed re-enable" is true in the safe direction (deny) and false in the operational direction: the only way to clear a hold today is direct SQL. That is a design gap the plan should acknowledge rather than leave to Phase 4 prose.

**F-06 — LOW — `PUT`/`PATCH`/`DELETE` to `/api/wallets` return an HTML 501 with a server banner.**
`BaseHTTPRequestHandler` default. Combined with the absent authentication (SEC-01, already registered) this leaks implementation detail. Not exploitable on its own since the app is never to be started.

**F-07 — LOW — Nothing in the application ever sets `settings['inventory:<wallet>']`, so `Integrity.allowed()` is false in **both** modes unless a fixture writes that key directly.**
`allowed()` in synthetic mode requires the setting; `Collector.baseline()` never sets it; `Wallets.change('enable')` *deletes* it. It is set only by the test harness. This is the single load-bearing guard in the codebase and its only writer is a test fixture. It is fail-closed, so the direction is safe, but the plan's SAFE-01 "revalidate unchanged guard with every diff" should also require an explicit statement of *how* the guard is intended to become true, and an assertion that no non-test code path can set it.

**F-08 — LOW — `tools/http_check.py` starts a real HTTP server on `0.0.0.0` (via `main()`), overriding `Collector.cycle` by monkeypatching it in a `-c` string.**
This is a preserved historical tool that the current instructions forbid running. It binds `0.0.0.0`, matching SEC-01's exposure concern. It should be marked non-runnable in the archive index so a future reviewer does not run it "as documented".

**F-09 — INFORMATIONAL — Documentation/packet contradictions I could verify.**
`EXTERNAL_REVIEW_GUIDE.md` says the package "is four documents" while the archive contains 157 members and a full source tree (the guide does then describe the input set; the sentence is misleading). `docs/remediation/AUDITOR_INSTRUCTIONS.md`, `README.md` and older phase numbering are acknowledged as superseded by the master plan, and the master plan/register do prevail in every case I checked. I preserved these as evidence and did not edit them.

## 8. H01–H05 and the master remediation plan

### 8.1 H01–H05

| ID | Register status | My assessment |
|---|---|---|
| **H01** — no authoritative exhaustive source checkpoint | BLOCKED, HIGH | **Agree.** Locally, durable *received-page* capture is real and works (multiplicity and provider ordinal preserved; terminal page required; frontiers refuse to certify incomplete batches). But a terminal cursor is a capture frontier, not a checkpoint, and A14-06/07 mean even the capture record is lossy on failure and can be published under the wrong scope. Completeness is unprovable locally → **BLOCKED** is correct. |
| **H02** — no canonical identity/ordering/finality | BLOCKED, HIGH | **Agree.** Multiplicity and tie-flagging are genuinely implemented (`observation_flags` for `identical_economics` and `same_timestamp_opposing`) and `economic_key` normalises numeric spellings without deduplicating. But `economic_key` is a *local* heuristic over REST fields; it is not a chain identity. A14-05 shows the conflicting-payload record is not preserved. → **BLOCKED** correct. |
| **H03** — lifecycle reconstruction unproved | BLOCKED, HIGH | **Agree, with emphasis.** The typed-leg arithmetic is clean and genuinely refuses `CORRECTION/REVERSAL/REORG/UNKNOWN` and unsupported kinds. But A14-03 (zero-basis splits accepted), A14-04 (unproved payouts) and the absence of any real decoder make "complete lifecycle" unprovable. Synthetic-only. → **BLOCKED** correct. |
| **H04** — gaps not reconstructable / no safe re-enable | BLOCKED, HIGH | **Agree.** Gap and hold records exist and fail closed. But F-04 (hold history overwritten) and F-05 (no release path) mean the *review* half of "reviewed hold release" does not exist. → **BLOCKED** correct. |
| **H05** — no independent audit or forward evidence | BLOCKED, HIGH | **Agree, and this report does not clear it.** Even taking my reproduction at face value, the second bullet of H05 (real forward evidence, execution calibration) is untouched by any local work, and the first bullet (separate review) is only partly addressed (see §2). → **BLOCKED** correct. |

**One containment claim I want to narrow.** The register's SAFE-01 says the permanent paper-only restriction is "OPEN" and the prior containment check demonstrates it. I re-derived that containment independently and it holds: with a *forged* `source_states.state='verified'` and a forged `inventory:` setting on a production-kind DB, `allowed()` returns `False`, due BUY and SELL orders are both `rejected` ("source integrity/reconciliation unverified"), zero fills are created, the position is untouched, one hold is written, and relabelling production→synthetic raises `ValueError`. **SAFE-01's containment is CONFIRMED.** But note it rests on one `return False` literal, and (F-07) the guard's "true" branch is reachable only from fixtures — so it is robust *and* unimplemented, which the register states honestly.

### 8.2 Master remediation plan — is it sound?

**Substantially yes, in ordering and in discipline. It is not yet sufficient as an acceptance specification.**

What is genuinely good, and I want to be fair about it:
- Governance is honest: it says it cannot self-certify independence, says Phase 0 is BLOCKED, and refuses to let a plan approval imply implementation approval. That is the right posture and it is rare.
- The per-group protocol (§5) is close to what I would write: freeze a pre-fix snapshot, reproduce the original case there, keep failures, never weaken assertions, separate arithmetic processes, STOP for approval after each group.
- The finding→group mapping is correct and A14-08/10-first ordering is the right sequencing (storage + ownership before anything that writes).
- It distinguishes local from external evidence well (§9) and refuses to let any synthetic proxy clear an external gate.

Where it must be revised before Phase 1A:

1. **Acceptance tests are written from the fix's point of view, not the defect's.** §1C says "archive case 999 PnL with unchanged equity must fail" — good — but it never requires that the *new* test fail on the *pre-fix* snapshot. Several group gates ("tests pass") would be satisfied by tests that cannot detect the original defect. **Require, per group, a recorded red→green artefact against the frozen pre-fix snapshot.**
2. **The 119-test count must be demoted.** F-01 shows it is invariant under the exact corruptions under audit. It must not appear in any acceptance gate except as a regression-only guard, explicitly labelled as carrying no assurance for A14 properties.
3. **A14-05 and F-04 belong in the same group.** Both need the same append-only evidence table. Planning them in separate groups (1E vs an unlisted hold-history fix) risks two competing schemas and a second migration.
4. **A14-06's real shape must be written into 1F.** It is not "all retries failed"; it is "the exception path persists at most one body, and may persist none" (my cases c and d). The group's acceptance must include *a successful body followed by a later failure*, and *an attempt log with no `last_raw`*.
5. **A14-07's mitigation "baselines remain quarantined" must not be recorded as containment of the class.** Once Phase 2 arms a real adapter, the same `collect()` decides what "covered" means. 1G should state the invariant as a property of `collect()`, independent of `allowed()`.
6. **1A must add lock canonicalisation and a Store-level ownership requirement** (A14-10, my symlink probe). As written, 1A tests "path aliases/symlinks" but does not state the required mechanism or the desired outcome for two lock files, so the test could be written to pass against today's behaviour.
7. **1C must add snapshot-equity and closed-position-cycle reconciliation** (my A14-01 e/f), or the fix will leave the equity curve and win-rate unverified while the finding is marked VERIFIED_FIXED.
8. **1D must add zero-value basis and n-way splits** (my A14-03 b/c) and the negative-cash redemption (A14-04 d).
9. **Add an evidence-provenance requirement** (my F-02): every gate artefact should carry the DB SHA-256 and the source snapshot ID, so a later reviewer can tell which bytes produced which green result. Without this, the plan's own protocol step 1 ("reconfirm identity, hashes, stop on drift") cannot be applied to evidence produced inside a group.
10. **Phase 9's SEC-01 needs to be visible earlier as a hard prohibition, not only a phase.** The current text does say "No public deployment"—keep it, but F-06 shows the handler has no default-deny for non-GET verbs; that is a one-line hardening that belongs in 1A's "startup ownership" scope rather than in a phase after wallets exist.

**Not a plan defect, worth flagging:** Plan §8 item 1 correctly refuses to let the user's approval substitute for independent review. This report should therefore be filed as *reviewer input*, not as the Phase 0 sign-off — see §12.

## 9. Severity summary (my ratings)

| ID | Audit 14 rating | My rating | Change |
|---|---|---|---|
| A14-01 | HIGH | HIGH | agree; scope +2 fields (snapshots, closed_positions) |
| A14-02 | HIGH | HIGH | agree; scope +2 row classes (effects, cloned) |
| A14-03 | HIGH (synthetic) | HIGH (synthetic) | agree; zero-basis split is a new instance |
| A14-04 | HIGH (synthetic) | HIGH (synthetic) | agree |
| A14-05 | MEDIUM | MEDIUM | agree; verified across all 36 tables |
| A14-06 | MEDIUM | **MEDIUM (blast radius raised)** | not only all-failed retries; **successful** bodies are also lost, and a branch persists nothing |
| A14-07 | MEDIUM | MEDIUM (conservative) | containment is of the instance, not the class |
| A14-08 | LOW | LOW (migration) / MEDIUM (as tamper evidence) | collision class broader than reported; scope must be labelled |
| A14-09 | MEDIUM | MEDIUM | agree; reproduced in a different engine |
| A14-10 | MEDIUM | MEDIUM; **lock aliasing HIGH for multi-operator** | dynamic reproduction; symlink gives two owners |
| F-01 | — | **HIGH** | new |
| F-02, F-03, F-04, F-05 | — | MEDIUM | new |
| F-06, F-07, F-08, F-09 | — | LOW / INFO | new |

No finding in this report is rated on the basis of a real-money or real-wallet loss, because **none was demonstrated and I did not attempt one**. Every economic effect described is synthetic-fixture arithmetic.

## 10. What remains BLOCKED / unverified (explicit)

I did **not** and could not verify, and no claim here should be read as verification:

1. **Canonical source completeness, identity, ordering or finality** (H01, H02, SRC-01..03). No chain, no upstream API, no block/tx/log index. A terminal REST cursor is not a checkpoint; missing inventory is unknown, not zero.
2. **Real lifecycle decoding** (H03, LIFE-01..03). All lifecycle evidence is symbolic fixtures. Fixtures can validate a specified operation model; they cannot validate a real decoder.
3. **Actual gap reconstruction and reviewed hold release** (H04, GAP-01). No real history exists in this snapshot (zero wallets, zero fills).
4. **Forward wallet evidence, execution calibration, strategy performance** (H05, EXEC-02, STRAT-01..03). Untouched by any local work.
5. **The protected runtime databases** (`data/lab.sqlite`, `data/lab-verified-backup.sqlite`). Deliberately excluded; I never opened, copied or hashed them. Their stated hashes are **unverified claims** from this reviewer's position.
6. **PLAYWRIGHT browser reproduction** — substituted with jsdom (§3).
7. **Cross-version reproducibility** — I ran 3.11.2 / SQLite 3.40.1, the authors 3.13.16 / 3.46.1, with no requirements file. Divergence is unpinned and untested.
8. **The `WORKING_TREE.patch` / Git-state claims.** No `.git` in the archive, so the HEAD reference and the "17 modified, 90 untracked" working-tree state are **assertions** I could only check for internal consistency, not re-derive.
9. **Crash/restart durability in a real process** — my probes are in-process; I did not kill a process mid-write.
10. **Whether any defect here is attributable to a specific upstream provider behaviour** — no upstream observation exists.

## 11. Commands and artefacts (reproducibility)

Everything below ran against `runC` (a copy; `lab/` byte-identical to the snapshot). Full probe sources are preserved at `/home/user/audit-review/indy/probes/` and results at `/home/user/audit-review/indy/results/`.

```bash
# 1 verify + extract (supplied script, unmodified)
sha256sum copylab-external-review.zip
python3 -B - <<'PY' ... PY            # -> Verified 157 archive members

# 2 baseline regression, two configurations
cd runA && python3 -m unittest discover -s tests -q          # 119 tests, OK
PYTHONPATH=/tmp/noneti python3 -m unittest discover -s tests -q   # 119 tests, OK (sockets blocked)

# 3 authors' harness, re-executed (cross-check only)
cd runB && python3 -B docs/phase0-audit14/adversarial_checks.py   # exit 0, 8 defect + 2 control cases

# 4 my independent probes
cd runC && python3 -B ../../indy/probes/p1_a1401_a1402.py "$PWD"   # 16 cases
cd runC && python3 -B ../../indy/probes/p2_a1403_a1408.py "$PWD"   # 21 cases
cd runC && python3 -B ../../indy/probes/p3_a1406_a1407_a1410.py "$PWD"  # 12 cases

# 5 A14-09 in jsdom against the real renderer
python3 -B indy/dom/state.json.py runC indy/dom/state.json
node indy/dom/a1409.js runC/lab/dashboard.html indy/dom/state.json indy/results/a1409-results.json

# 6 post-audit preservation
sha256sum copylab-external-review.zip      # unchanged
# + manifest re-verification: 0 mismatches
```

Exit codes are recorded per case in the results JSON under `defect_reproduced`; note that a `defect_reproduced: true` means **the defect was observed**, not that the system passed. My probe scripts deliberately record *both* directions (archived case and the control that must be caught), so a probe that silently stopped working would show up as a control flipping to `false`.

## 12. Recommendation

**BLOCK.** Specifically:

1. **Do not start Phase 1A.** Phase 0 is not satisfied. This report is reviewer *input*; by the master plan's own §4/§8-1 it cannot substitute for a genuinely separate reviewer, and I have said in §2 why I am only partly that.
2. **Revise the master plan** per §8.2 items 1–10 before any group is approved. Items 1, 2 and 6 are the ones that would let a Phase 1A re-run look green while A14-10 and A14-08 remain unfixed.
3. **Re-baseline the register** with my §6 sub-cases (A14-01 e/f; A14-02 c/e; A14-03 b/c; A14-04 d; A14-05 c; A14-06 c/d; A14-10 aliasing) as *additional acceptance inputs*, and add F-01…F-05 as new register entries with their own IDs. I have **not** edited `MASTER_DEFECT_REGISTER.md` or any other project file; the requested changes are stated here for the owner to apply.
4. **Obtain an outside-the-stack reviewer** for the Phase 0 sign-off, with a name/organisation that can be held to it, and have them re-run §11 step 4 against the same snapshot. They should be able to falsify any of my 49 cases; if they cannot, the findings stand.
5. **Keep the paper-only guard exactly as it is** (`return False` for production) until Phase 2 has a canonical adapter *and* a `collect()` that cannot publish a wrong-scope frontier. Removing or weakening it would convert A14-07 from a contained evidence defect into an active one.

**No remediation is authorised by this report. No runtime migration, app start, worker start, wallet query or deployment is authorised. STOP after this report.**

---

*Report ends. 49 independently authored probe cases, 8 archived-signature cross-checks, 1 substituted browser engine, 0 project files modified.*
