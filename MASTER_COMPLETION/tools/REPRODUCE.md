# Reproducing the CopyLab red-phase acceptance suite

**Audience:** an outside reviewer verifying `INDEP-AUDIT-01` and `MCD-01` independently.
**Goal:** reach your own conclusion in minutes, without trusting my results.

---

## 0. What you are reproducing

The current CopyLab snapshot (`288a69f…`) violates **32 concrete safety invariants**. The suite
`tools/acceptance_suite.py` asserts the *desired* behaviour for each. Against this snapshot **all 32 must
fail**. If any passes, either the snapshot drifted or the test is defective — investigate before proceeding,
because a false green is the failure mode this suite exists to prevent.

No fixes are included. This is a **red** harness.

## 1. Prerequisites

- Linux, Python 3.11+ (I used 3.11.2 / SQLite 3.40.1; the project documents 3.13.16 / 3.46.1 — record yours)
- Node.js 18+ **only** for the A14-09 UI test; `jsdom` must be resolvable (see §4)
- No network, no project dependencies, no Playwright

## 2. Verify the sealed artefact first

```bash
sha256sum copylab-external-review.zip
# expect: f19437429a3dc239813840628920496123bf5fc2be3f0bf6c3af3fd2f9b11c23
```

Extract with the archive's own script (it is in `copylab-external-review-INSTRUCTIONS.md` §2). It refuses
to overwrite, validates paths/duplicates/symlinks, and re-verifies all 157 members.

```bash
# expect: Verified 157 archive members; no application code executed.
```

Then make a **second** disposable copy for execution so the extracted input stays pristine:

```bash
cp -a copylab-external-review-extracted/paper-copy-lab /tmp/work-copylab
chmod -R u+w /tmp/work-copylab
```

## 3. Establish offline isolation (do not skip)

Merely unsetting a proxy does not prove isolation. Block the socket layer:

```bash
mkdir -p /tmp/noneti
cat > /tmp/noneti/sitecustomize.py <<'PY'
import socket
def _deny(*a, **k): raise OSError('network denied by audit isolation policy')
socket.socket.connect = _deny
socket.socket.connect_ex = _deny
socket.create_connection = _deny
socket.getaddrinfo = _deny
PY

# prove it works (must print "isolation active")
PYTHONPATH=/tmp/noneti python3 -c "
import socket
try: socket.create_connection(('1.1.1.1',80),timeout=1)
except Exception as e: print('isolation active:',e)"
```

## 4. jsdom for the UI test (optional)

The A14-09 test executes the **real** `lab/dashboard.html` renderer in jsdom. If `jsdom` is unavailable the
test reports `ERROR`, never a false pass.

```bash
cd MASTER_COMPLETION/tools
npm install jsdom --no-audit --no-fund     # ~4s, offline thereafter
node -e "require('jsdom');console.log('jsdom ok')"
```

`acceptance_suite.py` resolves jsdom via `MASTER_COMPLETION/tools/node_modules`. If you install elsewhere,
point it there or accept the `ERROR` (it is not a silent pass).

## 5. Run the red phase

```bash
cd /tmp/work-copylab
PYTHONPATH=/tmp/noneti PYTHONDONTWRITEBYTECODE=1 \
  python3 -B /path/to/MASTER_COMPLETION/tools/acceptance_suite.py "$PWD" \
  --json /tmp/red-mine.json
```

**Expected:**

```
TOTAL 32   PASS 0   FAIL 32   -> phase=RED
```

Exit code **1** is the expected result. Exit 0 would mean every invariant already holds — impossible for
this snapshot, and a finding in itself.

## 6. Compare against my result

```bash
python3 - <<'PY'
import json
a=json.load(open('/tmp/red-mine.json')); b=json.load(open('MASTER_COMPLETION/evidence/red-phase-results.json'))
am={(c['finding'],c['test']):c['result'] for c in a['cases']}
bm={(c['finding'],c['test']):c['result'] for c in b['cases']}
print('only in mine  :',sorted(set(am)-set(bm)))
print('only in stored:',sorted(set(bm)-set(am)))
print('result differs:',[(k,am[k],bm[k]) for k in am.keys()&bm.keys() if am[k]!=bm[k]])
PY
```

## 7. Reproduce the 49 probe cases

```bash
cd /tmp/work-copylab
PYTHONPATH=/tmp/noneti python3 -B MASTER_COMPLETION/evidence/probes/p1_a1401_a1402.py "$PWD"  # 16
PYTHONPATH=/tmp/noneti python3 -B MASTER_COMPLETION/evidence/probes/p2_a1403_a1408.py "$PWD"  # 21
PYTHONPATH=/tmp/noneti python3 -B MASTER_COMPLETION/evidence/probes/p3_a1406_a1407_a1410.py "$PWD"  # 12
```

Each prints per-case JSON. `defect_reproduced: true` means **the defect was observed** — not that the system
passed. Several cases are deliberately *controls* that must be caught (`defect_reproduced: false`); if a
control flips to `true`, that probe has broken and its other results are suspect.

For A14-09:

```bash
mkdir -p /tmp/uiwork && cd /tmp/uiwork && npm install jsdom --no-audit --no-fund
python3 -B MASTER_COMPLETION/evidence/probes/state.json.py /tmp/work-copylab /tmp/uiwork/state.json
node MASTER_COMPLETION/evidence/probes/a1409.js /tmp/work-copylab/lab/dashboard.html \
     /tmp/uiwork/state.json /tmp/uiwork/a1409.json
```

## 8. Verify the project's own claim about itself

```bash
cd /tmp/work-copylab
PYTHONPATH=/tmp/noneti PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
# expect: Ran 119 tests ... OK
```

This is the project's sole positive control. **Note what that means:** 119/119 pass while all 32 invariants
above are violated. That is `F-01`, and it is why `MCD-01` R2 asks for the count to be demoted from an
acceptance gate to a regression guard.

## 9. Preservation check

Your extracted input must be untouched:

```bash
python3 - <<'PY'
import json,hashlib,os
os.chdir('/path/to/copylab-external-review-extracted')
m=json.load(open('_COPYLAB_TRANSFER/MANIFEST.json'))
bad=[n for n,v in m['files'].items() if hashlib.sha256(open(n,'rb').read()).hexdigest()!=v['sha256']]
print('mismatches:',len(bad),'of',len(m['files']))
PY
# expect: mismatches: 0 of 156
```

## 10. Reporting back

For each disagreement with `MASTER_COMPLETION/evidence/red-phase-results.json`, record: case id, expected,
observed, your environment, and whether you believe my test or the system is wrong. Both are useful. A
test that passes pre-fix is a **suite defect** and should be reported as such — I found five such defects in
my own first draft (`MCD-01` §5.3), including one that contradicted my own audit report.

If you can **falsify** any of the 49 probe cases, that is the most valuable thing you can return: it means a
finding in `INDEP-AUDIT-01` is overstated and must be corrected in the register.

---

## Appendix — isolation limits I could not enforce

- I cannot prove your environment is offline; that is yours to establish and state.
- I cannot prove the snapshot you hold is the one I reviewed without the SHA-256 in §2.
- Cross-version parity is unpinned (no requirements file). Record your Python/SQLite; divergence is a finding.
- The A14-09 test substitutes jsdom for Chromium. It exercises the real renderer code, not Chromium's paint.
  Treat it as evidence about *rendering logic*, not about browser behaviour.
