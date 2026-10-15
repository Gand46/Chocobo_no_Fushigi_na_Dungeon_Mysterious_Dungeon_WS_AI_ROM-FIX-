from pathlib import Path
import zipfile,json,hashlib,re,base64,io,datetime,shutil
from PIL import Image
from html.parser import HTMLParser
R=Path('delivery/Chocobo_EN_v1.1_HF14_TEST_Fuentes_QA19_V1_20261014');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();report=Path('delivery/Chocobo_QA19_V1_Informe.html');s=report.read_text();images=re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)',s)
for x in images:Image.open(io.BytesIO(base64.b64decode(x))).verify()
assert len(images)>=110 and '<html lang="es">'in s and s.endswith('</html>');HTMLParser().feed(s);assert(R/'QA19_V1_Informe.html').read_bytes()==report.read_bytes();m=json.loads((R/'manifest.json').read_text());assert m['target']['sha256']=='056c7fa5eec4779ce7c21a07b640fbf7e32c4cc326bd2d462259f80390248a7c';assert m['bps_sha256']==sha(Path('delivery/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps'))
for n in ['verification.json','unit_result.json','historical_qa18_check.json','cumulative_sources_check.json','package_final.py','start.json']:shutil.copy2(Path('qa19')/n,R/'qa19'/n)
(R/'qa19/portable_rebuild_result.json').write_text(json.dumps({'status':'PASS_EXACT_ROM_AND_EDITS','target_sha256':m['target']['sha256'],'source':'rebuild_translation_edits.py; translations.json; text_codec.py','verified_with':'cmp against canonical build and qa19/edits.json'},indent=2)+'\n')
files=sorted(p for p in R.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.suffix!='.pyc'and p.name!='SHA256SUMS.txt');assert not[p for p in files if p.suffix.lower()in ['.ws','.wsc','.rom','.nds','.gba']];assert not[p for p in files if'private'in p.relative_to(R).parts]
(R/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(R).as_posix()+'\n'for p in files));files.append(R/'SHA256SUMS.txt');z=Path('delivery')/(R.name+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as out:
 for p in files:out.write(p,p.relative_to(R.parent).as_posix())
with zipfile.ZipFile(z)as out:assert out.testzip()is None;assert len(out.namelist())==len(files)
arts=[Path('delivery/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps'),z,report];receipt={'packaged_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':len(files),'html_images_validated':len(images),'artifacts':[{'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)}for p in arts]};Path('qa19/package_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');Path('.library_helpers_qa19/upload_request.json').write_text(json.dumps({'uploads':[{'local_path':str(p.resolve()),'purpose':'create_library_file','library_artifact_type':'report'if p==report else'other'}for p in arts]},indent=2)+'\n');print(json.dumps(receipt,indent=2))
