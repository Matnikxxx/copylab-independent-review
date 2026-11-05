# MCD-09 — Proposed additive schema design: attempt identity and collection scope identity

**Document ID:** `MCD-09` · **Group:** **G2 (plan 1F + 1G)** · **Resolves:** GOV-09 (design portion only)
**Status:** **DESIGN ONLY.** No migration written, no migration run, no schema change applied, no runtime
database touched. G2 is **NOT AUTHORISED**.
**Basis:** owner R4 and R5 amendments, dispositioned in `MCD-06` §2–§3.
**Invariants in force:** `MCD-08` SR-09/SR-10 (no runtime DB change, no migration), `MCD-01` INV-04/INV-09.

---

## 0. Scope and the key discovery that shaped this design

Two additive columns are proposed:

| # | Column | Table | Serves |
|---|---|---|---|
| A | `attempt_ordinal` (+ `transport_attempts` evidence columns) | `transport_deliveries` | R4 / A14-06 criteria #18, #19, #21 |
| B | `scope_hash` (+ `scope_params`) | `collection_batches` | R5 / A14-07 criteria #22, #24, #25 |

**Discovery (verified during this design, not assumed).** The existing preservation check in
`lab/migrations.py::upgrade_existing` computes `table_digests(db, tables)` **before** and **after**
`apply_new(db)`, and raises `ValueError('legacy rows changed')` on any difference. I measured the interaction:

```
ADDITIVE COLUMN, ZERO DATA CHANGE:
  before: 9b3016260f53bde9
  after : bec28dcf719141d3
  digest changed? True    <-- legacy_rows_preserved would FAIL
  actual legacy column values unchanged: [(1, 'w', '{}')]
```

`table_digests` encodes `SELECT *` rows, so **adding a column changes tuple arity and therefore the digest,
even though no legacy value changed.** Consequence: a naive `ALTER TABLE ... ADD COLUMN` inside the current
migration flow makes a *correct* additive migration report failure.

> **Therefore A14-08 (G1) is a hard prerequisite for G2's schema.** The digest must become
> column-identity-aware (or the preservation check must compare legacy columns explicitly) *before* either
> column is added. This is independent confirmation of the G1→G2 ordering in `MCD-07` §4, discovered from the
> design work rather than asserted from the plan.

---

## 1. Column A — HTTP attempt identity (`transport_deliveries`)

### 1.1 Current schema (verbatim, V3)

```sql
CREATE TABLE transport_deliveries(
  id INTEGER PRIMARY KEY, batch INTEGER, page_number INTEGER,
  received REAL, raw TEXT NOT NULL, disposition TEXT);
```

### 1.2 Defects this design must satisfy

| Criterion | Obligation |
|---|---|
| #18 `all_failed_attempt_bodies_retained` | every attempt body **and** its code/error/receipt time durable |
| #19 `attempt_order_and_metadata_distinguishable` | attempts with **identical body text** remain distinguishable; no body-based de-dup |
| #21 `successful_body_survives_later_failure` | a 200 received before a later timeout survives, with metadata |

### 1.3 Proposed additive schema

```sql
-- additive only; no existing column altered or dropped
ALTER TABLE transport_deliveries ADD COLUMN attempt_ordinal INTEGER;   -- 1-based, within (batch, page_number)
ALTER TABLE transport_deliveries ADD COLUMN http_code      TEXT;       -- '503', '000', or NULL if unknown
ALTER TABLE transport_deliveries ADD COLUMN error_text     TEXT;       -- transport error, truncated
ALTER TABLE transport_deliveries ADD COLUMN body_bytes     INTEGER;    -- length of raw, for large-body triage
ALTER TABLE transport_deliveries ADD COLUMN attempt_state  TEXT;       -- 'received'|'failed'|'unknown'

-- uniqueness of an attempt within its page; legacy NULL ordinals are exempt by SQLite semantics
CREATE UNIQUE INDEX IF NOT EXISTS ux_transport_attempt
  ON transport_deliveries(batch, page_number, attempt_ordinal)
  WHERE attempt_ordinal IS NOT NULL;

-- fast recovery queries: "what did we actually receive for this batch?"
CREATE INDEX IF NOT EXISTS ix_transport_batch
  ON transport_deliveries(batch, page_number, attempt_ordinal);
```

**Why `attempt_ordinal` and not a UUID.** It is monotonic, cheap, ordered, and human-readable in evidence
reviews. A UUID would be equally unique but would make "attempt 2 of 3" unreadable in a report, which matters
for the R4 obligation that a reviewer can see *which* attempt was lost.

**Why `body_bytes`.** Bodies are already stored in `raw`; the length column enables a completeness check
(three attempts, three lengths, three ordinals) without re-reading large text, and supports the eventual
size/retention policy in OPS-02.

### 1.4 Backward compatibility

| Concern | Resolution |
|---|---|
| Existing rows have `attempt_ordinal IS NULL` | Permitted. Repeated NULLs do not violate a UNIQUE index in SQLite — **verified**: three legacy rows with `NULL` inserted successfully under the index. |
| Existing readers | `SELECT *` callers see additional columns and must tolerate them. `source_verify` reads `raw`/`disposition` by name, unaffected. |
| Existing writers | The current single-insert path writes NULL ordinals and keeps working; it simply fails criteria #18/#19 until G2's writer change lands. **That is intended** — the schema alone must not appear to fix the defect. |
| Old databases opened by new code | Reader must treat `attempt_ordinal IS NULL` as *legacy, identity unknown*, never as attempt 1. |

### 1.5 Integrity constraints (what the schema can and cannot enforce)

| Constraint | Enforced by |
|---|---|
| one row per attempt per page | partial UNIQUE index (above) |
| `raw` never empty | existing `NOT NULL`; **stricter** `CHECK(length(raw) >= 0)` is redundant — see §3.4 on why no CHECK on `raw` |
| ordinal positive when present | `CHECK(attempt_ordinal IS NULL OR attempt_ordinal > 0)` — proposed, see §3.3 |
| attempt FK to batch | **cannot** be enforced: SQLite FKs are off by default and the existing V3 schema declares none; adding `REFERENCES` would silently do nothing unless `PRAGMA foreign_keys=ON` is set per connection. Recorded as a *known limitation*, to be compensated by explicit verification (A14-02's lesson). |

### 1.6 Migration safety (proposed, **not executed**)

1. Additive `ALTER TABLE ... ADD COLUMN` only — no table rebuild, no data rewrite, no `DROP`.
2. `CREATE INDEX IF NOT EXISTS` — idempotent, safe to re-run.
3. Must run inside the existing `BEGIN IMMEDIATE` + verified-backup flow, **after** the G1 digest fix.
4. Must be preceded by a verified backup whose restore is drilled (OPS-01).
5. Must be verified by comparing legacy columns explicitly (not whole-row `SELECT *` digests) — see §0.
6. **Never run against a runtime database** by this project stage (`MCD-08` SR-09/SR-10).

### 1.7 Acceptance tests for Column A

Beyond criteria #18/#19/#21, G2 must add:

| Test | Asserts |
|---|---|
| `attempt_ordinal_unique_per_page` | two rows with the same (batch, page, ordinal) are rejected |
| `legacy_null_ordinals_permitted` | multiple NULL ordinals coexist (backward compat) |
| `attempt_order_matches_receipt_time` | ordinal order is consistent with `received` ordering |
| `body_bytes_matches_raw` | `body_bytes == length(raw)` for every new row |
| `attempt_state_transitions` | `received` → `captured`/`failed` only; no resurrection after failure |
| `restart_mid_attempt_metadata` | a crash between response receipt and persistence yields `attempt_state='unknown'`, never a fabricated body |

---

## 2. Column B — collection scope identity (`collection_batches`)

### 2.1 Current schema (verbatim, V3)

```sql
CREATE TABLE collection_batches(
  id INTEGER PRIMARY KEY, wallet TEXT, endpoint TEXT, params TEXT, started REAL,
  finished REAL, status TEXT NOT NULL, next_cursor TEXT, page_number INTEGER DEFAULT 0,
  error TEXT, coverage TEXT NOT NULL DEFAULT 'unproven');
CREATE TABLE capture_frontiers(
  wallet TEXT, endpoint TEXT, batch INTEGER, captured_at REAL,
  coverage TEXT NOT NULL, PRIMARY KEY(wallet, endpoint));
```

### 2.2 Defects this design must satisfy

| Criterion | Obligation |
|---|---|
| #22 `collect_enforces_scope_without_allowed` | `collect()` rejects or forks on mismatch, with `allowed()` never consulted |
| #24 `scope_identity_persisted_per_batch` | an explicit, populated scope identity exists and is *used* |
| #25 `scope_substitution_rejected` | a pending CLOSED walk is never sent as an OPEN request |
| #23 `frontier_not_published_for_wrong_scope` | a frontier belongs to a scope, not to `(wallet, endpoint)` |

### 2.3 Proposed scope definition (normative)

```
scope_hash = sha256( canonical_json( scope_payload ) )

scope_payload = {
  "wallet":      lowercase address,
  "endpoint":    e.g. "/v2/positions",
  "api_version": "v2",
  "filters":     { every request param that narrows the result set, sorted },
  "window":      {"start": int|null, "end": int|null},
  "page":        {"limit": int|null, "sort_direction": str|null}
}
```

**Explicitly excluded from the hash** (these are *progress*, not *scope*): `cursor`, `next_cursor`,
`page_number`, `started`, `finished`. Including them would make every page a new scope and destroy resumability.

**Canonicalisation rules** (testable, and the source of most bugs in this area):
1. Lower-case the wallet address; do **not** lower-case `endpoint` or free-text params.
2. Keys sorted lexicographically at every level; no insignificant whitespace; `separators=(',',':')`.
3. Absent filter ≠ filter with `null` value. Use omission, not `null`, so `{status omitted}` ≠ `{"status": null}`.
4. Booleans as `true`/`false`; integers as integers; **no** float coercion of integer timestamps.
5. Unknown/new params are **included** by default (fail-safe: an unrecognised filter changes the hash, which
   causes a mismatch → refuse/fork, never silent reuse).

### 2.4 Proposed additive schema

```sql
ALTER TABLE collection_batches ADD COLUMN scope_hash   TEXT;   -- sha256 of canonical scope payload
ALTER TABLE collection_batches ADD COLUMN scope_params TEXT;   -- canonical JSON actually used, for audit

CREATE UNIQUE INDEX IF NOT EXISTS ux_batch_scope_active
  ON collection_batches(wallet, endpoint, scope_hash)
  WHERE scope_hash IS NOT NULL AND status IN ('incomplete','collecting');

CREATE INDEX IF NOT EXISTS ix_batch_scope ON collection_batches(scope_hash);
```

**Why the partial unique index.** It enforces *at most one active batch per exact scope* while permitting many
completed batches for the same scope over time (history is evidence, not duplication). This is the database
half of R5's requirement; the `collect()` change is the other half.

### 2.5 Required `collect()` behaviour change (design, not code)

Today: `SELECT ... WHERE wallet=? AND endpoint=? AND status IN ('incomplete','collecting')`.

Proposed, in order:

1. Compute `scope_hash` from the caller's **requested** params **before** any lookup.
2. Look up a pending batch **for that exact `scope_hash`**.
   - **found** → resume it (same scope, safe).
   - **not found**, but a pending batch exists for `(wallet, endpoint)` with a **different** hash → this is a
     scope mismatch. Two permitted outcomes only:
     - **refuse** (raise, leaving the old batch intact), or
     - **fork** a new batch with the requested scope (old batch preserved as `incomplete`).
   - **never**: adopt the pending params and send them under the caller's request.
3. Write `scope_hash` and `scope_params` on every new batch.
4. Publish a frontier keyed by `scope_hash`, not by `(wallet, endpoint)` — requires the companion change below.

### 2.6 Companion change: `capture_frontiers` key

```sql
-- additive: carry the scope, keep the legacy PK for compatibility
ALTER TABLE capture_frontiers ADD COLUMN scope_hash TEXT;
```

The legacy `PRIMARY KEY(wallet, endpoint)` permits only one frontier per endpoint, which is precisely defect
#23. A full fix needs a **new table** (or a rebuilt PK), which is *not* additive — so:

> **Design decision (flagged to the owner, not silently taken):** criterion #23 cannot be fully satisfied by
> the additive design above. It requires either (a) a `capture_frontiers_v2` table keyed by `scope_hash` with
> the old table retained read-only, or (b) a table rebuild. Both are **migration decisions beyond this
> document's authority**. G2 must choose (a) — the safer, non-destructive route — and the choice is recorded
> as **GOV-14** for approval when G2 is authorised.

### 2.7 Backward compatibility

| Concern | Resolution |
|---|---|
| Existing batches have `scope_hash IS NULL` | Treated as **unknown scope**. Never resumable as a *trusted* match; the reader must refuse to resume them silently (prefer: fork). |
| Existing frontiers have `scope_hash IS NULL` | Readable, but `collect()` must not treat them as evidence for any specific scope. |
| Old code reading new DB | Ignores the new columns; behaviour degrades to today's (defective) semantics — so the migration must not be run until the *code* change ships, or the schema would appear fixed while the defect persists. **Ordering: code+test first, disposable migration second, runtime never in this stage.** |

### 2.8 Acceptance tests for Column B

Beyond #22–#25:

| Test | Asserts |
|---|---|
| `scope_hash_canonicalisation` | key order, whitespace, and absent-vs-null produce one hash for one logical scope |
| `scope_hash_sensitivity` | changing wallet, endpoint, any filter, or window changes the hash |
| `cursor_excluded_from_scope` | page advance does not change the hash (resumability preserved) |
| `unknown_param_changes_scope` | an unrecognised param alters the hash (fail-safe) |
| `active_batch_uniqueness` | two active batches for one scope rejected |
| `completed_batches_not_unique` | repeated completed batches for one scope permitted (history) |
| `legacy_null_scope_not_trusted` | a NULL-scope pending batch is refused or forked, never resumed |
| `fork_preserves_old_batch` | forking leaves the original batch `incomplete` and unmodified |

---

## 3. Migration safety, cross-cutting

### 3.1 Preconditions (all must hold before G2 may propose a migration)

1. **G1 complete and reviewed** — especially the A14-08 digest fix (§0).
2. Verified backup + **drilled restore** (OPS-01).
3. All writers stopped and proven stopped (OPS-02 / A14-10 canonical lock).
4. Disposable-file rehearsal with legacy fixtures, then byte-level comparison of legacy columns.

### 3.2 Ordering

```
G1 digest+lock  ->  code change (writers/scanners)  ->  disposable migration  ->  verify  ->  STOP
                                                                                     |
                                                            runtime migration NEVER in this stage
```

### 3.3 CHECK constraints — proposed with caution

`CHECK` constraints cannot be added by `ALTER TABLE ADD COLUMN` in SQLite (only as part of the column
definition, which applies to *new* rows only) and enforcing them on legacy rows requires a table rebuild.
Proposal: declare `CHECK(attempt_ordinal IS NULL OR attempt_ordinal > 0)` **in the column definition** so it
governs new rows, and enforce legacy validity in the **verifier** rather than by rebuild. Rationale: a rebuild
is the riskiest operation in the whole migration and buys little here.

### 3.4 What this design deliberately does not do

- No `DROP`, no `RENAME`, no table rebuild, no data backfill of `scope_hash` for legacy rows (backfilling would
  invent a scope identity that was never recorded — an INV-08 / SR-25 violation).
- No `PRAGMA foreign_keys=ON` flip (it changes deletion semantics globally and would silently alter existing
  behaviour).
- No retention/size policy (OPS-02), no encryption at rest, no redaction of `raw` bodies (SEC-01).

---

## 4. Effort, risk and what could still go wrong

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Digest change (§0) ships without G1 | medium if ordering is skipped | migration reports false failure, or worse, is "fixed" by disabling the check | G1 gate is blocking; `MCD-07` §4 ordering |
| `capture_frontiers` key cannot be fixed additively | **certain** | #23 not fully satisfiable in the additive design | GOV-14 decision required at G2 authorisation |
| Scope hash canonicalisation drifts between writer and reader | medium | spurious mismatches → constant forking | single shared `scope_hash()` function, golden vectors, both sides tested |
| Attempt ordinal assigned after the fact | medium | ordering wrong, defeating #19 | ordinal assigned at request issue, not at persistence |
| Body-size growth unbounded | medium | DB bloat, slow evidence review | `body_bytes` + OPS-02 retention policy |

**No code was written for any of the above.** Effort estimate is withheld deliberately: it would be a schedule
commitment for unauthorised work.

---

## 5. Status

| Item | State |
|---|---|
| GOV-09 design portion | **CLOSED** by this document |
| GOV-09 implementation portion | OPEN — requires G2 authorisation (not granted) |
| GOV-14 (`capture_frontiers` non-additive key) | **NEW, OPEN** — owner decision needed at G2 |
| Any migration written/run | **NO** |
| Any runtime DB touched | **NO** |
| G1–G5 | **NOT AUTHORISED** |

*Design only. The two ALTER statements above are proposals for a future authorised group; they have never been
executed against any database in this package.*
