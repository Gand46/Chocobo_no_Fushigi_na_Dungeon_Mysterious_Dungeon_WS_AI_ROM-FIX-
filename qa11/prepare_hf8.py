from pathlib import Path
import json,shutil,hashlib,struct,zlib,datetime
w=Path.cwd();old=w/'delivery/Chocobo_EN_v1.1_HF7_TEST_Fuentes_QA10_20261014';root=w/'delivery/Chocobo_EN_v1.1_HF8_TEST_Fuentes_QA11_20261014'
shutil.copytree(old,root,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
history=root/'docs/history/hf7_qa10';history.mkdir(parents=True,exist_ok=True)
for p in ['README.md','INFORME_ES.md','CONTEXTO_PROYECTO.md','manifest.json','CHANGELOG.md','docs/approval_matrix.json','docs/quality_gates.json','docs/issue_register.json','docs/issue_register.csv']:
 if (root/p).exists():shutil.copy2(root/p,history/Path(p).name)
art=root/'assets/title/user_v01';shutil.copytree(w/'qa11/Chocobo_WS_Logo_EN_v0.1',art,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
c=json.loads((root/'src/corrections.json').read_text());c['edits']=[e for e in c['edits'] if not e['id'].startswith('TITLE_')]+json.loads((w/'qa11/title_edits.json').read_text());(root/'src/corrections.json').write_text(json.dumps(c,indent=2)+'\n')
b=(w/'private_roms/qa11_title.ws').read_bytes();prev=(w/'private_roms/hf7_release/Chocobo_EN_v1.1_HF7_TEST.ws').read_bytes();legacy=(w/'private_roms/EN.ws').read_bytes();jp=(w/'private_roms/JP.ws').read_bytes();assert hashlib.sha256(prev).hexdigest()==json.loads((old/'manifest.json').read_text())['target']['sha256']
m=json.loads((root/'manifest.json').read_text());m['previous_hf7']=m['target'];m.update(version='1.1-HF8-TEST',audit_revision='QA11_USER_LOGO_INTEGRATION',title='USER_PROVIDED_LOGO_V01_INTEGRATED_RUNTIME_CONFIRMED',date_timezone='America/Bogota',changed_bytes_vs_hf7=sum(a!=v for a,v in zip(prev,b)),changed_bytes_vs_english=sum(a!=v for a,v in zip(legacy,b)),changed_bytes_vs_japanese=sum(a!=v for a,v in zip(jp,b)),rom_changes_in_QA11=sum(a!=v for a,v in zip(prev,b)),user_logo_archive_sha256=hashlib.sha256((w/'upload/Chocobo_WS_Logo_EN_v0.1_Fuentes_y_Animacion.zip').read_bytes()).hexdigest())
m['target']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b):08X}','ws_checksum':f'{sum(b[:-2])&65535:04X}'};m.pop('bps_sha256',None)
(root/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
s=(root/'build.py').read_text().replace('HF7','HF8').replace('English native title + TitanSaddle residual glyph','user-provided English logo v0.1 with native animation + TitanSaddle residual glyph');(root/'build.py').write_text(s)
s=(root/'tests/test_project.py').read_text().replace("m['changed_bytes_vs_english'],4491",f"m['changed_bytes_vs_english'],{m['changed_bytes_vs_english']}");(root/'tests/test_project.py').write_text(s)
# Preserve previous title authoring with explicit historical status; new importer is canonical.
p=root/'tools/generate_title_fix.py';s=p.read_text();p.write_text('"""Historical HF7 lettering generator. HF8 uses integrate_title_assets.py and assets/title/user_v01."""\n'+s)
for f in (root/'patches').glob('*.bps'):f.unlink()
for p in [root/'tools/verify_evidence.py']:
 if p.exists():p.write_text(p.read_text().replace('HF7','HF8'))
(w/'qa11/start.json').write_text(json.dumps({'started_utc':'2026-10-14T08:09:48+00:00','base':'HF7','base_sha256':m['previous_hf7']['sha256'],'scope':'Integrate user-provided logo without redesign; synthetic/gameplay issues unchanged','safety_cap_minutes':40},indent=2))
print(json.dumps({k:m[k] for k in ['target','changed_bytes_vs_hf7','changed_bytes_vs_english','changed_bytes_vs_japanese']},indent=2))
