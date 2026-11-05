"""INDEPENDENT PROBES: A14-01 (paper verifier) and A14-02 (source verifier).

Author: independent reviewer agent. Written from source inspection, not copied from
docs/phase0-audit14/adversarial_checks.py. Disposable temp DBs only. No app/worker,
no network, no runtime data. Never modifies the extracted snapshot.
"""
import json, os, sqlite3, subprocess, sys, tempfile
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
from lab.store import Store, now
from lab.engine import Engine
from lab.integrity import Integrity

CFG = json.loads((ROOT / 'config.json').read_text())
RES = []
TMP = Path(tempfile.mkdtemp(prefix='indy-a1401-'))


def rec(case, observed, defect, note=''):
    RES.append({'case': case, 'observed': observed, 'defect_reproduced': defect, 'note': note})
    print(json.dumps(RES[-1], default=str))


def new_paper(name):
    s = Store(str(TMP / name), CFG, synthetic=True)
    return s, Engine(s, CFG)


def add_order_fill(e, s, side, qty, price, fee='0', model='A', track='ideal', wallet='fixture-wallet', token='T', event=None):
    oid = s.db.execute(
        'INSERT INTO orders(event,model,track,wallet,token,market,side,qty,reference,due,status,reason) '
        'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
        (event or f'ind-{now()}-{side}-{qty}-{price}', model, track, wallet, token, 'M', side, str(qty), str(price), now(), 'filled', 'independent probe')).lastrowid
    o = s.one('SELECT * FROM orders WHERE id=?', (oid,))
    with s.tx():
        e.a.fill(o, qty, price, fee, '0')
    return oid


def run_audit(dbpath):
    out = TMP / ('audit-' + Path(dbpath).name + '.json')
    r = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/audit.py'), '--db', dbpath, '--out', str(out)],
                       cwd=str(ROOT), capture_output=True, text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    rep = json.loads(out.read_text()) if out.exists() else {}
    return r.returncode, rep.get('errors'), rep


# ---------------------------------------------------------------- A14-01 variants
# (a) baseline: clean ledger must PASS
s, e = new_paper('a1-clean.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
add_order_fill(e, s, 'SELL', '4', '.8')
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-clean.sqlite'))
rec('A14-01/a clean ledger passes (control)', {'exit': rc, 'errors': errs, 'fills_replayed': rep.get('fills_replayed'), 'portfolios_checked': rep.get('portfolios_checked')}, rc == 0 and not errs)

# (b) archived case: ledger.realized tampered only
s, e = new_paper('a1-realized.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
add_order_fill(e, s, 'SELL', '10', '.8')
s.db.execute("UPDATE ledger SET realized='999' WHERE realized<>'0'")
m = e.a.metrics('A', 'ideal')
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-realized.sqlite'))
rec('A14-01/b ledger.realized tampered (archived case)',
    {'verifier_exit': rc, 'verifier_errors': errs, 'equity': m['portfolio_equity'], 'total_pnl': m['total_pnl'],
     'equity_minus_starting': str(F(m['portfolio_equity']) - F(1000))},
    rc == 0 and not errs, 'equity identity broken while verifier exits 0')

# (c) NEW: ledger.realized tampered with cash/fill columns left intact, plus fee tampered
s, e = new_paper('a1-fee.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5', '0.10')
s.db.execute("UPDATE ledger SET fee='55'")
m = e.a.metrics('A', 'ideal')
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-fee.sqlite'))
rec('A14-01/c NEW ledger.fee tampered (cash/realized untouched)',
    {'verifier_exit': rc, 'verifier_errors': errs, 'reported_fees': m['fees']}, rc == 0 and not errs,
    'audit.py never reconciles ledger.fee against fills.fee')

# (d) NEW: cost_delta tampered on BUY (ledger cost basis) -> positions still match, so silently accepted
s, e = new_paper('a1-cost.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
s.db.execute("UPDATE ledger SET cost_delta='12345'")
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-cost.sqlite'))
rec('A14-01/d NEW ledger.cost_delta tampered', {'verifier_exit': rc, 'verifier_errors': errs}, rc == 0 and not errs)

# (e) reported_equity/total_pnl identity: does audit.py recompute equity from ledger at all?
s, e = new_paper('a1-snapshot.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
s.db.execute("UPDATE snapshots SET equity='999999'")
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-snapshot.sqlite'))
rec('A14-01/e NEW snapshots.equity tampered', {'verifier_exit': rc, 'verifier_errors': errs}, rc == 0 and not errs,
    'snapshot equity series is not verified')

# (f) closed_positions tampered (realized of the cycle) -> metrics win_rate/PnL path
s, e = new_paper('a1-closed.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
add_order_fill(e, s, 'SELL', '10', '.8')
s.db.execute("UPDATE closed_positions SET proceeds='99999'")
m = e.a.metrics('A', 'ideal')
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-closed.sqlite'))
rec('A14-01/f NEW closed_positions.proceeds tampered', {'verifier_exit': rc, 'verifier_errors': errs, 'closed_pnl_not_used_in_metrics_total': True}, rc == 0 and not errs)

# (g) MISSING ledger row (deleted) -> orphans check catches fills w/o ledger, so must fail (guard)
s, e = new_paper('a1-missing.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
s.db.execute('DELETE FROM ledger')
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-missing.sqlite'))
rec('A14-01/g control: deleted ledger row IS caught', {'verifier_exit': rc, 'verifier_errors': errs}, not (rc != 0), 'control - must be caught')

# (h) NEW: negative quantity / oversell tamper in positions only
s, e = new_paper('a1-qty.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
s.db.execute("UPDATE positions SET qty='-5'")
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-qty.sqlite'))
rec('A14-01/h NEW positions.qty negative (stored) tamper', {'verifier_exit': rc, 'verifier_errors': errs}, rc == 0 and not errs)

# (i) NEW: fill duplicated in ledger semantics - cash_delta tampered, orphan-free
s, e = new_paper('a1-cash.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
s.db.execute("UPDATE ledger SET cash_delta='0'")
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-cash.sqlite'))
rec('A14-01/i NEW ledger.cash_delta tampered', {'verifier_exit': rc, 'verifier_errors': errs}, rc == 0 and not errs)

# (j) fill.qty tampered -> should be caught (verifier uses fill.qty); control
s, e = new_paper('a1-fillqty.sqlite')
add_order_fill(e, s, 'BUY', '10', '.5')
s.db.execute("UPDATE fills SET qty='11'")
s.db.close()
rc, errs, rep = run_audit(str(TMP / 'a1-fillqty.sqlite'))
rec('A14-01/j control: fills.qty tampered IS caught', {'verifier_exit': rc, 'verifier_errors': errs}, not (rc != 0))

# ---------------------------------------------------------------- A14-02 variants
sys.path.insert(0, str(ROOT))
import importlib.util
spec = importlib.util.spec_from_file_location('indy_source_verify', ROOT / 'tools/source_verify.py')
sv = importlib.util.module_from_spec(spec); spec.loader.exec_module(sv)


def new_source(name):
    return Store(str(TMP / name), synthetic=True)


def cert(s, identity, kind, payload, ordering):
    i = Integrity(s)
    eid = i.synthetic_event('fixture-wallet', identity, kind, payload, ordering)
    i.lifecycle(eid)
    return eid


# (a) archived orphan
s = new_source('a2-orphan.sqlite')
s.db.execute('INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) '
             'VALUES(?,?,?,?,?,?,?,?)', (None, 'fixture-wallet', 'T', '0', '0', '999', '999', 'indy-orphan'))
r = sv.verify(s.path)
s.db.close()
rec('A14-02/a orphan movement (event=NULL)', r, r['errors'] == [] and r['source_cash'] == '0')

# (b) NEW orphan pointing at a NONEXISTENT event id
s = new_source('a2-dangling.sqlite')
cert(s, 'buy-1', 'BUY', {'legs': [{'identity': 'l1', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e1']}, 0)
s.db.execute('INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) '
             'VALUES(?,?,?,?,?,?,?,?)', (99999, 'fixture-wallet', 'T', '5', '0', '777', '777', 'indy-dangling'))
r = sv.verify(s.path)
s.db.close()
rec('A14-02/b dangling event id movement', r, r['errors'] == [])

# (c) NEW: mutations on an existing event that never appear in its payload (extra stored movement)
s = new_source('a2-extra.sqlite')
eid = cert(s, 'buy-2', 'BUY', {'legs': [{'identity': 'l2', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e2']}, 0)
s.db.execute('INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) '
             'VALUES(?,?,?,?,?,?,?,?)', (eid, 'fixture-wallet', 'OTHER', '3', '1', '1', '1', 'indy-extra-leg'))
r = sv.verify(s.path)
s.db.close()
rec('A14-02/c extra movement on a valid event (leg not in payload)', r, r['errors'] == [])

# (d) NEW: orphan MOVEMENT with a real-looking wallet but a duplicate leg identity in an applied event
s = new_source('a2-dup.sqlite')
cert(s, 'buy-3', 'BUY', {'legs': [{'identity': 'l3', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e3']}, 0)
s.db.execute("INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) "
             "SELECT NULL,wallet,token,delta,cost_delta,cash,realized,'indy-clone' FROM source_movements")
r = sv.verify(s.path)
s.db.close()
rec('A14-02/d cloned movement rows with event=NULL', r, r['errors'] == [])

# (e) NEW: orphan effect row (source_effects with unknown/dangling event)
s = new_source('a2-effect.sqlite')
cert(s, 'buy-4', 'BUY', {'legs': [{'identity': 'l4', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e4']}, 0)
s.db.execute("INSERT INTO source_effects VALUES(?,?,?)", ('fixture-wallet', 'indy-orphan-effect', 424242))
r = sv.verify(s.path)
s.db.close()
rec('A14-02/e orphan source_effects row', r, r['errors'] == [])

# (f) NEW: cash-only tamper of an APPLIED event's stored movement is caught? control
s = new_source('a2-tamper.sqlite')
cert(s, 'buy-5', 'BUY', {'legs': [{'identity': 'l5', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e5']}, 0)
s.db.execute("UPDATE source_movements SET cash='-6'")
r = sv.verify(s.path)
s.db.close()
rec('A14-02/f control: applied movement cash tamper IS caught', r, bool(r['errors']))

output = TMP / 'results.json'
output.write_text(json.dumps(RES, indent=2, default=str))
Path('/home/user/audit-review/indy/results/p1-results.json').write_text(output.read_text())
print('WROTE', output, '->', len(RES), 'cases')
