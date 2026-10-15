from pathlib import Path
import zipfile,json,hashlib,re,base64,io,datetime,shutil
from PIL import Image
R=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();report=Path('delivery/Chocobo_QA18_M4_Informe.html');s=report.read_text();embedded=re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)',s);assert len(embedded)==1
for x in embedded:Image.open(io.BytesIO(base64.b64decode(x))).verify()
assert '<html lang="es">'in s and s.endswith('</html>');assert (R/'QA18_M4_Informe.html').read_bytes()==report.read_bytes();m=json.loads((R/'manifest.json').read_text());assert m['target']['sha256']=='a6bb2ee9e1d973f92aa7eac1a158f2873cde185075fc8a3b042dbe1f1dcb303f'
for n in ['verification.json','unit_stdout.txt','coverage_summary.json','historical_qa17_check.json']:shutil.copy2(Path('qa18')/n,R/'qa18'/n)
# Preserve the packaging recipe itself before enumerating.
shutil.copy2(Path(__file__),R/'qa18/package_final.py')
files=sorted(p for p in R.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.suffix!='.pyc'and p.name!='SHA256SUMS.txt');assert not[p for p in files if p.suffix.lower()in ['.ws','.wsc','.rom','.nds','.gba']];assert not[p for p in files if 'private'in p.relative_to(R).parts]
(R/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(R).as_posix()+'\n'for p in files));files.append(R/'SHA256SUMS.txt');z=Path('delivery')/(R.name+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as out:
 for p in files:out.write(p,p.relative_to(R.parent).as_posix())
with zipfile.ZipFile(z)as out:assert out.testzip()is None;assert len(out.namelist())==len(files)
arts=[Path('delivery/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps'),z,report];receipt={'packaged_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':len(files),'artifacts':[{'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)}for p in arts]};Path('qa18/package_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');Path('.library_helpers_qa18/upload_request.json').write_text(json.dumps({'uploads':[{'local_path':str(p.resolve()),'purpose':'create_library_file','library_artifact_type':'report'if p==report else'other'}for p in arts]},indent=2)+'\n');print(json.dumps(receipt,indent=2))
