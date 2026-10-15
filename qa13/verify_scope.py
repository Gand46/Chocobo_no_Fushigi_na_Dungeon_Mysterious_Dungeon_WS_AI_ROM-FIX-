#!/usr/bin/env python3
"""Verify recorded QA13 observations; no emulator exit is treated as proof by itself."""
from pathlib import Path
import argparse, csv, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa7'))
from chocobo_save import inspect
p=argparse.ArgumentParser();p.add_argument('--runs',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
R=a.runs; checks=[]
H='c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284'
J='38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728'
E='84983bea3e2452d0be35173d0f8cd3fa45568ea6e2fbacb25373bccb7a3d312b'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,condition,evidence):
 if not condition:raise AssertionError(name)
 checks.append(dict(check=name,status='PASS',evidence=evidence))
def data(n,f='sram.bin'):return (R/n/f).read_bytes()
def u16(b,a):return int.from_bytes(b[a:a+2],'little')
def rows(n,f):return list(csv.DictReader((R/n/f).open()))
def stored(b):return b[0x75ac:0x75b4]+b[0x75b6:0x7f90]
def complete(n,h=H):
 d=R/n;m=json.loads((d/'run.json').read_text());check(n+': completed final/known ROM',m['completed'] and m['exit']==0 and m['rom_sha256']==h and not m.get('timed_out',False),m['rom_sha256'])
 if 'plan_sha256'in m:check(n+': captured plan hash',sha(d/'plan.lua')==m['plan_sha256'],m['plan_sha256'])
 else:check(n+': observer/cases hashes',sha(d/'observer.lua')==m['script_sha256'] and sha(d/'cases.lua')==m['cases_sha256'],m['script_sha256'])
for n,h in [('q13_equipment_sorted',H),('q13_equipment_en_control',E),('q13_equipment_jp_control',J)]:
 complete(n,h);rs=rows(n,'results.csv')
 check(n+': six correct targets returned to field',len(rs)==6 and all(x['menu_state']=='0011' and x['poweroff']=='false' for x in rs),rows(n,'events.csv'))
 check(n+': bounded stores and persistent writes',not rows(n,'buffer_guard.csv') and not rows(n,'persistent_writes.csv'),'Four watched stores; 175AC..17F8F')
 observed=rows(n,'text_reads.csv');expected={'slot00_65_flags10':(6,{57,55}),'slot08_65_flags10':(6,{57,55}),'slot17_9D_flags10':(7,{39,38}),'slot00_9D_flags11':(7,{39,38}),'slot17_65_flags11':(6,{57,55})}
 for name,(fam,ids) in expected.items():
  check(n+': native property getters '+name,ids.issubset({int(x['index']) for x in observed if x['case']==name and int(x['family'])==fam}),'Correct property pair reached after native bag sort')
 for x in rs:
  b=data(n,x['case']+'_sram.bin');check(n+': full bag '+x['case'],b[0x6c9e]==18 and sum(b[0x6c9f+i*5]!=0 for i in range(18))==18,'18 occupied native 5-byte inventory records')
for n,h in [('q13_atla_stress',H),('q13_atla_jp_control',J)]:
 complete(n,h);s=(R/n/'opcodes.csv').read_text();b=data(n)
 check(n+': rescue milestones',all(('E0:'+x)in s for x in ['9A1C','9D07','9E44']) and b[0x730c]&1==1,'Native event trace and rescue flag 18')
for n in ['q13_atla_boss','q13_atla_ending','q13_atla_walk']:complete(n)
b=data('q13_atla_ending');c=data('q13_atla_walk')
check('Atla stress chain: village and movement',b[0x7301]==0 and c[0x7301]==0 and b[0x4ac7:0x4ac9]!=c[0x4ac7:0x4ac9],{'ending_xy':list(b[0x4ac7:0x4ac9]),'after_walk_xy':list(c[0x4ac7:0x4ac9]),'boss_assisted':True})
for n,f,event in [('q13_cold99',99,0xa216),('q13_elevator_caller30',30,0),('q13_elevator_caller32',32,0),('q13_elevator_caller99',99,0xa216),('q13_elevator_cold31',31,0),('q13_elevator_cold33',33,0x10)]:
 complete(n);b=data(n);check(n+': floor/event',b[0x7301]==3 and u16(b,0x7303)==f and u16(b,0x7335)==event,{'floor':f,'event':f'{event:04X}'})
complete('q13_telep99');b=data('q13_telep99');check('Telep: town reached',b[0x7301]==0 and u16(b,0x7303)==1,'Native Use with injected TelepCard')
for n,h in [('q13_elevator_jp30',J),('q13_elevator_jp_cache_consumer',J),('q13_elevator_walk30',H),('q13_elevator_jp_walk30',J)]:complete(n,h)
b=data('q13_elevator_jp30');c=data('q13_elevator_jp_cache_consumer')
check('JP causal counterfactual: cache refresh corrects map',u16(b,0x7303)==u16(c,0x7303)==30 and u16(b,0x7335)==0xa216 and u16(c,0x7335)==0,'Same JP ROM and post-Telep state; extra intervention refreshes only five cached digits at native consumers')
rs=rows('q13_elevator_jp_cache_consumer','cache_interventions.csv')
check('Cache mismatch observed at event consumer',len(rs)>0 and rs[0]['floor']=='29' and rs[0]['prior_digits']=='8 9 0 0 0',rs[0])
for n in ['q13_elevator_walk30','q13_elevator_jp_walk30']:
 rs=rows(n,'steps.csv');check(n+': bounded movement without stored-data writes',len({(x['x'],x['y']) for x in rs})>1 and not rows(n,'persistent_writes.csv') and stored(data(n))==stored(data('q13_telep99')),{'distinct_positions':len({(x['x'],x['y']) for x in rs}),'frames':1800})
loadcopies=0
for save,cold,floor in [('q13_equipment_native_save','q13_equipment_cold',2),('q13_elevator_native_save30','q13_elevator_cold31',31),('q13_elevator_native_save32','q13_elevator_cold33',33)]:
 complete(save);complete(cold)
 saved=data(save,'native_save_after.sav');before=data(save,'before_copy.sav');after=data(save,'after_copy.sav')
 check(save+': 2516 exact native payload writes',int((R/save/'payload_write_count.txt').read_text())==2516 and before[0x6bd8:0x75ac]==after[0x75b6:0x7f8a]==saved[0x75b6:0x7f8a],'9000:0373 live snapshot vs native copy and disk save')
 check(save+': protected commit valid',inspect(saved)['protected_valid'],inspect(saved))
 inp=data(cold,'input_save.sav');final=data(cold);copies=list((R/cold).glob('load_*_copied.sav'))
 check(cold+': source is the newly saved data',saved==inp,'Fresh emulator process; no savestate')
 check(cold+': two exact native load copies',len(copies)==2 and all(q.read_bytes()[0x6bd8:0x75ac]==inp[0x75b6:0x7f8a] for q in copies),'All 2516 bytes per native copy')
 loadcopies+=len(copies)
 check(cold+': data survives restart',stored(final)==stored(inp) and inspect(final)['protected_valid'] and u16(final,0x7303)==floor,{'floor':floor,'bytes_per_copy':2516})
b=data('q13_equipment_cold');check('Full fused bag survives disk restart',sum(b[0x6c9f+i*5]!=0 for i in range(18))==18 and b[0x6c9f:0x71d1]==data('q13_equipment_native_save','before_copy.sav')[0x6c9f:0x71d1],'Inventory and complete 117x10 synthesis table byte-identical')
n='q13_jp_restart_after_wrong_map';complete(n,J);inp=data(n,'input_save.sav');b=data(n);copies=list((R/n).glob('load_*_copied.sav'))
check('JP wrong-map restart: no stored-data erasure',stored(b)==stored(inp) and len(copies)==2 and all(q.read_bytes()[0x6bd8:0x75ac]==inp[0x75b6:0x7f8a] for q in copies) and u16(b,0x7303)==99,'Original coherent legacy save resumes after bounded wrong-map traversal')
result={'status':'PASS_SYNTHETIC','checks':checks,'check_count':len(checks),'new_protected_save_cycles':3,'protected_native_load_copies':loadcopies,'bytes_per_copy':2516,'rom_changes_in_qa13':0,'historical_equipment_cause':'NOT_REPRODUCED','historical_atla_variant':'EXACT_TRIGGER_UNKNOWN','natural_save_reset_cause':'NOT_REPRODUCED','wrong_map_cause':'STALE_FLOOR_DIGITS_REPRODUCED_SYNTHETICALLY_IN_JP_AND_CORRECTED_BY_EXISTING_HF6_GUARD','natural_access_required_for_this_acceptance':False,'global_approval':False}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
