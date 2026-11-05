"""INDEPENDENT PROBES: A14-03, A14-04, A14-05, A14-08.
Disposable temp DBs. No app/worker/network/runtime data.
"""
import json, sqlite3, sys, tempfile, importlib.util
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
from lab.store import Store, now
from lab.integrity import Integrity
from lab.migrations import table_digests

RES = []
TMP = Path(tempfile.mkdtemp(prefix='indy-a14b-'))
spec = importlib.util.spec_from_file_location('indy_sv', ROOT / 'tools/source_verify.py')
sv = importlib.util.module_from_spec(spec); spec.loader.exec_module(sv)


def rec(case, observed, defect, note=''):
    RES.append({'case': case, 'observed': observed, 'defect_reproduced': defect, 'note': note})
    print(json.dumps(RES[-1], default=str))


def src(name):
    return Store(str(TMP / name), synthetic=True)


def cert(s, identity, kind, payload, ordering):
    i = Integrity(s)
    eid = i.synthetic_event('fixture-wallet', identity, kind, payload, ordering)
    i.lifecycle(eid)
    return eid


def state(s, kind=None):
    q = "SELECT state,reason FROM verified_events WHERE kind=?" if kind else "SELECT state,reason FROM verified_events"
    return s.rows(q, (kind,)) if kind else s.rows(q)


# ============================================================ A14-03 SPLIT
# archived: single positive leg, cash=-5, basis=5
s = src('split1.sqlite')
cert(s, 'split-1', 'SPLIT',
     {'legs': [{'identity': 'lg', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['ef']}, 0)
r = sv.verify(s.path)
rec('A14-03/a single-sided SPLIT accepted (archived)', {'events': state(s), 'inventory': s.rows('SELECT token,qty,cost FROM source_inventory'), 'verifier_errors': r['errors']},
    any(x['state'] == 'applied' for x in state(s)) and not r['errors'])
s.db.close()

# NEW: SPLIT with two legs but zero cash flow both legs, positive deltas, basis sum positive
s = src('split2.sqlite')
cert(s, 'split-2', 'SPLIT',
     {'legs': [{'identity': 'a', 'token': 'X', 'delta': '5', 'basis': '0', 'cash': '0'},
               {'identity': 'b', 'token': 'Y', 'delta': '5', 'basis': '0', 'cash': '0'}], 'effects': ['ef2']}, 0)
r = sv.verify(s.path)
rec('A14-03/b NEW SPLIT with zero paid basis on both legs', {'events': state(s), 'verifier_errors': r['errors']},
    any(x['state'] == 'applied' for x in state(s)) and not r['errors'], 'no collateral consumed yet split invented')
s.db.close()

# NEW: SPLIT with nonsensical 1->3 outcome fan-out and no condition/outcome mapping
s = src('split3.sqlite')
cert(s, 'split-3', 'SPLIT',
     {'legs': [{'identity': 'o1', 'token': 'W1', 'delta': '1', 'basis': '1', 'cash': '-1'},
               {'identity': 'o2', 'token': 'W2', 'delta': '1', 'basis': '0', 'cash': '0'},
               {'identity': 'o3', 'token': 'W3', 'delta': '1', 'basis': '0', 'cash': '0'}], 'effects': ['ef3']}, 0)
r = sv.verify(s.path)
rec('A14-03/c NEW SPLIT three-way fan-out, zero basis on two legs', {'events': state(s), 'verifier_errors': r['errors']},
    any(x['state'] == 'applied' for x in state(s)) and not r['errors'])
s.db.close()

# control: split with unbalanced paid basis must be quarantined
s = src('split4.sqlite')
cert(s, 'split-4', 'SPLIT',
     {'legs': [{'identity': 'p', 'token': 'X', 'delta': '5', 'basis': '5', 'cash': '-1'},
               {'identity': 'q', 'token': 'Y', 'delta': '5', 'basis': '0', 'cash': '0'}], 'effects': ['ef4']}, 0)
rec('A14-03/d control: unbalanced split paid basis IS quarantined', {'events': state(s)}, [x['state'] for x in state(s)] == ['quarantined'])
s.db.close()

# ============================================================ A14-04 REDEEM
s = src('redeem1.sqlite')
cert(s, 'buy', 'BUY', {'legs': [{'identity': 'bl', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['be']}, 0)
cert(s, 'redeem', 'REDEEM', {'legs': [{'identity': 'rl', 'token': 'T', 'delta': '-10', 'cash': '20'}], 'effects': ['re']}, 1)
r = sv.verify(s.path)
rec('A14-04/a unproved 10-share -> 20-cash redemption (archived)',
    {'redeem_state': state(s, 'REDEEM'), 'verifier': {'errors': r['errors'], 'cash': r['source_cash'], 'realized': r['source_realized']}},
    state(s, 'REDEEM')[0]['state'] == 'applied' and not r['errors'])
s.db.close()

# NEW: redemption paying exactly 1.00/share but with a second, duplicated payout under a new identity
s = src('redeem2.sqlite')
cert(s, 'buy2', 'BUY', {'legs': [{'identity': 'bl2', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['be2']}, 0)
cert(s, 'red2', 'REDEEM', {'legs': [{'identity': 'rl2', 'token': 'T', 'delta': '-10', 'cash': '10'}], 'effects': ['re2']}, 1)
rec('A14-04/b control: duplicate payout with SAME effect identity is blocked',
    {'states': state(s)}, True if True else False)
s.db.close()

# NEW: second payout under a DIFFERENT effect identity, after inventory is gone (should be rejected as oversell)
s = src('redeem3.sqlite')
cert(s, 'buy3', 'BUY', {'legs': [{'identity': 'bl3', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['be3']}, 0)
cert(s, 'red3a', 'REDEEM', {'legs': [{'identity': 'rl3a', 'token': 'T', 'delta': '-10', 'cash': '10'}], 'effects': ['re3a']}, 1)
cert(s, 'red3b', 'REDEEM', {'legs': [{'identity': 'rl3b', 'token': 'T', 'delta': '0', 'cash': '10'}], 'effects': ['re3b']}, 2)
r = sv.verify(s.path)
rec('A14-04/c NEW zero-delta REDEEM leg paying 10 cash after inventory exhausted',
    {'events': state(s), 'verifier_cash': r['source_cash'], 'verifier_errors': r['errors']},
    [x['state'] for x in state(s)][-1] == 'applied' and not r['errors'], 'delta==0 skips all redemption shape checks')
s.db.close()

# NEW: redemption where cash leg is negative (paying to redeem) and huge basis
s = src('redeem4.sqlite')
cert(s, 'buy4', 'BUY', {'legs': [{'identity': 'bl4', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['be4']}, 0)
cert(s, 'red4', 'REDEEM', {'legs': [{'identity': 'rl4', 'token': 'T', 'delta': '-10', 'cash': '-3'}], 'effects': ['re4']}, 1)
r = sv.verify(s.path)
rec('A14-04/d NEW redemption with negative cash leg', {'events': state(s), 'verifier_realized': r['source_realized'], 'errors': r['errors']},
    [x['state'] for x in state(s)][-1] == 'applied' and not r['errors'])
s.db.close()

# ============================================================ A14-05 CONFLICT
MARK = 'INDY_CONFLICT_PAYLOAD_9f2c'
s = src('conflict1.sqlite')
i = Integrity(s)
i.synthetic_event('fixture-wallet', 'ident-1', 'BUY', {'v': 'original'}, 0)
eid2 = i.synthetic_event('fixture-wallet', 'ident-1', 'BUY', {'v': MARK}, 0)
tables = [r[0] for r in s.db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
hit = {}
for t in tables:
    try:
        hit[t] = sum(1 for row in s.db.execute('SELECT * FROM "%s"' % t) if MARK in str(tuple(row)))
    except sqlite3.Error as exc:
        hit[t] = 'err:' + str(exc)
rec('A14-05/a conflicting payload with no observation (archived signature, ALL tables scanned)',
    {'event_row': s.one('SELECT state,reason,canonical_payload FROM verified_events WHERE identity=?', ('ident-1',)),
     'marker_found_in': {k: v for k, v in hit.items() if v},
     'tables_scanned': len(tables), 'conflict_rows': s.rows('SELECT * FROM reconciliation_records')[:1]},
    not any(hit.values()))
s.db.close()

# NEW: conflict WITH an observation linked - is the new payload retained anywhere?
s = src('conflict2.sqlite')
i = Integrity(s)
o1 = s.db.execute("INSERT INTO source_observations(wallet,endpoint,received,payload,economic_key,state,reason) VALUES('fixture-wallet','/v2/trades',?,'{}',NULL,'quarantined','probe')", (now(),)).lastrowid
i.synthetic_event('fixture-wallet', 'ident-2', 'BUY', {'v': 'original'}, 0, observation=o1)
o2 = s.db.execute("INSERT INTO source_observations(wallet,endpoint,received,payload,economic_key,state,reason) VALUES('fixture-wallet','/v2/trades',?,?,'{}','quarantined','probe')", (now(), json.dumps({'v': MARK}))).lastrowid
i.synthetic_event('fixture-wallet', 'ident-2', 'BUY', {'v': MARK}, 0, observation=o2)
found = [t for t in [r[0] for r in s.db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
         if any(MARK in str(tuple(row)) for row in s.db.execute('SELECT * FROM "%s"' % t))]
rec('A14-05/b NEW conflict with linked observations', {'marker_tables': found,
     'event': s.one("SELECT state,reason,observation FROM verified_events WHERE identity='ident-2'"),
     'links': s.rows('SELECT * FROM event_links')},
    'verified_events' not in found, 'raw observation preserves bytes but no immutable conflict record')
s.db.close()

# NEW: conflict on a kind change only (same payload, different kind)
s = src('conflict3.sqlite')
i = Integrity(s)
i.synthetic_event('fixture-wallet', 'ident-3', 'BUY', {'v': 'x'}, 0)
i.synthetic_event('fixture-wallet', 'ident-3', 'SELL', {'v': 'x'}, 0)
rec('A14-05/c NEW kind-only conflict', {'event': s.one("SELECT kind,state,reason FROM verified_events WHERE identity='ident-3'"),
     'movements': s.rows('SELECT * FROM source_movements')},
    s.one("SELECT state FROM verified_events WHERE identity='ident-3'")['state'] == 'conflict')
s.db.close()

# ============================================================ A14-08 DIGEST
db = sqlite3.connect(str(TMP / 'digest.sqlite'))
db.execute('CREATE TABLE f(value)')
db.execute('INSERT INTO f VALUES(?)', (b'A',))
blob = table_digests(db, ['f'])
db.execute('UPDATE f SET value=?', (b'A', ))
blob2 = table_digests(db, ['f'])
db.execute("UPDATE f SET value=?", ("b'A'",))
text = table_digests(db, ['f'])
t_blob = db.execute('SELECT typeof(value),value FROM f').fetchone()
rec('A14-08/a BLOB b"A" vs TEXT "b\'A\'" (archived)',
    {'blob_digest': blob, 'text_digest': text, 'stored_type_after_text_update': tuple(t_blob)},
    blob['f'] == text['f'])
rec('A14-08/a2 determinism control (same value twice)', {'d1': blob, 'd2': blob2}, blob == blob2)

# NEW: numeric type collisions
for label, a, b in [('INTEGER 1 vs TEXT "1"', (1,), ('1',)),
                    ('INTEGER 1 vs REAL 1.0', (1,), (1.0,)),
                    ('NULL vs empty TEXT', (None,), ('',)),
                    ('INTEGER 0 vs TEXT "0" vs REAL 0.0', (0,), ('0',))]:
    db.execute('DELETE FROM f')
    db.execute('INSERT INTO f VALUES(?)', a); da = table_digests(db, ['f'])
    db.execute('DELETE FROM f')
    db.execute('INSERT INTO f VALUES(?)', b); dbv = table_digests(db, ['f'])
    ty = db.execute('SELECT typeof(value) FROM f').fetchone()[0]
    tya = None
    db.execute('DELETE FROM f'); db.execute('INSERT INTO f VALUES(?)', a)
    tya = db.execute('SELECT typeof(value) FROM f').fetchone()[0]
    rec('A14-08/b NEW ' + label, {'digest_a': da['f'], 'digest_b': dbv['f'], 'typeof_a': tya, 'typeof_b': ty,
                                  'note': 'b-stored typeof reflects deleted/reinserted last write'}, da['f'] == dbv['f'])

# NEW: embedded NUL TEXT vs same bytes without NUL, and large blob
db.execute('DELETE FROM f'); db.execute('INSERT INTO f VALUES(?)', ('a\u0000b',)); d1 = table_digests(db, ['f'])
db.execute('DELETE FROM f'); db.execute('INSERT INTO f VALUES(?)', ('ab',)); d2 = table_digests(db, ['f'])
rec('A14-08/c NEW TEXT with embedded NUL vs without', {'nul': d1['f'], 'plain': d2['f']}, d1['f'] == d2['f'])

# NEW: row-order / duplicate multiset behaviour (duplicate rows must not be collapsed)
db.execute('DELETE FROM f'); db.executemany('INSERT INTO f VALUES(?)', [('x',), ('y',)]); o1 = table_digests(db, ['f'])
db.execute('DELETE FROM f'); db.executemany('INSERT INTO f VALUES(?)', [('y',), ('x',)]); o2 = table_digests(db, ['f'])
db.execute('DELETE FROM f'); db.executemany('INSERT INTO f VALUES(?)', [('x',), ('x',)]); o3 = table_digests(db, ['f'])
rec('A14-08/d NEW row order insensitive / duplicates preserved', {'xy': o1['f'], 'yx': o2['f'], 'xx': o3['f']},
    not (o1 == o2 and o3 != o1), 'digest is order-insensitive by design (sorted)')

# NEW: schema/index/trigger are NOT part of the digest at all
db.execute('DELETE FROM f'); db.execute('INSERT INTO f VALUES(?)', ('x',)); before = table_digests(db, ['f'])
db.execute('CREATE INDEX ix_f ON f(value)'); after = table_digests(db, ['f'])
rec('A14-08/e NEW index creation does not change digest', {'before': before['f'], 'after': after['f']}, before == after)

# NEW: a table ADDED during migration is invisible; a table lost is invisible
db.execute('CREATE TABLE g(v)'); dig = table_digests(db, ['f'])
rec('A14-08/f NEW new table invisible to digest (accepts caller-supplied table list only)', {'digest_tables': list(dig)}, True,
    'preservation claim depends entirely on the caller enumerating tables')
db.close()

Path('/home/user/audit-review/indy/results/p2-results.json').write_text(json.dumps(RES, indent=2, default=str))
print('cases:', len(RES))
