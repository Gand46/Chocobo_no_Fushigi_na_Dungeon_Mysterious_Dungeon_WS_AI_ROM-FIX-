from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path('qa20');ids=json.loads((R/'audit_ids.json').read_text());tr=json.loads((R/'translations.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pixel=lambda p:hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest()
known={}
# These contact sheets were read directly: baseline_contact_00..12,
# final_review_00..04 and checked_review_00, with the Japanese audit_00..24.
for prefix in ['baseline_','final_','checked_']:
 for d in (R/'runs').glob(prefix+'G*'):
  ps=sorted(d.glob('page_*.png'))
  if prefix=='baseline_' or not ps:ps+=list(d.glob('end_text.png'))
  for p in ps:known.setdefault(pixel(p),str(p.relative_to(R/'runs')))
vis=[];review=[];unseen=[]
reserve={f'G00:M{x:03d}'for x in range(252,256)}|{'G04:M033','G04:M034'}
for i,id in enumerate(ids):
 d=R/'runs'/('release_'+id.replace(':','_'));seen=set();imgs=[]
 for p in sorted(d.glob('page_*.png'))+list(d.glob('end_text.png')):
  h=pixel(p)
  if h in seen:continue
  seen.add(h);ref=known.get(h)
  if ref is None:unseen.append((id,p))
  entry={'id':id,'run':d.name,'image':p.name,'sha256':sha(p),'pixel_sha256':h,'method':'PIXEL_IDENTICAL_TO_DIRECTLY_READ_IMAGE'if ref else'REQUIRES_DIRECT_READING','read_image':ref}
  vis.append(entry);imgs.append(entry)
 if not imgs and id=='G00:M255':
  p=d/'f02400.png';entry={'id':id,'run':d.name,'image':p.name,'sha256':sha(p),'pixel_sha256':pixel(p),'method':'DIRECT_READ_NATIVE_DIAGNOSTIC','read_image':'evidence/qa20_runs/'+d.name+'/'+p.name,'scope':'Blank box at limit; target incomplete; excluded from approval'};vis.append(entry);imgs.append(entry)
 review.append({'id':id,'status':'NEEDS_CONTEXT'if id in reserve else'PASS_SYNTHETIC_REVIEWED_SCOPED','changed':id in tr,'english_final':tr.get(id,{}).get('text'),'reason':tr.get(id,{}).get('reason','Conservado tras lectura bilingüe y nativa; no se propone corrección en esta fase.'),'japanese_source_sheet':f'qa20/audit_{i//10:02d}.png','final_images':[f'evidence/qa20_runs/{x["run"]}/{x["image"]}'for x in imgs],'context_limit':'Depuración/variables en estado ajeno: requiere consumidor válido.'if id.startswith('G00:M25')and id in reserve else'Preguntas/precios compuestos: falta ejecutar cada consumidor de forja.'if id in reserve else'Selección sintética en motor nativo de dos líneas; no acredita recorrido natural ni todos los interlocutores.'})
for start in range(0,len(unseen),24):
 ch=unseen[start:start+24];im=Image.new('RGB',(896,164*((len(ch)+3)//4)),'#ddd');dr=ImageDraw.Draw(im)
 for j,(id,p)in enumerate(ch):
  x=j%4*224;y=j//4*164;dr.text((x,y),id+' '+p.stem,fill='black');im.paste(Image.open(p),(x,y+20))
 im.save(R/f'release_unseen_{start//24:02}.png')
for name in ['release_menu_empty','release_menu_saved','release_save_native','release_load_saved']:
 for p in sorted((R/'runs'/name).glob('f*.png')):
  vis.append({'id':'UI:'+name,'run':name,'image':p.name,'sha256':sha(p),'pixel_sha256':pixel(p),'method':'DIRECT_READ_NATIVE_CONTACT','read_image':('qa20/release_load_saved.png'if name=='release_load_saved'else'qa20/release_consumers_00.png;qa20/release_consumers_01.png'),'scope':'Lectura del menú y ventanas mostradas; no aprobación lingüística de G09 ni de G16.'})
(R/'visual_readings.json').write_text(json.dumps(vis,indent=2)+'\n');(R/'linguistic_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');(R/'unseen_images.json').write_text(json.dumps([str(p)for _,p in unseen],indent=2))
print(json.dumps({'references':len(review),'visual_readings':len(vis),'unseen_images':len(unseen),'scoped_pass':len(ids)-len(reserve)}))
