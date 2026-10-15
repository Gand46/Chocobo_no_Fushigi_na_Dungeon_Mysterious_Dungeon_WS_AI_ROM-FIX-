"""Rebuild 65 G14 skill/element label repairs from the pinned HF17 and clean JP."""
from pathlib import Path
import argparse,hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import replace_checked
from qa15.inventory_layout import story_inventory,words_until_end
from qa21.text_codec import encode
p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
jp=a.japanese_rom.read_bytes();m=json.loads((ROOT/'docs/history/qa22/manifest_hf17.json').read_text());sha=lambda r:hashlib.sha256(r).hexdigest()
assert sha(jp)==m['original']['sha256']
old=bytearray(jp);replace_checked(old,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits']);prior=json.loads((ROOT/'docs/history/qa22/corrections_hf17.json').read_text())['edits'];replace_checked(old,prior);old[-2:]=struct.pack('<H',sum(old[:-2])&65535);assert sha(old)==m['target']['sha256'];base=bytes(old)
rows,groups=story_inventory(base,'HF17');rows={x['id']:x for x in rows};groups={x['group']:x for x in groups};out=bytearray(base)
T=json.loads((ROOT/'qa23/translations.json').read_text());assert len(T)==65
cursor=0x6fca0;assert cursor==max(int(e['offset'],16)+len(bytes.fromhex(e['after'])) for e in prior if 0x6f000<=int(e['offset'],16)<0x70000)
assert base[cursor:0x70000]==jp[cursor:0x70000]==b'\xff'*(0x70000-cursor)
edits=[];alloc=[]
for id,d in T.items():
 row=rows[id];assert row['bank']==6 and row['unique_pointer'] and row['terminated'],id
 words=encode(d['text']);assert words is not None and len(words)<=13,(id,d['text']);raw=struct.pack('<'+'H'*(len(words)+1),*(list(words)+[0xffff]));old_start=int(row['pointer'],16);old_end=int(row['end'],16);capacity=old_end-old_start
 if len(raw)<=capacity:offset=old_start;payload=raw+bytes(capacity-len(raw));mode='inplace'
 else:
  offset=cursor;cursor+=len(raw);assert cursor<=0x70000,(id,hex(cursor));payload=raw;mode='allocated'
  table=int(groups[row['group']]['table'],16)+row['message']*2
  assert struct.unpack_from('<H',base,table)[0]==old_start&65535
  after=struct.pack('<H',offset&65535);edits.append({'id':id+'_pointer','offset':hex(table),'before':base[table:table+2].hex(),'after':after.hex(),'reason':d['reason']});out[table:table+2]=after
 edits.append({'id':id+'_payload','offset':hex(offset),'before':base[offset:offset+len(payload)].hex(),'after':payload.hex(),'reason':d['reason']});out[offset:offset+len(payload)]=payload
 alloc.append({'id':id,'mode':mode,'pointer':hex(offset),'bytes':len(payload),'old_pointer':row['pointer'],'text':d['text'],'words':list(words),'reason':d['reason']})
# V4 name reconciliation: the same ドル君 in G08/G11 is already Chip in English.
# Both colored name payloads use three native cells, so preserve all page and
# color controls and replace only those six bytes within each G09 resource.
name_fixes=json.loads((ROOT/'qa23/name_reconciliation.json').read_text())
assert set(name_fixes)=={'G09:M086','G09:M089'}
old_name=struct.pack('<HHH',*encode('Doru'));new_name=struct.pack('<HHH',*encode('Chip'))
assert len(old_name)==len(new_name)==6
for id,d in name_fixes.items():
 row=rows[id];start=int(row['pointer'],16);end=int(row['end'],16)
 assert base[start:end].count(old_name)==1 and base[start:end].count(new_name)==0,id
 offset=base.index(old_name,start,end)
 edits.append({'id':id+'_name_inplace','offset':hex(offset),'before':old_name.hex(),'after':new_name.hex(),'reason':d['reason']})
 out[offset:offset+6]=new_name
out[-2:]=struct.pack('<H',sum(out[:-2])&65535)
(a.out/'candidate.ws').write_bytes(out);(a.out/'edits.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n');(a.out/'allocations.json').write_text(json.dumps(alloc,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'refs':len(T),'allocated':sum(x['mode']=='allocated'for x in alloc),'inplace':sum(x['mode']=='inplace'for x in alloc),'end':hex(cursor),'hf18_sha256':sha(out),'changed_vs_hf17':sum(x!=y for x,y in zip(base,out))}))
