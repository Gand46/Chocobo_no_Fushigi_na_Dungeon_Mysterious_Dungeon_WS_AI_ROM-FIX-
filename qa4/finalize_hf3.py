from pathlib import Path
import json,shutil,csv,hashlib,zlib
R=Path('delivery/Chocobo_EN_v1.1_HF3_TEST_Fuentes_QA_20261013');old=Path('delivery/Chocobo_EN_v1.1_HF2_TEST_Fuentes_QA_20261013');D=Path('delivery')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
patch=Path('private_roms/hf3_build/Chocobo_EN_v1.1_HF3_TEST_JP_CCAA4853.bps')
shutil.move(R/'patches/Chocobo_EN_v1.1_HF2_TEST_JP_CCAA4853.bps',R/'patches/historical/Chocobo_EN_v1.1_HF2_TEST_JP_CCAA4853.bps')
shutil.copy2(patch,R/'patches'/patch.name);shutil.copy2(patch,D/patch.name)
shutil.copy2('private_roms/hf3_build/build_result.json',R/'docs/build_result_hf3.json')
m=json.loads((R/'manifest.json').read_text());m['bps_sha256']=sha(patch);m['native_save_load']='PASS_BASIC_COLD_BOOT_MESEN_HF3';(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
# Current evidence and explicit provenance. Exclude malformed pre-render PNGs.
selected=['q4_whistle_resource_trace2','q4_whistle_palette_trace','q4_whistle_hf2_validation','q4_whistle_hf3_validation','q4_lafoss_hf3','q4_lafoss_origin','q4_flare_hf3','q4_hf3_save','q4_hf3_cold','q4_hf3_dispel_before','q4_hf3_dispel_after']
E=R/'evidence/qa4';E.mkdir(exist_ok=True)
for n in selected:shutil.copytree(Path('runs')/n,E/n,ignore=shutil.ignore_patterns('loaded.png','f00001.png'))
for suite in ['equipment','resources']:shutil.copytree(Path('runs')/f'q4_hf3_{suite}',R/'evidence/runs'/f'HF3_TEST_{suite}')
native=E/'q4_hf3_save/native_save';native.mkdir();sav=Path('profiles/q3_cold/Saves/Chocobo_EN_v1.1_HF3_TEST.sav');shutil.copy2(sav,native/sav.name)
shutil.copy2(D/'Chocobo_HF3_Silbato_20261013.png',R/'evidence/Chocobo_HF3_Silbato_20261013.png')
shutil.copy2('runs/q4_transitions.png',E/'transition_frames_638_642.png')
for n in ['whistle_comparison.json','whistle_asset_check.json','whistle_edits.json']:shutil.copy2(Path('qa4')/n,R/'docs'/n)
# Editable generator; the historical probe entry point remains in qa4 for exact provenance.
shutil.copy2('qa4/generate_whistle_fix.py',R/'tools/generate_whistle_fix.py')
p=R/'tools/generate_whistle_fix.py';s=p.read_text();s=s[:s.index("if __name__=='__main__':")]+'''if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description="Regenerate the four HF3 Whistle edits from the pinned HF2 image")
 p.add_argument('hf2_rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 edits,report=generate(a.hf2_rom.read_bytes());a.out.write_text(json.dumps(edits,indent=2)+'\\n');print(json.dumps(report,indent=2))
''';p.write_text(s)
# Update trace verifier to preserve each historical ROM identity.
p=R/'tools/verify_evidence.py';s=p.read_text().replace("if not e['id'].startswith('LAFOSS_')","if not e['id'].startswith(('LAFOSS_', 'WHISTLE_'))")
s=s.replace("variants={'JP':jp,'EN_v1.1':bytes(en),'HF1_TEST':bytes(hf1),'HF2_TEST':hf}","hf2=bytearray(en)\n    replace_checked(hf2,[e for e in load_json('src/corrections.json')['edits'] if not e['id'].startswith('WHISTLE_')])\n    hf2[-2:]=(sum(hf2[:-2])&65535).to_bytes(2,'little')\n    variants={'JP':jp,'EN_v1.1':bytes(en),'HF1_TEST':bytes(hf1),'HF2_TEST':bytes(hf2),'HF3_TEST':hf}")
s=s.replace('patches/Chocobo_EN_v1.1_HF2_TEST_JP_CCAA4853.bps','patches/Chocobo_EN_v1.1_HF3_TEST_JP_CCAA4853.bps');p.write_text(s)
p=R/'tests/test_project.py';p.write_text(p.read_text().replace("m['changed_bytes_vs_english'],93","m['changed_bytes_vs_english'],826"))
# Refresh exact runtime scripts after their last executed edit.
for p in Path('qa4').iterdir():
 if p.is_file() and p.suffix in ['.py','.lua','.json']:shutil.copy2(p,R/'qa4'/p.name)
issues=[
('TR-01','PARTIAL_HF1_PRESERVED','10 corrected resources rerun on HF3; script-wide layout unapproved'),
('TR-02','FIXED_SYNTHETIC_HF3','Whistle missing tile and palette aliases repaired; 2399 frame comparison; native menu with injected inventory'),
('TR-03','UNCHANGED_JAPANESE','Title remains untranslated'),
('EN-01','NOT_REPRODUCED_BOUNDED','30 HF3 native equipment actions; no freeze; advanced save scenarios remain untested'),
('EN-02','GUARD_PASSES_FULL_EFFECT_PENDING','HF3 consumes Lafoss and continues; original selector returns absent model FFFF; damage and missing animation not restored'),
('EN-03','NOT_REPRODUCED_BOUNDED','HF3 Dispel before/after cursed native equip works; artificial acquisition; curse remains and equipment removed'),
('JP-01','NOT_VALIDATED','Event floor/elevator save scenario needs a traceable pre-event checkpoint; basic cold load passed only'),
('JP-02','NOT_VALIDATED','Second dungeon ending needs traceable pre-ending progress'),
('JP-03','NOT_VALIDATED','99 to 30 teleport route needs traceable floor-99 checkpoint'),
('JP-04','NOT_VALIDATED','Atla rescue needs traceable pre-rescue checkpoint'),
('HW-USER','CLOSED_OUT_OF_ROM_SCOPE','User established electrical cause of physical cartridge freeze; not a ROM diagnosis target')]
with (R/'docs/issue_register.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['id','status','scope']);w.writerows(issues)
(R/'docs/issue_register.json').write_text(json.dumps([dict(zip(['id','status','scope'],r))for r in issues],indent=2)+'\n')
gates={'version':'HF3_TEST','build':'PASS','bps_roundtrip':'PASS','independent_bps':'PENDING_FINAL_VERIFICATION','checksum':'PASS','lafoss_no_hang_synthetic':'PASS','lafoss_full_spell_semantics':'NOT_VALIDATED','whistle_visual':'PASS_BOUNDED_MESEN_SYNTHETIC_INVENTORY','whistle_transition_difference':'3_FRAMES_REVIEWED_RECORDED','basic_cold_save_load_mesen':'PASS','late_event_save_integrity':'NOT_VALIDATED','second_emulator':'NOT_VALIDATED','hardware':'NOT_VALIDATED','physical_incident':'ELECTRICAL_CAUSE_ESTABLISHED_OUT_OF_SCOPE','global_linguistic_visual':'NOT_VALIDATED','final_approved':False}
(R/'docs/quality_gates.json').write_text(json.dumps(gates,indent=2)+'\n')
prov={n:json.loads((E/n/'run.json').read_text())for n in selected}
prov['cold_save_chain']={'file':'evidence/qa4/q4_hf3_save/native_save/'+sav.name,'sha256':sha(sav),'save_process':'q4_hf3_save','new_process_without_savestate':'q4_hf3_cold','save_origin':'HF1 save prompt checkpoint then native save action on HF3','not_an_independent_full_playthrough':True}
(R/'evidence/qa4_provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
report='''# Chocobo WonderSwan — HF3 TEST, 13 de octubre de 2026

El bloqueo del cartucho físico queda cerrado fuera del alcance de ROM: el usuario confirmó una causa eléctrica distinta. Esta fase se centra en los defectos de la ROM japonesa y su traducción inglesa. No se atribuyen las fotografías físicas a un fallo del parche.

## Resultado nuevo

Se reparó el silbato (TR-02). La ROM japonesa carga 37 tiles del gráfico, pero su mapa referencia el tile 38 en 18 celdas. La zona sin cargar conserva un glifo del menú, por eso el residuo cambia entre japonés e inglés. La fuente comprimida está en ROM 105B76 (592 bytes descomprimidos); el mapa está en 130C48 (2048 bytes). La traza real confirma esos punteros y la escritura de 3800 hasta 3A4F, dejando 3A50 con texto.

La reparación conserva íntegros los tiles 0–36. Añade tres tiles de color uniforme: índices 37/38/39 con píxeles 2/1/3. Las 18 celdas usan seis veces el color 2, ocho el 1 y cuatro el 3. Esto no es una elección artística: las paletas originales [5,1,3,6], [5,6,1,3], [5,3,6,1] y los bordes vecinos demuestran las equivalencias del color 2. Se incorporan esas equivalencias al gráfico porque la rutina nativa 5000:4935 sustituye la paleta de todo el mapa durante la animación.

Recursos nuevos: 333 bytes en 10C800 y 419 en 13FC60, ambos en relleno FF comprobado del mismo banco. Punteros 100078 y 130040 actualizados. No se cambia código ejecutable en HF3, ni la tipografía. Se mantienen todas las correcciones HF1 y la protección HF2.

## Validación efectuada

- Constructor desde la japonesa CCAA4853: resultado reproducible, checksum correcto, cero offsets inesperados; BPS acumulativo original→HF3.
- Silbato: inventario inyectado, selección y uso mediante menú nativo, mismo estado de mazmorra HF1. Se comparan 2399 capturas decodificables (fotogramas 2–2400); 2204 son idénticas. En 192 las diferencias quedan dentro de las 18 celdas reparadas. Tres fotogramas (638–640) muestran diferencias de transición de carga fuera de esas celdas; se revisaron y conservan en evidencia. No se afirma identidad temporal absoluta. Se excluye el primer PNG inválido anterior al primer render del emulador.
- RAM en fotograma 720: los 37 tiles originales son idénticos; los tres nuevos contienen los colores esperados; las diferencias del mapa se restringen a las 18 celdas. El silbato se consume y el juego vuelve a responder a las acciones.
- Lafoss y Flare: consumidos mediante menú; el mundo continúa y responde al movimiento. La protección Lafoss no reconstruye su animación o potencia completa.
- Lafoss: nueva traza localiza el origen en 4000:226C. El selector de modelo usa el ID FF de SRAM 6B14 y devuelve FFFF desde la tabla 14229F antes de llamar al dibujado desde 4000:2252. Es una ausencia en la selección gráfica original, no un glifo de traducción. No se sustituye por Flare ni se inventan daños.
- DispelDrink: las dos órdenes, adquirido antes y después de equipar la montura maldita, funcionan en HF3 bajo adquisición artificial. Equipo 09→01 y bebida 59→botella 64: se retira el equipo, permanece su maldición. La compra natural sigue sin comprobarse.
- Guardado básico: acción nativa en HF3 y carga del .sav en un proceso nuevo sin savestate; vuelve a la casa con HP 30/30 y permite moverse. No acredita guardado en eventos avanzados.
- 30 acciones nativas de equipo y diez recursos de texto reejecutados en HF3. Son pruebas acotadas con inventario sintético.

## Pendientes validados como abiertos

| ID | Estado al cierre |
|---|---|
| TR-01 | Diez recursos corregidos; falta revisar disposición y legibilidad del guion completo. |
| TR-02 | Reparado y validado en la secuencia de Mesen descrita; hardware y segundo emulador pendientes. |
| TR-03 | Pantalla de título sigue en japonés. |
| EN-01 | No reproducido en pruebas acotadas de equipo; no cerrado globalmente. |
| EN-02 | Protección contra bloqueo pasa; animación y semántica completa de Lafoss pendientes. |
| EN-03 | No reproducido en las dos órdenes sintéticas; adquisición natural pendiente. |
| JP-01 | Ascensor/pisos de evento/pantalla blanca: falta estado previo trazable y reproducción. |
| JP-02 | Final de segunda mazmorra: falta estado previo trazable y reproducción. |
| JP-03 | Teletransporte 99→30: falta ruta y estado previo trazable. |
| JP-04 | Rescate de Atla: falta estado previo trazable y reproducción. |
| HW-USER | Cerrado fuera del alcance de ROM por causa eléctrica confirmada por el usuario. |

El material disponible sólo acredita progreso temprano y guardado básico. No se convierten estados inventados de final de juego en pruebas de los eventos JP-01–04. La siguiente prioridad es obtener progreso trazable hasta esos eventos y revisar Lafoss desde el selector ya localizado. Esta entrega sigue siendo TEST, no RC ni traducción completa. Segundo emulador y hardware no validados.

## Aplicación y reproducción

Aplicar sólo `patches/Chocobo_EN_v1.1_HF3_TEST_JP_CCAA4853.bps` a la japonesa limpia de 2097152 bytes, CRC32 CCAA4853. No aplicar encima de HF1/HF2 ni de la traducción previa. Salida CRC32 302765E7, checksum A43B; SHA-256 en manifest.json. No se distribuye ROM comercial.

```sh
python3 build.py /ruta/JP.ws --out /ruta/salida_nueva
python3 -m unittest discover -s tests
python3 tools/verify_evidence.py /ruta/JP.ws
python3 tools/verify_independent_bps.py /ruta/JP.ws
```

Ejemplo de repetición del silbato: `python3 qa4/run.py /ruta/HF3.ws evidence/qa3/q3_dungeon/checkpoint.mss qa4/whistle_validation.lua salida_nueva --mesen /ruta/Mesen --timeout 25`.

Mesen 2.1.1 Linux x64: SHA-256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Los scripts exigen acceso Lua de I/O para escribir evidencia. Los estados y adquisiciones artificiales se identifican en qa4_provenance.json. Los informes previos quedan en docs/history/hf2; no sustituyen el alcance actualizado. Los registros históricos conservan los resultados anteriores para auditoría.
'''
(R/'INFORME_ES.md').write_text(report)
(D/'Informe_Chocobo_HF3_TEST_20261013.txt').write_text(report)
(R/'README.md').write_text('''# Chocobo English v1.1 + HF3 TEST

Cumulative reconstructed editable patch sources. Apply the current BPS directly to the clean Japanese ROM (CRC32 CCAA4853), never on top of an earlier translation/patch.

HF3 preserves the ten HF1 text fixes and HF2 invalid-model guard, and repairs the Whistle resource: complete solid tiles and normalize palette aliases. The original 37 graphic tiles and native font are unchanged. See INFORME_ES.md for evidence, reproduction commands and limitations.

Physical cartridge failure: the user established a separate electrical cause; it is outside this ROM audit.

TEST, not RC. Lafoss full animation/damage, title translation, global layout, advanced events, second emulator and hardware remain unvalidated. Current authority: manifest.json, src/corrections.json and docs/issue_register.csv. Historical reports are retained only as history.

Build: `python3 build.py /path/JP.ws --out /path/new_output`.
No commercial ROM is included. Full cumulative editable translation recipe, fixes, builder, BPS and QA evidence are included.
''')
(R/'CHANGELOG.md').write_text('''# HF3 TEST — 2026-10-13

- Repair original Whistle missing tile and palette aliases with same-bank resource relocation.
- Preserve HF1 text corrections and HF2 Lafoss invalid-model guard.
- Recheck 2399 Whistle frames, Lafoss/Flare, both Dispel orders, native save and cold load, 30 equipment actions and ten resources.
- Locate Lafoss model selector in the original ROM; complete spell semantics remain open.
- Close the physical-cartridge incident outside ROM scope per the user's established electrical cause.
- Keep event-floor/elevator, ending, teleport and Atla reports open pending traceable progress.

Earlier change logs: docs/history/hf2/CHANGELOG.md.
''')
(R/'CONTEXTO_CONTINUACION.md').write_text('''# Continuidad — HF3 TEST, 2026-10-13

Autoridad: manifest.json, INFORME_ES.md, docs/issue_register.csv y src/corrections.json. Original CCAA4853; HF3 302765E7 / SHA 85a8be61fdac2feb777ed1726235b46b36f8950265a1788e7d7c9a0bc90f4b11. BPS acumulativo original→HF3. No repetir HF1–3 ni afirmar RC.

El usuario estableció causa eléctrica del bloqueo físico. Cerrado fuera de ROM; no reabrir esa incertidumbre.

Silbato reparado: tiles0..36 preservados; tres sólidos2/1/3 agregados; normalización18celdas de paleta al píxel equivalente. Nuevos recursos10C800/13FC60, punteros100078/130040. 2399frames comparados, 2204idénticos,192sólo18celdas,3transición638–640 revisados. Recurso y modelo original demostrados por trazas. Ver docs/whistle_comparison.json, evidence/qa4.

Lafoss: protección HF2 conservada, nuevo origen del modeloFFFF en selector4000:226C, tablaROM14229F, itemSRAM6B14=FF, llamada4000:2252→5000:432C. No usar Flare sustituto ni declarar daño/animación completos. q4_lafoss_origin guarda pila. El efecto completo sigue abierto.

Dispel HF3 antes/después de equipar maldición: bebida59→64, equipo09→01; adquisición artificial. GuardadoHF3 nativo y carga en nuevo proceso sin savestate PASS básico. No extiende aprobación a eventos avanzados. Evidencia conserva estadoHF1 temprano de origen y cadena del .sav.

Pendientes: TR01 revisiónglobal, TR03título, EN01casosavanzados, EN02efectocompleto, EN03compranatural, JP01ascensor/eventos/guardado, JP02finalsegunda, JP03warp99→30, JP04Atla. Faltan estados de progreso trazable para JP01–04; no inventarlos ni marcar PASS. Segundo emulador/hardware siguen pendientes. Priorizar Lafoss y progreso avanzado comprobable. Corte universal40min, no bucles de navegación largos.

Arnés: conservar eliminación callback final ANTES de emu.stop; PNGloaded y frame1 pueden ser inválidos antes de primer render. La bolsa puede ignorar pulsos durante ataques. Comprobar selección real de objeto, no inferirla de los botones enviados.
''')
print('Prepared sources',m['target'])
