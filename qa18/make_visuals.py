from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
cases=[('final_G00_M015',300,'Oh, sorry.'),('final_G00_M015',600,'After you came all / this way.'),('final_G06_M012',360,"... I see. / So Camilla's Dad was"),('final_G06_M012',600,'taken by something / and had a dungeon'),('final_G06_M012',840,'built under the inn.'),('final_G06_M073',330,'Touching the back / will revert your level to'),('final_G06_M073',600,'You cannot undo.'),('final_G09_M191',330,'Hm...'),('final_G09_M191',600,'To put it / more bluntly...'),('final_slot_native',120,'1 Slot Point'),('final_slot_native',300,'100 Gil'),('final_slot_native',600,'Exchange Slot Points?'),('final_dyn_G00_M253_max',330,'Cost 65535Gil'),('final_dyn_G16_M034_max',330,'Double KnockTalon / Level 65535!')]
canvas=Image.new('RGB',(448*3,312*5),'#f5f4ec');d=ImageDraw.Draw(canvas);readings=[]
for i,(n,f,t)in enumerate(cases):
 p=Path('qa18/runs')/n/f'f{f:05d}.png';im=Image.open(p).convert('RGB').resize((448,288),Image.Resampling.NEAREST);x=i%3*448;y=i//3*312;canvas.paste(im,(x,y+24));d.text((x+4,y+4),f'{n.removeprefix("final_")}  f{f}',fill='black');readings.append({'run':n,'image':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'observed_reading':t,'layout':'PASS_SYNTHETIC_SCOPED','semantic_approval':False if n=='final_G06_M073'else'NOT_GLOBAL_LINGUISTIC_REVIEW'})
canvas.save('qa18/final_contact.png');Path('qa18/visual_readings.json').write_text(json.dumps(readings,indent=2)+'\n')
