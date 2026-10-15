from pathlib import Path
import json,hashlib,csv,shutil,base64
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];D=W/'delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA16_M2_20261014';Q=W/'qa16'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rows(p):return list(csv.DictReader(p.open()))
def csvout(p,rr):
 with p.open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
old='magic_boundaries';new='magic_display99';r=D/'evidence/qa16_runs'/new
shutil.copytree(Q/'runs'/new,r,dirs_exist_ok=True);shutil.copy2(Q/'layout_observer.lua',r/'observer.lua');shutil.copy2(Q/(new+'.lua'),D/'qa16'/(new+'.lua'))
prov=json.loads((D/'evidence/qa16_runs'/old/'provenance.json').read_text());dump(r/'provenance.json',prov)
ix=json.loads((D/'docs/QA16_RUN_INDEX.json').read_text());prev=next(x for x in ix if x['run']==old);prev.update(status='DIAGNOSTIC_EXCLUDED',scope='Raw255 source produces truncated decimal display (ATB55). Out-of-two-digit-domain stress; not an approved numeric boundary and not a demonstrated reachable ROM defect. Superseded by magic_display99.')
m=json.loads((r/'run.json').read_text());entry=dict(prev);entry.update(run=new,status='PASS_SYNTHETIC_SCOPED',scope='Seven spells, Lv.99, ATB99 and NEXT99P visible without clipping; display-domain test, not natural progression claim.',plan_sha256=m['plan_sha256']);ix.append(entry);ix.sort(key=lambda x:x['run']);dump(D/'docs/QA16_RUN_INDEX.json',ix)
vr=json.loads((D/'qa16/visual_readings.json').read_text())
for x in vr:
 if x['run']==old:x.update(run=new,sha256=sha(r/x['image']),reading='Lv.99, ATB99 and NEXT99P; Blizzard/Thunder/Aero/Shine visible without overlap. Seven spell names executed across scrolling.')
dump(D/'qa16/visual_readings.json',vr)
# Recompute current approved bindings and monitored events.
win={int(x['id']):int(x['inner_width_px'])for x in rows(D/'qa15/census_final/window_presets.csv')};bind={};guard=[]
for x in ix:
 rr=D/'evidence/qa16_runs'/x['run'];approved=x['status']=='PASS_SYNTHETIC_SCOPED'
 if approved:
  for z in rows(rr/'getters.csv'):bind.setdefault(tuple(int(z[k])for k in ['window','family','index']),set()).add(x['run'])
 if(rr/'stores.csv').exists():
  zz=rows(rr/'stores.csv');guard.append({'run':x['run'],'distinct_store_events':len(zz),'full_row_52byte_overflow':sum(z['row_overflow']=='true'for z in zz),'window_width_overflow':sum((int(z['relative_byte'])+int(z['stride_bytes']))*4>win[int(z['window'])]for z in zz),'status':'SCOPED_MONITOR_NOT_ALL_WRITES','approved_run':approved})
csvout(D/'qa16/runtime_getter_bindings.csv',[dict(window=k[0],family=k[1],index=k[2],runs='|'.join(sorted(v)),status='EXECUTED_SELECTED_VISUAL_SAMPLES_NOT_EVERY_GLYPH')for k,v in sorted(bind.items())]);csvout(D/'qa16/store_guard_summary.csv',guard)
for path in [D/'docs/QA16_VALIDATION.json',D/'manifest.json']:
 obj=json.loads(path.read_text());s=obj['qa16']if path.name=='manifest.json'else obj;s.update(all_runs=36,magic_extremes='Approved fixture uses99 in level/ATB/point sources and displays99. Raw255 fixture excluded as out-of-two-digit-domain stress.');dump(path,obj)
old64=base64.b64encode((Q/'runs'/old/'f00720.png').read_bytes()).decode();new64=base64.b64encode((r/'f00720.png').read_bytes()).decode()
for path in [W/'delivery/Chocobo_QA16_M2_Informe.html',D/'qa16/Chocobo_QA16_M2_Informe.html']:
 s=path.read_text().replace(old64,new64).replace('magic_boundaries','magic_display99').replace('35 ejecuciones','36 ejecuciones').replace('niveles 1/99 y estrés con campos de origen 255','niveles 1/99, ATB99 y NEXT99P').replace('niveles1/99 y estrés con campos de origen255','niveles 1/99, ATB99 y NEXT99P').replace('No certifica que todos esos valores sean alcanzables.','El ensayo previo con255 queda excluido: rebasa el formato de dos cifras. No certifica progreso natural.').replace('Lv.99, multiple spell names and gauges; visible fields remain separate. Raw255 source does not mean a displayed255 or a reachable game value.','Lv.99, ATB99, NEXT99P: seven spell names across scrolling; no visible overlap.')
 path.write_text(s)
for path in [D/'INFORME_ES.md',D/'CONTEXTO_CONTINUACION.md',D/'docs/QA16_REPRODUCCION.md']:
 s=path.read_text().replace('35 ejecuciones','36 ejecuciones');s+='\nQA16 final: `magic_display99` sustituye al ensayo `magic_boundaries` en la lista de PASS. Los valores 99 se muestran completos (Lv.99, ATB99 y NEXT99P). El ensayo anterior con 255 se conserva como diagnóstico excluido porque supera el formato de dos cifras. No demuestra un defecto alcanzable de la ROM.\n';path.write_text(s)
# Update compact sheet with the accepted fixture.
for path in [W/'delivery/Chocobo_QA16_M2_Evidencia.png',D/'qa16/QA16_M2_Evidencia.png']:
 im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im);draw.rectangle((490,206,950,232),fill='#f5f1e6');draw.text((490,210),'Magic: Lv.99 / ATB99 / NEXT99P',fill='#162b36');im.paste(Image.open(r/'f00720.png').convert('RGB').crop((0,0,224,144)),(490,233));im.save(path)
print('Final accepted magic fixture:',new)
