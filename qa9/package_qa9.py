from pathlib import Path
import json,shutil,hashlib,csv
from PIL import Image,ImageDraw,ImageFont
root=Path('delivery/Chocobo_EN_v1.1_HF6_TEST_Fuentes_QA9_20261014')
qa=root/'qa9';shutil.copytree('qa9',qa,ignore=shutil.ignore_patterns('__pycache__','*.o','floor_digits.bin','upload*.json'),dirs_exist_ok=True)
dest=root/'evidence/qa9_runs';dest.mkdir(exist_ok=True)
index=[]
for run in sorted(Path('runs').glob('q9_*')):
 if not (run/'run.json').exists():continue
 shutil.copytree(run,dest/run.name,dirs_exist_ok=True)
 m=json.loads((run/'run.json').read_text());name=run.name;params={};scope='DIAGNOSTIC_ONLY'
 if name in ['q9_fountain_full','q9_hf6_fountain_full','q9_jp_fountain_full']:params={'FOUNTAIN_FULL':'1'};scope='SYNTHETIC_COHERENT_FOUNTAIN_FROG_FULL'
 if name=='q9_fountain_min':params={'FOUNTAIN_FULL':'0'};scope='SYNTHETIC_COHERENT_FOUNTAIN_FROG_MINIMUM'
 if name.startswith('q9_flag'):
  addr,mask=name.removeprefix('q9_flag').split('_');params={'FLAG_ADDR':str(int(addr,16)),'FLAG_MASK':str(int(mask,16))};scope='ISOLATED_FLAG_DIAGNOSTIC_NOT_NATURAL_PROGRESSION'
 if name.startswith('q9_final') or name=='q9_scoped99':scope='HF6_SYNTHETIC_COLD_LOAD_FROM_STALE_CACHE'
 if 'elevator' in name or 'entry30' in name or 'active30' in name:params['TARGET_FLOOR']='30';scope='EXCLUDED_INCOMPLETE_SCRIPT_ENTRY_NOT_CONTINUOUS_ELEVATOR'
 if 'telep_reentry30' in name:scope='NATIVE_TELEP99_THEN_SYNTHETIC_REENTRY_CONTAINER_THEN_NATIVE_COLD_LOAD'
 if name=='q9_telep99':scope='NATIVE_USE_TELEP_CARD_0B_INJECTED_IN_BAG_ON_SYNTHETIC_F99'
 if 'native_cold99' in name:scope='NATIVE_SAVE98_AND_COLD_LOAD99_WITH_COHERENT_CACHE'
 if name=='q9_native_save98':scope='NATIVE_SAVE_AND_GO_ON_ON_STAIR_RELOCATED_ADJACENT_TO_PLAYER'
 if name=='q9_ending_pair4d_12':scope='DISCARDED_HYPOTHESIS_FLAGS_NOT_FOUNTAIN'
 if name=='q9_white_probability1':scope='DIAGNOSTIC_POKE_ONLY_NOT_SHIPPED_FIX'
 index.append({'run':name,'scope':scope,'parameters':params,'rom_sha256':m['rom_sha256'],'state_sha256':m.get('state_sha256'),'input_save_sha256':m.get('input_save_sha256'),'checkpoint_sha256':hashlib.sha256((run/'checkpoint.mss').read_bytes()).hexdigest() if (run/'checkpoint.mss').exists() else None,'completed':m['completed']})
(root/'docs/QA9_RUN_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
shutil.copy2('qa9/verification.json',root/'docs/QA9_VERIFICATION.json')
script_hashes={str(p.relative_to(qa)):hashlib.sha256(p.read_bytes()).hexdigest() for p in qa.rglob('*') if p.suffix in ['.lua','.py','.s']}
(root/'docs/QA9_SCRIPT_HASHES.json').write_text(json.dumps(script_hashes,indent=2)+'\n')
images=[('HF5: F99 bloqueado','runs/q9_cold99_trace/f04300.png'),('HF6: F99 reconstruido','runs/q9_scoped99/f04300.png'),('HF5: F30 con mapa de jefe','runs/q9_hf5_telep_reentry30/f04300.png'),('HF6: F30 normal','runs/q9_hf6_telep_reentry30/f04300.png'),('Fuente/rana: escena del final','runs/q9_hf6_fountain_full/f06600.png'),('Control posterior en el pueblo','runs/q9_scoped_fountain_walk/f00480.png')]
sheet=Image.new('RGB',(936,1120),'#eceee9');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
d.text((18,12),'Chocobo HF6 TEST — evidencia QA9',fill='#202e30',font=title);d.text((18,49),'Acceso sintetico documentado; ascensor continuo y aprobacion global pendientes.',fill='#384a4b',font=font)
for i,(label,p) in enumerate(images):
 x=16+(i%2)*464;y=90+(i//2)*340;d.text((x,y),label,font=font,fill='#202e30');sheet.paste(Image.open(p).convert('RGB').resize((448,314),Image.Resampling.NEAREST),(x,y+26))
p=Path('delivery/Evidencia_Chocobo_HF6_QA9_20261014.png');sheet.save(p);shutil.copy2(p,root/'evidence'/p.name)
print('Packaged runs',len(index))
