from pathlib import Path
import csv,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qa15.inventory_layout import story_inventory,words_until_end
from qa21.text_codec import MAP,RIGHT_SINGLE
from qa22.hf16_base import input_path,reconstruct
j=input_path().read_bytes();r=reconstruct(j)
rows={x['id']:x for x in story_inventory(r,'HF16')[0]};jr={x['id']:x for x in story_inventory(j,'JP')[0]}
ids=json.loads(Path('qa19/five_validation_plan.json').read_text())['partitions']['V4']
inv={}
for k,vs in MAP.items():
 for v in vs:
  if v not in inv or len(k)>len(inv[v]):inv[v]=k
for k,v in RIGHT_SINGLE.items():inv[v]=k
# Original dialogue may use technical terminators and literal low-word dynamic insertion.
def decode(rom,row):
 words,_,_=words_until_end(rom,int(row['pointer'],16));out=[];i=0
 while i<len(words):
  w=words[i];i+=1
  if w>=0xfff0:
   if w in (0xfff2,0xfffd,0xfffe,0xfffc):out.append({'fff2':' <END>','fffd':' <PAGE>','fffe':' / ','fffc':' <CLEAR> '}[f'{w:04x}']);continue
   if w in (0xfff4,0xfff8,0xfffa,0xfffb):
    arg=words[i];i+=1;out.append(f'<{w:04X}:{arg:04X}>');continue
   out.append(f'<{w:04X}>');continue
  out.append(inv.get(w,f'<{w:04X}>'))
 return ''.join(out).strip(),words
with Path('qa22/baseline_text.csv').open('w') as o:
 writer=csv.writer(o);writer.writerow(['id','en_pointer','jp_pointer','en_words','jp_words','en_decoded','en_codes','jp_codes'])
 for id in ids:
  e,ew=decode(r,rows[id]);_,jw=decode(j,jr[id]);writer.writerow([id,rows[id]['pointer'],jr[id]['pointer'],len(ew),len(jw),e,' '.join(f'{w:04X}'for w in ew),' '.join(f'{w:04X}'for w in jw)])
print('rows',len(ids))
