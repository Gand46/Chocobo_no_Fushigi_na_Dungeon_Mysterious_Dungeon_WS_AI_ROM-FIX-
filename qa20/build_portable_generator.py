from pathlib import Path
s=Path('qa20/prepare_candidate.py').read_text();start=s.index("base=Path(");end=s.index(';out=bytearray(base)',start)
s=s[:start]+'''import argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import replace_checked
p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
jp=args.japanese_rom.read_bytes();m=json.loads((ROOT/'manifest.json').read_text());assert hashlib.sha256(jp).hexdigest()==m['original']['sha256']
prior=bytearray(jp);replace_checked(prior,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits']);current=json.loads((ROOT/'src/corrections.json').read_text())['edits'];last=json.loads((ROOT/'qa20/edits.json').read_text());assert current[-len(last):]==last
replace_checked(prior,current[:-len(last)]);prior[-2:]=struct.pack('<H',sum(prior[:-2])&65535);base=bytes(prior);assert hashlib.sha256(base).hexdigest()==m['previous_hf14']['sha256']''' +s[end:]
s=s.replace("sys.path.insert(0,'work/Chocobo_QA20_V2');from qa15.inventory_layout import story_inventory,words_until_end","sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from qa15.inventory_layout import story_inventory,words_until_end")
for f in ['translations.json'] :s=s.replace("Path('qa20/"+f+"')","(ROOT/'qa20/"+f+"')")
for f in ['edits.json','allocations.json','changed_ids.json']:s=s.replace("Path('qa20/"+f+"')","(args.out/'"+f+"')")
s=s.replace("Path('qa20/private/candidate.ws')","(args.out/'candidate.ws')")
Path('qa20/rebuild_translation_edits.py').write_text(s)
