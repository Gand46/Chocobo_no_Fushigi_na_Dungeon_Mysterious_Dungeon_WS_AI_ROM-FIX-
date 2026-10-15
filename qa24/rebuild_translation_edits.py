"""Rebuild QA24 repairs semantically from checked HF18 sources and clean JP."""
from pathlib import Path
import argparse,json,struct,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import replace_checked
from qa15.inventory_layout import story_inventory
from qa21.text_codec import encode
def reconstruct(jp):
 m=json.loads((ROOT/'docs/history/qa23/manifest_hf18.json').read_text())
 assert hashlib.sha256(jp).hexdigest()==m['original']['sha256']
 r=bytearray(jp)
 replace_checked(r,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits'])
 replace_checked(r,json.loads((ROOT/'docs/history/qa23/corrections_hf18.json').read_text())['edits'])
 r[-2:]=struct.pack('<H',sum(r[:-2])&65535)
 assert hashlib.sha256(r).hexdigest()==m['target']['sha256']
 return bytes(r)
def repair(base):
 out=bytearray(base);edits=[]
 rows,groups=story_inventory(base,'HF18');rows={x['id']:x for x in rows};groups={x['group']:x for x in groups}
 def add(id,off,after,reason):
  old=base[off:off+len(after)];assert len(old)==len(after)
  edits.append(dict(id=id,offset=hex(off),before=old.hex(),after=after.hex(),reason=reason));out[off:off+len(after)]=after
 shared={}
 for id,d in json.loads((ROOT/'qa24/story_repairs.json').read_text()).items():
  row=rows[id];start=int(row['pointer'],16);end=int(row['end'],16)
  if d['mode']=='control_argument':
   off=int(d['offset'],16);assert start<=off<end and base[off:off+2].hex()==d['before']
   add(id+'_argument',off,bytes.fromhex(d['after']),d['reason']);continue
  words=d.get('prefix',[]).copy()
  for i,line in enumerate(d['lines']):
   if i:words.append(0xfffe)
   enc=encode(line);assert enc is not None and len(enc)<=13,(id,line)
   words.extend(enc)
  words+=d['suffix'];raw=struct.pack('<'+'H'*len(words),*words)
  if d.get('allocate'):
   off=int(d['allocate'],16)
   if off not in shared:
    assert base[off:off+len(raw)]==b'\xff'*len(raw)
    add(id+'_shared_payload',off,raw,d['reason']);shared[off]=raw
   else:assert shared[off]==raw
   ptr=int(groups[row['group']]['table'],16)+row['message']*2
   assert struct.unpack_from('<H',base,ptr)[0]==start&65535
   add(id+'_pointer',ptr,struct.pack('<H',off&65535),d['reason'])
  else:
   assert len(raw)<=end-start,(id,len(raw),end-start)
   add(id+'_payload',start,raw+bytes(end-start-len(raw)),d['reason'])
 if (ROOT/'qa24/getter_edits.json').exists():
  gs=json.loads((ROOT/'qa24/getter_edits.json').read_text())
  if isinstance(gs,dict):gs=gs['edits']
  for e in gs:
   off=int(e['offset'],16);assert base[off:off+len(bytes.fromhex(e['before']))].hex()==e['before']
   add(e['id'],off,bytes.fromhex(e['after']),e['reason'])
 check=bytearray(base);replace_checked(check,edits);assert check==out
 out[-2:]=struct.pack('<H',sum(out[:-2])&65535)
 return bytes(out),edits
def main():
 p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 base=reconstruct(a.japanese_rom.read_bytes());rom,edits=repair(base);a.out.mkdir(parents=True,exist_ok=True)
 (a.out/'candidate.ws').write_bytes(rom);(a.out/'edits.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'edits':len(edits),'changed_vs_hf18':sum(a!=b for a,b in zip(base,rom))}))
if __name__=='__main__':main()
