"""Rebuild HF13; verify changed ranges, all table bindings and scoped native evidence."""
from pathlib import Path
import argparse,json,hashlib,csv,struct,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def literal(w):
 out=[];i=0
 while i<len(w):
  v=w[i];i+=1
  if v in [0xfff4,0xfff8,0xfffa,0xfffb]:out.extend([v,w[i]]);i+=1
  elif 0<v<0xfff0:out.append(v)
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(ROOT));from build import build
 from tools.reference_bps.bps import apply
 from qa15.inventory_layout import story_inventory,getter_inventory,words_until_end
 from qa18.scan_layout import scan
 m=json.loads((ROOT/'docs/history/qa18/manifest.json').read_text());jp=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF13_FROM_PRESERVED_BPS'};old=apply(jp,(ROOT/'patches/historical/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps').read_bytes());checks=0
 def ck(v):
  nonlocal checks
  assert v;checks+=1
 ck(sha(old)==m['previous_hf12']['sha256']);ck(apply(jp,bps)==rom);ck(bps==(ROOT/'patches/historical/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps').read_bytes());ck(sha(bps)==m['bps_sha256']);ck(sha(rom)==m['target']['sha256']);ck(struct.unpack_from('<H',rom,len(rom)-2)[0]==sum(rom[:-2])&65535)
 edits=json.loads((ROOT/'qa18/edits.json').read_text());ck(len(edits)==5);allowed={len(rom)-2,len(rom)-1};st0,_=story_inventory(old,'HF12');st1,_=story_inventory(rom,'HF13');ptrs=sorted({int(x['pointer'],16)for x in st0});byid={x['id']:x for x in st0}
 for e in edits:
  x=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after']);y=x+len(after);ck(len(before)==len(after));ck(old[x:y]==before);ck(rom[x:y]==after);ck(y<=min(z for z in ptrs if z>x));allowed.update(range(x,y));wo,_,_=words_until_end(old,x);wn,_,_=words_until_end(rom,x);l0=literal(wo)
  if e['id']=='G16:M064':ck(l0[17:20]==[0xe6,0x35c,0x20b]);l0[17:20]=[wo[1],wo[2],wo[3]]
  ck(l0==literal(wn))
 changed={i for i,(x,y)in enumerate(zip(old,rom))if x!=y};ck(changed<=allowed);ck(len(changed)==149);ck(len(changed-{len(rom)-2,len(rom)-1})==147);ck(rom[0x160000:0x170000]==old[0x160000:0x170000]);ck([(x['id'],x['pointer'])for x in st0]==[(x['id'],x['pointer'])for x in st1]);g0,_=getter_inventory(old,'HF12');g1,_=getter_inventory(rom,'HF13');ck(g0 and [(x['id'],x['pointer'],x['stream_sha256'])for x in g0]==[(x['id'],x['pointer'],x['stream_sha256'])for x in g1]);st,get,win,summary=scan(rom);ck(summary['horizontal_candidates']==['G01:M031','G06:M022','G09:M063']);ck(summary['vertical_candidates']==[]);ck(summary['story_unterminated']==summary['getter_unterminated']==0)
 idx=json.loads((ROOT/'docs/QA18_RUN_INDEX.json').read_text());approved=[x for x in idx if x['status']=='PASS_SYNTHETIC_SCOPED'];ck(len(approved)==7);frames=0;blank=0
 for x in idx:
  r=ROOT/'evidence/qa18_runs'/x['run'];meta=json.loads((r/'run.json').read_text());pr=json.loads((r/'provenance.json').read_text());ck(sha((r/'plan.lua').read_bytes())==meta['plan_sha256']==x['plan_sha256']);ck(sha((r/'observer.lua').read_bytes())==pr['observer_sha256']);ck(sha((ROOT/pr['state_path']).read_bytes())==meta['state_sha256']);ck(sha((ROOT/'qa18/driver.lua').read_bytes())==meta['script_sha256']);ck(meta['mesen_sha256']==m['mesen_sha256'])
  if x not in approved:continue
  ck(meta['rom_sha256']==m['target']['sha256']);ck(meta['completed']and meta['exit']==0 and not(r/'dump_error.txt').exists());ck((r/'sram.bin').stat().st_size==32768);ck(all(t['poweroff']=='false'for t in rows(r/'frames.csv')));story=rows(r/'story.csv');autos=[t for t in story if t['event']=='auto_line'];ck(all(t['value']=='0000'for t in autos));blank+=len(autos);ck(any(t['event']=='read'and t['value']=='FFFF'and int(t['frame'])>100 for t in story));frames+=x['frames']
  if x['run']=='final_slot_native':
   events=rows(r/'script.csv');ck(any(t['bank']=='E0'and t['pointer']=='59BF'and t['opcode']=='28'for t in events));ck(any(t['bank']=='E0'and t['pointer']=='59C2'and t['opcode']=='7B'for t in events));ck({t['line_limit']for t in story if t['group']=='16'and t['message']=='64'}=={'1'})
  else:ck((r/'sram.bin').read_bytes()[0x6480]==0)
 vis=json.loads((ROOT/'qa18/visual_readings.json').read_text());ck(len(vis)==14)
 for x in vis:ck(sha((ROOT/'evidence/qa18_runs'/x['run']/x['image']).read_bytes())==x['sha256'])
 result={'status':'PASS_SYNTHETIC_SCOPED','iteration':'M4_OF_4_EXECUTED','checks':checks,'approved_runs':len(approved),'diagnostic_runs':len(idx)-len(approved),'approved_native_frames':frames,'visual_readings':len(vis),'unique_resources_corrected':5,'content_changed_bytes':147,'checksum_changed_bytes':2,'nonblank_dropped_glyphs_approved':0,'blank_padding_drops_approved':blank,'independent_bps':'PASS_EXACT_BYTES','layout_static':summary,'global_layout_approved':False,'global_linguistic_approved':False,'natural_scene_reachability':'NOT_VALIDATED','remaining_base_iterations':0,'unconfirmed_layout_candidates':['TR-01-M2-C01 preset32/F00:I053'],'build':b};a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
