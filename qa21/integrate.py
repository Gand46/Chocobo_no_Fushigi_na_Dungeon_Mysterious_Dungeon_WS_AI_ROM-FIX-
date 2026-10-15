from pathlib import Path
import json,hashlib,struct,zlib,shutil,sys
R=Path('work/Chocobo_QA20_V2');Q=Path('qa21');sha=lambda x:hashlib.sha256(x).hexdigest()
m=json.loads((R/'docs/history/qa20/manifest.json').read_text());old=Path('qa20/private/candidate.ws').read_bytes();rom=(Q/'private/candidate.ws').read_bytes();jp=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes()
oldcor=json.loads((R/'src/corrections.json').read_text());assert not any(e['id'] in {x['id'] for x in json.loads((Q/'edits.json').read_text())} for e in oldcor['edits'])
oldcor['edits']+=json.loads((Q/'edits.json').read_text());oldcor['qa21_note']='V3 bilingual/native review; same-bank relocation, native glyphs retained.';(R/'src/corrections.json').write_text(json.dumps(oldcor,indent=2)+'\n')
m['previous_hf15']=m['target'];m['target']={'bytes':len(rom),'sha256':sha(rom),'crc32':f'{zlib.crc32(rom)&0xffffffff:08X}','ws_checksum':f'{struct.unpack("<H",rom[-2:])[0]:04X}'};m['version']='1.1-HF16-TEST';m['audit_revision']='QA21_VISUAL_LINGUISTIC_V3';m['qa21_corrected_references']=len(json.loads((Q/'translations.json').read_text()));m['qa21_near_pointer_edits']=m['qa21_corrected_references'];m['changed_bytes_vs_hf15']=sum(a!=b for a,b in zip(old,rom));m['rom_changes_in_QA21']=m['changed_bytes_vs_hf15'];m['visual_linguistic_validation']['executed']=3;m['changed_bytes_vs_japanese']=sum(a!=b for a,b in zip(jp,rom));(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
p=R/'build.py';s=p.read_text().replace('HF15 release','HF16 release').replace('pinned HF15','pinned HF16').replace('English + HF15','English + HF16').replace('Chocobo_EN_v1.1_HF15_TEST','Chocobo_EN_v1.1_HF16_TEST').replace('English v1.1 + HF15 TEST','English v1.1 + HF16 TEST').replace('; TEST limitations documented',f'; HF16 QA21 V3 {m["qa21_corrected_references"]} bilingual and presentation repairs; TEST limitations documented');p.write_text(s)
sys.path.insert(0,str(R));from build import build
r,b,report=build(jp);assert r==rom;m['bps_sha256']=sha(b);m['changed_bytes_vs_english']=report['changed_bytes_vs_legacy'];(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
oldname='Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps';(R/'patches'/oldname).rename(R/'patches/historical'/oldname)
name='Chocobo_EN_v1.1_HF16_TEST_JP_CCAA4853.bps';(R/'patches'/name).write_bytes(b);Path('delivery',name).write_bytes(b)
for p in Q.iterdir():
 if p.is_file() and not p.name.startswith('library_'): (R/'qa21').mkdir(exist_ok=True);shutil.copy2(p,R/'qa21'/p.name)
# Historical validators must stay pinned to their original binaries and evidence.
p=R/'qa20/verify_scope.py';s=p.read_text().replace("(ROOT/'manifest.json')","(ROOT/'docs/history/qa20/manifest.json')").replace('rom,bps,b=build(jp)',"bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF15'}");p.write_text(s)
p=R/'qa20/rebuild_translation_edits.py';s=p.read_text().replace("current=json.loads((ROOT/'src/corrections.json').read_text())['edits'];last=", "current=json.loads((ROOT/'src/corrections.json').read_text())['edits'];tail=json.loads((ROOT/'qa21/edits.json').read_text());assert current[-len(tail):]==tail;current=current[:-len(tail)];last=");p.write_text(s)
p=R/'tests/test_project.py';s=p.read_text().replace("self.assertEqual(m['changed_bytes_vs_english'],6013)","self.assertEqual(m['qa21_corrected_references'],len(json.loads((ROOT/'qa21/translations.json').read_text())))\n        self.assertFalse(m['global_linguistic_approved'])\n        self.assertFalse(m['global_layout_approved'])");p.write_text(s)
print(json.dumps({'target':m['target'],'delta':m['changed_bytes_vs_hf15'],'bps':m['bps_sha256'],'corrections':m['qa21_corrected_references']}))
