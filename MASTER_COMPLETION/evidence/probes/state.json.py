import json,sys,sqlite3,tempfile
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(sys.argv[1]);sys.path.insert(0,str(ROOT))
from lab.store import Store
from lab.engine import Engine
from lab.main import App
cfg=json.loads((ROOT/'config.json').read_text())
t=tempfile.mkdtemp();s=Store(t+'/ui.sqlite',cfg)
state=App.state(SimpleNamespace(s=s,e=Engine(s,cfg),c=cfg,csrf='indy-ui-fixture'))
s.db.close()
# fixture health rows only; no app startup, no real state
state['health']=[
 {'component':'synthetic-ancient-ok','ts':0,'ok':1,'detail':'fixture: 1970 observation, never refreshed'},
 {'component':'synthetic-fresh-ok','ts':1793883000,'ok':1,'detail':'fixture'},
 {'component':'synthetic-stale-bad','ts':1793883000,'ok':0,'detail':'fixture'},
]
state['forward_validation_ready']=False
Path(sys.argv[2]).write_text(json.dumps(state))
print('state keys',len(state))
