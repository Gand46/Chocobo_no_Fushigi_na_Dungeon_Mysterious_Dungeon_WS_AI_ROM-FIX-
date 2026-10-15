from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,'delivery/Chocobo_EN_v1.1_HF12_TEST_Fuentes_QA17_M3_20261014/qa15')
from inventory_layout import story_inventory,story_shape
old=Path('qa17/private/hf12_final/Chocobo_EN_v1.1_HF12_TEST.ws').read_bytes();r=bytearray(old);rows,_=story_inventory(old,'HF12');rows={x['id']:x for x in rows};edits=[]
def fix(id,fn,reason):
 row=rows[id];a=int(row['pointer'],16);b=int(row['end'],16);w=list(struct.unpack('<'+'H'*((b-a)//2),old[a:b]));v=fn(w);new=struct.pack('<'+'H'*len(v),*v)
 assert len(new)<=b-a,(id,len(new),b-a)
 # Compare every literal and inline control argument, omitting zero padding only.
 def glyphs(w):
  out=[];i=0
  while i<len(w):
   z=w[i];i+=1
   if z in [0xfff4,0xfff8,0xfffa,0xfffb]:out += [z,w[i]];i+=1
   elif 0<z<0xfff0:out.append(z)
  return out
 assert glyphs(w)==glyphs(v) or id=='G16:M064',id
 before=old[a:a+len(new)];r[a:a+len(new)]=new
 edits.append(dict(id=id,offset=f'0x{a:06X}',before=before.hex(),after=new.hex(),reason=reason,old_words=len(w),new_words=len(v),lines=story_shape(v[:-1])[0]))
fix('G16:M064',lambda w:w[:7]+[0xfff2,0xfffd]+w[13:18]+[0xfff2,0xfffd]+w[19:24]+w[1:4]+w[27:31]+[0xfff2,0xffff],'Three input-paced pages in native one-line exchange script E0:59B5. Preserve rate 1 Slot Point / 100 Gil. Repair inherited fo lot glyph sequence to Slot using the same resource\'s verified S, lo, t-space glyphs; question reads Exchange Slot Points?.')
fix('G00:M015',lambda w:w[:7]+[0xfff2,0xfffd]+w[8:24]+w[25:],'Pause after apology, then show the complete two-line sentence. Remove one trailing padding cell to stay within slot.')
fix('G06:M012',lambda w:w[:17]+[0]+w[17:24]+[0xfffd]+w[25:44]+[0xfff2,0xfffd]+w[45:55]+[0xfff2,0xffff],'Clear after existing timed wait; add input pause/clear before third line of long paragraph. Separate Camilla\'s and Dad; preserve colored name, palette arguments and all nonblank glyphs.')
fix('G06:M073',lambda w:w[:21]+[0]+w[22:24]+[0xfffd]+w[25:],'Join isolated to with preceding line, adding a word separator (13 cells total); clear after existing wait so final sentence uses its own page. All original glyphs retained; inherited translation semantics not approved.')
fix('G09:M191',lambda w:w[:6]+[w[7],w[6],0xfffd]+w[9:],'Complete three-dot ellipsis before timed wait, then clear before two-line To put it / more bluntly... sentence. Preserve glyph sequence and FFF5 pauses.')
r[-2:]=struct.pack('<H',sum(r[:-2])&65535)
Path('qa18/private/candidate2.ws').write_bytes(r);Path('qa18/edits.json').write_text(json.dumps(edits,indent=2)+'\n')
print(hashlib.sha256(r).hexdigest());print([(x['id'],x['new_words'],x['lines'])for x in edits])
