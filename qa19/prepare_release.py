from pathlib import Path
import shutil,json,hashlib,zlib,sys
BASE=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014');OUT=Path('delivery/Chocobo_EN_v1.1_HF14_TEST_Fuentes_QA19_V1_20261014')
old=Path('qa18/private/hf13_release/Chocobo_EN_v1.1_HF13_TEST.ws').read_bytes();new=Path('qa19/private/candidate.ws').read_bytes();jp=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes();edits=json.loads(Path('qa19/edits.json').read_text());sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha(old)=='a6bb2ee9e1d973f92aa7eac1a158f2873cde185075fc8a3b042dbe1f1dcb303f';assert sha(new)=='056c7fa5eec4779ce7c21a07b640fbf7e32c4cc326bd2d462259f80390248a7c'
allowed={len(old)-2,len(old)-1}
for e in edits:
 a=int(e['offset'],16);b=a+len(bytes.fromhex(e['after']));assert old[a:b].hex()==e['before'];assert new[a:b].hex()==e['after'];allowed.update(range(a,b))
changed=[i for i,(a,b)in enumerate(zip(old,new))if a!=b];assert set(changed)<=allowed

# Re-copy the immutable base over this task's draft; no deletion of source files.
shutil.copytree(BASE,OUT,dirs_exist_ok=True);hist=OUT/'docs/history/qa18';hist.mkdir(parents=True,exist_ok=True)
for n in ('README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','manifest.json'):shutil.copy2(OUT/n,hist/n)
p=OUT/'src/corrections.json';d=json.loads(p.read_text());d['edits']+=edits;p.write_text(json.dumps(d,indent=2)+'\n')
p=OUT/'build.py';s=p.read_text().replace('HF13','HF14').replace('HF14 QA18 M4 five bounded pagination and spacing repairs','HF13 QA18 M4 five bounded pagination and spacing repairs; HF14 QA19 V1 36 references corrected in same-bank verified free space');p.write_text(s)
shutil.move(OUT/'patches/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps',OUT/'patches/historical/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps')
p=OUT/'qa18/verify_scope.py';s=p.read_text().replace("m=json.loads((ROOT/'manifest.json').read_text());jp=a.japanese_rom.read_bytes();rom,bps,b=build(jp)","m=json.loads((ROOT/'docs/history/qa18/manifest.json').read_text());jp=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF13_FROM_PRESERVED_BPS'}").replace("ROOT/'patches/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps'","ROOT/'patches/historical/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps'");p.write_text(s)
p=OUT/'manifest.json';m=json.loads(p.read_text());m['previous_hf13']=dict(m['target']);m['version']='1.1-HF14-TEST';m['audit_revision']='QA19_VISUAL_LINGUISTIC_V1';m['target']={'bytes':len(new),'sha256':sha(new),'crc32':f'{zlib.crc32(new)&0xffffffff:08X}','ws_checksum':f'{sum(new[:-2])&65535:04X}'};m['rom_changes_in_QA19']=len(changed);m['changed_bytes_vs_hf13']=len(changed);m['new_bps_required']=True;m['corrected_resources_legacy_counter']=m['corrected_resources'];m['qa19_corrected_references']=36;m['changed_bytes_vs_japanese']=sum(a!=b for a,b in zip(jp,new));m['visual_linguistic_validation']={'completed':0,'planned':5,'global_approval':False};m['qa19']={'status':'TEST_PENDING_FINAL_EVIDENCE','references_reviewed':83,'references_changed':36,'unique_new_payloads':sum(x['id'].endswith('_payload')for x in edits),'global_visual_approved':False,'global_linguistic_approved':False};p.write_text(json.dumps(m,indent=2)+'\n');print(m['target'])
