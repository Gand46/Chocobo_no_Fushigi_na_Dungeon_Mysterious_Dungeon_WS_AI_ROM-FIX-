"""Verify recorded QA9 runtime evidence and exact HF6 patch extent (no global approval)."""
from pathlib import Path
import argparse,json,hashlib,struct
p=argparse.ArgumentParser();p.add_argument('hf5',type=Path);p.add_argument('hf6',type=Path);p.add_argument('runs',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
old=a.hf5.read_bytes();new=a.hf6.read_bytes();assert hashlib.sha256(new).hexdigest()=='87ecaab08786651ee9431d6e386b0b73147e759aee282c053f6a75249e820d73'
allowed=set(range(0x14d398,0x14d39b))|set(range(0x14fda8,0x14fdda))|{len(new)-2,len(new)-1};changed={i for i,(x,y) in enumerate(zip(old,new))if x!=y};assert changed<=allowed and len(changed)==53
assert int.from_bytes(new[-2:],'little')==sum(new[:-2])&65535
rows=[]
for n in [11,22,33,44,55,66,77,88,98,100,30,99]:
 name=f'q9_final{n}' if n!=99 else 'q9_scoped99';root=a.runs/name;meta=json.loads((root/'run.json').read_text());assert meta['completed'] and meta['rom_sha256']==hashlib.sha256(new).hexdigest()
 b=(root/'sram.bin').read_bytes();assert struct.unpack_from('<H',b,0x7303)[0]==n
 copies=list(root.glob('load_*_copied.sav'));assert len(copies)==2
 for cp in copies:
  d=cp.read_bytes();assert d[0x6bd8:0x75ac]==d[0x75b6:0x7f8a]
 rows.append({'run':name,'floor':n,'event':f'{struct.unpack_from("<H",b,0x7335)[0]:04X}','native_copies_exact':len(copies)})
for name,event in [('q9_hf5_telep_reentry30',0xa217),('q9_hf6_telep_reentry30',0)]:
 b=(a.runs/name/'sram.bin').read_bytes();assert struct.unpack_from('<H',b,0x7303)[0]==30;assert struct.unpack_from('<H',b,0x7335)[0]==event
for name in ['q9_fountain_min','q9_fountain_full','q9_hf6_fountain_full']:
 s=(a.runs/name/'script_states.csv').read_text();assert 'E0:ABE2' in s
for name in ['q9_hf5_native_cold99','q9_hf6_native_cold99']:
 b=(a.runs/name/'sram.bin').read_bytes();assert struct.unpack_from('<H',b,0x7303)[0]==99 and struct.unpack_from('<H',b,0x7335)[0]==0xa216
result={'scope':'SYNTHETIC_STALE_CACHE_FIX; not full elevator/game approval','changed_bytes':len(changed),'changed_offsets':[f'{i:06X}' for i in sorted(changed)],'floor_matrix':rows,'telep_reentry30_map_before':'A217','telep_reentry30_map_after':'0000','telep_reentry_method':'native Telep99, synthetic SRAM reentry, native cold loader','fountain_variants':'coherent minimum15Geyser+5Frog and full45Geyser+15Frog complete E0:ABE2','native_coherent_save98_load99':'PASS both HF5 and HF6; not evidence of native save corruption'}
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
