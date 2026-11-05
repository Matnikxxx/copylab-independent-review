# MCD-03 — A14-08 correction record (preserved, not rewritten)

**Document ID:** `MCD-03` · **Corrects:** `INDEP-AUDIT-01` §6 → A14-08, and §9 (severity table)
**Status:** correction **ACCEPTED** by owner 2026-11-05 (decision #2), conditional on "the corrected finding
is supported by reproducible evidence". This document supplies that evidence and preserves the history.
**Rule applied:** the original claim is **quoted verbatim and left intact** in `INDEP-AUDIT-01`. This record
appends. It does not edit history — consistent with `INV-09` / `INV-11` (append-only evidence, append-only
register).

---

## 1. What was claimed (verbatim, still standing in the original report)

From `INDEP-AUDIT-01` §6, A14-08:

> "So the finding is **not** an artefact of one unlucky pair. Because `default=str` maps `bytes` to the *text*
> `b'A'`, and because SQLite affinity already collapses numeric spellings, several distinct stored states hash
> identically."

and from the §6 observation table:

```
affinity NUMERIC: blob b'A'  ==  text "b'A'"
                  int 1      ==  text "1"   ==  real 1.0
                  int 0      ==  text "0.0"
affinity TEXT   : blob b'A'  ==  text "b'A'"
                  int 1      ==  text "1"
```

and from §9:

> "collision class broader than reported"

## 2. What is wrong with it

The **table entries were accurately observed** — I printed `typeof()` and it did read `integer` vs
`integer`. The **prose inference was wrong**: those rows are *not* collisions, they are **evidence that no
collision exists**, because SQLite had already coerced `'1'` and `1.0` into the *same* storage class
`INTEGER`. There was no type difference left for the digest to lose. The digest cannot be blamed for failing
to distinguish two things that are stored identically.

I then wrote prose ("several distinct stored states hash identically") that contradicted my own table. That
is the error: **conclusion outran evidence**, in the exact direction that inflates a finding.

## 3. The corrected finding

Re-measured with **columns of no affinity**, where SQLite provably preserves the stored type (`typeof()`
differs between the two fixtures), so any collision is genuine:

| Stored value A | `typeof` A | Stored value B | `typeof` B | Digest | Genuine type collision? |
|---|---|---|---|---|---|
| `b'A'` | `blob` | `"b'A'"` | `text` | **identical** | **YES** |
| `b'1'` | `blob` | `"b'1'"` | `text` | **identical** | **YES** |
| `NULL` | `null` | `''` | `text` | different | no |
| `0` | `integer` | `'0.0'` | `integer` (coerced) | identical | **no — same stored type** |
| `1` | `integer` | `'1'` | `integer` (coerced) | identical | **no — same stored type** |
| `'a\u0000b'` | `text` | `'ab'` | `text` | different | no |
| two `x` rows | — | one `x` row | — | different (duplicates kept) | correct |
| rows `(x,y)` | — | rows `(y,x)` | — | identical | by design (sorted) |

**Corrected statement of A14-08:**

> `migrations.table_digests()` uses `json.dumps(..., default=str)`. Python `bytes` are rendered by `str()` as
> their repr, so a stored **BLOB** `b'A'` and a stored **TEXT** `"b'A'"` produce the same encoded cell and
> therefore the same digest. This is a genuine storage-type-preservation failure for the **BLOB-vs-repr-text
> family only**, reproducible at every column affinity. Numeric spellings that SQLite affinity already
> coerces to one storage class do **not** collide, and were incorrectly reported as doing so.

## 4. Effect on severity and scope

| Aspect | Before | After | Direction |
|---|---|---|---|
| Severity (migration use) | LOW | **LOW** | unchanged |
| Severity (as tamper evidence) | MEDIUM | MEDIUM | unchanged |
| Collision class | "broader than reported" | **narrower**: one mechanism, one family | **scope reduced** |
| Mechanism | `default=str` + affinity | **`default=str` only** | **simplified** |
| Finding existence | CONFIRMED | **CONFIRMED** | unchanged |

**Net effect: the finding stands; the overstatement does not.** A14-08 remains OPEN, LOW, Group G1. Two
acceptance criteria assert only the corrected family (MCD-02 #23, #24). The archived `fe21b3a1…ecad`
signature is unaffected — it is the BLOB/TEXT pair, which is the genuine case.

## 5. Reproducible evidence (the owner's condition)

Everything below runs offline on a disposable copy; see `tools/REPRODUCE.md` §2–§5 for setup.

**(a) Executable assertion** — `tools/acceptance_suite.py`, criterion #24:

```
[FAIL] A14-08  digest_distinguishes_blob_from_text
        collision: blob and text(text) share digest fe21b3a17c7cc0eb...
```

**(b) The disambiguating measurement** — the script below prints `typeof` for both sides, so a reader can
see whether a *genuine* type difference existed before the digest was taken. Run it yourself:

```python
import sqlite3, tempfile, sys
sys.path.insert(0, '.')                      # the extracted paper-copy-lab
from lab.migrations import table_digests

t = tempfile.mkdtemp()
VALS = [('NULL', None), ('int 0', 0), ('int 1', 1), ('real 1.0', 1.0), ('text ""', ''),
        ('text "1"', '1'), ('text "0.0"', '0.0'), ('blob b"A"', b'A'),
        ('text "b\'A\'"', "b'A'"), ('blob b"1"', b'1'), ('nul text', 'a\x00b')]

for sqltype in ('', 'NUMERIC', 'TEXT', 'BLOB', 'REAL'):
    obs = {}
    for name, v in VALS:
        con = sqlite3.connect(t + '/x.sqlite')
        con.execute('DROP TABLE IF EXISTS f')
        con.execute(f'CREATE TABLE f(value {sqltype})')
        try:
            con.execute('INSERT INTO f VALUES(?)', (v,))
        except Exception:
            con.close(); continue
        ty = con.execute('SELECT typeof(value) FROM f').fetchone()[0]
        obs.setdefault(table_digests(con, ['f'])['f'], []).append((name, ty))
        con.close()
    genuine = [g for g in obs.values() if len({ty for _, ty in g}) > 1]
    print(f'affinity {sqltype or "NONE":7}: genuine type-collisions -> {genuine or "none"}')
```

**Observed output** (my environment: Python 3.11.2 / SQLite 3.40.1):

```
affinity NONE   : genuine type-collisions -> [[('blob b"A"', 'blob'), ('text "b\'A\'"', 'text')]]
affinity NUMERIC: genuine type-collisions -> [[('blob b"A"', 'blob'), ('text "b\'A\'"', 'text')]]
affinity TEXT   : genuine type-collisions -> [[('blob b"A"', 'blob'), ('text "b\'A\'"', 'text')]]
affinity BLOB   : genuine type-collisions -> [[('blob b"A"', 'blob'), ('text "b\'A\'"', 'text')]]
affinity REAL   : genuine type-collisions -> [[('blob b"A"', 'blob'), ('text "b\'A\'"', 'text')]]
```

One family, five affinities, no numeric cases. That is the corrected finding, and it is **smaller** than
what I originally wrote.

**(c) The misleading version preserved** — reproducing the *original* error, so a reviewer can confirm the
mistake was prose rather than measurement:

```python
# This is what produced the inflated claim. NOTE the column has NUMERIC affinity,
# so SQLite coerces '1' and 1.0 to INTEGER before the digest ever sees them.
con.execute('CREATE TABLE f(value NUMERIC)')
con.execute('INSERT INTO f VALUES(?)', ('1',))
print(con.execute('SELECT typeof(value) FROM f').fetchone()[0])   # -> 'integer'  (not 'text')
```

## 6. Why this matters beyond one sentence

The failure mode was **conclusion outrunning evidence in the direction that inflates severity/scope**. In an
audit whose value depends on not overstating, that is the worst direction to be wrong in. It is also
instructive that the defect was caught by **building the executable criterion** — writing "#24 must fail,
and here is why" forced the mechanism to be stated precisely, and the imprecise version could not survive
that. This is the concrete argument for plan change **R1**.

It also strengthens, rather than weakens, the case for external review: if I can overstate a LOW finding in
my own report, the reviewer should assume I may have done so elsewhere and check the other 48 cases with the
same rigour. **Falsifying my findings is the most valuable thing a reviewer can return.**

## 7. Open items created by this record

| ID | Item | Owner |
|---|---|---|
| GOV-05 | Acknowledge this correction in the audit record; `INDEP-AUDIT-01` §6/§9 remain unedited by design | owner + reviewer |
| GOV-07 | Independent reviewer should re-derive §3 and confirm or reject the corrected scope | external reviewer |
| — | No change to A14-08 status, severity or group | closed |

---

*This record is append-only. It does not modify `INDEP-AUDIT-01`, the snapshot, or the defect register.*
