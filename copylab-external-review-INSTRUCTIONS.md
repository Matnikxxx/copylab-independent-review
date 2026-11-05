# CopyLab external review transfer instructions

**These materials contain uncommitted implementation changes. The archive represents a working-tree snapshot, not merely the stated Git commit.**

This package is preparation for independent review. It is not an independent audit,
does not resolve Audit 14, and does not authorise Phase 1A. Paper-only permanently.
No fix, runtime migration, app/worker startup, wallet query or deployment is authorised.

## Snapshot and completed packaging checks

- Archive: `/home/user/copylab-external-review.zip`, 1,239,236 bytes.
- Archive SHA-256: `f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23`.
- Branch: `main`; reference HEAD: `288a69f64c24438cfe69ea176e6f3d6ce7333499`.
- Creation date (user local): 2026-11-05; actual packaging clock UTC: 2026-11-05T12:02:15.330980+00:00.
- Snapshot ID (canonical source inventory hash): `b4159070b4ebe77a22ada54bd750ef1cd37ddbf08996778813dedfb818c21d6f`.
- 150 project files (60 tracked, 90 untracked), plus 7 transfer metadata files = **157 ZIP members**.
- 107 original files excluded: 1 Runtime worker lock, not source/evidence, 2 Protected runtime database/verified backup, 104 Git internals.
- No suspected secrets/ambiguous files detected by the documented heuristic rules;
  no redactions made. This is not a mathematical guarantee that every possible secret
  is absent. Binary evidence was preserved; arbitrary image/opaque content is a limitation.
- ZIP CRC/open/extraction check succeeded; all members verified by SHA-256, including
  the inner manifest via the detached manifest hash. Relative paths and all working-tree
  source bytes matched. Original repository (including Git internal file bytes), status,
  branch/HEAD and tracked diff remained unchanged at the post-packaging comparison.
- Prior manifests (106/59/29/136/12 overlapping entries) all match.
- Protected databases were read as file bytes for hashes ONLY; no SQLite connection,
  modification or migration occurred. No tests or project application code executed.
- No matching app/worker/migration process observed before/after; no process controlled.
  Process inspection is point-in-time, not a guarantee against arbitrary hidden writers.

## 1. Verify before extraction

Keep the ZIP and detached SHA256.txt together. In a fresh directory on Linux:

```bash
head -n 1 copylab-external-review-SHA256.txt | sha256sum -c -
```

Use `shasum -a 256` or Python hashlib on systems without sha256sum. The second line
checks the manifest AFTER extraction. These are integrity hashes, not an external
signature or proof of trusted authorship. Obtain the checksum through a trusted channel
if authenticity against replacement matters.

## 2. Safe extraction and full member verification

This script uses Python standard library only, does not execute any supplied code,
refuses overwriting an existing destination and validates paths/duplicates/symlinks.
Run from the folder holding ZIP and checksum; do not extract over any real project.

```bash
python3 -B - <<'PY'
from pathlib import Path, PurePosixPath
import hashlib,json,zipfile,stat
archive=Path('copylab-external-review.zip')
lines=Path('copylab-external-review-SHA256.txt').read_text().splitlines()
checks=dict((line.split(None,1)[1].strip(),line.split(None,1)[0]) for line in lines)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(archive)==checks[archive.name], 'ZIP hash mismatch'
out=Path('copylab-external-review-extracted');assert not out.exists()
with zipfile.ZipFile(archive) as z:
 names=z.namelist();assert len(names)==len(set(names))
 for item in z.infolist():
  p=PurePosixPath(item.filename)
  assert not p.is_absolute() and '..' not in p.parts and '\\' not in item.filename
  assert p.parts[0] in ('paper-copy-lab','_COPYLAB_TRANSFER')
  assert not stat.S_ISLNK(item.external_attr >> 16)
  assert '.git' not in p.parts and not item.filename.startswith('paper-copy-lab/data/')
  assert not item.filename.endswith(('-wal','-shm','.sqlite','.sqlite3','.db','.pyc','.pyo'))
 assert z.testzip() is None
 z.extractall(out)
manifest_path=out/'_COPYLAB_TRANSFER/MANIFEST.json'
assert digest(manifest_path)==checks['_COPYLAB_TRANSFER/MANIFEST.json']
m=json.loads(manifest_path.read_text())
expected=set(m['files'])|{'_COPYLAB_TRANSFER/MANIFEST.json'}
actual={p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
assert actual==expected and len(actual)==m['included_file_count']
for n,v in m['files'].items():
 p=out/n;assert p.stat().st_size==v['size'] and digest(p)==v['sha256'],n
assert not (out/'paper-copy-lab/.git').exists()
assert not (out/'paper-copy-lab/data').exists()
print('Verified',len(actual),'archive members; no application code executed.')
PY
```

## 3. Input layout and audit entry points

- `paper-copy-lab/`: original relative paths, actual current working-tree files.
- `_COPYLAB_TRANSFER/MANIFEST.json`: exact snapshot metadata and every other member hash.
  Self hash is detached to avoid an impossible recursive self-hash.
- `_COPYLAB_TRANSFER/SNAPSHOT.json`, `GIT_STATUS.txt`, `WORKING_TREE.patch`: identity,
  complete status and binary-capable tracked diff. Patch is context, not needed to apply
  changes: the supplied files ALREADY contain them. Do not apply it again.
- `FILE_INVENTORY.csv`: original and transferred hashes, size, tracking/redaction status.
- `EXCLUSIONS_AND_SECURITY.json`: every excluded filename/reason, scanner and limitations.
- `PRESERVATION.json`: baseline file hashes, prior manifest checks, protected DB hashes
  and process-inspection method. No runtime database bytes or Git objects are included.

Read `paper-copy-lab/docs/external-independent-review/EXTERNAL_REVIEW_GUIDE.md` first,
then TEST_MATRIX, COMMANDS and EVIDENCE_INDEX in that directory. Read the actual Audit 14,
master plan/register, full source and all relevant failure history. Do not trust supplied
technical conclusions or historical green tests without independent investigation.

The preparation commands assume SOURCE=/home/user/paper-copy-lab on the owner machine.
**For this archive, do NOT use that path, Git branch commands on an absent .git, or the
owner-machine snapshot block verbatim.** Set input to your fresh extracted paper-copy-lab,
check hashes/metadata above instead of Git objects, and create a SECOND disposable work
copy with fresh results outside the untouched extracted input. Never point any command
back to an existing runtime project. The manifest is a working-tree inventory, not a
new commit or a Git repository. Missing original data/ entries in historical manifests
are intentional exclusions, not successfully verified file transfers.

Use offline/network-denied isolation for probes; inspect every command before running.
Current environment in preparation docs lacks Playwright/Chromium; provision dependencies
separately if approved. No startup tools, real HTTP integration, configuration/migration
commands or wallet collection are permitted. A14-10 dynamic sketch was not executed;
reviewer must validate it. Historical temporary DBs are not distributed; recreate fixtures.

Required external proof still missing includes genuinely separate reviewer conclusions,
canonical source completeness/identity/finality, complete real lifecycle/gap reconstruction,
forward wallet observations and execution/strategy calibration. This archive cannot
supply those by packaging synthetic data. Authentication/operations are not complete.
The reviewer must disclose independence, reproduce/challenge findings, document every
command/result/limitation and stop after a separately authored report. No author claims
or signature here substitutes for that review.

Transfer package prepared for external review only. Audit 14 remains unresolved. Phase 0 remains BLOCKED. Phase 1A is NOT authorised.
