from pathlib import Path
import json,hashlib,zipfile,datetime
W=Path(__file__).resolve().parents[1];D=W/'delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA16_M2_20261014'
v=json.loads((D/'docs/QA16_VERIFICATION.json').read_text())
s=json.loads((D/'docs/QA16_VALIDATION.json').read_text());s['verification']=v;(D/'docs/QA16_VALIDATION.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
m=json.loads((D/'manifest.json').read_text());m['qa16']['verification_summary']={k:v[k]for k in ['checks','approved_synthetic_runs','recorded_runs','independent_bps']};(D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for p in [W/'delivery/Chocobo_QA16_M2_Informe.html',D/'qa16/Chocobo_QA16_M2_Informe.html',D/'INFORME_ES.md']:
 p.write_text(p.read_text().replace('337',str(v['checks'])).replace('35 ejecuciones','36 ejecuciones'))
record=json.loads((D/'docs/QA16_ITERATION.json').read_text());record['sealed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['verification_checks']=v['checks'];record['approved_runs']=16;record['diagnostic_runs']=20;(D/'docs/QA16_ITERATION.json').write_text(json.dumps(record,indent=2)+'\n')
# Uncompressed execution artifacts remain in evidence; no executable, full ROM or raw disassembly input is distributed.
files=sorted(p for p in D.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name!='SHA256SUMS.txt')
assert not any(p.suffix.lower()in{'.ws','.wsc','.gba','.nes','.exe'}for p in files)
assert not list((D/'qa16').glob('*.bin'))
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(D))for p in files];(D/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n');files.append(D/'SHA256SUMS.txt')
z=Path(str(D)+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as f:
 for p in files:f.write(p,D.name+'/'+str(p.relative_to(D)))
with zipfile.ZipFile(z)as f:
 assert f.testzip()is None
 assert len(f.namelist())==len(files)
print(json.dumps({'file':str(z),'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'entries':len(files),'zip_crc':'PASS','ROM_files':0},indent=2))
