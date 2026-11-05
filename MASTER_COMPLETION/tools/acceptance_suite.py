"""CopyLab Phase-0 RED-PHASE ACCEPTANCE SUITE (design artefact, not a fix).

Purpose
-------
Every test here asserts the DESIRED (safe) invariant for a confirmed finding.
Run against the current snapshot, these tests MUST FAIL. That failure set is the
"red baseline" that later remediation must turn green, one finding at a time.

If any test in this file PASSES against the pre-fix snapshot, that test is either
wrong or the finding does not exist. Treat a surprise pass as a suite defect and
investigate before accepting any later green run.

Scope discipline
----------------
- Disposable temp DBs only. No application, worker, server or collector startup.
- No network. No runtime database. No wallet query. No project file is written.
- Symbolic fixture labels only; nothing here is a blockchain fact.

Usage
-----
    python3 -B acceptance_suite.py <path-to-paper-copy-lab> [--json OUT]

Exit code: 0 if EVERY test passed (i.e. all findings fixed), 1 otherwise.
Against the pre-fix snapshot exit code 1 is the EXPECTED result.
"""
import argparse, json, os, subprocess, sys, tempfile, traceback
from fractions import Fraction as F
from pathlib import Path

RES = []


def test(fid, name, severity, invariant):
    """Register a red-phase test. invariant = the safe behaviour being demanded."""
    def deco(fn):
        RES.append({'finding': fid, 'test': name, 'severity': severity,
                    'invariant': invariant, '_fn': fn})
        return fn
    return deco


def run(root):
    ok = fail = 0
    out = []
    for case in RES:
        row = {k: v for k, v in case.items() if not k.startswith('_')}
        try:
            ctx = Harness(root)
            try:
                case['_fn'](ctx)
                row['result'] = 'PASS'
                ok += 1
            finally:
                ctx.close()
        except AssertionError as exc:
            row['result'] = 'FAIL'
            row['detail'] = str(exc)[:600]
            fail += 1
        except Exception as exc:  # noqa: BLE001 - a broken probe must not look green
            row['result'] = 'ERROR'
            row['detail'] = f'{type(exc).__name__}: {exc}'[:600]
            fail += 1
        out.append(row)
    return out, ok, fail


class Harness:
    """One disposable workspace per test."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        sys.path.insert(0, str(self.root))
        self.tmp = tempfile.TemporaryDirectory(prefix='copylab-redphase-')
        self.dir = Path(self.tmp.name)
        self.cfg = json.loads((self.root / 'config.json').read_text())

    def close(self):
        for s in getattr(self, '_stores', []):
            try:
                s.db.close()
            except Exception:
                pass
        self.tmp.cleanup()

    # ---- helpers -------------------------------------------------------
    def store(self, name, synthetic=True, config=True):
        from lab.store import Store
        if not hasattr(self, '_stores'):
            self._stores = []
        s = Store(str(self.dir / name), self.cfg if config else None, synthetic=synthetic)
        self._stores.append(s)
        return s

    def integrity(self, s):
        from lab.integrity import Integrity
        return Integrity(s)

    def cert(self, s, identity, kind, payload, ordering):
        i = self.integrity(s)
        eid = i.synthetic_event('fixture-wallet', identity, kind, payload, ordering)
        i.lifecycle(eid)
        return eid

    def paper_with_fill(self, name, side, qty, price, fee='0'):
        from lab.engine import Engine
        from lab.store import now
        s = self.store(name)
        e = Engine(s, self.cfg)
        oid = s.db.execute(
            'INSERT INTO orders(event,model,track,wallet,token,market,side,qty,reference,due,status,reason) '
            'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
            (f'red-{side}-{qty}', 'A', 'ideal', 'fixture-wallet', 'T', 'M', side, str(qty), str(price), now(), 'filled', 'red-phase')).lastrowid
        o = s.one('SELECT * FROM orders WHERE id=?', (oid,))
        with s.tx():
            e.a.fill(o, qty, price, fee, '0')
        return s, e

    def audit(self, dbpath):
        """Run the shipped paper verifier as a separate process, as an operator would."""
        out = self.dir / ('audit-' + Path(dbpath).name + '.json')
        r = subprocess.run([sys.executable, '-B', str(self.root / 'tools/audit.py'),
                            '--db', str(dbpath), '--out', str(out)],
                           cwd=str(self.root), capture_output=True, text=True,
                           env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        rep = json.loads(out.read_text()) if out.exists() else {}
        return r.returncode, rep.get('errors'), rep

    def source_verify(self, dbpath):
        import importlib.util
        spec = importlib.util.spec_from_file_location('redphase_sv', self.root / 'tools/source_verify.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.verify(str(dbpath))


# =====================================================================
# A14-01  paper verifier must detect ledger corruption
# =====================================================================
@test('A14-01', 'ledger_realized_corruption_detected', 'HIGH',
      'A tampered ledger.realized must make the verifier exit non-zero')
def t(h):
    s, e = h.paper_with_fill('a1a.sqlite', 'BUY', '10', '.5')
    s.db.execute("UPDATE ledger SET realized='999'")
    m = e.a.metrics('A', 'ideal')
    rc, errs, _ = h.audit(s.path)
    assert rc != 0 and errs, f'verifier exit={rc} errors={errs} while total_pnl={m["total_pnl"]}'


@test('A14-01', 'ledger_fee_corruption_detected', 'MEDIUM',
      'A tampered ledger.fee must be detected against fills.fee')
def t(h):
    s, e = h.paper_with_fill('a1b.sqlite', 'BUY', '10', '.5', '0.10')
    s.db.execute("UPDATE ledger SET fee='55'")
    rc, errs, _ = h.audit(s.path)
    assert rc != 0 and errs, f'verifier exit={rc} errors={errs} (fee not reconciled)'


@test('A14-01', 'ledger_cost_delta_corruption_detected', 'MEDIUM',
      'A tampered ledger.cost_delta must be detected')
def t(h):
    s, e = h.paper_with_fill('a1c.sqlite', 'BUY', '10', '.5')
    s.db.execute("UPDATE ledger SET cost_delta='12345'")
    rc, errs, _ = h.audit(s.path)
    assert rc != 0 and errs, f'verifier exit={rc} errors={errs}'


@test('A14-01', 'snapshot_equity_corruption_detected', 'MEDIUM',
      'A tampered snapshots.equity must be detected or the curve marked unverified')
def t(h):
    from lab.store import now
    s, e = h.paper_with_fill('a1d.sqlite', 'BUY', '10', '.5')
    s.db.execute('INSERT INTO snapshots(model,track,ts,equity,metrics) VALUES(?,?,?,?,?)',
                 ('A', 'ideal', now(), '999999', json.dumps({'maximum_drawdown': '0'})))
    rc, errs, _ = h.audit(s.path)
    assert rc != 0 and errs, f'verifier exit={rc} errors={errs} (equity curve unverified)'


@test('A14-01', 'closed_position_cycle_corruption_detected', 'MEDIUM',
      'A tampered closed_positions.proceeds must be detected')
def t(h):
    s2, e2 = h.paper_with_fill('a1e.sqlite', 'BUY', '10', '.5')
    from lab.store import now
    oid = s2.db.execute(
        'INSERT INTO orders(event,model,track,wallet,token,market,side,qty,reference,due,status,reason) '
        'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
        ('red-sell', 'A', 'ideal', 'fixture-wallet', 'T', 'M', 'SELL', '10', '.8', now(), 'filled', 'red')).lastrowid
    o = s2.one('SELECT * FROM orders WHERE id=?', (oid,))
    with s2.tx():
        e2.a.fill(o, '10', '.8', '0', '0')
    s2.db.execute("UPDATE closed_positions SET proceeds='99999'")
    rc, errs, _ = h.audit(s2.path)
    assert rc != 0 and errs, f'verifier exit={rc} errors={errs} (closed cycle unverified)'


@test('A14-01', 'verifier_does_not_hardcode_integrity_ok', 'MEDIUM',
      'An empty database must not be reported as 10 verified portfolios')
def t(h):
    s = h.store('a1f.sqlite')
    rc, errs, rep = h.audit(s.path)
    assert rep.get('fills_replayed') == 0, 'fixture not empty'
    assert rep.get('portfolios_checked') != 10 or rc != 0, \
        f'hardcoded portfolios_checked={rep.get("portfolios_checked")} on an empty DB'


# =====================================================================
# A14-02  source verifier must cover every stored row
# =====================================================================
@test('A14-02', 'orphan_movement_detected', 'HIGH',
      'A movement with no reachable event must be reported by row identity')
def t(h):
    s = h.store('a2a.sqlite')
    s.db.execute('INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) '
                 'VALUES(?,?,?,?,?,?,?,?)', (None, 'fixture-wallet', 'T', '0', '0', '999', '999', 'red-orphan'))
    r = h.source_verify(s.path)
    assert r['errors'], f'errors={r["errors"]} source_cash={r["source_cash"]} (orphan invisible)'


@test('A14-02', 'dangling_event_movement_detected', 'HIGH',
      'A movement referencing a nonexistent event must be reported')
def t(h):
    s = h.store('a2b.sqlite')
    h.cert(s, 'b1', 'BUY', {'legs': [{'identity': 'l1', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e1']}, 0)
    s.db.execute('INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) '
                 'VALUES(?,?,?,?,?,?,?,?)', (99999, 'fixture-wallet', 'T', '5', '0', '777', '777', 'red-dangling'))
    r = h.source_verify(s.path)
    assert r['errors'], f'errors={r["errors"]} (dangling FK invisible; schema has no FK)'


@test('A14-02', 'extra_leg_on_valid_event_detected', 'HIGH',
      'A movement whose leg is absent from its event payload must be reported')
def t(h):
    s = h.store('a2c.sqlite')
    eid = h.cert(s, 'b2', 'BUY', {'legs': [{'identity': 'l2', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e2']}, 0)
    s.db.execute('INSERT INTO source_movements(event,wallet,token,delta,cost_delta,cash,realized,leg_identity) '
                 'VALUES(?,?,?,?,?,?,?,?)', (eid, 'fixture-wallet', 'GHOST', '3', '1', '1', '1', 'red-extra'))
    r = h.source_verify(s.path)
    assert r['errors'], f'errors={r["errors"]} (extra leg invisible)'


@test('A14-02', 'orphan_effect_detected', 'HIGH',
      'A source_effects row pointing at a nonexistent event must be reported')
def t(h):
    s = h.store('a2d.sqlite')
    h.cert(s, 'b3', 'BUY', {'legs': [{'identity': 'l3', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['e3']}, 0)
    s.db.execute('INSERT INTO source_effects VALUES(?,?,?)', ('fixture-wallet', 'red-orphan-effect', 424242))
    r = h.source_verify(s.path)
    assert r['errors'], f'errors={r["errors"]} (orphan effect invisible)'


# =====================================================================
# A14-03  SPLIT must be operation-complete
# =====================================================================
@test('A14-03', 'single_sided_split_quarantined', 'HIGH',
      'A split with no complementary outcome must be quarantined, not applied')
def t(h):
    s = h.store('a3a.sqlite')
    h.cert(s, 's1', 'SPLIT', {'legs': [{'identity': 'g', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['f']}, 0)
    st = s.one('SELECT state FROM verified_events')['state']
    assert st != 'applied', f'single-sided split state={st}'


@test('A14-03', 'zero_basis_split_quarantined', 'HIGH',
      'A split consuming no paid basis must be quarantined (cannot mint inventory)')
def t(h):
    s = h.store('a3b.sqlite')
    h.cert(s, 's2', 'SPLIT', {'legs': [
        {'identity': 'x', 'token': 'X', 'delta': '5', 'basis': '0', 'cash': '0'},
        {'identity': 'y', 'token': 'Y', 'delta': '5', 'basis': '0', 'cash': '0'}], 'effects': ['f2']}, 0)
    st = s.one('SELECT state FROM verified_events')['state']
    assert st != 'applied', f'zero-basis split state={st}; 0 == 0 satisfies the paid-basis identity'


@test('A14-03', 'nway_split_requires_operation_spec', 'HIGH',
      'A 3-way fan-out with no condition/outcome mapping must be quarantined')
def t(h):
    s = h.store('a3c.sqlite')
    h.cert(s, 's3', 'SPLIT', {'legs': [
        {'identity': 'o1', 'token': 'W1', 'delta': '1', 'basis': '1', 'cash': '-1'},
        {'identity': 'o2', 'token': 'W2', 'delta': '1', 'basis': '0', 'cash': '0'},
        {'identity': 'o3', 'token': 'W3', 'delta': '1', 'basis': '0', 'cash': '0'}], 'effects': ['f3']}, 0)
    st = s.one('SELECT state FROM verified_events')['state']
    assert st != 'applied', f'unspecified 3-way split state={st}'


# =====================================================================
# A14-04  REDEEM must require settlement proof
# =====================================================================
@test('A14-04', 'unproved_out_of_range_redemption_quarantined', 'HIGH',
      'A payout above one unit per share with no proof must be quarantined')
def t(h):
    s = h.store('a4a.sqlite')
    h.cert(s, 'rb', 'BUY', {'legs': [{'identity': 'bl', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['be']}, 0)
    h.cert(s, 'rr', 'REDEEM', {'legs': [{'identity': 'rl', 'token': 'T', 'delta': '-10', 'cash': '20'}], 'effects': ['re']}, 1)
    st = s.one("SELECT state FROM verified_events WHERE kind='REDEEM'")['state']
    assert st != 'applied', f'unproved redemption state={st}'


@test('A14-04', 'negative_cash_redemption_rejected', 'MEDIUM',
      'A redemption leg paying negative cash must not be applied as a payout')
def t(h):
    s = h.store('a4b.sqlite')
    h.cert(s, 'nb', 'BUY', {'legs': [{'identity': 'bn', 'token': 'T', 'delta': '10', 'basis': '5', 'cash': '-5'}], 'effects': ['bne']}, 0)
    h.cert(s, 'nr', 'REDEEM', {'legs': [{'identity': 'rn', 'token': 'T', 'delta': '-10', 'cash': '-3'}], 'effects': ['rne']}, 1)
    st = s.one("SELECT state FROM verified_events WHERE kind='REDEEM'")['state']
    assert st != 'applied', f'negative-cash redemption state={st}'


# =====================================================================
# A14-05  conflicting payload must be preserved append-only
# =====================================================================
MARK = 'REDPHASE_CONFLICT_MARKER_7f3a'


@test('A14-05', 'conflicting_payload_retained', 'MEDIUM',
      'A conflicting certificate payload must be durably retrievable after the conflict')
def t(h):
    s = h.store('a5a.sqlite')
    i = h.integrity(s)
    i.synthetic_event('fixture-wallet', 'c1', 'BUY', {'v': 'original'}, 0)
    i.synthetic_event('fixture-wallet', 'c1', 'BUY', {'v': MARK}, 0)
    tables = [r[0] for r in s.db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    found = [t for t in tables if any(MARK in str(tuple(row)) for row in s.db.execute('SELECT * FROM "%s"' % t))]
    assert found, f'conflicting payload not retained in any of {len(tables)} tables'


@test('A14-05', 'conflict_record_is_append_only', 'MEDIUM',
      'A conflict must leave an immutable record; state flip alone is insufficient')
def t(h):
    s = h.store('a5b.sqlite')
    i = h.integrity(s)
    i.synthetic_event('fixture-wallet', 'c2', 'BUY', {'v': 'original'}, 0)
    i.synthetic_event('fixture-wallet', 'c2', 'BUY', {'v': MARK}, 0)
    # An append-only design must retain BOTH raw payloads in dedicated evidence tables.
    # verified_events is mutable application state and does not count as conflict evidence.
    tables = [r[0] for r in s.db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    evidence_tables = [t for t in tables if t not in ('verified_events', 'reconciliation_records')]
    found = [t for t in evidence_tables
             if any(MARK in str(tuple(row)) for row in s.db.execute('SELECT * FROM "%s"' % t))]
    assert found, ('no append-only conflict evidence: the conflicting payload is absent from every '
                   f'non-state table ({len(evidence_tables)} checked); only mutable state/review rows exist')


# =====================================================================
# A14-06  every received attempt must be durable
# =====================================================================
@test('A14-06', 'all_failed_attempt_bodies_retained', 'MEDIUM',
      'Every received attempt body AND its metadata must be durable after total failure (R4 AMENDED)')
def t(h):
    from lab.store import now
    s = h.store('a6a.sqlite')
    base = now()
    ATTEMPTS = [('503', 'body-1', 'err-503'), ('502', 'body-2', 'err-502'), ('429', 'body-3', 'err-429')]

    class FailThree:
        def get(self, *a, **k):
            self.attempt_log = [{'received': base + i, 'http_code': c, 'body': b, 'error': e}
                                for i, (c, b, e) in enumerate(ATTEMPTS)]
            self.last_raw = 'body-3'
            raise RuntimeError('all failed')
    try:
        h.integrity(s).collect(FailThree(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
    except RuntimeError:
        pass
    rows = s.rows('SELECT * FROM transport_deliveries ORDER BY id')
    # R4: every relevant attempt body must be preserved, not just the last.
    raws = [r['raw'] for r in rows]
    assert len(rows) == 3, f'{len(rows)} durable rows for 3 received attempts: {raws}'
    for code, body, err in ATTEMPTS:
        assert body in raws, f'attempt body {body!r} lost; durable={raws}'
    # R4: AND associated metadata per attempt (code, error, receipt time), not just the body.
    for i, (code, body, err) in enumerate(ATTEMPTS):
        row = next(r for r in rows if r['raw'] == body)
        blob = ' '.join(str(v) for v in row.values())
        assert code in blob, f'attempt {i+1} body preserved without its HTTP code {code}'
        assert err in blob, f'attempt {i+1} body preserved without its error {err!r}'
        assert abs(float(row['received']) - (base + i)) < 2, \
            f'attempt {i+1} receipt time not preserved (received={row["received"]}, expected~{base+i})'


@test('A14-06', 'successful_body_survives_later_failure', 'MEDIUM',
      'An HTTP 200 body received before a later timeout must survive WITH its success metadata (R4 AMENDED)')
def t(h):
    from lab.store import now
    s = h.store('a6b.sqlite')
    base = now()

    class PartialThenRaise:
        def get(self, *a, **k):
            self.attempt_log = [{'received': base, 'http_code': '200', 'body': 'good-200', 'error': ''},
                                {'received': base + 5, 'http_code': '504', 'body': 'bad-504', 'error': 'timeout'}]
            self.last_raw = 'bad-504'
            raise TimeoutError('timeout')
    try:
        h.integrity(s).collect(PartialThenRaise(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
    except TimeoutError:
        pass
    rows = s.rows('SELECT * FROM transport_deliveries ORDER BY id')
    raws = [r['raw'] for r in rows]
    assert 'good-200' in raws, f'successful body destroyed; durable={raws}'
    assert 'bad-504' in raws, f'failing body destroyed; durable={raws}'
    ok = next(r for r in rows if r['raw'] == 'good-200')
    blob = ' '.join(str(v) for v in ok.values())
    assert '200' in blob, f'successful attempt lost its HTTP 200 code: {blob[:120]}'
    assert abs(float(ok['received']) - base) < 2, 'successful attempt lost its receipt time'


@test('A14-06', 'attempt_order_and_metadata_distinguishable', 'MEDIUM',
      'Concurrent same-body attempts must remain individually distinguishable with metadata (R4 AMENDED)')
def t(h):
    from lab.store import now
    s = h.store('a6d.sqlite')
    base = now()

    class SameBodyThreeCodes:
        def get(self, *a, **k):
            # Identical body text, three different outcomes. Collapsing on body text would
            # hide two attempts, so per-attempt identity+metadata (not body dedup) is required.
            self.attempt_log = [{'received': base + i, 'http_code': c, 'body': 'identical-body', 'error': f'e{i}'}
                                for i, c in enumerate(['500', '502', '503'])]
            self.last_raw = 'identical-body'
            raise RuntimeError('all failed')
    try:
        h.integrity(s).collect(SameBodyThreeCodes(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
    except RuntimeError:
        pass
    rows = s.rows('SELECT * FROM transport_deliveries ORDER BY id')
    assert len(rows) == 3, f'{len(rows)} rows for 3 attempts with identical bodies (attempt identity lost)'
    seen = set()
    for r in rows:
        blob = ' '.join(str(v) for v in r.values())
        codes = [c for c in ('500', '502', '503') if c in blob]
        assert codes, f'attempt row carries no HTTP code: {blob[:120]}'
        seen.add(codes[0])
    assert seen == {'500', '502', '503'}, f'distinct per-attempt outcomes collapsed: {seen}'


@test('A14-06', 'attempt_without_last_raw_is_durable', 'MEDIUM',
      'An attempt log with no last_raw (pre-response failure) must still be durable')
def t(h):
    from lab.store import now
    s = h.store('a6c.sqlite')

    class NoRaw:
        def get(self, *a, **k):
            self.attempt_log = [{'received': now(), 'http_code': '000', 'body': 'dns-failure', 'error': 'resolve failed'}]
            raise RuntimeError('network down')
    try:
        h.integrity(s).collect(NoRaw(), 'fixture-wallet', '/v2/trades', {'user': 'fixture-wallet'})
    except RuntimeError:
        pass
    rows = s.rows('SELECT * FROM transport_deliveries')
    raws = [r['raw'] for r in rows]
    assert 'dns-failure' in raws, f'durable bodies={raws}; nothing persisted at all'


# =====================================================================
# A14-07  collection scope must be immutable
# =====================================================================
@test('A14-07', 'scope_substitution_rejected', 'MEDIUM',
      'A pending CLOSED walk must not be sent as the caller\'s OPEN request')
def t(h):
    s = h.store('a7a.sqlite')
    i = h.integrity(s)

    class Interrupt:
        def __init__(self): self.n = 0
        def get(self, *a, **k):
            self.n += 1
            if self.n == 1:
                return {'data': [], 'pagination': {'has_more': True, 'next_cursor': 'cur-1'}}
            raise RuntimeError('interrupted')

    class Resume:
        def __init__(self): self.calls = []
        def get(self, *a, **k):
            self.calls.append(k)
            return {'data': [], 'pagination': {'has_more': False, 'next_cursor': None}}

    try:
        i.collect(Interrupt(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'CLOSED'})
    except RuntimeError:
        pass
    r = Resume()
    try:
        i.collect(r, 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'OPEN'})
    except Exception:
        pass
    sent = r.calls[0] if r.calls else {}
    assert sent.get('status') != 'CLOSED', f'OPEN request was sent as status={sent.get("status")}'


@test('A14-07', 'frontier_not_published_for_wrong_scope', 'MEDIUM',
      'A completed walk must not be published as the requested scope\'s frontier')
def t(h):
    s = h.store('a7b.sqlite')
    i = h.integrity(s)

    class Interrupt:
        def __init__(self): self.n = 0
        def get(self, *a, **k):
            self.n += 1
            if self.n == 1:
                return {'data': [], 'pagination': {'has_more': True, 'next_cursor': 'cur-1'}}
            raise RuntimeError('interrupted')

    class Resume:
        def get(self, *a, **k):
            return {'data': [], 'pagination': {'has_more': False, 'next_cursor': None}}
    try:
        i.collect(Interrupt(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'CLOSED'})
    except RuntimeError:
        pass
    i.collect(Resume(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'OPEN'})
    fronts = s.rows('SELECT * FROM capture_frontiers')
    bad = []
    for f in fronts:
        b = s.one('SELECT params FROM collection_batches WHERE id=?', (f['batch'],))
        if b and 'CLOSED' in b['params']:
            bad.append(f)
    assert not bad, f'frontier published for a CLOSED walk under an OPEN request: {bad}'


@test('A14-07', 'collect_enforces_scope_without_allowed', 'MEDIUM',
      'collect() itself must reject/isolate a scope mismatch, independent of allowed() or callers (R5 AMENDED)')
def t(h):
    s = h.store('a7c.sqlite')
    i = h.integrity(s)

    class Interrupt:
        def __init__(self): self.n = 0
        def get(self, *a, **k):
            self.n += 1
            if self.n == 1:
                return {'data': [], 'pagination': {'has_more': True, 'next_cursor': 'cur-1'}}
            raise RuntimeError('interrupted')

    class Resume:
        def __init__(self): self.calls = []
        def get(self, *a, **k):
            self.calls.append(k)
            return {'data': [], 'pagination': {'has_more': False, 'next_cursor': None}}

    try:
        i.collect(Interrupt(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'CLOSED'})
    except RuntimeError:
        pass
    batches_before = len(s.rows('SELECT * FROM collection_batches'))
    r = Resume()
    rejected = False
    try:
        i.collect(r, 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'OPEN'})
    except Exception:
        rejected = True
    # Acceptable outcomes are exactly two: explicit rejection, or an INDEPENDENT new batch
    # carrying the requested scope. Silently reusing the pending batch is the defect.
    # Note: allowed() is never consulted here, and no caller-side scope check is performed.
    batches_after = len(s.rows('SELECT * FROM collection_batches'))
    forked = batches_after > batches_before
    if not rejected and not forked:
        sent = r.calls[0] if r.calls else {}
        raise AssertionError(f'scope mismatch neither rejected nor forked: reused pending batch, '
                             f'sent status={sent.get("status")!r} for a requested OPEN scope')
    if forked:
        newest = s.one('SELECT * FROM collection_batches ORDER BY id DESC LIMIT 1')
        assert 'OPEN' in str(newest.get('params')), \
            f'forked batch does not carry the requested scope: {newest.get("params")}'


@test('A14-07', 'scope_identity_persisted_per_batch', 'MEDIUM',
      'Each batch must persist an explicit scope identity so resume validity never depends on wallet+endpoint (R5 AMENDED)')
def t(h):
    s = h.store('a7d.sqlite')
    i = h.integrity(s)

    class Ok:
        def get(self, *a, **k):
            return {'data': [], 'pagination': {'has_more': False, 'next_cursor': None}}

    i.collect(Ok(), 'fixture-wallet', '/v2/positions', {'user': 'fixture-wallet', 'status': 'OPEN', 'limit': 500})
    cols = [c[1] for c in s.db.execute('PRAGMA table_info(collection_batches)').fetchall()]
    batch = s.one('SELECT * FROM collection_batches ORDER BY id DESC LIMIT 1')
    # A scope identity must be an explicit, comparable field (e.g. scope_hash), not implied
    # by the (wallet, endpoint) lookup key that collect() uses to find resumable work.
    explicit = [c for c in cols if 'scope' in c.lower() or 'hash' in c.lower() or 'intent' in c.lower()]
    assert explicit, (f'collection_batches has no explicit scope-identity column (columns={cols}); '
                      f'resume validity rests on wallet+endpoint alone')
    value = next((batch[c] for c in explicit if batch.get(c)), None)
    assert value, f'scope identity column(s) {explicit} present but unpopulated: {batch}'


# =====================================================================
# A14-08  digest must be storage-type preserving
# =====================================================================
@test('A14-08', 'digest_distinguishes_blob_from_text', 'LOW',
      'BLOB b"A" and TEXT "b\'A\'" must produce different digests (default=str collision)')
def t(h):
    import sqlite3
    from lab.migrations import table_digests
    db = sqlite3.connect(str(h.dir / 'd8a.sqlite'))
    db.execute('CREATE TABLE f(value)')
    db.execute('INSERT INTO f VALUES(?)', (b'A',))
    a = table_digests(db, ['f'])['f']
    db.execute('UPDATE f SET value=?', ("b'A'",))
    ty = db.execute('SELECT typeof(value) FROM f').fetchone()[0]
    b = table_digests(db, ['f'])['f']
    db.close()
    assert a != b, f'collision: blob and text({ty}) share digest {a[:16]}'


@test('A14-08', 'digest_distinguishes_blob_from_its_repr_text', 'LOW',
      'A BLOB and the TEXT of its own Python repr must not collide through default=str')
def t(h):
    import sqlite3
    from lab.migrations import table_digests
    db = sqlite3.connect(str(h.dir / 'd8b.sqlite'))
    # Column with NO affinity so SQLite preserves the stored type. A collision here is a
    # genuine type-preservation failure, not an artefact of column affinity coercion.
    db.execute('CREATE TABLE f(value)')
    db.execute('INSERT INTO f VALUES(?)', (b'A',))
    ta = db.execute('SELECT typeof(value) FROM f').fetchone()[0]
    a = table_digests(db, ['f'])['f']
    db.execute('UPDATE f SET value=?', ("b'A'",))
    tb = db.execute('SELECT typeof(value) FROM f').fetchone()[0]
    b = table_digests(db, ['f'])['f']
    db.close()
    assert ta != tb, 'fixture did not preserve distinct storage types'
    assert a != b, f'collision: {ta} and {tb} share digest {a[:16]} (default=str renders bytes as the text b"..." )'


# =====================================================================
# A14-09  stale health must not render green
# =====================================================================
@test('A14-09', 'stale_health_not_green', 'MEDIUM',
      'A ts=0 ok=1 health row must not render as Healthy')
def t(h):
    html = (h.root / 'lab/dashboard.html').read_text()
    node = Path(__file__).resolve().parent.parent / 'evidence' / 'probes' / 'a1409.js'
    state_py = Path(__file__).resolve().parent.parent / 'evidence' / 'probes' / 'state.json.py'
    if not node.exists() or not state_py.exists():
        raise AssertionError('A14-09 probe harness missing (a1409.js / state.json.py)')
    state_file = h.dir / 'state.json'
    subprocess.run([sys.executable, '-B', str(state_py), str(h.root), str(state_file)], check=True,
                   capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    out = h.dir / 'a1409.json'
    r = subprocess.run(['node', str(node), str(h.root / 'lab/dashboard.html'), str(state_file), str(out)],
                       capture_output=True, text=True)
    if not out.exists():
        raise AssertionError(f'jsdom probe failed: {(r.stderr or "")[:300]}')
    res = json.loads(out.read_text())
    label = res.get('ancient_row_state_label')
    assert label != 'Healthy', f'stale ts=0 row rendered as {label!r}'


# =====================================================================
# A14-10  ownership must precede mutable initialization
# =====================================================================
@test('A14-10', 'lock_identity_is_canonical', 'MEDIUM',
      'A DB reached via symlink must use the same worker lock as the real path')
def t(h):
    import fcntl
    real = h.dir / 'real.sqlite'
    h.store('real.sqlite').db.close()
    link = h.dir / 'alias.sqlite'
    link.symlink_to(real)
    a = open(str(real) + '.worker.lock', 'a')
    fcntl.flock(a, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        b = open(str(link) + '.worker.lock', 'a')
        try:
            fcntl.flock(b, fcntl.LOCK_EX | fcntl.LOCK_NB)
            raise AssertionError('symlinked path acquired a SECOND exclusive lock: two owners possible')
        except BlockingIOError:
            pass
        finally:
            b.close()
    finally:
        a.close()


@test('A14-10', 'store_requires_ownership_before_write', 'MEDIUM',
      'While another owner holds the worker lock, a second Store must refuse or be read-only')
def t(h):
    import fcntl, sqlite3
    p = h.dir / 'owned.sqlite'
    h.store('owned.sqlite').db.close()
    lock = open(str(p) + '.worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)   # an owner holds it
    try:
        from lab.store import Store
        try:
            s2 = Store(str(p), h.cfg)
        except (ValueError, RuntimeError, BlockingIOError, SystemExit):
            return  # refusing is the safe outcome
        # It opened. It must not be a writer: any write attempt must fail.
        became_writer = False
        try:
            s2.db.execute("INSERT INTO settings VALUES('redphase','probe')")
            became_writer = True
        except sqlite3.Error:
            pass
        s2.db.close()
        assert not became_writer, ('a second Store() became a WRITER while the owner held the worker '
                                  'lock; Store() itself is not ownership-aware, so safety depends on '
                                  'every caller remembering to flock')
    finally:
        lock.close()


@test('A14-10', 'backup_requires_ownership', 'LOW',
      'A backup must not proceed while another process holds writer ownership')
def t(h):
    import fcntl
    from lab.store import Store
    p = h.dir / 'bk.sqlite'
    s = Store(str(p), h.cfg)
    lock = open(str(p) + '.worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)   # a different "owner" holds it
    dest = h.dir / 'bk-copy.sqlite'
    try:
        try:
            s.backup(str(dest))
        except (ValueError, RuntimeError, BlockingIOError, SystemExit):
            return  # refusing is the safe outcome
        assert not dest.exists(), 'backup succeeded while another owner held the worker lock'
    finally:
        lock.close()
        s.db.close()


# =====================================================================
# F-*  audit-tooling integrity findings from INDEP-AUDIT-01
# =====================================================================
@test('F-02', 'verifier_binds_database_identity', 'MEDIUM',
      'The verifier report must identify the database it verified (hash)')
def t(h):
    s, e = h.paper_with_fill('f2.sqlite', 'BUY', '10', '.5')
    import hashlib, re
    rc, errs, rep = h.audit(s.path)
    blob = json.dumps(rep).lower()
    # A path echo is NOT identity binding: the bytes at that path can change afterwards.
    # Demand the actual SHA-256 of the verified database bytes somewhere in the report.
    want = hashlib.sha256(Path(s.path).read_bytes()).hexdigest()
    assert want in blob, ('verifier report does not bind the verified database bytes '
                          f'(no sha256 {want[:12]}...); findings cannot be attributed to a snapshot')


@test('F-03', 'signing_scan_fails_closed', 'MEDIUM',
      'If the signing-code scan finds no source files it must error, not silently pass')
def t(h):
    decoy = h.dir / 'nowhere'
    decoy.mkdir()
    s, e = h.paper_with_fill('f3.sqlite', 'BUY', '10', '.5')
    out = h.dir / 'f3.json'
    r = subprocess.run([sys.executable, '-B', str(h.root / 'tools/audit.py'),
                        '--db', s.path, '--out', str(out)],
                       cwd=str(decoy), capture_output=True, text=True,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    rep = json.loads(out.read_text()) if out.exists() else {}
    assert r.returncode != 0 or any('scan' in str(x).lower() or 'source' in str(x).lower()
                                    for x in rep.get('errors', [])), \
        f'exit={r.returncode} errors={rep.get("errors")} - scan silently empty when cwd has no lab/'


@test('F-04', 'hold_history_is_append_only', 'MEDIUM',
      'Two successive holds must leave both reasons retrievable')
def t(h):
    from lab.store import now
    s = h.store('f4.sqlite')
    s.db.execute("INSERT INTO positions VALUES('A','ideal','fixture-wallet','T','M','2','1')")
    i = h.integrity(s)
    i.hold('fixture-wallet', 'gap A')
    i.hold('fixture-wallet', 'gap B')
    # Sample the FINAL state only. Unioning an earlier snapshot with a later one would
    # pass even if the second write destroyed the first (the mistake this test guards).
    reasons = {r['reason'] for r in s.rows('SELECT reason FROM paper_holds')}
    assert {'gap A', 'gap B'} <= reasons, f'hold history overwritten: final visible reasons={reasons}'


@test('F-05', 'hold_release_is_attributable', 'MEDIUM',
      'There must be a release path that records who released and on what evidence')
def t(h):
    s = h.store('f5.sqlite')
    s.db.execute("INSERT INTO positions VALUES('A','ideal','fixture-wallet','T','M','2','1')")
    i = h.integrity(s)
    i.hold('fixture-wallet', 'gap A')
    tables = [r[0] for r in s.db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    src = ''.join(p.read_text() for p in (h.root / 'lab').glob('*.py'))
    has_release = ('release' in src.lower()) or any('release' in t.lower() for t in tables)
    assert has_release, 'no hold-release mechanism or release record exists in code or schema'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--json')
    a = ap.parse_args()
    rows, ok, fail = run(a.root)
    rows.sort(key=lambda r: (r['finding'], r['test']))
    for r in rows:
        mark = {'PASS': 'PASS', 'FAIL': 'FAIL', 'ERROR': 'ERR '}[r['result']]
        print(f'[{mark}] {r["finding"]:8} {r["test"]:46} {r.get("detail","")}')
    summary = {'suite': 'copylab-red-phase-acceptance', 'snapshot_head': '288a69f64c24438cfe69ea176e6f3d6ce7333499',
               'total': len(rows), 'passed': ok, 'failed_or_error': fail,
               'expected_against_prefix_snapshot': 'failed_or_error == total',
               'phase': 'RED' if fail else 'GREEN', 'cases': rows}
    if a.json:
        Path(a.json).write_text(json.dumps(summary, indent=2))
    print(f'\nTOTAL {len(rows)}  PASS {ok}  FAIL {fail}   -> phase={summary["phase"]}')
    print('Red phase is EXPECTED against the pre-fix snapshot: every invariant above should fail.')
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
