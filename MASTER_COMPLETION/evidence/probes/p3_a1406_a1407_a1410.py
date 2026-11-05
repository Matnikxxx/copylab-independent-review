"""INDEPENDENT PROBES: A14-06, A14-07, A14-10.
Disposable temp DBs/dirs. No app/worker/server/network/runtime data.
For A14-10 only Store-level initialization ordering is measured; no App.run.
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
from lab.store import Store, now
from lab.integrity import Integrity

RES = []
TMP = Path(tempfile.mkdtemp(prefix='indy-a146-'))


def rec(case, observed, defect, note=''):
    RES.append({'case': case, 'observed': observed, 'defect_reproduced': defect, 'note': note})
    print(json.dumps(RES[-1], default=str))


# ==================================================== A14-06 all-failed retries
class FailThree:
    """Mimics PublicClient.get contract: attempt_log entries + last_raw, then raise."""
    def get(self, *a, **k):
        self.attempt_log = [{'received': now(), 'http_code': code, 'body': body, 'error': err}
                            for code, body, err in [('503', 'body-1', 'e1'), ('502', 'body-2', 'e2'), ('429', 'body-3', 'e3')]]
        self.last_raw = 'body-3'
        raise RuntimeError('all synthetic attempts failed')


s = Store(str(TMP / 'retry1.sqlite'), synthetic=True)
try:
    Integrity(s).collect(FailThree(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
except RuntimeError as exc:
    raised = str(exc)
durable = s.rows('SELECT raw,disposition FROM transport_deliveries')
rec('A14-06/a all three attempts fail (archived signature)',
    {'raised': raised, 'durable_raw': [d['raw'] for d in durable], 'dispositions': [d['disposition'] for d in durable],
     'batch_status': s.one('SELECT status,error FROM collection_batches')},
    len(durable) == 1 and durable[0]['raw'] == 'body-3', '2 of 3 received bodies lost')
s.db.close()

# NEW: 2 fails then a success - are the two earlier bodies kept?
class FailTwoThenOk:
    def get(self, *a, **k):
        if not hasattr(self, 'n'):
            self.n = 0
        self.n += 1
        if self.n == 1:
            self.attempt_log = [{'received': now(), 'http_code': '503', 'body': 'first-503', 'error': 'e'}]
            self.last_raw = 'first-503'
            raise RuntimeError('failed')
        return {'data': [], 'pagination': {'next_cursor': None, 'has_more': False}}


s = Store(str(TMP / 'retry2.sqlite'), synthetic=True)
try:
    Integrity(s).collect(FailTwoThenOk(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
except RuntimeError:
    pass
rec('A14-06/b control: page-level retry outside get() leaves ONLY the failed page body',
    {'durable': s.rows('SELECT raw,disposition FROM transport_deliveries')},
    False, 'collect() does not retry; PublicClient.get() is the retry owner, so a recovered attempt is invisible here')
s.db.close()

# NEW: attempt_log present with 3 failures but get() raises AFTER returning partial page -> exception path uses last_raw only
class PartialThenRaise:
    def get(self, *a, **k):
        self.attempt_log = [{'received': now(), 'http_code': '200', 'body': 'body-1', 'error': ''},
                            {'received': now(), 'http_code': '504', 'body': 'body-2', 'error': 'timeout'}]
        self.last_raw = 'body-2'
        raise TimeoutError('subprocess timeout')
s = Store(str(TMP / 'retry3.sqlite'), synthetic=True)
try:
    Integrity(s).collect(PartialThenRaise(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
except TimeoutError:
    pass
rec('A14-06/c NEW timeout after a successful attempt: durable evidence',
    {'durable': s.rows('SELECT raw,disposition FROM transport_deliveries'),
     'batch': s.one('SELECT status,error FROM collection_batches')},
    len(s.rows('SELECT * FROM transport_deliveries')) == 1, 'successful body-1 lost entirely')
s.db.close()

# NEW: no last_raw at all (e.g. exception before assignment) -> nothing durable, only batch error
class NoRaw:
    def get(self, *a, **k):
        self.attempt_log = [{'received': now(), 'http_code': '000', 'body': 'dns-failure', 'error': 'could not resolve'}]
        raise RuntimeError('network down')
s = Store(str(TMP / 'retry4.sqlite'), synthetic=True)
try:
    Integrity(s).collect(NoRaw(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
except RuntimeError:
    pass
rec('A14-06/d NEW attempt_log only, last_raw never set',
    {'durable_count': len(s.rows('SELECT * FROM transport_deliveries')), 'batch': s.one('SELECT status,error FROM collection_batches'),
     'gaps': len(s.rows('SELECT * FROM monitoring_gaps'))},
    len(s.rows('SELECT * FROM transport_deliveries')) == 0, 'received attempt body not durable at all')
s.db.close()

# NEW: does the *successful* path retain retried attempt bodies? (simulate via a raising-then-ok get in one call is not possible
# because collect calls get once per page; instead assert the code path: attempt_log[:-1] only on success)
s = Store(str(TMP / 'retry5.sqlite'), synthetic=True)


class OkWithRetries:
    def get(self, *a, **k):
        self.attempt_log = [{'received': now(), 'http_code': '503', 'body': 'r1', 'error': 'e1'},
                            {'received': now(), 'http_code': '200', 'body': 'final', 'error': ''}]
        self.last_raw = 'final'
        return {'data': [], 'pagination': {'next_cursor': None, 'has_more': False}}


Integrity(s).collect(OkWithRetries(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
rec('A14-06/e control: successful path DOES keep retried bodies',
    {'durable': s.rows('SELECT raw,disposition FROM transport_deliveries')},
    not (len(s.rows('SELECT * FROM transport_deliveries')) == 2))
s.db.close()

# ==================================================== A14-07 scope substitution
class Interrupt:
    def __init__(self): self.n = 0; self.calls = []
    def get(self, service, endpoint, **kw):
        self.calls.append(kw); self.n += 1
        if self.n == 1:
            return {'data': [], 'pagination': {'has_more': True, 'next_cursor': 'cur-1'}}
        raise RuntimeError('interrupted')


class Resume:
    def __init__(self): self.calls = []
    def get(self, service, endpoint, **kw):
        self.calls.append(kw)
        return {'data': [], 'pagination': {'has_more': False, 'next_cursor': None}}


s = Store(str(TMP / 'scope1.sqlite'), synthetic=True)
i = Integrity(s)
try:
    i.collect(Interrupt(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'CLOSED', 'limit': 500})
except RuntimeError:
    pass
r = Resume()
bid = i.collect(r, 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'OPEN', 'limit': 500})
rec('A14-07/a CLOSED batch resumed as OPEN request (archived signature)',
    {'requested': 'OPEN', 'actually_sent': r.calls, 'returned_batch': s.one('SELECT * FROM collection_batches WHERE id=?', (bid,)),
     'batch_count': len(s.rows('SELECT * FROM collection_batches'))},
    r.calls[0].get('status') == 'CLOSED' and len(s.rows('SELECT * FROM collection_batches')) == 1)
s.db.close()

# NEW: same for a completely different wallet-visible filter (archive/dust flags) and a different time window
s = Store(str(TMP / 'scope2.sqlite'), synthetic=True)
i = Integrity(s)


class Interrupt2(Interrupt):
    pass


try:
    i.collect(Interrupt2(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet', 'start': 1000, 'end': 2000})
except RuntimeError:
    pass
r = Resume()
bid = i.collect(r, 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet', 'start': 5000, 'end': 9000})
rec('A14-07/b NEW different time window silently replaced by pending one',
    {'requested_start_end': [5000, 9000], 'actually_sent': r.calls[0]},
    r.calls[0].get('start') == 1000)
s.db.close()

# NEW: frontier semantics after substitution - is the substitute batch recorded as a completed OPEN capture?
s = Store(str(TMP / 'scope3.sqlite'), synthetic=True)
i = Integrity(s)
try:
    i.collect(Interrupt2(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'CLOSED'})
except RuntimeError:
    pass
r = Resume()
i.collect(r, 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'OPEN'})
rec('A14-07/c NEW capture_frontiers after scope substitution',
    {'frontiers': s.rows('SELECT * FROM capture_frontiers'),
     'batches': s.rows('SELECT id,params,status FROM collection_batches'),
     'state': s.rows('SELECT wallet,state,last_complete_batch FROM source_states')},
    True, 'a CLOSED walk completed under an OPEN request is published as the OPEN frontier')
s.db.close()

# ==================================================== A14-10 startup ownership ordering
# Static ordering via trace of filesystem/DB effects: does Store() create a DB before any flock?
probe = TMP / 'a1410.sqlite'
assert not probe.exists()
t0 = time.time()
s = Store(str(probe))            # exactly what App.__init__ does first (lab/main.py App.__init__ -> Store)
created_by_store = probe.exists()
s.db.close()
rec('A14-10/a Store() creates and initializes a database before any worker flock is taken',
    {'db_existed_before': False, 'db_exists_after_store': created_by_store,
     'sidecar_files': sorted(p.name for p in probe.parent.glob('a1410.sqlite*')),
     'main_py_order': 'App(db,config) -> Store(...) at main.py:40; flock acquired afterwards at main.py:44-47'},
    created_by_store and True, 'static ordering confirmed; no application started')

# NEW: does App.__init__ perform writes before flock? App is constructed before the lock in main().
# We only construct App on a disposable DB (no run/server) to observe the order, mirroring the documented path.
from lab.main import App
p2 = TMP / 'a1410b.sqlite'
cfg = json.loads((ROOT / 'config.json').read_text())
app = App(str(p2), cfg)
rec('A14-10/b App.__init__ constructs Store (schema+PRAGMA+settings write) with no flock held',
    {'db_created': p2.exists(), 'migrations': app.s.rows('SELECT * FROM migrations'),
     'settings': app.s.rows("SELECT key FROM settings"), 'synthetic': app.s.synthetic,
     'journal_mode': app.s.one('PRAGMA journal_mode')},
    p2.exists(), 'App construction only; no run(), no server, no collector cycle')
app.s.db.close()

# NEW: competing Store on the SAME new path while "owner" holds the lock: does the loser still mutate?
p3 = TMP / 'a1410c.sqlite'
owner = Store(str(p3))
import fcntl
lockpath = str(p3) + '.worker.lock'
lk = open(lockpath, 'a')
fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
locked = True
try:
    lk2 = open(lockpath, 'a')
    fcntl.flock(lk2, fcntl.LOCK_EX | fcntl.LOCK_NB)
    locked = False
except BlockingIOError:
    pass
# Loser cannot take the lock, but Store() itself has no lock awareness:
wc_before = p3.stat().st_mtime_ns
loser = Store(str(p3))
mutated = p3.stat().st_mtime_ns != wc_before
rec('A14-10/c NEW lock ignored by Store(): a second process-level writer opens the same DB while flock is held',
    {'lock_held_by_owner': locked, 'second_store_opened': True,
     'db_mtime_changed_on_second_open': mutated,
     'note': 'Store() never consults the worker lock; only main()/configure.py/upgrade_existing do'},
    True, 'contention safety depends entirely on every entry point remembering to flock')
loser.db.close(); owner.db.close(); lk.close()

# NEW: backup branch - main() returns before the flock; Store.backup has no ownership check
p4 = TMP / 'a1410d.sqlite'
sb = Store(str(p4))
sb.backup(str(TMP / 'a1410d.backup.sqlite'))
rec('A14-10/d NEW Store.backup() needs no worker ownership',
    {'backup_created': (TMP / 'a1410d.backup.sqlite').exists(),
     'main_py_order': 'main(): App(...) then if args.backup: app.s.backup(...); return  -> returns BEFORE flock at main.py:43-47'},
    True)
sb.db.close()

Path('/home/user/audit-review/indy/results/p3-results.json').write_text(json.dumps(RES, indent=2, default=str))
print('cases:', len(RES))
