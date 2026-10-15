from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,'delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA16_M2_20261014/qa15')
from inventory_layout import story_inventory,story_shape
src=Path('qa15/private/hf11_final/Chocobo_EN_v1.1_HF11_TEST.ws');old=src.read_bytes();r=bytearray(old);rows,_=story_inventory(old,'HF11');rows={x['id']:x for x in rows};edits=[]
def fix(id,fn,reason):
 row=rows[id];a=int(row['pointer'],16);b=int(row['end'],16);w=list(struct.unpack('<'+'H'*((b-a)//2),old[a:b]));v=fn(w);new=struct.pack('<'+'H'*len(v),*v);before=old[a:a+len(new)];r[a:a+len(new)]=new
 assert max(story_shape(v[:-1])[0])<=13,(id,story_shape(v[:-1])[0])
 edits.append(dict(id=id,offset=f'0x{a:06X}',before=before.hex(),after=new.hex(),reason=reason,old_words=len(w),new_words=len(v),lines=story_shape(v[:-1])[0]))
fix('G01:M039',lambda w:w[:10]+w[11:21]+[0xfff2,0xffff], 'Restore original resource boundary before G01:M040. Remove one ellipsis dot to retain input pause and terminator; next message bytes preserved.')
fix('G03:M012',lambda w:w[:11]+[0xad,0xfff2,0xffff], 'Remove three erroneous ff digraphs. Japanese says thanks to brother; complete with exclamation.')
fix('G04:M031',lambda w:w[:6]+[0xfffe]+w[6:18]+[0xfff2,0xfffd]+w[19:], 'Split before colored name; pause and clear before dungeon sentence. Preserve all glyphs, palette and timed pause.')
fix('G04:M034',lambda w:w[5:15]+[0xfffe]+w[21:29]+[0xae,0xfff2,0xffff], 'Two price confirmations 1000 Gil and 500 Gil, OK? Remove redundant Cost is prefixes and erroneous ff/ae residuals; values and question meaning preserved.')
fix('G04:M048',lambda w:w[:7]+w[7:18]+[0xae,0xfff2,0xffff], 'Preserve What is it? / Another Teleport Box? Remove ff digraphs and Japanese ae residue.')
fix('G06:M099',lambda w:w[:24]+w[25:28]+[0xfffe]+w[28:], 'Move explicit break after items; preserve every glyph, palette and existing wait.')
fix('G08:M020',lambda w:w[:16]+[0xfffe]+w[16:22]+[0xfffc,0xfffd]+w[25:], 'Break before had babies; remove trailing padding; clear after existing wait before triplets sentence. Palette and content preserved.')
fix('G16:M004',lambda w:w[:9]+[0xfff2,0xfffd]+w[10:18]+[0xfffe]+w[18:25]+[0xfff2,0xffff], 'Warning on first input page; full sentence on second two-line page. Remove trailing padding only.')
fix('G16:M070',lambda w:w[:23]+[0xfffd]+w[24:43]+[0xfff2,0xfffd]+w[43:], 'Clear after first input page; pause before Shiren the Wanderer to prevent third-line scroll and dropped glyph. Extend into verified unused same-resource tail.')
fix('G00:M253',lambda w:[0x00c1,0x020a,0x0278]+w[3:], 'Cost label ends with a space, separating its numeric substitution. Equivalent price meaning and identical control structure.')
fix('G16:M034',lambda w:w[:2]+[0xfffe]+w[2:5]+[0]+w[10:], 'Put object name on first line and Level plus numeric value on second. Remove is now phrase to avoid fused name/Level boundary. Shared aliases M035 and M036 preserved.')
r[-2:]=struct.pack('<H',sum(r[:-2])&65535)
Path('qa17/private/candidate.ws').write_bytes(r);Path('qa17/edits.json').write_text(json.dumps(edits,indent=2)+'\n')
print(hashlib.sha256(r).hexdigest());print([(x['id'],x['new_words'],x['lines'])for x in edits])
