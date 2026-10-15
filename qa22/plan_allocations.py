from pathlib import Path
import json,re,struct,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qa21.text_codec import encode
from qa15.inventory_layout import story_inventory
from qa22.hf16_base import input_path,reconstruct
rom=reconstruct(input_path().read_bytes());rows={x['id']:x for x in story_inventory(rom,'HF16')[0]}
T=json.loads(Path('qa22/translations.json').read_text());out=[];used=0;inplace=0
def enc(s):
 v=[]
 for part in re.split(r'(\{[^}]+\})',s):
  if not part:continue
  if part.startswith('{'):
   token=part[1:-1];v.extend([0xfffa,6]);v.extend([0xC1,0xE,0x7A,0x198,0x275,0xC2,0x5] if token=="Camilla's Dad" else encode(token));v.extend([0xfffa,0])
  else:v.extend(encode(part))
 return v
def width(s):return len(enc(s))-4*s.count('{')
def wrap(s):
 lines=[];line=''
 for word in re.findall(r'\{[^}]+\}[^\s]*|[^\s]+',s):
  cand=(line+' '+word).strip()
  if width(cand)>13:
   assert line,(s,word);lines.append(line);line=word
  else:line=cand
 if line:lines.append(line)
 assert all(width(x)<=13 for x in lines),(s,lines)
 return lines
def layout(s,pages=None):
 if pages is None:lines=wrap(s)
 else:
  assert ' '.join(pages)==s
  lines=[]
  for page in pages:
   page_lines=wrap(page);assert 1<=len(page_lines)<=2
   if lines and len(lines)%2:lines.append('')
   lines.extend(page_lines)
 v=[]
 for i,x in enumerate(lines):
  if i:v.extend([0xfffe]if i%2 else[0xfff2,0xfffd])
  if x:v.extend(enc(x))
 return v+[0xfff2,0xffff],lines
for id,d in T.items():
 words,lines=layout(d['text'],d.get('pages'));new=len(words)*2;row=rows[id];old=int(row['end'],16)-int(row['pointer'],16);shared=not row['unique_pointer']
 if new<=old and not shared:inplace+=1
 else:used+=new
 out.append({'id':id,'new_bytes':new,'old_bytes':old,'mode':'inplace'if new<=old and not shared else'allocate','lines':lines})
Path('qa22/allocation_plan.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('new',len(out),'inplace',inplace,'allocated bytes',used,'free',0x70000-0x6f708,'overage',used-(0x70000-0x6f708))
print('inplace ids',[x['id'] for x in out if x['mode']=='inplace'])
