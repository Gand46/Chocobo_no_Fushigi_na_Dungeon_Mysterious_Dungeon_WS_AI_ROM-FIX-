from pathlib import Path
s=Path('qa21/prepare_candidate.py').read_text();start=s.index('base=Path(');end=s.index(';out=bytearray(base)',start)
s=s[:start]+'''import argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import replace_checked
from qa15.inventory_layout import getter_inventory
p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
jp=args.japanese_rom.read_bytes();m=json.loads((ROOT/'manifest.json').read_text());assert hashlib.sha256(jp).hexdigest()==m['original']['sha256']
prior=bytearray(jp);replace_checked(prior,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits']);current=json.loads((ROOT/'docs/history/qa20/corrections.json').read_text())['edits'];replace_checked(prior,current);prior[-2:]=struct.pack('<H',sum(prior[:-2])&65535);base=bytes(prior);assert hashlib.sha256(base).hexdigest()==m['previous_hf15']['sha256']''' +s[end:]
s=s.replace("sys.path.insert(0,'work/Chocobo_QA20_V2');from qa15.inventory_layout import story_inventory,words_until_end","sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from qa15.inventory_layout import story_inventory,words_until_end").replace("json.loads(Path('work/Chocobo_QA20_V2/src/corrections.json').read_text())['edits']","current")
s=s.replace("out[-2:]=",'''grows={x['id']:x for x in getter_inventory(base,'HF15')[0]}
for ident,d in json.loads((ROOT/'qa21/getter_translations.json').read_text()).items():
 row=grows[ident];offset=int(row['pointer'],16);words,_,_=words_until_end(base,offset);ew=list(encode(d['text']));assert len(ew)<=len(words);raw=struct.pack('<'+'H'*len(words),*(ew+[0]*(len(words)-len(ew))));edits.append({'id':ident+'_getter_payload','offset':hex(offset),'before':base[offset:offset+len(raw)].hex(),'after':raw.hex(),'reason':d['reason']});out[offset:offset+len(raw)]=raw
out[-2:]=''' )
s=s.replace("Path('qa21/translations.json')","(ROOT/'qa21/translations.json')")
for f in ['edits.json','allocations.json','changed_ids.json']:s=s.replace("Path('qa21/"+f+"')","(args.out/'"+f+"')")
s=s.replace("Path('qa21/private/candidate.ws')","(args.out/'candidate.ws')")
Path('qa21/rebuild_translation_edits.py').write_text(s)
