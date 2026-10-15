from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess,datetime
from PIL import Image,ImageDraw,ImageFont
w=Path.cwd();root=w/'delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA12_20261014';delivery=root.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Native screenshots: only crop the emulator's LCD footer, then nearest-neighbor scale.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
sheet=Image.new('RGB',(960,1410),'#efeee5');d=ImageDraw.Draw(sheet)
d.text((18,14),'Chocobo HF9 TEST — cuatro correcciones de texto',fill='#1b2921',font=font)
d.text((18,47),'ANTES · HF8',fill='#665c51',font=small);d.text((496,47),'DESPUÉS · HF9',fill='#254d39',font=small)
items=[('Propiedad contra no muertos','runs/q12_property_all_before/prop_6_19_20_f720.png','runs/q12_property_final_hf9/prop_6_19_20_f720.png'),('Ataque de tres direcciones','runs/q12_property_all_before/prop_6_25_26_f720.png','runs/q12_property_final_hf9/prop_6_25_26_f720.png'),('Propiedad de fuego de la silla','runs/q12_property_all_before/prop_7_01_02_f720.png','runs/q12_property_final_hf9/prop_7_01_02_f720.png'),('Nombre de Sleep Card','runs/q12_item_check_fixed/item_03_f720.png','runs/q12_critical_hf9/sleep_card_f720.png')]
for i,(label,left,right) in enumerate(items):
 y=78+i*328;d.text((18,y),label,fill='#1b2921',font=small)
 for x,path in [(18,left),(496,right)]:sheet.paste(Image.open(w/path).crop((0,0,224,144)).resize((448,288),Image.Resampling.NEAREST),(x,y+27))
preview=delivery/'Chocobo_HF9_QA12_Correcciones.png';sheet.save(preview)
(root/'evidence').mkdir(exist_ok=True);shutil.copy2(preview,root/'evidence'/preview.name)
# Include executable QA sources and labeled diagnostic runs, not upload helpers or private ROMs.
shutil.copytree(w/'qa12',root/'qa12',dirs_exist_ok=True,ignore=shutil.ignore_patterns('upload*','delivery_manifest.json','__pycache__','disasm_*.txt'))
fixture=root/'evidence/qa12_fixtures';fixture.mkdir(parents=True,exist_ok=True);shutil.copy2(w/'runs/q3_dungeon/checkpoint.mss',fixture/'checkpoint.mss')
index=[]
excluded={'q12_item_layout':'EXCLUDED_WRONG_ACTION_SELECTOR','q12_fused_records':'EXCLUDED_INVALID_PROPERTY_IDS_FAULT_INJECTION','q12_fusion_probe':'DIAGNOSTIC_NO_LINKED_PROPERTY_RECORD','q12_property_all_hf9':'INTERMEDIATE_CANDIDATE_NOT_FINAL_HASH'}
final={'q12_property_final_hf9','q12_critical_hf9'}
for p in sorted((w/'runs').glob('q12_*')):
 if not p.is_dir():continue
 meta=json.loads((p/'run.json').read_text());assert meta['completed'] and not meta['timed_out']
 dest=root/'evidence/qa12_runs'/p.name;shutil.copytree(p,dest,dirs_exist_ok=True)
 assert sha(dest/'observer.lua')==meta['script_sha256'];assert sha(dest/'cases.lua')==meta['cases_sha256']
 role=excluded.get(p.name,'FINAL_HF9_SYNTHETIC_NATIVE_MENU' if p.name in final else ('JP_CONTROL' if 'jp' in p.name else 'BASELINE_OR_EXPLORATORY'))
 index.append({'run':p.name,'role':role,'metadata':meta,'state_fixture':'evidence/qa12_fixtures/checkpoint.mss','source_state_sha256':sha(fixture/'checkpoint.mss'),'image_count':len(list(p.glob('*.png'))),'run_metadata_sha256':sha(p/'run.json')})
(root/'docs/QA12_RUN_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
(root/'docs/QA12_SCRIPT_HASHES.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in sorted((root/'qa12').rglob('*')) if p.suffix in {'.py','.lua'}},indent=2)+'\n')
# Verify the portable command against the packaged evidence.
r=subprocess.run(['python3','qa12/verify_scope.py','--hf8',str(w/'private_roms/hf8_release/Chocobo_EN_v1.1_HF8_TEST.ws'),'--hf9',str(w/'private_roms/hf9_release/Chocobo_EN_v1.1_HF9_TEST.ws'),'--runs','evidence/qa12_runs','--out','qa12/packaged_validation.json'],cwd=root,text=True,capture_output=True)
assert r.returncode==0,r.stdout+r.stderr
(root/'docs/QA12_PACKAGED_VERIFICATION_LOG.txt').write_text(r.stdout+r.stderr)
for p in root.rglob('__pycache__'):
 if p.is_dir():shutil.rmtree(p)
for p in root.rglob('*'):
 if p.is_file():assert p.suffix.lower() not in {'.ws','.wsc','.rom','.bios','.exe','.so'},str(p)
manifest=root/'SHA256SUMS.txt';files=[p for p in sorted(root.rglob('*')) if p.is_file() and p!=manifest]
manifest.write_text(''.join(f'{sha(p)}  {p.relative_to(root)}\n' for p in files))
z=delivery/(root.name+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in sorted(root.rglob('*')):
  if p.is_file():out.write(p,Path(root.name)/p.relative_to(root))
with zipfile.ZipFile(z) as check:assert check.testzip() is None
artifacts=[delivery/'Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps',z,delivery/'Informe_Chocobo_HF9_QA12_20261014.txt',preview]
info=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in artifacts]
(w/'qa12/delivery_manifest.json').write_text(json.dumps(info,indent=2)+'\n')
(w/'qa12/upload_request.json').write_text(json.dumps({'uploads':[{'local_path':str(p),'purpose':'create_library_file','library_artifact_type':t} for p,t in zip(artifacts,['other','other','report','image'])]},indent=2)+'\n')
print(json.dumps(info,indent=2));print('Packaged files:',len(files)+1)
