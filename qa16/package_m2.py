"""Assemble cumulative QA16 evidence; this procedure does not alter ROM bytes."""
from pathlib import Path
import json,csv,hashlib,shutil,base64,html,datetime,subprocess
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent.parent
B=W/'delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA15_M1_20261014'
D=W/'delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA16_M2_20261014'
Q=W/'qa16'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def readcsv(p):return list(csv.DictReader(p.open()))
def csvout(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
passed={
'ui_route':'Main menu; baseline Status; Check/Exit submenu. No claim for other attempted branches.',
'status_extreme':'Record 99F, Money 99,999,999 Gil, lower status rows and scrolling.',
'status_equipped_plus':'Longest item name ID136 with +99, native inventory-equipped construction.',
'status_equipped_minus':'Longest item name ID136 with -99, native inventory-equipped construction.',
'magic_route':'Four initial spell rows, Lv.1, ATB50, labels and gauges.',
'magic_boundaries':'Seven spell names, Lv.99; ATB/point source bytes255. Raw display stress, gameplay attainability not asserted.',
'inventory_boundaries':'Native sorted list and descriptions; long IDs136/137/138; +99/-99; multiple scroll positions.',
'quantity_unknown':'Visible quantities1/99, unidentified names F14:I010/I020.',
'unknown_names_long':'Unidentified names F14:I087/I093, both maximum144px in family14; quantities1/99.',
'shop_native_entry':'Native Buy/Sell and eight-digit balance; initial Buy-disabled state. Synthetic script entry.',
'shop_buy_list':'Enabled Buy, five merchandise IDs, scrolling and prices100/200/300/1000; balance99,999,999.',
'shop_buy_insufficient':'Buy with zero money leaves money and inventory unchanged; no separate error text observed.',
'shop_buy_purchase':'Potion ID73 acquired, balance99,999,999 ->99,999,899, exact100 Gil debit.',
'shop_sell_plus':'Despite plan name, actual selected item is Fire ID233 quantity99; confirmation200Gil; cancel preserves inventory.',
'shop_sell_confirm_plus':'Actual ID136+99 sale confirmation2898Gil; acceptance removes item and credits2898Gil.',
'shop_sell_confirm_minus':'Actual ID157-99 sale confirmation1Gil; acceptance removes item and credits1Gil.'}
notes={
'shop_default':'TIMEOUT_NOT_PASS; incompatible story-flag fixture entered an introductory scene; no freeze attribution.',
'status_long_plus':'DIRECT_EQUIPMENT_POKE_INEFFECTIVE: native setup rebuilds equipment from inventory; superseded.',
'status_long_minus':'DIRECT_EQUIPMENT_POKE_INEFFECTIVE: native setup rebuilds equipment from inventory; superseded.',
'shop_route':'No shop UI/text, merely town movement attempt.',
'shop_trace':'No interaction: approach did not reach counter.',
'shop_enter':'Checkpoint production: enters shop; no text layout approval.',
'shop_buy':'NPC says Nothing is for sale; not a commercial UI test.',
'shop_context_trace':'Identified NPC script branches; not a commercial UI test.',
'shop_flag8':'Alternate story dialogue; not commercial UI.',
'shop_flag4':'Progress branch followed, empty inventory test leads to Nothing is for sale.',
'shop_inventory':'Story cutscene with injected inventory; no Buy/Sell coverage.',
'shop_sell_minus':'Misleading plan name: actual ID136+99 selected; used diagnostic evidence, superseded by confirmed transaction.',
'window_32':'Forced preset first page Store1..5 only; no gameplay context established.',
'window_36':'Forced Yes/No preset only; not a validated gameplay flow.',
'window_40':'Forced Read it/Return it preset only; not a validated gameplay flow.',
'window_47':'Forced item-name preset only; not a validated gameplay flow.',
'window_49':'Forced incompatible preset returns to title; excluded from defect/pass claims.',
'storage_scroll':'Input did not scroll forced preset; no tail coverage.',
'storage_tail':'CANDIDATE_ONLY: forced preset32 + forced64C4=5; F00:I053 crosses narrow window. Native reachability unknown; do not change shared text.'}
shutil.copytree(B,D,dirs_exist_ok=True)
for n in ['README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md']:
 shutil.copy2(B/n,D/'docs/history'/('QA15_'+n))
(D/'qa16').mkdir(exist_ok=True)
# Export disassembly, not raw commercial ROM fragments.
for n,a in [('shop_init',0x4c72),('shop_consumer',0x7702),('storageconsumer',0x8f2c),('magicinit',0x4b08),('ae11',0xae11),('h71',0x4e)]:
 p=Q/(n+'.bin')
 if p.exists():(Q/(n+'.txt')).write_text(subprocess.check_output(['objdump','-D','-b','binary','-mi8086','-M','intel',f'--adjust-vma={a}',str(p)],text=True))
for p in Q.iterdir():
 if p.is_file() and p.suffix in ['.lua','.py','.json','.txt']:shutil.copy2(p,D/'qa16'/p.name)
shutil.copytree(Q/'runs',D/'evidence/qa16_runs',dirs_exist_ok=True)
windows={int(x['id']):int(x['inner_width_px']) for x in readcsv(B/'qa15/census_final/window_presets.csv')}
state_sources={
'2cb9e29b3749ce0caf9628ff93f8c5b52ebe5eb7212627175290a38d9adb5f82':'evidence/qa3/q3_dungeon/checkpoint.mss',
'2d31195743c2ac0b6e377febcb1b5b3657df23ba7fc9e0803a6e59cc523fe99d':'evidence/qa3/shop_dialog/checkpoint.mss',
'0c654b5f27632f457869e144f0807fd568324df2937d60ca865d5cc4306565b5':'evidence/qa16_runs/shop_enter/checkpoint.mss',
'8debfd849d2ae1dce4732f9ba87704f8d488ee37c2c3746eb53ac02a320f2447':'evidence/qa16_runs/shop_buy/checkpoint.mss'}
index=[];bindings={};guards=[]
for r in sorted((D/'evidence/qa16_runs').iterdir()):
 m=json.loads((r/'run.json').read_text());v3=(r/'stores.csv').exists();observer=Q/('layout_observer.lua' if v3 else 'layout_observer_v2.lua');shutil.copy2(observer,r/'observer.lua')
 access=['SAVESTATE']
 plan=(r/'plan.lua').read_text()
 if 'emu.write' in plan:access.append('WRAM_POKE')
 if '0x64a1' in plan or r.name.startswith('window_') or r.name in ['storage_tail','storage_scroll']:access.append('POINTER_INJECTION')
 prov={'observer_sha256':sha(observer),'observer_version':3 if v3 else 2,'driver_sha256':m['script_sha256'],'state_path':state_sources[m['state_sha256']],'state_sha256':m['state_sha256'],'access':access,'memory_note':'WRAM_POKE is the project access tag; physical fixture memory is wsCartRam (SRAM), not wsWorkRam. No fixture is a ROM edit.'}
 dump(r/'provenance.json',prov)
 entry={'run':r.name,'status':'PASS_SYNTHETIC_SCOPED' if r.name in passed else ('CANDIDATE_NOT_CLOSED' if r.name=='storage_tail' else 'DIAGNOSTIC_EXCLUDED'),'scope':passed.get(r.name,notes.get(r.name,'')),'access':access,'exit':m['exit'],'completed':m['completed'],'rom_sha256':m['rom_sha256'],'state_sha256':m['state_sha256'],'plan_sha256':m['plan_sha256'],'observer_sha256':sha(observer)};index.append(entry)
 if r.name in passed:
  for x in readcsv(r/'getters.csv'):
   k=tuple(int(x[y]) for y in ['window','family','index']);bindings.setdefault(k,set()).add(r.name)
 if v3:
  rr=readcsv(r/'stores.csv');bad=[x for x in rr if (int(x['relative_byte'])+int(x['stride_bytes']))*4>windows[int(x['window'])]]
  guards.append({'run':r.name,'distinct_store_events':len(rr),'full_row_52byte_overflow':sum(x['row_overflow']=='true' for x in rr),'window_width_overflow':len(bad),'status':'SCOPED_MONITOR_NOT_ALL_WRITES','approved_run':r.name in passed})
bindingrows=[dict(window=k[0],family=k[1],index=k[2],runs='|'.join(sorted(v)),status='EXECUTED_SELECTED_VISUAL_SAMPLES_NOT_EVERY_GLYPH') for k,v in sorted(bindings.items())]
csvout(D/'qa16/runtime_getter_bindings.csv',bindingrows);csvout(D/'qa16/store_guard_summary.csv',guards);dump(D/'docs/QA16_RUN_INDEX.json',index)
# Manual pixel readings already performed before source comparisons. Not OCR.
readings=[
('status_equipped_plus','f00480.png','Record99F; Money99999999Gil; Double KnockTalon +99; visible right edge.'),
('status_equipped_minus','f00480.png','Double KnockTalon -99; visible right edge.'),
('inventory_boundaries','f01020.png','Scrolled list: FaithCard, RottNut, Double KnockTalon+99, Level4 DeathTalon-99; description fits.'),
('quantity_unknown','f00420.png','MossyCollar, SmallCollar; Fire99, Blizzard1, Teleport Box99; Unidentified item.'),
('unknown_names_long','f00420.png','Card with a Hole; Bent Back Card; neither name is clipped.'),
('magic_route','f00600.png','Fire, Blizzard, Thunder, Aero; Lv.1; ATB50; gauges.'),
('magic_boundaries','f00720.png','Lv.99, multiple spell names and gauges; visible fields remain separate. Raw255 source does not mean a displayed255 or a reachable game value.'),
('shop_native_entry','f00120.png','Money99999999Gil, Buy/Sell; Buy disabled.'),
('shop_buy_list','f01080.png','DispelDrink300, EyeDrops200, TelepCard1000; money line intact.'),
('shop_buy_purchase','f00720.png','Money99999899Gil after100Gil purchase.'),
('shop_buy_insufficient','f00720.png','Money0Gil; list retained; no dedicated insufficient-money text observed.'),
('shop_sell_plus','f00720.png','Fire99;200Gil; OK/End. Plan label plus does not describe selected item.'),
('shop_sell_confirm_plus','f00780.png','Double KnockTalon+99;2898Gil; OK/End; no clipping.'),
('shop_sell_confirm_minus','f00780.png','TanSaddle-99;1Gil; OK/End; no clipping.'),
('storage_tail','f00360.png','Go to which... clipped in forced Store6 position; Store7..10 below. Candidate only; no reachable caller established.')]
dump(D/'qa16/visual_readings.json',[{'run':n,'image':f,'sha256':sha(Q/'runs'/n/f),'reading':txt,'method':'DIRECT_NATIVE_PIXELS_NOT_OCR','context_masked_or_independent':False,'status':'CANDIDATE_ONLY' if n=='storage_tail' else 'PASS_VISUAL_SCOPED'}for n,f,txt in readings])
summary={'revision':'QA16_M2','status':'M2_EXECUTED_BOUNDED_PASS_WITH_OPEN_CONTEXT_CANDIDATE','rom_version':'HF11_TEST_UNCHANGED','rom_changes_in_QA16':0,'bps_changed':False,'approved_scoped_runs':len(passed),'all_runs':len(index),'bindings':len(bindings),'windows_in_approved_getter_bindings':sorted({k[0] for k in bindings}),'global_layout_approved':False,'global_linguistic_approved':False,'prior_story_alerts':13,'new_context_candidate':'M2-C01: preset32/family0 index53 at forced scroll5; native reachability unresolved','confirmed_new_reachable_rom_defects':0,'completed_layout_iterations':2,'base_total':4,'remaining_base':2,'estimate_is_guarantee':False,'magic_extremes':'Synthetic raw field stress, not gameplay-range certification','inherited':'QA10/12 item/property samples and QA13/14 functional/logo evidence: unchanged ROM, not rerun','text_monitor_limit':'Common copy/name stores only; zero counts are not a proof for all writes or numeric routines.'}
dump(D/'docs/QA16_VALIDATION.json',summary)
m=json.loads((D/'manifest.json').read_text());m.update(audit_revision='QA16_GLOBAL_LAYOUT_M2',rom_changes_in_QA16=0,new_bps_required=False);m['layout_iteration'].update(completed=2,remaining_base=2,global_approval=False);m['qa16']=summary;dump(D/'manifest.json',m)
p=json.loads((B/'docs/QA15_PLAN_MAQUETACION.json').read_text());p.update(revision='QA16_M2',layout_completed=2,layout_base_remaining=2);p['iterations'][1].update(status='EXECUTED_BOUNDED_WITH_OPEN_CONTEXT_CANDIDATE',work='Menus/status/magic/inventory and native Buy/Sell synthetic flows. Sixteen scoped runs passed. Candidate M2-C01 retained; no ROM edit justified.');p['iterations'][3]['work']+=' Resolve M2-C01 reachability before changing shared F00:I053.';dump(D/'docs/QA16_PLAN_MAQUETACION.json',p)
issues=json.loads((D/'docs/issue_register.json').read_text())
for x in issues:
 if x['id']=='TR-01-M':x.update(status='OPEN_M2_EXECUTED_SCOPED_PASSES',scope='M1 corrected G05:M002. M2:16 scoped synthetic runs passed on unchanged HF11.13 story alerts remain forM3; M2-C01 forced storage-tail clipping requires valid caller/reachability proof. Global layout remains OPEN.',completed_layout_iterations=2,remaining_base_layout_iterations=2)
issues.append({'id':'TR-01-M2-C01','status':'CANDIDATE_CONTEXT_NOT_VALIDATED','scope':'Preset32 init18460AF lists indices48..57; F00:I053 is a floor question,160px, forced second page clips in96px inner box. Native consumer188F2C proven; actual gameplay caller/scroll5 not proven. Do not replace the shared resource until reachability and other consumers are resolved.','access':['SAVESTATE','WRAM_POKE','POINTER_INJECTION'],'evidence':'evidence/qa16_runs/storage_tail'})
issues[-1]['scope']=issues[-1]['scope'].replace('18460AF','1860AF')
dump(D/'docs/issue_register.json',issues)
fields=sorted({k for x in issues for k in x});csvout(D/'docs/issue_register.csv',[{k:json.dumps(x.get(k,''),ensure_ascii=False) if isinstance(x.get(k), (list,dict)) else x.get(k,'') for k in fields} for x in issues])
context='''# Continuar desde HF11 TEST / QA16 M2

M2 de4 ejecutada con16 PASS_SYNTHETIC acotados; maquetación global y fidelidad lingüística siguen abiertas. No hay cambios de ROM ni BPS frente aHF11/QA15. No crearHF12 a partir de esta revisión.

Autoridad actual: manifest.json, docs/QA16_VALIDATION.json, QA16_RUN_INDEX.json, QA16_PLAN_MAQUETACION.json, issue_register.json. Siguiente M3: diálogos/tutoriales/eventos/créditos,13 alertas heredadas,9 recursos dinámicos. M4 integra y reconcilia los contextos pendientes. Dos iteraciones base restantes son estimación, no promesa de cierre total.

Estado y equipamiento: ingresar los registros de inventario en6C9F, no sólo6BF5, porque la inicialización reconstruye el equipo. Flags18h equipan e identifican. Campo nivel99/+99 y157/-99. Nombre largoF03:I136+modificador termina en208px, dentro del área. Cantidad visible99 en Fire/Teleport Box; F14:I087/I093 son los dos nombres no identificados más anchos144px.

Comercio: el checkpoint qa3/shop_dialog está afuera de la tienda. qa16 shop_enter alcanza el interior. Las primeras rutas sólo leen diálogo de historia. Rama op71: banco0 bits en7309+2*(id//16). La prueba útil cambia, una vez en CPU4D160 antes de seleccionar bancoC2, 649B=E0 y64A1=0D0E desdeE1:1DA2. No entrar en0D0D: esRET de guion. Activar bit26h en730D (40h) habilitaBuy. Buy/Sell son ventanas11..16. NO marcar como natural. El script conserva el bucle nativo de lista, precio y compra/venta. Compra:99,999,999→99,999,899, nuevaPotionID73. VentaID136+99:2898Gil; ID157-99:1Gil. Confirmar selección real: el inventario se ordena y las primeras pruebas llamadasplus/minus elegíanFire oel+99, noel-99.

CandidatoM2-C01: preset32, initializer1860AF, row188F2C, F00:I053. Primera páginaStore1..5; forzar64C4=5 muestra pregunta de pisos recortada antes deStore7..10. La tabla prevé10filas pero no se encontró caller nativo válido que llegue aesa página. Es candidata de contexto, NO defecto alcanzable demostrado. El recursoJP también ocupa la misma posición; no cambiarlo porStore6 sin revisar todos los consumidores. Los intentos window49 y shop_default NOson fallos deROM: contexto incompatible / timeout.

Reproducción: qa16/run.py ROM checkpoint plan out --mesen Mesen --timeout15; LAYOUT_OBSERVER=qa16/layout_observer.lua (v3) oelobserver.lua archivado con cada ejecución. Metadatos ystate_path están enprovenance.json. v2 no registra stores/initializers/script. TagWRAM_POKE se conserva por convención del proyecto; las escrituras físicas de fixtures van awsCartRam/SRAM. Pruebas de magia conbytes255 son stress de entrada, noafirmación de límites alcanzables. Cero guardas comunes noevalúa todas las escrituras ni todas las rutinas numéricas.

QA10/12,QA13funcional yQA14logo se heredan por identidad exacta delROM; no repetir barridos255/96,logo orecorridos naturales sin riesgo nuevo. Paquete no incluyeROM,BIOS,emulador. El BPS es acumulativo desdeJPCCAA4853.
'''
(D/'CONTEXTO_CONTINUACION.md').write_text(context)
(D/'README.md').write_text('''# Chocobo English HF11 TEST · QA16 M2

LaROM HF11 ysuBPS no cambian. Esta entrega amplía pruebas y fuentes acumulativas de maquetación.16 recorridos sintéticos acotados aprobados; un candidato nuevo requiere contexto válido. No se aprueba maquetación global, revisión lingüística, hardware ni segundo emulador.

Aplicar patches/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps directamente aJPCRC32CCAA4853. No requiere parches intermedios. Build: python3 build.py /ruta/JP.ws --out /ruta/privada. Revisión nueva: docs/QA16_VALIDATION.json y qa16/visual_readings.json; reproducción: docs/QA16_REPRODUCCION.md. LaROM comercial,BIOS y emulador no se distribuyen.

M3 atenderá diálogos/eventos/créditos y13 alertas pendientes; M4 integrará resultados y el candidatoM2-C01. Consultar CONTEXTO_CONTINUACION.md antes de continuar.
''')
(D/'docs/QA16_REPRODUCCION.md').write_text('''# QA16 · Reproducción y límites

UsarMesen2.1.1 SHA256ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Un solo proceso por perfil, settings.json={} junto alejecutable. No es necesarioXvfb. Driver yobservador quedan fijados por hash. Cargar laROM HF11 reconstruida, nunca distribuirla.

```sh
LAYOUT_OBSERVER="$PWD/evidence/qa16_runs/shop_buy_purchase/observer.lua" python3 qa16/run.py /ruta/HF11.ws evidence/qa16_runs/shop_enter/checkpoint.mss qa16/shop_buy_purchase.lua /ruta/salida --mesen /ruta/Mesen --timeout 15
python3 qa16/verify_scope.py --japanese-rom /ruta/JP.ws --out /ruta/QA16_VERIFICATION.json
```

Cada provenance.json da state_path ytipo de acceso. SAVESTATE siempre; WRAM_POKE parafixtures SRAM; POINTER_INJECTION para guion/selector sintético. Observarplan.lua para todas las escrituras. El comando usa un escenario concreto, no un recorrido natural. Un proceso terminado no otorgaPASS: verificar transacción, getters, selección real, imágenes, integridad y ausencia de dump_error.

stores.csv registra los stores comunes7AFF/7B7D/7BC1/7BFD/7B5A, no todas las escrituras ni las rutinas numéricas. Ancho:rel_byte*4px, avance2bytes para8000h y4para glifo normal. Se compara con ancho interior del preset; los resultados visuales corresponden a capturas identificadas envisual_readings.json. No se usaOCR. La revisión fue con contexto, no ciega ni independiente.

shop_default tuvo timeout yqueda excluido. status_long_plus/minus son intentos ineficaces. window49 no esfixtureválido. storage_tail fuerza contexto aún no encontrado: cinco stores exceden el ancho de suventana, noelbuffer52bytes. No cambiarF00:I053 con esa única prueba. Se mantienen13 alertasde M1 sin afirmar13fallos.
''')
# Compact native-pixel evidence sheet: screenshots are only nearest-neighbor scaled.
selected=[readings[i] for i in [0,1,4,6,8,9,12,13]]
canvas=Image.new('RGB',(960,800),'#f5f1e6');draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for i,(n,f,t) in enumerate(selected):
 x=10+(i%2)*480;y=10+(i//2)*196
 draw.text((x,y),n.replace('shop_','').replace('status_',''),font=font,fill='#162b36')
 im=Image.open(Q/'runs'/n/f).convert('RGB').crop((0,0,224,144)).resize((448,288),Image.Resampling.NEAREST)
 # One-to-one native pixels in report; sheet uses 1x with large margins to retain full windows.
 im=Image.open(Q/'runs'/n/f).convert('RGB').crop((0,0,224,144)).resize((336,216),Image.Resampling.NEAREST)
 im=Image.open(Q/'runs'/n/f).convert('RGB').crop((0,0,224,144))
 canvas.paste(im,(x,y+27));draw.text((x+235,y+45),'PASS\nSYNTHETIC',font=font,fill='#176541')
canvas.save(D/'qa16/QA16_M2_Evidencia.png');shutil.copy2(D/'qa16/QA16_M2_Evidencia.png',W/'delivery/Chocobo_QA16_M2_Evidencia.png')
body='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Chocobo · QA16 · Maquetación M2</title><style>body{font:16px/1.5 system-ui;max-width:1100px;margin:40px auto;padding:0 24px;color:#142a34;background:#faf8f1}h1{font-size:34px}h2{margin-top:36px}.badge{background:#dcebdd;padding:8px 14px;display:inline-block;border-radius:6px}table{border-collapse:collapse;width:100%}td,th{padding:12px;border-bottom:1px solid #cdd4d3;text-align:left}figure{margin:0;padding:18px;background:white;border:1px solid #d5d9d5}img{width:100%;max-width:448px;image-rendering:pixelated}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}figcaption{font-size:14px;margin-top:8px}code{overflow-wrap:anywhere}small{color:#50606b}</style><h1>Maquetación global · iteración 2 de 4</h1><p class="badge">HF11 TEST · QA16 · 16 pruebas sintéticas acotadas aprobadas</p><p>Se verificaron ventanas, desplazamiento, nombres y campos variables de estado, magia, inventario y comercio. No se confirmó un nuevo defecto alcanzable que justifique editar la ROM. HF11 y el BPS acumulativo permanecen idénticos.</p><table><tr><th>Bloque</th><th>Resultado de M2</th></tr><tr><td>Estado</td><td>99F, saldo de ocho cifras, nombre máximo con +99/−99 y desplazamiento: PASS_SYNTHETIC.</td></tr><tr><td>Inventario</td><td>Nombres de equipo largos, cantidades1/99, descripciones muestreadas y dos nombres no identificados máximos: PASS_SYNTHETIC.</td></tr><tr><td>Magia</td><td>Siete nombres, niveles1/99 y estrés con campos de origen255: PASS visual acotado. No certifica que todos esos valores sean alcanzables.</td></tr><tr><td>Comercio</td><td>Buy/Sell, lista y precios. Compra100Gil, rechazo con saldo0, venta+99 por2898Gil y−99 por1Gil: PASS_SYNTHETIC. Guion de acceso inyectado.</td></tr><tr><td>Almacenes</td><td>CandidatoM2-C01: recorte en segunda página forzada. Falta demostrar un caller válido; no se cambia la cadena compartida.</td></tr></table><h2>Capturas nativas comprobadas</h2><div class="grid">'''
for n,f,t in selected:
 data=base64.b64encode((Q/'runs'/n/f).read_bytes()).decode();body+=f'<figure><img alt="{html.escape(n)}" src="data:image/png;base64,{data}"><figcaption>{html.escape(t)}</figcaption></figure>'
n,f,t=readings[-1];body+='</div><h2>Pendiente nuevo: contexto del almacén</h2><p>El preset32 construye diez índices consecutivos. Al forzar la segunda página, F00:I053 contiene la pregunta de pisos (160px) en una ventana con96px interiores; cinco escrituras comunes cruzan ese ancho. La ROM japonesa comparte la estructura. No se ha demostrado que el juego alcance esa página ni que deba sustituirse el recurso. Este caso no recibePASS y no se presenta como fallo natural confirmado.</p>'
body+=f'<figure><img alt="Candidato en página forzada" src="data:image/png;base64,{base64.b64encode((Q/"runs"/n/f).read_bytes()).decode()}"><figcaption>{html.escape(t)}</figcaption></figure>'
body+='''<h2>Lo que sigue abierto</h2><p>M3: diálogos, tutoriales, eventos, créditos y las13 alertas heredadas; una está confirmada (G03:M012) y las otras12 necesitan contexto. M4: integración y conciliación de cobertura, incluidoM2-C01. La revisión lingüística sigue separada. Quedan dos iteraciones base estimadas; no se garantiza que todos los contextos desconocidos quepan en ellas.</p><p>Las16 aprobaciones corresponden a escenarios delimitados, no a16 pantallas únicas ni al100%del juego. Se conservan35 ejecuciones, incluidas las diagnósticas y el timeout excluido. Las guardas nuevas observan copiadores comunes, no toda la memoria ni todas las rutinas numéricas. La revisión visual es directa, con contexto, sinOCR; no hay segundo revisor independiente. QA10/12 yQA13/14 se heredan por identidad deROM, sin repetir barridos cerrados.</p><h2>Entrega</h2><p>Fuentes acumulativas, planesLua, trazasCSV, capturas, estados de prueba, registro de descartes y verificador. Aplicar el BPS HF11 directamente a la japonesaCRC32CCAA4853. Sin ROM,BIOS ni emulador incluidos.</p>'''
body+=f'<p><small>ROM HF11 SHA256:<code>{m["target"]["sha256"]}</code><br>BPS SHA256:<code>{m["bps_sha256"]}</code><br>Fecha:14 de octubre de2026. Estado:TEST, noRC.</small></p></html>'
report=W/'delivery/Chocobo_QA16_M2_Informe.html';report.write_text(body);shutil.copy2(report,D/'qa16'/report.name)
(D/'INFORME_ES.md').write_text('''# Resultado QA16 / M2

16 PASS_SYNTHETIC acotados,35ejecuciones archivadas. ROM yBPS HF11 sin cambios. Estado, magia, inventario ycompra/venta están vinculados a sus consumidores; valores ytransacciones exactos endocs/QA16_VALIDATION.json y QA16_RUN_INDEX.json. Capturas ylecturas enqa16/visual_readings.json; informe legible enqa16/Chocobo_QA16_M2_Informe.html.

CandidatoM2-C01, preset32/F00:I053: segunda página forzada recorta una pregunta de pisos; falta caller nativo válido. No se otorgaPASS ni se cambiaROM por esta prueba. No es una regresión introducida enM2.

M3/M4 siguen pendientes; las13 alertas narrativas deM1 yla revisión lingüística no se cierran aquí. No aprobar maquetación global por estos resultados. M2 es una iteración ejecutada con alcance acotado, no un barrido exhaustivo de todas las variantes de interfaz.
''')
(D/'CHANGELOG.md').write_text('# QA16 M2 · 2026-10-14\n\nPruebas y documentación ampliadas; cero cambios deROM/BPS.16 escenarios sintéticos aprobados y candidato de contextoM2-C01 abierto.\n\n'+(B/'CHANGELOG.md').read_text())
print(json.dumps(summary,ensure_ascii=False,indent=2));print(D)
