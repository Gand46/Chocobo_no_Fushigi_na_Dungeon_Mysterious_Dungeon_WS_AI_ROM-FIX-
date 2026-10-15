"""Bounded static layout scan. Candidate counters never certify runtime legibility."""
from pathlib import Path
import argparse,sys,json,csv,collections
ROOT=Path(__file__).resolve().parents[1]
if not(ROOT/'qa15/inventory_layout.py').exists():ROOT=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014')
sys.path.insert(0,str(ROOT/'qa15'))
from inventory_layout import story_inventory,getter_inventory,window_inventory,words_until_end,csvout

def vertical(w):
 lines=0;nonempty=False;longest=0;i=0
 while i<len(w):
  v=w[i];i+=1
  if v in [0xfff4,0xfff8,0xfffa,0xfffb]:i+=1
  if v in [0xfff4,0xfff8] or 0<v<0xfff0:nonempty=True
  if v==0xfffe:lines+=nonempty;nonempty=False
  if v in [0xfff2,0xfffc,0xfffd]:longest=max(longest,lines+nonempty);lines=0;nonempty=False
 return max(longest,lines+nonempty)
def scan(r):
 st,_=story_inventory(r,'HF13');get,_=getter_inventory(r,'HF13');win=window_inventory(r);issues=[]
 for x in st:
  w,_,_=words_until_end(r,int(x['pointer'],16));x['max_explicit_nonblank_lines_between_waits']=vertical(w)
  if x['max_explicit_nonblank_lines_between_waits']>2:issues.append(x['id'])
 return st,get,win,{'story_references':len(st),'story_unique_pointers':len({x['pointer']for x in st}),'story_nonempty':sum(x['nonempty']for x in st),'story_literal_references':sum(x['max_literal_cells']>0 for x in st),'story_control_only_nonempty':sum(x['nonempty']and x['max_literal_cells']==0 for x in st),'story_dynamic_references':sum(x['dynamic']for x in st),'story_unterminated':sum(not x['terminated']for x in st),'horizontal_candidates':[x['id']for x in st if x['exceeds_13_literal_cells']],'vertical_candidates':issues,'getter_entries':len(get),'getter_nonempty':sum(x['nonempty']for x in get),'getter_unterminated':sum(not x['terminated']for x in get),'window_presets':len(win),'unique_geometries':len({(x['x_tiles'],x['y_parameter'],x['width_tiles'],x['mode'],x['height_tiles'])for x in win}),'status':'STATIC_ONLY_NOT_GLOBAL_VISUAL_APPROVAL'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True);st,get,win,summary=scan(a.rom.read_bytes());csvout(a.out/'HF13_dialogue.csv',st);csvout(a.out/'HF13_getter.csv',get);csvout(a.out/'window_presets.csv',win);(a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
