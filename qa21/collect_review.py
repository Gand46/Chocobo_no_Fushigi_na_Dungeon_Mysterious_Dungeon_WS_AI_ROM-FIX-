from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
Q=Path('qa21');ids=json.loads((Q/'audit_ids.json').read_text());tr=json.loads((Q/'translations.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pixel=lambda p:hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest()
known={}
# Directly read: baseline_contact_00..11 and final_review_00..04.
for prefix in ['baseline_','final_']:
 for r in (Q/'runs').glob(prefix+'G*'):
  for p in sorted(r.glob('page_*.png'))+list(r.glob('end_text.png')):known.setdefault(pixel(p),str(p.relative_to(Q/'runs')))
if (Q/'release_direct_read.json').exists():
 for x in json.loads((Q/'release_direct_read.json').read_text()):
  p=Q/'runs'/x['path'];assert pixel(p)==x['pixel_sha256'];known[x['pixel_sha256']]=x['path']
reserve={'G06:M100','G11:M011'};vis=[];review=[];unseen=[]
for i,id in enumerate(ids):
 r=Q/'runs'/('verified_'+id.replace(':','_'));seen=set();images=[]
 for p in sorted(r.glob('page_*.png'))+list(r.glob('end_text.png')):
  h=pixel(p)
  if h in seen:continue
  seen.add(h);ref=known.get(h)
  if not ref:unseen.append({'id':id,'path':str(p.relative_to(Q/'runs')),'pixel_sha256':h})
  x={'id':id,'run':r.name,'image':p.name,'sha256':sha(p),'pixel_sha256':h,'method':'PIXEL_IDENTICAL_TO_DIRECT_NATIVE_READING'if ref else'REQUIRES_DIRECT_READING','read_image':ref};vis.append(x);images.append(f'evidence/qa21_runs/{r.name}/{p.name}')
 review.append({'id':id,'status':'NEEDS_CONTEXT'if id in reserve else'PASS_SYNTHETIC_REVIEWED_SCOPED'if all(x['read_image']for x in vis if x['id']==id)and images else'PENDING_VISUAL_READING','changed':id in tr,'english_final':tr.get(id,{}).get('text'),'reason':tr.get(id,{}).get('reason','Conservado tras lectura bilingüe y lectura nativa del caso sintético.'),'japanese_source_sheet':f'qa21/audit_{i//8:02d}.png','final_images':images,'context_limit':'Depuración: consumidor real pendiente.'if id=='G06:M100'else'Fragmento de cantidad de plantas: falta el número y la ventana compuesta del consumidor.'if id=='G11:M011'else'Selección sintética en el motor original; no acredita interlocutor ni recorrido natural.'})
for start in range(0,len(unseen),24):
 ch=unseen[start:start+24];im=Image.new('RGB',(896,164*((len(ch)+3)//4)),'#ddd');d=ImageDraw.Draw(im)
 for k,x in enumerate(ch):
  xx=k%4*224;yy=k//4*164;d.text((xx,yy),x['id']+' '+Path(x['path']).stem,fill='black');im.paste(Image.open(Q/'runs'/x['path']).crop((0,0,224,144)),(xx,yy+20))
 im.save(Q/f'release_unseen_{start//24:02}.png')
(Q/'unseen_images.json').write_text(json.dumps(unseen,indent=2));(Q/'visual_readings.json').write_text(json.dumps(vis,indent=2));(Q/'linguistic_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2));print({'refs':len(review),'images':len(vis),'unseen':len(unseen),'pass':sum(x['status']=='PASS_SYNTHETIC_REVIEWED_SCOPED'for x in review)})
