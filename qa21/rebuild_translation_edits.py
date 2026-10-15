from pathlib import Path
import sys,json,struct,hashlib,re
sys.path.insert(0,str(Path(__file__).parent));from text_codec import encode
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from qa15.inventory_layout import story_inventory,words_until_end
import argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import replace_checked
from qa15.inventory_layout import getter_inventory
p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
jp=args.japanese_rom.read_bytes();m=json.loads((ROOT/'manifest.json').read_text());assert hashlib.sha256(jp).hexdigest()==m['original']['sha256']
prior=bytearray(jp);replace_checked(prior,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits']);current=json.loads((ROOT/'docs/history/qa20/corrections.json').read_text())['edits'];replace_checked(prior,current);prior[-2:]=struct.pack('<H',sum(prior[:-2])&65535);base=bytes(prior);assert hashlib.sha256(base).hexdigest()==m['previous_hf15']['sha256'];out=bytearray(base);rows,groups=story_inventory(base,'HF15');rows={x['id']:x for x in rows};groups={x['group']:x for x in groups};edits=[];alloc=[];cursor=0x6e588
assert cursor==max(int(e['offset'],16)+len(bytes.fromhex(e['after'])) for e in current if 0x6e000<=int(e['offset'],16)<0x70000)
assert base[cursor:0x70000]==jp[cursor:0x70000]==b'\xff'*(0x70000-cursor)
def enc(s):
 words=[];parts=re.split(r'(\{[^}]+\})',s)
 for part in parts:
  if not part:continue
  if part.startswith('{'):words += [0xfffa,6]+([0xC1,0xE,0x7A,0x198,0x275,0xC2,0x5] if part[1:-1]=="Camilla's Dad" else list(encode(part[1:-1])))+[0xfffa,0]
  else:words+=list(encode(part))
 return words
def width(s):return len(enc(s))-4*s.count('{')
def layout(s):
 lines=[];line=''
 for word in re.findall(r'\{[^}]+\}[^\s]*|[^\s]+',s):
  candidate=(line+' '+word).strip()
  if width(candidate)>13:
   assert line;lines.append(line);line=word
  else:line=candidate
 if line:lines.append(line)
 assert all(width(x)<=13 for x in lines)
 w=[]
 for i,x in enumerate(lines):
  if i:w += [0xfffe] if i%2 else [0xfff2,0xfffd]
  w+=enc(x)
 return w+[0xfff2,0xffff],lines
for id,d in json.loads((ROOT/'qa21/translations.json').read_text()).items():
 row=rows[id];assert row['bank']==6;w,ls=layout(d['text']);raw=struct.pack('<'+'H'*len(w),*w);a=cursor;cursor+=len(raw);assert cursor<0x70000
 ptr=int(groups[row['group']]['table'],16)+2*row['message'];assert struct.unpack_from('<H',base,ptr)[0]==int(row['pointer'],16)&65535
 for ident,x,data in [(id+'_payload',a,raw),(id+'_pointer',ptr,struct.pack('<H',a&65535))]:
  edits.append({'id':ident,'offset':hex(x),'before':base[x:x+len(data)].hex(),'after':data.hex(),'reason':d['reason']});out[x:x+len(data)]=data
 alloc.append({'id':id,'pointer':hex(a),'bytes':len(raw),'lines':ls,'words':w,'reason':d['reason']})
grows={x['id']:x for x in getter_inventory(base,'HF15')[0]}
for ident,d in json.loads((ROOT/'qa21/getter_translations.json').read_text()).items():
 row=grows[ident];offset=int(row['pointer'],16);words,_,_=words_until_end(base,offset);ew=list(encode(d['text']));assert len(ew)<=len(words);raw=struct.pack('<'+'H'*len(words),*(ew+[0]*(len(words)-len(ew))));edits.append({'id':ident+'_getter_payload','offset':hex(offset),'before':base[offset:offset+len(raw)].hex(),'after':raw.hex(),'reason':d['reason']});out[offset:offset+len(raw)]=raw
out[-2:]=struct.pack('<H',sum(out[:-2])&65535);(args.out/'candidate.ws').write_bytes(out);(args.out/'edits.json').write_text(json.dumps(edits,indent=2));(args.out/'allocations.json').write_text(json.dumps(alloc,indent=2));(args.out/'changed_ids.json').write_text(json.dumps([x['id']for x in alloc]));print('references',len(alloc),'used',hex(cursor),'sha',hashlib.sha256(out).hexdigest())
