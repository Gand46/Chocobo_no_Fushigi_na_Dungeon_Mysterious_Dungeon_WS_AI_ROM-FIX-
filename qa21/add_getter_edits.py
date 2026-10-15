from pathlib import Path
import json,sys,struct,hashlib,zlib
Q=Path('qa21');R=Path('work/Chocobo_QA20_V2');sys.path.insert(0,str(Q));from text_codec import encode
sys.path.insert(0,str(R));from qa15.inventory_layout import getter_inventory,words_until_end
base=Path('qa20/private/candidate.ws').read_bytes();rom=bytearray((Q/'private/candidate.ws').read_bytes());rows={x['id']:x for x in getter_inventory(base,'HF15')[0]};trs={'F06:I019':{'text':'Strong vs undead','reason':'Eficacia contra enemigos no muertos; sustituye Strong to por Strong vs.'},'F06:I022':{'text':'Strong vs poison foes','reason':'Eficacia contra enemigos venenosos; no resistencia al estado veneno.'}};edits=json.loads((Q/'edits.json').read_text());c=json.loads((R/'src/corrections.json').read_text());g=[]
for id,d in trs.items():
 a=int(rows[id]['pointer'],16);words,_,_=words_until_end(base,a);ew=list(encode(d['text']));assert len(ew)<=len(words);payload=struct.pack('<'+'H'*len(words),*(ew+[0]*(len(words)-len(ew))));e={'id':id+'_getter_payload','offset':hex(a),'before':base[a:a+len(payload)].hex(),'after':payload.hex(),'reason':d['reason']};rom[a:a+len(payload)]=payload;edits.append(e);g.append({'id':id,'pointer':hex(a),'bytes':len(payload),'words':ew,'text':d['text'],'reason':d['reason']})
 overlaps=[x for x in c['edits']if int(x['offset'],16)<a+len(payload)and int(x['offset'],16)+len(bytes.fromhex(x['after']))>a]
 if overlaps:
  assert len(overlaps)==1;old=overlaps[0];assert int(old['offset'],16)==a and len(bytes.fromhex(old['after']))>=len(payload);assert old['after'][:len(payload)*2]==e['before'];old['after']=e['after']+old['after'][len(payload)*2:];old['reason']+='; QA21: '+d['reason']
 else:c['edits'].append(e)
rom[-2:]=struct.pack('<H',sum(rom[:-2])&65535);(Q/'private/candidate.ws').write_bytes(rom);(Q/'edits.json').write_text(json.dumps(edits,indent=2));(Q/'getter_translations.json').write_text(json.dumps(trs,ensure_ascii=False,indent=2));(Q/'getter_allocations.json').write_text(json.dumps(g,ensure_ascii=False,indent=2));(R/'src/corrections.json').write_text(json.dumps(c,indent=2)+'\n')
m=json.loads((R/'manifest.json').read_text());m['target']={'bytes':len(rom),'sha256':hashlib.sha256(rom).hexdigest(),'crc32':f'{zlib.crc32(rom)&0xffffffff:08X}','ws_checksum':f'{struct.unpack("<H",rom[-2:])[0]:04X}'};m['qa21_getter_corrected_references']=2;m['changed_bytes_vs_hf15']=sum(a!=b for a,b in zip(base,rom));m['rom_changes_in_QA21']=m['changed_bytes_vs_hf15'];(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
p=R/'build.py';p.write_text(p.read_text().replace('HF16 QA21 V3 64 bilingual and presentation repairs','HF16 QA21 V3 64 story repairs and two equipment property wording repairs'))
from build import build
jp=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes();out,bps,res=build(jp);assert out==rom;m['bps_sha256']=hashlib.sha256(bps).hexdigest();m['changed_bytes_vs_english']=res['changed_bytes_vs_legacy'];m['changed_bytes_vs_japanese']=sum(a!=b for a,b in zip(jp,rom));(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');name='Chocobo_EN_v1.1_HF16_TEST_JP_CCAA4853.bps';(R/'patches'/name).write_bytes(bps);Path('delivery',name).write_bytes(bps)
for f in ['edits.json','getter_translations.json','getter_allocations.json']:(R/'qa21'/f).write_bytes((Q/f).read_bytes())
print(m['target'],m['changed_bytes_vs_hf15'],m['bps_sha256'])
