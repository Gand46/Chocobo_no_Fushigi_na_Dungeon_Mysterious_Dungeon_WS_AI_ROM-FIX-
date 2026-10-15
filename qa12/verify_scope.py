"""Verify QA12 byte scope and the concrete native-menu evidence. No general gameplay approval."""
from pathlib import Path
import csv,hashlib,json,struct,argparse
from PIL import Image,ImageChops
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--hf8',type=Path,required=True);parser.add_argument('--hf9',type=Path,required=True)
parser.add_argument('--runs',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
a=parser.parse_args();runs_dir=a.runs
before=a.hf8.read_bytes();after=a.hf9.read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(before)=='831d5778ba5887941235365a4065d8cc090c1a871fbdfc00f398c2b5c0ebc89c'
assert len(before)==len(after)==2097152
ranges=[(0x15caee,0x15cb0a),(0x15cba6,0x15cba8),(0x15cfb0,0x15cfb2),(0x16ea1c,0x16ea2c),(len(after)-2,len(after))]
changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
assert all(any(a<=i<b for a,b in ranges) for i in changed)
assert int.from_bytes(after[-2:],'little')==sum(after[:-2])&65535
runs={}
for name,expected in [('q12_item_check_fixed',163),('q12_property_all_before',49),('q12_property_final_hf9',49),('q12_critical_hf9',9),('q12_legacy_fused',6),('q12_jp_controls',7)]:
 p=runs_dir/name;meta=json.loads((p/'run.json').read_text());assert meta['completed'] and not meta['timed_out'] and meta['exit']==0
 rows=list(csv.DictReader((p/'results.csv').open()));assert len(rows)==expected
 assert all(r['poweroff']=='false' and r['menu_state']=='0004' and r['inventory_qty']=='1' and r['inventory_id']==r['item'] for r in rows)
 guard=sum(1 for _ in csv.DictReader((p/'buffer_guard.csv').open()));writes=sum(1 for _ in csv.DictReader((p/'persistent_writes.csv').open()))
 assert guard==writes==0
 reads=list(csv.DictReader((p/'text_reads.csv').open()))
 fam={f:sorted({int(r['index']) for r in reads if r['family']==str(f)}) for f in [2,3,6,7]}
 if name.startswith('q12_property_'):
  assert fam[6]==list(range(1,58)) and fam[7]==list(range(1,40))
 if name.endswith('_hf9'):assert meta['rom_sha256']==sha(after)
 runs[name]={'cases':expected,'completed':True,'rom_sha256':meta['rom_sha256'],'native_return_and_inventory':'PASS','four_watched_store_overruns':guard,'persistent_write_range_175AC_17F8F':writes,'distinct_family_counts':{str(k):len(v) for k,v in fam.items()}}
# Differential native screenshots: only the three fixed property rows may differ.
expected_cases={'prop_6_19_20','prop_6_25_26','prop_7_01_02'};diffs=[];compared=0
for p in sorted((runs_dir/'q12_property_all_before').glob('*.png')):
 other=runs_dir/'q12_property_final_hf9'/p.name
 assert other.is_file();compared+=1
 box=ImageChops.difference(Image.open(p).convert('RGB'),Image.open(other).convert('RGB')).getbbox()
 if box:
  case=p.stem.rsplit('_f',1)[0];assert case in expected_cases and p.name.endswith('_f720.png'),(p.name,box)
  # Changed property text is inside the native item-description box.
  assert 8<=box[0]<box[2]<=216 and 88<=box[1]<box[3]<=104,(p.name,box)
  diffs.append({'image':p.name,'changed_bbox':box})
assert len(diffs)==3 and compared==147
out={'target_sha256':sha(after),'base_sha256':sha(before),'changed_bytes_vs_hf8':len(changed),'allowed_ranges':[[f'{a:06X}',f'{b:06X}'] for a,b in ranges],'changed_offsets':[f'{i:06X}' for i in changed],'unexpected_changed_offsets':0,'checksum':'PASS','runs':runs,'property_image_comparison':{'compared':compared,'changed':diffs,'unchanged':compared-len(diffs)},'scope':'Synthetic fixtures plus native buttons and renderer. Properties cover all 96 nonzero descriptors in 49 pairs, not all pair combinations or native acquisition. No historical equipment-freeze reproduction; no global layout approval.'}
a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
