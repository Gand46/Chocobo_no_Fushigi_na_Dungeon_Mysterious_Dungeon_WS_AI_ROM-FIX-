from pathlib import Path
import shutil,json,hashlib,zlib,struct,sys
BASE=Path('delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA16_M2_20261014');OUT=Path('delivery/Chocobo_EN_v1.1_HF12_TEST_Fuentes_QA17_M3_20261014')
old=Path('qa15/private/hf11_final/Chocobo_EN_v1.1_HF11_TEST.ws').read_bytes();new=Path('qa17/private/candidate.ws').read_bytes();jp=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes()
assert hashlib.sha256(old).hexdigest()=='83de8ad93ddfab014670c9ddeea0e71656da55a0f429512e4182e3c280d759bf'
assert hashlib.sha256(new).hexdigest()=='ffb5561da6e9f15df0bdd3e028fe78b19f05a79916f88cc5503ea25216bfe3d1'
edits=json.loads(Path('qa17/edits.json').read_text());allowed={len(old)-2,len(old)-1};sys.path.insert(0,str(BASE/'qa15'));from inventory_layout import story_inventory
rows,_=story_inventory(old,'HF11');ptrs=sorted(set(int(x['pointer'],16) for x in rows))
for e in edits:
 a=int(e['offset'],16);b=a+len(bytes.fromhex(e['after']));assert old[a:b].hex()==e['before'];assert new[a:b].hex()==e['after'];assert b<=min(x for x in ptrs if x>a);allowed.update(range(a,b))
changed=[i for i,(a,b)in enumerate(zip(old,new))if a!=b];assert set(changed)<=allowed
shutil.copytree(BASE,OUT)
hist=OUT/'docs/history/qa16';hist.mkdir(parents=True,exist_ok=True)
for n in ('README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','manifest.json'):shutil.copy2(OUT/n,hist/n)
p=OUT/'src/corrections.json';d=json.loads(p.read_text())
for e in edits:d['edits'].append({k:e[k] for k in ('id','offset','before','after','reason')})
p.write_text(json.dumps(d,indent=2)+'\n')
p=OUT/'build.py';s=p.read_text().replace('HF11','HF12').replace('HF12 scoped G05:M002 line break repair','HF11 G05:M002 repair; HF12 QA17 M3 eleven bounded dialogue/template repairs');p.write_text(s)
shutil.move(OUT/'patches/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps',OUT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps')
p=OUT/'manifest.json';m=json.loads(p.read_text());m['previous_hf11']=dict(m['target']);m['version']='1.1-HF12-TEST';m['audit_revision']='QA17_GLOBAL_LAYOUT_M3';m['target']={'bytes':len(new),'sha256':hashlib.sha256(new).hexdigest(),'crc32':f'{zlib.crc32(new)&0xffffffff:08X}','ws_checksum':f'{sum(new[:-2])&65535:04X}'}
m['rom_changes_in_QA17']=len(changed);m['changed_bytes_vs_hf11']=len(changed);m['new_bps_required']=True;m['corrected_resources']+=len(edits);m['changed_bytes_vs_japanese']=sum(a!=b for a,b in zip(jp,new));m['layout_iteration']={'completed':3,'planned':4,'remaining_base':1,'global_approval':False}
m['qa17']={'new_corrected_unique_resources':11,'new_corrected_references':13,'static_alerts_repaired':9,'padding_only_alerts':3,'composite_resource_context_pending':['G16:M064'],'dynamic_unique_templates':7,'dynamic_references':9,'global_layout_approved':False,'global_linguistic_approved':False,'status':'TEST_PENDING_FINAL_EVIDENCE'}
p.write_text(json.dumps(m,indent=2)+'\n')
# Historical QA validators explicitly target the preserved HF11 patch and manifest.
p=OUT/'qa15/verify_scope.py';s=p.read_text().replace("m=json.loads((ROOT/'manifest.json').read_text());src=a.japanese_rom.read_bytes();rom,patch,b=build(src)","m=json.loads((ROOT/'docs/history/qa16/manifest.json').read_text());src=a.japanese_rom.read_bytes();patch=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(src,patch);b={'scope':'HISTORICAL_HF11_FROM_PRESERVED_BPS'}").replace("ROOT/'patches/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps'","ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps'");p.write_text(s)
p=OUT/'qa16/verify_scope.py';s=p.read_text().replace("manifest=json.loads((ROOT/'manifest.json').read_text());src=a.japanese_rom.read_bytes();rom,bps,b=build(src)","manifest=json.loads((ROOT/'docs/history/qa16/manifest.json').read_text());src=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes();rom=independent_apply(src,bps);b={'scope':'HISTORICAL_HF11_FROM_PRESERVED_BPS'}").replace("ROOT/'patches/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps'","ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps'");p.write_text(s)
Path('qa17/expected.json').write_text(json.dumps({'target':m['target'],'changed_offsets':[f'{x:06X}'for x in changed],'content_changed_bytes':len([x for x in changed if x<len(new)-2]),'checksum_changed_bytes':len([x for x in changed if x>=len(new)-2])},indent=2)+'\n')
print(m['target']);print('changed bytes',len(changed))
