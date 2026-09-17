import json,time
from dataclasses import asdict,replace
from datetime import UTC,datetime
from pathlib import Path
from jobhunter.config import Settings
from jobhunter.market_membership_service import build_market_membership_service
from jobhunter.market_store import MarketStore

out=Path('data/experiments/market-i3-20260917T162216Z')
base=json.loads((out/'report.json').read_text())
s=Settings.load('jobhunter.toml').model_copy(update={'database_path':out/'sandbox.sqlite3'})
market=MarketStore(s.database_path)
first=market.get_definition_version(1)
intent=('Applied AI / ML engineering where the primary work is developing, evaluating, or '
        'improving AI/ML models, agents, retrieval, or AI system behavior. '
        'Backend/API/database/infrastructure roles primarily enabling or integrating AI services '
        'are adjacent rather than core. Using AI tools for general software or content production '
        'does not qualify for this target.')
definition=market.create_definition_version(first.target_market_id,spec=replace(first.spec,membership_intent=intent),created_at=datetime.now(UTC))
service=build_market_membership_service(s)
provider=service._provider
class Recorder:
 def __init__(self): self.calls=0; self.job=None
 @property
 def identity(self): return provider.identity
 def classify(self,payload):
  self.calls+=1
  (out/f'{self.job}-clarified-input.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
  decision=provider.classify(payload)
  (out/f'{self.job}-clarified-decision.json').write_text(decision.model_dump_json(indent=2))
  return decision
recorder=Recorder();service._provider=recorder
report={'base_head':base['head'],'model':base['model'],'comparison':'only target definition changed; same model/prompt/evidence','target_version':definition.id,'membership_intent':intent,'refresh_after_hours':2160,'results':[]}
for prior in base['results']:
 job=prior['job'];recorder.job=job;started=time.monotonic()
 row={'job':job,'expected':prior['expected'],'synthetic':prior['synthetic']}
 print('START',job,flush=True)
 try:
  result=service.qualify(target_definition_version_id=definition.id,source_job_id=job,refresh_after_hours=2160)
  row['membership']=asdict(result.membership)
  row['expected_match']=result.membership.disposition==prior['expected']
  calls=recorder.calls
  reused=service.qualify(target_definition_version_id=definition.id,source_job_id=job,refresh_after_hours=2160)
  row['reuse_ok']=reused.outcome=='reused' and reused.membership.id==result.membership.id and calls==recorder.calls
 except Exception as exc:
  row['error_type']=type(exc).__name__; row['error']=str(exc)
 row['seconds']=round(time.monotonic()-started,2)
 report['results'].append(row)
 (out/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('RESULT',json.dumps(row,ensure_ascii=False),flush=True)
report['provider_calls']=recorder.calls
report['completed_at']=datetime.now(UTC).isoformat()
(out/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('COMPLETE',flush=True)
