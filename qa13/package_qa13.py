from pathlib import Path
import shutil,json,hashlib,zipfile,csv,subprocess,datetime
from PIL import Image,ImageDraw,ImageFont
w=Path.cwd();root=w/'delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA13_20261014';delivery=root.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Correct descriptive comments/labels for future reruns; captured executed plans remain immutable.
p=w/'qa13/atla_stress.lua';s=p.read_text().replace('-- No memory writes and no script-pointer redirection in this plan.','-- Synthetic HP/inventory edits; no story-flag or rescue script-pointer redirection.');p.write_text(s)
for name in ['equipment_sorted','equipment_checkpoint']:
 p=w/'qa13'/name/'run_suite.py';p.write_text(p.read_text().replace('SYNTHETIC_SINGLE_BAG_RECORD_NATIVE_MENU','SYNTHETIC_FULL_BAG_SORTED_TARGET_NATIVE_CHECK'))
for p in [delivery/'Informe_Chocobo_HF9_QA13_20261014.txt',root/'INFORME_ES.md',w/'qa13/write_docs.py']:
 p.write_text(p.read_text().replace('107 comprobaciones','122 comprobaciones').replace('qa13_checks=107','qa13_checks=122'))
g=json.loads((root/'docs/quality_gates.json').read_text());g['qa13_checks']=122;(root/'docs/quality_gates.json').write_text(json.dumps(g,indent=2)+'\n')
shutil.copytree(w/'qa13',root/'qa13',dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.bin','upload*','delivery_manifest.json','__pycache__','check_data.py'))
fixtures=root/'evidence/qa13_fixtures';fixtures.mkdir(parents=True,exist_ok=True)
for src,dest in [('runs/q3_dungeon/checkpoint.mss','dungeon_baseline.mss'),('runs/q7_d2_dialogue_progress/checkpoint.mss','d2_preboss.mss'),('qa9/event_fixtures/D3_to_99_coherent_digits.sav','D3_to_99_coherent_digits.sav')]:shutil.copy2(w/src,fixtures/dest)
excluded={
'q13_equipment_full':'EXCLUDED_TARGET_SELECTED_BEFORE_NATIVE_SORT',
'q13_equipment_save_prompt':'EXCLUDED_OBSERVER_DEPENDENCY_FAILURE_NO_GAME_EVIDENCE',
'q13_equipment_stair':'EXCLUDED_STAIR_MENU_NOT_REACHED',
'q13_equipment_stair_down':'EXCLUDED_STAIR_MENU_NOT_REACHED',
'q13_equipment_save':'EXCLUDED_NO_NATIVE_SAVE_OCCURRED_ZERO_PAYLOAD_WRITES',
'q13_elevator_stair_down':'EXCLUDED_STAIR_MENU_NOT_REACHED',
'q13_elevator_probe':'EXCLUDED_INCOMPLETE_ELEVATOR_CALLER_STATE05',
'q13_elevator_complete':'EXCLUDED_WRONG_CALLER_STATE05',
'q13_elevator_jp_cache30':'DIAGNOSTIC_EARLY_CACHE_WRITE_OVERWRITTEN_NOT_EFFECTIVE_CONTROL'
}
index=[]
for p in sorted((w/'runs').glob('q13_*')):
 if not (p/'run.json').exists():continue
 d=root/'evidence/qa13_runs'/p.name;shutil.copytree(p,d,dirs_exist_ok=True)
 m=json.loads((d/'run.json').read_text())
 if p.name not in excluded:assert m['completed'] and m['exit']==0 and not m.get('timed_out',False)
 if 'plan_sha256'in m:assert sha(d/'plan.lua')==m['plan_sha256']
 else:assert sha(d/'observer.lua')==m['script_sha256'] and sha(d/'cases.lua')==m['cases_sha256']
 role=excluded.get(p.name,'FINAL_HF9_SYNTHETIC_EVIDENCE')
 if p.name not in excluded and m['rom_sha256']!=json.loads((root/'manifest.json').read_text())['target']['sha256']:role='REFERENCE_ROM_CAUSAL_OR_REPRODUCTION_CONTROL'
 params={}
 if p.name.startswith('q13_elevator_') and p.name in {'q13_elevator_caller30','q13_elevator_caller32','q13_elevator_caller99','q13_elevator_jp30','q13_elevator_jp_cache30','q13_elevator_jp_cache_consumer'}:params['TARGET_FLOOR']=99 if p.name.endswith('99') else (32 if p.name.endswith('32') else 30)
 index.append({'run':p.name,'role':role,'parameters_from_invocation':params,'metadata':m,'metadata_sha256':sha(d/'run.json'),'image_count':len(list(d.glob('*.png')))})
# Link every state-based run to an included exact fixture or predecessor checkpoint.
lookup={sha(p):str(p.relative_to(root)) for p in (root/'evidence/qa13_fixtures').glob('*.mss')}
for p in (root/'evidence/qa13_runs').rglob('*.mss'):lookup.setdefault(sha(p),str(p.relative_to(root)))
for item in index:
 h=item['metadata'].get('state_sha256')
 if h:assert h in lookup,(item['run'],h);item['input_state']=lookup[h]
 else:item['input_state']=None
 if item['metadata'].get('input_save_sha256'):item['input_save']=f"evidence/qa13_runs/{item['run']}/input_save.sav"
(root/'docs/QA13_RUN_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
(root/'docs/QA13_FIXTURES.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in fixtures.iterdir()},indent=2)+'\n')
shutil.copy2(w/'qa13/validation.json',root/'docs/QA13_VALIDATION.json');shutil.copy2(w/'private_roms/qa13_rebuild/build_result.json',root/'docs/QA13_BUILD_RESULT.json')
assert (w/'private_roms/qa13_rebuild/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps').read_bytes()==(root/'patches/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps').read_bytes()
(root/'docs/QA13_REPRODUCCION.md').write_text('''# QA13: reproducción y alcance

Mesen usado: SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. ROM HF9: manifest.json. No se incluyen emulador/ROM. Usar una copia de SRAM y un perfil aislado por proceso. Los comandos siguientes se ejecutan desde la raíz del paquete; cada salida debe ser nueva.

## Evidencias sin emulador

`python3 qa13/verify_scope.py --runs evidence/qa13_runs --out qa13/revalidation.json`

122 comprobaciones, incluyendo metadatos y resultados de juego. No confundir este número con122 recorridos ni con revisión global. Las capturas se revisaron directamente y la lámina sólo recorta el pie del emulador y escala los píxeles al doble, sin redibujarlos.

## Ejemplos de ejecución

```sh
python3 build.py /ruta/JP.ws --out /ruta/build
python3 qa13/equipment_sorted/run_suite.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws evidence/qa13_fixtures/dungeon_baseline.mss out_equipment --mesen /ruta/perfil/Mesen --suite equipment --timeout 60
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws evidence/qa13_fixtures/d2_preboss.mss qa13/atla_stress.lua out_atla --mesen /ruta/perfil/Mesen --timeout 40
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws - qa13/cold_event_trace.lua out_cold99 --mesen /ruta/perfil/Mesen --timeout 40 --input-save evidence/qa13_fixtures/D3_to_99_coherent_digits.sav
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws out_cold99/checkpoint.mss qa13/telep_use.lua out_telep --mesen /ruta/perfil/Mesen --timeout 40
TARGET_FLOOR=30 python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws out_telep/checkpoint.mss qa13/elevator_caller.lua out_elevator30 --mesen /ruta/perfil/Mesen --timeout 40
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws out_elevator30/checkpoint.mss qa13/save_caller_trace.lua out_save30 --mesen /ruta/perfil/Mesen --timeout 40
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws - qa13/cold_event_trace.lua out_cold31 --mesen /ruta/perfil/Mesen --timeout 40 --input-save out_save30/native_save_after.sav
```

Repetir la entrada del ascensor con TARGET_FLOOR32/99 sólo cuando se necesite verificar un cambio nuevo. Los ensayos entregados ya los cubren. El control causal JP sustituye únicamente ROM y plan: elevator_causal_trace.lua reproduce el mapaA216 en30; elevator_cache_at_consumer.lua lo corrige a0000 mediante caché en RAM. Reutilizar el mismo checkpoint posterior a Telep. No interpretar elevator_cache_counterfactual.lua (escritura demasiado temprana) como un control exitoso.

El ascensor se inicia inyectando su contexto completo y el temporal de destino; la acción, mapa y retorno posteriores son nativos. Guardar se inicia mediante el guion de escalera1950; no se alcanzó esa escalera andando. Los comentarios viejos del plan capturado de Atla decían «no memory writes»: el cuerpo muestra la inyección de HP/bolsa, siempre documentada; la cabecera de la fuente reutilizable ya está corregida. El campo method de las corridas de equipamiento heredaba «single bag record»; el cuerpo, casos y capturas prueban bolsa18. La etiqueta del lanzador reutilizable se corrigió. Las copias ejecutadas y sus hashes se preservaron sin editarlos.

QA13_RUN_INDEX.json enlaza cada entrada por SHA256 a su fixture o checkpoint incluido, registra parámetros y separa los9 intentos descartados/diagnósticos de la evidencia aceptada. Un intento fallido del observador no es un bloqueo de la ROM. Los timeouts son límites del harness, no pruebas del fallo histórico.

Atla tiene HP1 y bolsa completa antes del rescate. d2_boss_assist.lua bajaHP del jefe y mantieneHP del jugador: combate asistido explícito. ending_progress.lua y post_ending_walk.lua continúan por botones. Ver límites en INFORME_ES.md.
''')
# Native evidence montage. Never synthesize gameplay pixels.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
sheet=Image.new('RGB',(960,1115),'#f2f0e7');draw=ImageDraw.Draw(sheet)
draw.text((18,15),'Chocobo HF9 · QA13 · PASS_SYNTHETIC',fill='#1b3027',font=font)
draw.text((18,48),'Capturas nativas · pruebas asistidas y límites en el informe',fill='#46544b',font=small)
items=[('JP: piso30 con mapa del99','q13_elevator_jp30/f03600.png'),('HF9: piso30 con mapa correcto','q13_elevator_caller30/f03600.png'),('Equipo maldito: Check, bolsa18','q13_equipment_sorted/slot00_9D_flags11_f1430.png'),('Atla: hito de rescate9E44','q13_atla_stress/event_9E44.png'),('Guardado30 → carga fría31','q13_elevator_cold31/f04300.png'),('Guardado32 → carga fría33','q13_elevator_cold33/f04300.png')]
for i,(title,source) in enumerate(items):
 x=18+(i%2)*478;y=85+(i//2)*330;draw.text((x,y),title,fill='#1b3027',font=small)
 image=Image.open(w/'runs'/source).crop((0,0,224,144)).resize((448,288),Image.Resampling.NEAREST);sheet.paste(image,(x,y+28))
draw.text((18,1080),'3 guardados nativos · 6 cargas exactas de2.516bytes · ROM/BPS sin cambios',fill='#46544b',font=small)
preview=delivery/'Chocobo_HF9_QA13_Evidencias.png';sheet.save(preview);shutil.copy2(preview,root/'evidence'/preview.name)
(root/'docs/QA13_SCRIPT_HASHES.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in sorted((root/'qa13').rglob('*')) if p.suffix in {'.py','.lua'}},indent=2)+'\n')
r=subprocess.run(['python3','qa13/verify_scope.py','--runs','evidence/qa13_runs','--out','qa13/packaged_validation.json'],cwd=root,text=True,capture_output=True);assert r.returncode==0,r.stdout+r.stderr
(root/'docs/QA13_PACKAGED_VERIFICATION.txt').write_text(r.stdout+r.stderr)
for p in root.rglob('__pycache__'):
 if p.is_dir():shutil.rmtree(p)
for p in root.rglob('*'):
 if p.is_file():assert p.suffix.lower() not in {'.ws','.wsc','.rom','.bios','.exe','.so'},p
manifest=root/'SHA256SUMS.txt';files=[p for p in sorted(root.rglob('*')) if p.is_file() and p!=manifest]
manifest.write_text(''.join(f'{sha(p)}  {p.relative_to(root)}\n' for p in files))
z=delivery/(root.name+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in sorted(root.rglob('*')):
  if p.is_file():out.write(p,Path(root.name)/p.relative_to(root))
with zipfile.ZipFile(z) as check:assert check.testzip() is None
artifacts=[z,delivery/'Informe_Chocobo_HF9_QA13_20261014.txt',preview]
info={'artifacts':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in artifacts], 'unchanged_bps':{'path':str(delivery/'Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps'),'sha256':sha(delivery/'Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps'),'existing_library_id':'libfile_3eff5efe8d7081918a2c8bc6414812cf'},'packaged_files':len(files)+1,'runs':len(index),'excluded_or_diagnostic':len(excluded)}
(w/'qa13/delivery_manifest.json').write_text(json.dumps(info,indent=2)+'\n')
(w/'qa13/upload_request.json').write_text(json.dumps({'uploads':[{'local_path':str(p),'purpose':'create_library_file','library_artifact_type':t} for p,t in zip(artifacts,['other','report','image'])]},indent=2)+'\n')
print(json.dumps(info,indent=2))
