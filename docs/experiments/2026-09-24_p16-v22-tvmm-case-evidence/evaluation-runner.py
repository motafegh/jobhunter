import hashlib
import json
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path
from jobhunter.config import Settings
from jobhunter.analysis_service import _analysis_fields_for_english
from jobhunter.analysis_service_v20 import _ANALYSIS_SCHEMA_V20
from jobhunter.analysis_service_v22 import _ENGLISH_SYSTEM_PROMPT_V22
from jobhunter.analysis_runtime_v22 import V22CandidateAnalysisProvider

out = Path('data/local-acceptance/i7/v22-post-alias-evaluation-20260924.json')
if out.exists():
    raise SystemExit('Evaluation already recorded; refusing another invocation')
settings = Settings.load('jobhunter.toml')
projection_path = Path('corpus/jobs/tvMm/english-projection.json')
projection = json.loads(projection_path.read_text())
fields = _analysis_fields_for_english(projection['fields'])
def fingerprints():
    paths = [settings.database_path, *Path('corpus').rglob('*.json')]
    paths += list(settings.database_path.parent.glob(settings.database_path.name + '-*'))
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
before = fingerprints()
record = {'status': 'started', 'head': 'effa8616af03f2c11674317e8daade654ac19c5f', 'projection_sha256': hashlib.sha256(projection_path.read_bytes()).hexdigest(), 'started_at': time.time()}
out.write_text(json.dumps(record, indent=2))
provider = V22CandidateAnalysisProvider(base_url=settings.lm_studio_base_url, configured_model=settings.effective_analysis_lm_studio_model(), api_token=settings.lm_studio_api_token, timeout_seconds=settings.inference_timeout_seconds, max_retries=settings.inference_max_retries)
try:
    result = provider.complete_structured(system_prompt=_ENGLISH_SYSTEM_PROMPT_V22, user_payload={'source_job_id': 'tvMm', 'analysis_mode': 'english', 'analysis_fields': fields}, schema_name='jobhunter_job_analysis_english_v22', schema=_ANALYSIS_SCHEMA_V20, model=settings.effective_analysis_lm_studio_model(), max_tokens=settings.analysis_max_tokens)
    record.update(status='validated_pending_semantic_review', result=asdict(result))
except Exception as exc:
    record.update(status='failed', error_type=type(exc).__name__, error=str(exc))
finally:
    record['elapsed_seconds'] = time.time() - record['started_at']
    record['sqlite_and_corpus_unchanged'] = before == fingerprints()
    with sqlite3.connect(f'file:{settings.database_path}?mode=ro', uri=True) as con:
        record['integrity'] = con.execute('pragma integrity_check').fetchall()
        record['foreign_keys'] = con.execute('pragma foreign_key_check').fetchall()
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2))
    print(json.dumps({k:v for k,v in record.items() if k not in ('result', 'error')}, indent=2), flush=True)
    if 'error' in record: print(record['error'][-2000:], flush=True)
