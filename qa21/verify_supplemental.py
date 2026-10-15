from pathlib import Path
from PIL import Image
import argparse,csv,json,hashlib
R=Path(__file__).resolve().parents[1];Q=R/'qa21';E=R/'evidence/qa21_runs'
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
m=json.loads((R/'manifest.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=lambda p:list(csv.DictReader(p.open()));checks=0;frames=0;binding=set();readings=[]
def ck(ok,label):
 global checks
 assert ok,label;checks+=1
width={int(x['id']):int(x['inner_width_px'])for x in rows(R/'qa15/census_final/window_presets.csv')}
names=['quantity_unknown','unknown_names_long','status_equipped_plus','status_equipped_minus'];expected={'quantity_unknown':{(4,14,10),(4,14,20),(5,2,233),(5,2,234)},'unknown_names_long':{(4,14,87),(4,14,93)},'status_equipped_plus':{(26,3,136)},'status_equipped_minus':{(26,3,136)}}
for label in ['JP','HF16V3']:
 for name in names:
  d=E/f'ui_{label}_{name}';meta=json.loads((d/'run.json').read_text());ck(meta['rom_sha256']==m['original'if label=='JP'else'target']['sha256'],d.name+' ROM');ck(meta['exit']==0 and meta['completed'],d.name+' complete');ck(meta['state_sha256']==sha(R/'evidence/qa3/q3_dungeon/checkpoint.mss'),d.name+' state');ck(meta['plan_sha256']==sha(d/'plan.lua'),d.name+' plan');ck(meta['script_sha256']==sha(Q/'driver.lua'),d.name+' driver');ck(all(x['poweroff']=='false'for x in rows(d/'frames.csv')),d.name+' powered');ck(not(d/'dump_error.txt').exists(),d.name+' dump')
  gs=rows(d/'getters.csv');got={tuple(int(x[k])for k in ['window','family','index'])for x in gs};ck(expected[name]<=got,d.name+' actual getter consumers')
  st=rows(d/'stores.csv');ck(all(x['row_overflow']=='false'for x in st),d.name+' row bounds');ck(all((int(x['relative_byte'])+int(x['stride_bytes']))*4<=width[int(x['window'])]for x in st),d.name+' consumer width')
  if label=='HF16V3':frames+=int((d/'completed.txt').read_text().split('=')[1]);binding|=got
 d=E/f'fused_{label}';meta=json.loads((d/'run.json').read_text());ck(meta['rom_sha256']==m['original'if label=='JP'else'target']['sha256'],d.name+' ROM');ck(meta['completed']and meta['exit']==0 and not meta['timed_out'],d.name+' complete');ck(meta['state_sha256']==sha(R/'evidence/qa3/q3_dungeon/checkpoint.mss'),d.name+' state');ck(meta['script_sha256']==sha(d/'observer.lua'),d.name+' observer');ck(meta['cases_sha256']==sha(d/'cases.lua'),d.name+' cases');rr=rows(d/'results.csv');ck(len(rr)==6,d.name+' six cases');ck(all(x['poweroff']=='false'and x['inventory_qty']=='1'and x['inventory_id']==x['item']for x in rr),d.name+' item and power');ck(not rows(d/'buffer_guard.csv'),d.name+' copy buffer guard')
 got={(int(x['family']),int(x['index']))for x in rows(d/'text_reads.csv')};ck({(6,19),(6,22),(6,50),(6,55),(7,23),(7,25),(7,30),(7,38)}<=got,d.name+' fused descriptors')
 if label=='HF16V3':frames+=int((d/'completed.txt').read_text().split('frames=')[1].strip())
for x in json.loads((Q/'supplemental_readings_index.json').read_text()):
 p=E/x['path'];readings.append(x|{'sha256':sha(p),'pixel_sha256':hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest(),'method':'DIRECT_NATIVE_BILINGUAL_READING'})
ck(readings==json.loads((Q/'supplemental_visual_readings.json').read_text()),'100 archived supplemental readings')
for entry in json.loads((Q/'visual_readings.json').read_text()):
 p=E/entry['run']/entry['image'];ck(sha(p)==entry['sha256'],'final image bytes '+entry['id'])
 pixel=hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest();ck(pixel==entry['pixel_sha256'],'final pixels '+entry['id'])
 if entry.get('read_image'):
  rp=E/entry['read_image'];ck(hashlib.sha256(Image.open(rp).convert('RGB').tobytes()).hexdigest()==pixel,'direct reading pixels '+entry['id'])
result={'status':'PASS_SYNTHETIC_SCOPED_NATIVE_CONSUMERS','checks':checks,'final_native_sessions':5,'japanese_comparison_sessions':5,'inventory_status_cases':4,'fused_cases':6,'final_frames':frames,'native_readings':len(readings),'unique_window_getter_bindings':len(binding),'bindings':[list(x)for x in sorted(binding)],'new_getter_repairs':2,'global_getter_approval':False,'user_summary':'Se compararon japonés e inglés en cuatro recorridos de inventario/estado y seis configuraciones de equipo fusionado. Cantidades 1/99, niveles +99/−99, dinero de ocho cifras, nombres sin identificar y ocho propiedades de fusión resultan legibles en la muestra. Dos etiquetas de eficacia contra tipos de enemigos se corrigieron.','report_images':[{'path':'ui_HF16V3_unknown_names_long/f00420.png','caption':'Nombres sin identificar y cantidades 99/1'},{'path':'ui_HF16V3_status_equipped_minus/f00600.png','caption':'Equipo −99 y dinero de ocho cifras'},{'path':'fused_HF16V3/fused_65_13_16_f720.png','caption':'Dos propiedades corregidas contra tipos de enemigos'}]}
ck(result['final_frames']==13641 and result['native_readings']==100,'archived supplemental totals')
result['revalidation_checks']=checks
result['archived_result_unchanged']=True
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'revalidation_checks':checks,'native_readings':len(readings)},ensure_ascii=False))
