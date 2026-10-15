"""Verify the bounded scope of HF5 edits and recorded runtime outcomes."""
from pathlib import Path
import argparse,json,hashlib,struct,csv
from PIL import Image,ImageChops
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('hf4_rom',type=Path);p.add_argument('hf5_rom',type=Path);p.add_argument('runs',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
old=a.hf4_rom.read_bytes();new=a.hf5_rom.read_bytes()
assert hashlib.sha256(old).hexdigest()=='1ec449933e812c8e4f5e83b882db17b4c5f1ce3b5ea85527d9a1dd2a0891060d'
assert hashlib.sha256(new).hexdigest()=='312f688f627f0c5ccf430c35c9632033344fc0397aa25c6f0db9d99a3630f9c8'
diff=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y]
assert diff==[0x1422c5,0x1422c6,0x16e6fa,0x16e6fb,0x1ea771,0x1ea772,0x1ffffe]
def selector(b,item):
 k=0
 while k<19 and item>=b[0x14228d+k]:k+=1
 return struct.unpack_from('<H',b,0x14229f+2*k)[0]
changed=[i for i in range(256) if selector(old,i)!=selector(new,i)]
assert changed==[255] and selector(new,255)==0xaf8
assert [i for i in range(65536) if (i<0xfe)!=(i<0x100)]==[254,255]
checks={}
for name,damage,defense in [('q8_lafoss_final',1000,0),('q8_lafoss_defense200',800,200),('q8_lafoss_defense2000',1,2000),('q8_damage_filanes_after',1000,0)]:
 t=(a.runs/name/'damage.txt').read_text();assert f'damage={damage},defense={defense}' in t
 checks[name]={'damage':damage,'defense':defense}
s=a.runs/'q8_lafoss_final';before=(s/'sram_f660.bin').read_bytes();after=(s/'sram_f810.bin').read_bytes()
assert struct.unpack_from('<H',before,0x5a34)[0]==10
assert struct.unpack_from('<H',after,0x5a34)[0]==0
assert (s/'sram.bin').read_bytes()[0x6ca0]!=255
rr={}
for label,n in [('before',5),('after',4)]:
 rows=list(csv.DictReader((a.runs/f'q8_text_missing_{label}'/'resource_reads.csv').open()));assert len(rows)==n;rr[label]=len(rows)
before_img=Image.open(a.runs/'q8_text_missing_before/Family0_Index81_f720.png').convert('RGB')
after_img=Image.open(a.runs/'q8_text_missing_after/Family0_Index81_f720.png').convert('RGB')
assert ImageChops.difference(before_img,after_img).getbbox() is None
copies=[]
for file in sorted((a.runs/'q8_cold_saved').glob('load_*_copied.sav')):
 b=file.read_bytes();assert b[0x6bd8:0x75ac]==b[0x75b6:0x7f8a];assert b[0x6c7d]==3;assert struct.unpack_from('<H',b,0x6c7e)[0]==28;copies.append(file.name)
assert len(copies)==2
for name in ['q8_equipment_slot0_65','q8_equipment_slot17_9d','q8_equipment_slot17_bf','q8_equipment_slot17_c0']:
 assert not (a.runs/name/'buffer_guard.csv').read_bytes();assert not (a.runs/name/'save_writes.csv').read_bytes()
r={'allowed_diff':'PASS','selector_static_inputs':256,'selector_changed_ids':changed,'damage_predicate_static_inputs':65536,'native_damage_traces':checks,'enemy_hp_before_after':[10,0],'text_native_word_reads':rr,'text_pixels_identical':True,'cold_load_exact_payloads':copies,'equipment_valid_cases':4,'scope':'Static selector comparison is not CPU execution; runtime outcomes are synthetic, not universal gameplay approval.'}
a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
