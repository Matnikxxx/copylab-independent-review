# MCD-10 — Environment and version pinning

**Document ID:** `MCD-10` · **Status:** ACTIVE · **Resolves:** blocker 10 (cross-version reproducibility unpinned)
**Constraint:** no dependency installation into the project; nothing here changes the snapshot (`MCD-08` SR-07/SR-08).

---

## 1. The problem

The snapshot contains **no** `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` or lock file
(verified: `find` for all five returns nothing). The archive's own review guide states this explicitly:

> "No requirements/lock file is present; cross-version reproducibility is unpinned.
> Observed preparation environment: Python 3.13.16, SQLite 3.46.1."

So every test result in this package carries an implicit environment claim that was never pinned. Blocker 10.

## 2. Exact versions used for the evidence in this package

| Component | Version | Where it matters |
|---|---|---|
| OS | Linux (Debian-based sandbox), non-root | `fcntl` flock semantics (A14-10) |
| **Python** | **3.11.2** (GCC 12.2.0 build) | the `sqlite3` module API, `Decimal`, dict ordering |
| `sqlite3` module | 2.6.0 | DB-API layer |
| **SQLite library** | **3.40.1** | `typeof()`, affinity rules, `json`, partial indexes |
| Node.js | **22.22.3** | A14-09 probe only (jsdom) |
| jsdom | installed at review time from npm | A14-09 probe only; **not** in the project |
| Playwright / Chromium | **NOT INSTALLED** | A14-09 authored probe; substituted with jsdom (limitation L1) |
| Runtime third-party Python deps | **none** | the project's core and tests are stdlib-only |

**Divergence from the authors' documented environment:**

| | Authors (documented) | This review (actual) | Delta |
|---|---|---|---|
| Python | 3.13.16 | 3.11.2 | **2 minor versions behind** |
| SQLite | 3.46.1 | 3.40.1 | **6 patch-levels behind (3.40 vs 3.46)** |

**Known-version gaps vs the documented environment (zero package deps declared anywhere):**

| Component | Unpinned requirement | This review | Authors |
|---|---|---|---|
| Python | README declares "3.11+ (tested 3.13)" | 3.11.2 | 3.13.16 |
| SQLite | README | 3.46.1 | 3.40.1 |
| `curl` | README (A14-06 real client used) | 8.10.1 (Debian trixie) | not documented |
| Playwright/Chromium | review guide | absent | absent |
| Node/jsdom | review guide | v22.22.3 / jsdom 27.0.0 | n/a |

## 3. What the divergence can and cannot explain

Checked rather than assumed. The three version-sensitive behaviours this package relies on:

| Behaviour used | Introduced | Present in 3.40.1? | Present in 3.46.1? | Verdict |
|---|---|---|---|---|
| Partial indexes (`... WHERE col IS NOT NULL`) | 3.8.0 | yes | yes | **no divergence risk** |
| `ALTER TABLE ADD COLUMN` | 3.2.0 | yes | yes | **no divergence risk** |
| `typeof()` / column affinity rules | ancient | yes | yes | **no divergence risk** |
| `json.dumps(..., default=str)` byte rendering | Python, not SQLite | yes | yes | **no divergence risk** |
| `PRAGMA journal_mode=WAL` header rewrite (A14-10) | 3.7.0 | yes | yes | **no divergence risk** |

**Conclusion:** none of the 35 criteria depend on a feature newer than SQLite 3.40, so the divergence is
**unlikely to change any result in this package**. That is a reasoned assessment, **not** a proof — see §5.

## 4. Reproduction requirements for the external reviewer

State these in your report so results are comparable:

```bash
python3 -VV
python3 -c "import sqlite3; print(sqlite3.version, sqlite3.sqlite_version)"
node --version 2>/dev/null || echo "node absent (A14-09 will ERROR)"
uname -a
```

**Minimum claimed supported:** Python 3.11+, Linux or macOS (Unix `fcntl` required).
**Minimum verified by this package:** Python 3.11.2 / SQLite 3.40.1 / Linux.
**Not verified at all:** Windows (no `fcntl`), Python 3.12, Python 3.13 (the authors' claim), SQLite ≥3.45.
Those five are **assertions, not measurements** — recorded as GOV-15.

**A14-09 note:** the reviewer should record whether they reproduced with Playwright (authors' intent) or jsdom
(this review). They are not equivalent: jsdom executes the renderer's logic, Chromium additionally exercises
layout/paint.

## 5. Outstanding uncertainty (explicit)

1. **Cross-version parity is unproven.** I reasoned that no criterion depends on post-3.40 behaviour (§3). I
   did not run the suite on 3.13/3.46 because doing so would have required provisioning a second interpreter —
   permitted, but it would not change the RED verdict and I chose to spend the effort on the package instead.
   A reviewer with 3.13/3.46 available should simply confirm 35/35 FAIL there too; if any test flips, that is a
   finding about my harness, not about CopyLab.
2. **Python 3.13 + 3.11 both pass the 119-test suite?** Unverified. The authors report 119/119 on 3.13; I
   observed 119/119 on 3.11. Neither of us tested the other's version.
3. **`curl` behaviour differs by version** and the real client shells out to it. Irrelevant to every criterion
   here (all use fake clients), relevant to any future live-collection work (G6).
4. **No lock file can be produced** without changing the snapshot (`SR-07`/`SR-08`). A future authorised group
   should add one; the project currently has no third-party Python dependencies, so it would pin the
   *interpreter and SQLite*, not packages.
5. **jsdom version drifts.** It was installed from npm at review time with no pin. `tools/package.json`
   records the dependency but not a resolved version. A reviewer installing later may get a different jsdom;
   the probe only needs DOM + `textContent`, which are stable, but this is stated rather than assumed.

## 6. Status

| Item | State |
|---|---|
| Blocker 10 (documentation) | **CLOSED** by this document — exact versions, divergence, impact analysis, reproduction requirements |
| Blocker 10 (actual parity evidence) | **OPEN** as GOV-15 — needs a reviewer on 3.13/3.46, or accepted as a stated limitation |
| Snapshot modified | **NO** |
| Dependencies installed into the project | **NO** |
