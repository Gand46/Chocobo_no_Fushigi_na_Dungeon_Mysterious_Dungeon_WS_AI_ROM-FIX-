from pathlib import Path
import json,hashlib,zlib,shutil
R=Path('work/Chocobo_QA20_V2');old=Path('qa19/private/hf14_release/Chocobo_EN_v1.1_HF14_TEST.ws').read_bytes();new=Path('qa20/private/candidate.ws').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(old)=='056c7fa5eec4779ce7c21a07b640fbf7e32c4cc326bd2d462259f80390248a7c'
hist=R/'docs/history/qa19';hist.mkdir(parents=True,exist_ok=True)
for n in ['README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','manifest.json']:shutil.copy2(R/n,hist/n)
p=R/'src/corrections.json';d=json.loads(p.read_text());d['edits']+=json.loads(Path('qa20/edits.json').read_text());p.write_text(json.dumps(d,indent=2)+'\n')
p=R/'build.py';s=p.read_text().replace('HF14','HF15').replace('HF15 QA19 V1 36 references','HF14 QA19 V1 36 references').replace(' + TitanSaddle','; HF15 QA20 V2 74 bilingual and presentation repairs + TitanSaddle');p.write_text(s)
m=json.loads((R/'manifest.json').read_text());m['previous_hf14']=m['target'];m['target']={'bytes':len(new),'sha256':sha(new),'crc32':f'{zlib.crc32(new)&0xffffffff:08X}','ws_checksum':f'{sum(new[:-2])&65535:04X}'};m['version']='1.1-HF15-TEST';m['audit_revision']='QA20_VISUAL_LINGUISTIC_V2';m['qa20_corrected_references']=74;m['changed_bytes_vs_hf14']=sum(a!=b for a,b in zip(old,new));m['visual_linguistic_validation']={'executed':2,'planned':5,'global_approval':False};(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
# Preserve old patch and make old verifier explicitly historical.
p=R/'patches/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps';shutil.move(p,R/'patches/historical'/p.name)
p=R/'qa19/verify_scope.py';s=p.read_text().replace("m=json.loads((ROOT/'manifest.json').read_text());jp=a.japanese_rom.read_bytes();rom,bps,b=build(jp)","m=json.loads((ROOT/'docs/history/qa19/manifest.json').read_text());jp=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF14'}").replace("ROOT/'patches/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps'","ROOT/'patches/historical/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps'");p.write_text(s)
print(m['target'],m['changed_bytes_vs_hf14'])
