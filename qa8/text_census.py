from pathlib import Path
import struct,csv,json,hashlib,argparse
parser=argparse.ArgumentParser(description='Bounded native text-family terminator census; not global layout approval.')
parser.add_argument('japanese_rom',type=Path)
parser.add_argument('translated_rom',type=Path)
parser.add_argument('--out',type=Path,default=Path('census'))
args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
jp=args.japanese_rom.read_bytes();en=args.translated_rom.read_bytes()
assert len(jp)==len(en)==2097152
assert hashlib.sha256(jp).hexdigest()=='38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728'
rows=[]
for family in range(19):
 off,seg=struct.unpack_from('<HH',jp,0x18d930+family*4);bank=0x10+(seg>>12);table=bank*65536+off;first=struct.unpack_from('<H',jp,table)[0];count=(first-off)//2
 assert 0<count<=512
 ptrs={}
 for label,b in [('JP',jp),('HF5',en)]:
  ptrs[label]=[bank*65536+x for x in struct.unpack_from(f'<{count}H',b,table)]
 for idx in range(count):
  row={'family':family,'index':idx,'table':f'{table:06X}','family_entries':count}
  for label,b in [('JP',jp),('HF5',en)]:
   start=ptrs[label][idx];higher=[x for x in ptrs[label] if x>start];end=min(higher) if higher else min(start+512,(bank+1)*65536)
   words=list(struct.unpack_from(f'<{(end-start)//2}H',b,start));stop=words.index(65535)+1 if 65535 in words else None
   row[label+'_start']=f'{start:06X}';row[label+'_slot_bytes']=end-start;row[label+'_terminated']=stop is not None;row[label+'_words_to_end']=stop;row[label+'_first_words']=' '.join(f'{w:04X}' for w in words[:12])
  row['candidate']=bool(row['JP_terminated'] and not row['HF5_terminated']);rows.append(row)
p=args.out/'text_census.csv'
with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
r={'families':19,'entries':len(rows),'cross_slot_candidates':[r for r in rows if r['candidate']],'scope':'Native getter descriptor families only; slot end inferred from next distinct pointer; candidates are not automatic defects or a global layout PASS.'}
r['japanese_sha256']=hashlib.sha256(jp).hexdigest();r['translated_sha256']=hashlib.sha256(en).hexdigest()
(args.out/'text_census.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
