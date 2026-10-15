"""Rebuild the 43 G09 text repairs from cumulative editable sources and clean JP ROM."""
from pathlib import Path
import argparse,hashlib,json,re,struct,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from qa21.text_codec import encode
from qa15.inventory_layout import story_inventory
from build import replace_checked
p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
jp=a.japanese_rom.read_bytes();m=json.loads((ROOT/'docs/history/qa21/manifest_hf16.json').read_text());sha=lambda r:hashlib.sha256(r).hexdigest()
assert sha(jp)==m['original']['sha256']
old=bytearray(jp);replace_checked(old,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits']);replace_checked(old,json.loads((ROOT/'docs/history/qa21/corrections_hf16.json').read_text())['edits']);old[-2:]=struct.pack('<H',sum(old[:-2])&65535);assert sha(old)==m['target']['sha256'];base=bytes(old)
rows,groups=story_inventory(base,'HF16');rows={x['id']:x for x in rows};groups={x['group']:x for x in groups};out=bytearray(base)
T=json.loads((ROOT/'qa22/translations.json').read_text());assert len(T)==43
cursor=0x6f708;assert base[cursor:0x70000]==jp[cursor:0x70000]==b'\xff'*(0x70000-cursor)
original_edits=json.loads((ROOT/'docs/history/qa21/corrections_hf16.json').read_text())['edits'];assert cursor==max(int(e['offset'],16)+len(bytes.fromhex(e['after'])) for e in original_edits if 0x6e000<=int(e['offset'],16)<0x70000)
def enc(s):
 words=[]
 for part in re.split(r'(\{[^}]+\})',s):
  if not part:continue
  if part.startswith('{'):
   token=part[1:-1]
   text=[0xC1,0xE,0x7A,0x198,0x275,0xC2,0x5] if token=="Camilla's Dad" else list(encode(token))
   words += [0xfffa,6]+text+[0xfffa,0]
  else:
   code=encode(part);assert code is not None,(s,part);words.extend(code)
 return words
def width(s):return len(enc(s))-4*s.count('{')
def wrap(s):
 lines=[];line=''
 for word in re.findall(r'\{[^}]+\}[^\s]*|[^\s]+',s):
  cand=(line+' '+word).strip()
  if width(cand)>13:
   assert line,(s,word);lines.append(line);line=word
  else:line=cand
 if line:lines.append(line)
 assert all(width(x)<=13 for x in lines),(s,lines)
 return lines
def layout(s,pages=None):
 if pages is None:lines=wrap(s)
 else:
  assert ' '.join(pages)==s
  lines=[]
  for page in pages:
   page_lines=wrap(page)
   assert 1<=len(page_lines)<=2,(s,page,page_lines)
   if lines and len(lines)%2:lines.append('')
   lines.extend(page_lines)
 words=[]
 for i,x in enumerate(lines):
  if i:words += [0xfffe] if i%2 else [0xfff2,0xfffd]
  if x:words+=enc(x)
 return words+[0xfff2,0xffff],lines
edits=[];alloc=[]
for id,d in T.items():
 row=rows[id];assert row['bank']==6 and row['unique_pointer'] and row['terminated'],id
 words,lines=layout(d['text'],d.get('pages'));raw=struct.pack('<'+'H'*len(words),*words);old_start=int(row['pointer'],16);old_end=int(row['end'],16);capacity=old_end-old_start
 if len(raw)<=capacity:
  offset=old_start;payload=raw+bytes(capacity-len(raw));mode='inplace'
 else:
  offset=cursor;cursor+=len(raw);assert cursor<=0x70000,(id,hex(cursor));payload=raw;mode='allocated'
  table=int(groups[row['group']]['table'],16)+row['message']*2
  assert struct.unpack_from('<H',base,table)[0]==old_start&65535
  after=struct.pack('<H',offset&65535)
  edits.append({'id':id+'_pointer','offset':hex(table),'before':base[table:table+2].hex(),'after':after.hex(),'reason':d['reason']})
  out[table:table+2]=after
 edits.append({'id':id+'_payload','offset':hex(offset),'before':base[offset:offset+len(payload)].hex(),'after':payload.hex(),'reason':d['reason']})
 out[offset:offset+len(payload)]=payload
 alloc.append({'id':id,'mode':mode,'pointer':hex(offset),'bytes':len(payload),'old_pointer':row['pointer'],'lines':lines,'words':words,'reason':d['reason']})
out[-2:]=struct.pack('<H',sum(out[:-2])&65535)
(a.out/'candidate.ws').write_bytes(out);(a.out/'edits.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n');(a.out/'allocations.json').write_text(json.dumps(alloc,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'refs':len(T),'allocated':sum(x['mode']=='allocated'for x in alloc),'inplace':sum(x['mode']=='inplace'for x in alloc),'end':hex(cursor),'hf17_sha256':sha(out),'changed_vs_hf16':sum(x!=y for x,y in zip(base,out))}))
