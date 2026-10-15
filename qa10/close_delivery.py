from pathlib import Path
import json,hashlib,subprocess,shutil,zipfile,datetime
from PIL import Image,ImageDraw,ImageFont
w=Path.cwd();root=w/'delivery/Chocobo_EN_v1.1_HF7_TEST_Fuentes_QA10_20261014';delivery=root.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for name,cmd in [('unit_tests',['python3','-m','unittest','discover','-s','tests','-v']),('independent_bps',['python3','tools/verify_independent_bps.py',str(w/'private_roms/JP.ws')])]:
 r=subprocess.run(cmd,cwd=root,text=True,capture_output=True);(w/'qa10'/f'{name}.log').write_text(r.stdout+r.stderr);checks.append({'check':name,'exit':r.returncode,'output':r.stdout+r.stderr});assert r.returncode==0,(name,r.stdout,r.stderr)
(w/'qa10/final_validation.json').write_text(json.dumps(checks,indent=2))
index=[]
accepted={'q10_release_title_verified':'Final HF7: native title and menu','q10_release_items_verified':'Final HF7: TitanSaddle, GilTalon and LifeSaddle +99','q10_equipment_all':'Prior title candidate: 92 ordinary equipment Check cases; no reproduction of freeze','q10_final_atla_rescue':'Previous HF7 title candidate: exact pre-boss D2F60 rescue from synthetic state; no further RAM injection','q10_final_atla_boss':'Inherited event evidence: assisted boss fight','q10_final_atla_ending':'Inherited event evidence: ending and return to village','q10_final_atla_walk':'Inherited event evidence: native walking after return','q10_title_plain_caption':'Accepted final title pixels; 36 isolated glyphs reviewed'}
for d in sorted((w/'runs').glob('q10_*')):
 if not d.is_dir():continue
 r={'run':d.name,'scope':accepted.get(d.name,'Diagnostic candidate only; not a final release PASS'),'files':len(list(d.rglob('*')))}
 for meta in ('run.json','completed.txt'):
  f=d/meta
  if f.exists():r[meta]=json.loads(f.read_text()) if meta.endswith('json') else f.read_text()
 r['checkpoint_hashes']={str(f.relative_to(d)):sha(f) for f in sorted(d.rglob('*.mss'))}
 index.append(r)
 shutil.copytree(d,root/'evidence/qa10_runs'/d.name,dirs_exist_ok=True)
(root/'docs/QA10_RUN_INDEX.json').write_text(json.dumps({'final_rom_sha256':'116cd3df2828e97c890049619f6f43bf10102490f0c709a3dc836ec54a6a065a','inherited_event_evidence':'Final changes from Atla-tested candidate affect title assets and ROM checksum only. Event scripts and gameplay bytes are identical; inherited evidence is not a new final-hash run.','runs':index},indent=2))
shutil.copytree(w/'qa10',root/'qa10',dirs_exist_ok=True,ignore=shutil.ignore_patterns('upload*','__pycache__'))
script_hashes={str(f.relative_to(root)):sha(f) for f in sorted((root/'qa10').rglob('*')) if f.is_file() and f.suffix in ('.py','.lua')}
(root/'docs/QA10_SCRIPT_HASHES.json').write_text(json.dumps(script_hashes,indent=2))
canvas=Image.new('RGB',(952,1160),'#f4f2e9');draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
items=[('Título anterior',w/'runs/q8_title_reference/f01000.png'),('HF7: título inglés',w/'runs/q10_release_title_verified/f01000.png'),('Antes: TitanSaddlew',w/'runs/q10_equipment_all/check_A4_f720.png'),('HF7: TitanSaddle',w/'runs/q10_release_items_verified/titan_A4_f720.png'),('Atla: rescate D2, piso 60',w/'runs/q10_final_atla_rescue/f03510.png'),('Regreso y control en el pueblo',w/'runs/q10_final_atla_walk/f00480.png')]
for i,(label,f) in enumerate(items):
 assert f.exists(),str(f)
 x=16+(i%2)*472;y=12+(i//2)*365;draw.text((x,y),label,font=font,fill='#182530');im=Image.open(f).convert('RGB');canvas.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x,y+34))
draw.text((16,1108),'Acceso sintético documentado. Bloqueo y maquetación global siguen pendientes.',font=small,fill='#182530')
img=delivery/'Evidencia_Chocobo_HF7_QA10_20261014.png';canvas.save(img);shutil.copy2(img,root/'evidence'/img.name)
# Clean caches; prohibit complete ROMs and emulator binaries in source distribution.
for d in root.rglob('__pycache__'):shutil.rmtree(d)
for f in root.rglob('*'):
 if f.is_file():assert f.suffix.lower() not in {'.ws','.wsc','.rom','.bios','.exe','.so'},str(f)
files=[f for f in sorted(root.rglob('*')) if f.is_file() and f.name!='SHA256SUMS.txt']
(root/'SHA256SUMS.txt').write_text(''.join(f'{sha(f)}  {f.relative_to(root)}\n' for f in files))
z=delivery/(root.name+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for f in sorted(root.rglob('*')):
  if f.is_file():out.write(f,Path(root.name)/f.relative_to(root))
with zipfile.ZipFile(z) as check:assert check.testzip() is None
artifacts=[delivery/'Chocobo_EN_v1.1_HF7_TEST_JP_CCAA4853.bps',z,delivery/'Informe_Chocobo_HF7_QA10_20261014.txt',img]
manifest=[{'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f)} for f in artifacts]
(w/'qa10/delivery_manifest.json').write_text(json.dumps(manifest,indent=2))
(w/'qa10/upload_request.json').write_text(json.dumps({'uploads':[{'local_path':str(f),'purpose':'create_library_file','library_artifact_type':t} for f,t in zip(artifacts,['other','other','report','image'])]}))
print(json.dumps(manifest,indent=2));print(datetime.datetime.now(datetime.timezone.utc).isoformat())
