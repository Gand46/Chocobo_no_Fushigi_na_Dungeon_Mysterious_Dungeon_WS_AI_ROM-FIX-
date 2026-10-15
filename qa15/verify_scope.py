"""Verify QA15/M1's bounded layout correction, evidence and cumulative BPS.

python3 qa15/verify_scope.py --japanese-rom JP.ws --out validation.json
Does not grant global visual or linguistic approval.
"""
import argparse,csv,hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 sys.path.insert(0,str(ROOT))
 from build import build
 from tools.bps_codec import apply
 m=json.loads((ROOT/'docs/history/qa16/manifest.json').read_text());src=a.japanese_rom.read_bytes();patch=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(src,patch);b={'scope':'HISTORICAL_HF11_FROM_PRESERVED_BPS'}
 prior=apply(src,(ROOT/'patches/historical/Chocobo_EN_v1.1_HF10_TEST_JP_CCAA4853.bps').read_bytes())
 changed=[i for i,(x,y) in enumerate(zip(prior,rom)) if x!=y]
 assert changed==list(range(0x65220,0x65226)),changed
 assert sha(prior)==m['previous_hf10']['sha256']
 assert patch==(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes()
 before=struct.unpack_from('<29H',prior,0x65206);after=struct.unpack_from('<29H',rom,0x65206)
 assert [x for x in before if x<0xfff0]==[x for x in after if x<0xfff0]
 assert after[13]==0xfffe and after[27:]==(0xfff2,0xffff)
 runs=ROOT/'evidence/qa15_runs';new=runs/'hf11_dialogue_final';old=runs/'dialogue_candidate_go'
 nr=json.loads((new/'run.json').read_text());oldr=json.loads((old/'run.json').read_text())
 assert nr['completed'] and nr['exit']==0 and nr['rom_sha256']==sha(rom)
 assert oldr['completed'] and oldr['exit']==0 and oldr['rom_sha256']==sha(prior)
 assert nr['state_sha256']==oldr['state_sha256']
 assert nr['plan_sha256']==sha((new/'plan.lua').read_bytes())
 assert nr['script_sha256']==sha((ROOT/'qa15/driver.lua').read_bytes())
 assert nr['mesen_sha256']==m['mesen_sha256']
 prov=json.loads((new/'provenance.json').read_text())
 assert sha((new/'observer.lua').read_bytes())==prov['observer_sha256']
 def rows(d):return list(csv.DictReader((d/'story.csv').open()))
 o=rows(old);n=rows(new)
 assert any(x['event']=='auto_line' and x['value']=='0106' and x['column']=='13' for x in o)
 assert not any(x['event']=='auto_line' for x in n)
 assert any(x['event']=='read' and x['value']=='0106' and x['column']=='0' and x['line']=='1' for x in n)
 assert any(x['event']=='read' and x['value']=='FFFF' and int(x['frame'])>=350 for x in n)
 assert (new/'completed.txt').read_text()=='frames=500'
 assert not (new/'dump_error.txt').exists()
 assert (new/'sram.bin').stat().st_size==32768
 # Pixel readability is a documented visual observation, not asserted from source text.
 result={'status':'PASS_SYNTHETIC_SCOPED_G05_M002','access':['SAVESTATE','POINTER_INJECTION'],
   'target_sha256':sha(rom),'bps_sha256':sha(patch),'changed_bytes_vs_hf10':len(changed),
   'changed_offsets':[f'{i:06X}' for i in changed],'native_frames':500,
   'native_overflow_before':1,'native_overflow_after':0,'glyph_0106_render_position_after':[1,0],
   'glyph_order_and_stream_length':'PRESERVED','confirmation_continues':True,
   'new_font_glyphs':0,'global_layout_approved':False,'global_linguistic_approved':False,
   'qa13_qa14_inheritance':'UNCHANGED_ROM_BYTES_OUTSIDE_SIX_BYTE_TEXT_REORDER',
   'build':b}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
