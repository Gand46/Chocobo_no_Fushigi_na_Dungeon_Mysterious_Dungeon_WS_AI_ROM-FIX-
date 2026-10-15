from pathlib import Path
import shutil,json,hashlib,zlib,struct
BASE=Path('delivery/Chocobo_EN_v1.1_HF12_TEST_Fuentes_QA17_M3_20261014');OUT=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014')
old=Path('qa17/private/hf12_final/Chocobo_EN_v1.1_HF12_TEST.ws').read_bytes();new=Path('qa18/private/candidate2.ws').read_bytes();jp=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes();edits=json.loads(Path('qa18/edits.json').read_text());sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha(old)=='ffb5561da6e9f15df0bdd3e028fe78b19f05a79916f88cc5503ea25216bfe3d1';assert sha(new)=='a6bb2ee9e1d973f92aa7eac1a158f2873cde185075fc8a3b042dbe1f1dcb303f'
allowed={len(old)-2,len(old)-1}
for e in edits:
 a=int(e['offset'],16);b=a+len(bytes.fromhex(e['after']));assert old[a:b].hex()==e['before'];assert new[a:b].hex()==e['after'];allowed.update(range(a,b))
changed=[i for i,(a,b)in enumerate(zip(old,new))if a!=b];assert set(changed)<=allowed
shutil.copytree(BASE,OUT);hist=OUT/'docs/history/qa17';hist.mkdir(parents=True,exist_ok=True)
for n in ('README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','manifest.json'):shutil.copy2(OUT/n,hist/n)
p=OUT/'src/corrections.json';d=json.loads(p.read_text())
for e in edits:d['edits'].append({k:e[k]for k in ('id','offset','before','after','reason')})
p.write_text(json.dumps(d,indent=2)+'\n')
p=OUT/'build.py';s=p.read_text().replace('HF12','HF13').replace('HF13 QA17 M3 eleven bounded dialogue/template repairs','HF12 QA17 M3 eleven bounded dialogue/template repairs; HF13 QA18 M4 five bounded pagination and spacing repairs');p.write_text(s)
shutil.move(OUT/'patches/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps',OUT/'patches/historical/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps')
p=OUT/'qa17/verify_scope.py';s=p.read_text().replace("m=json.loads((ROOT/'manifest.json').read_text());jp=a.japanese_rom.read_bytes();rom,bps,b=build(jp)","m=json.loads((ROOT/'docs/history/qa17/manifest.json').read_text());jp=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF12_FROM_PRESERVED_BPS'}").replace("ROOT/'patches/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps'","ROOT/'patches/historical/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps'");p.write_text(s)
p=OUT/'manifest.json';m=json.loads(p.read_text());m['previous_hf12']=dict(m['target']);m['version']='1.1-HF13-TEST';m['audit_revision']='QA18_GLOBAL_LAYOUT_M4';m['target']={'bytes':len(new),'sha256':sha(new),'crc32':f'{zlib.crc32(new)&0xffffffff:08X}','ws_checksum':f'{sum(new[:-2])&65535:04X}'};m['rom_changes_in_QA18']=len(changed);m['changed_bytes_vs_hf12']=len(changed);m['new_bps_required']=True;m['corrected_resources']+=len(edits);m['changed_bytes_vs_japanese']=sum(a!=b for a,b in zip(jp,new));m['layout_iteration']={'completed':4,'planned':4,'remaining_base':0,'global_approval':False};m['qa18']={'new_corrected_unique_resources':5,'global_layout_approved':False,'global_linguistic_approved':False,'status':'TEST_PENDING_FINAL_EVIDENCE'};p.write_text(json.dumps(m,indent=2)+'\n')
Path('qa18/expected.json').write_text(json.dumps({'target':m['target'],'changed_offsets':[f'{x:06X}'for x in changed],'content_changed_bytes':len([x for x in changed if x<len(new)-2]),'checksum_changed_bytes':len([x for x in changed if x>=len(new)-2])},indent=2)+'\n');print(m['target']);print('changed bytes',len(changed))
