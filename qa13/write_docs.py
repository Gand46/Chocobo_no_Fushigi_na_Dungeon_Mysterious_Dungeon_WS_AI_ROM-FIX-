from pathlib import Path
import shutil,json,csv,datetime,hashlib
w=Path.cwd();old=w/'delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA12_20261014';root=w/'delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA13_20261014'
shutil.copytree(old,root,dirs_exist_ok=False)
hist=root/'docs/history/hf9_qa12';hist.mkdir(parents=True)
for name in ['README.md','CONTEXTO_CONTINUACION.md','INFORME_ES.md','CHANGELOG.md','manifest.json']:
 if (root/name).exists():shutil.copy2(root/name,hist/name)
for name in ['issue_register.json','issue_register.csv','quality_gates.json','approval_matrix.json']:shutil.copy2(root/'docs'/name,hist/name)
report='''Chocobo English v1.1 + HF9 TEST — revisión QA13
14 de octubre de 2026. Pruebas sintéticas autorizadas por el usuario.

RESULTADO
Equipamiento, rescate de Atla, ascensor/99→30 y persistencia del guardado tienen PASS_SYNTHETIC en los escenarios descritos. Se cierra su requisito de acceso natural para esta aceptación. No equivale a haber identificado todos los fallos históricos: la causa del bloqueo de equipamiento, la condición exacta del testimonio de Atla y el reset espontáneo del guardado no se reprodujeron.

El mapa incorrecto de 99→30 sí se reprodujo en JP y tiene un control causal positivo. La corrección ya incorporada desde HF6 resuelve ese escenario en HF9. QA13 no cambia la ROM ni el BPS: es una ampliación verificable de evidencia, herramientas y estado de pendientes.

EQUIPAMIENTO — PASS_SYNTHETIC
Seis casos con 18 espacios ocupados: talon y saddle fusionados, nivel +99 o -99, malditos y sin identificar, entradas iniciales 0/8/17. El menú ordena la bolsa; el observador busca el ID después de ordenar para seleccionar el objeto correcto. Check y salida vuelven al campo (estado 0011); las 18 fichas permanecen. Cero cruces en los cuatro stores vigilados y cero escrituras en 175AC..17F8F. Los seis casos también pasan en JP y en la traducción inglesa de referencia. Esto amplía los 96 descriptores de QA12, sin atribuir el fallo histórico a un código no reproducido.
Tras Check, la bolsa completa se guarda mediante el menú nativo de escalera al que se entra sintéticamente. El guardado contiene los 2.516 bytes vivos exactos. Una ejecución nueva carga los mismos bytes, inventario y tabla completa de síntesis. La carga alcanza D1F2 y su diálogo nativo; no se presenta como recorrido natural completo de esa mazmorra.

ATLA — PASS_SYNTHETIC
Checkpoint anterior al rescate D2F60, con bolsa llena de equipo fusionado/maldito y HP=1. No se modifican las banderas de historia ni el puntero del rescate. Se observan los hitos E0:9A1C, 9D07 y 9E44 y la bandera18. La cadena HF9 continúa con combate expresamente asistido, créditos, pueblo y movimiento. El control JP también alcanza el hito y la bandera de rescate. La prueba cubre una variante de estrés declarada; no se conoce la combinación exacta del testimonio retrospectivo, por lo que no se denomina reproducción exacta de su fallo.

ASCENSOR Y 99→30 — PASS_SYNTHETIC; CAUSA DEL MAPA ERRÓNEO AISLADA
Cadena enlazada por estados: carga en frío de un guardado sintético coherente → F99 → Use nativo de TelepCard inyectada → pueblo → entrada sintética al llamador del ascensor → confirmación por botones → F30. No se fabrica un nuevo contenedor de guardado entre Telep y el ascensor.
El llamador real está en ROM1998D7: guion E0:13 (puntero2873), estado1FAE=0A, retorno1FB0=FE y1FB3=0. Los ensayos antiguos con estado05 omitían el retorno al controlador y no probaban la transición completa. El destino se escribe en el temporal060E; la confirmación, selector de eventos, mapa y retorno al juego son nativos. Hay acceso sintético y selección sintética: no es un recorrido desde partida nueva sin intervención.
HF9 alcanza F30/evento0000 y F32/evento0000; el ascensor a99 alcanza A216. Después de F30, 1.800 cuadros con pulsaciones de movimiento conservan el control (dos posiciones distintas y combate activo), sin escrituras al guardado.
Con la misma ROM JP y el mismo estado posterior a Telep, el ascensor a30 selecciona A216, el mapa especial del99. Un control adicional actualiza sólo los cinco dígitos de caché al leerlos en el selector: JP pasa a evento0000. La primera lectura registra caché98 con piso autoritativo29, antes del incremento al destino30. Son datos de etapas distintas. El fix HF6 existente refresca los dígitos precisamente en estos consumidores. Una actualización temprana al entrar en el menú es insuficiente porque los cálculos posteriores la reemplazan; ese intento queda como diagnóstico, no como PASS causal.
El mapa incorrecto JP admite movimiento durante el tramo observado; no se reprodujo el congelamiento posterior referido en el foro.

GUARDADO — PASS_SYNTHETIC DE INTEGRIDAD Y REINICIO
Tres escrituras nativas nuevas: bolsa fusionada en D1F1, D3F30 y D3F32. Cada una escribe exactamente2.516 bytes del bloque vivo; CRC, complemento y commitA5 quedan válidos. Tres procesos nuevos, sin savestate, realizan dos copias nativas exactas cada uno: seis comparaciones de2.516 bytes. Reanudan D1F2, D3F31 y D3F33/evento0010. F32→33 cubre guardar inmediatamente antes de un piso especial. El bloque persistente sigue idéntico tras cargar.
El control JP del mapa erróneo, tras1.800 cuadros, no escribe el guardado. Reiniciar con su SRAM conserva el bloque y carga F99 desde su guardado previo coherente. Por tanto, mapa erróneo no implica borrado en este escenario. No se identificó una causa natural universal de reset ni se recuperan datos ya sobrescritos. La protección HF4 frente a escritura parcial y corrupción conserva sus pruebas anteriores; no se recuentan como ejecuciones nuevas.

MÉTODO Y LÍMITES
Mesen fijado por SHA256; 122 comprobaciones automatizadas de evidencias, incluidas procedencia y hashes, además de inspección de capturas nativas. Un fin de proceso por sí solo no concede PASS. Se excluyen errores de selección, entradas incompletas de guion, escaleras inyectadas que no abrieron el menú y un fallo de dependencia del observador. Lista exacta en docs/QA13_RUN_INDEX.json.
Continúan abiertos: maquetación/lingüística global y revisión formal de glifos del logo aportado. Las causas históricas no reproducidas se conservan como investigación, sin exigir nuevamente acceso natural para aceptar estos casos sintéticos. No hay aprobación global, segundo emulador ni hardware.

IDENTIDAD Y ENTREGA
ROM HF9 SHA256 c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284
CRC32 4CA9F7B4; checksumWS E8BA.
BPS acumulativo sobre JP Rev2 CRC32 CCAA4853, SHA256 3021df81f13b79e3b5ca5df86e65cadda6c886847e353493025b4052723ab950.
El ZIP contiene fuentes acumulativas, BPS, observadores, estados/SRAM de prueba, capturas, trazas y verificador. No contiene ROM, BIOS ni emulador.

FUENTES HISTÓRICAS REVALIDADAS
Wazap, consultado14-10-2026: reporta fallos al guardar antes de pisos especiales o usar el ascensor; el comentario del20-06-2026 describe Telep99 y mapa especial al entrar en30, seguido de un bloqueo. Es testimonio, no prueba de corrupción binaria.
https://wazap.com/cheat/セーブデータ破損？バグ/570082/
RetroAchievements, consultado14-10-2026: advertencia de congelamiento seguido de pérdida de partida; sin SRAM ni pasos exactos en el hilo consultado.
https://retroachievements.org/forums/topic/14392
Yahoo q14305291199 no accesible mediante la consulta de esta fase; no se inventan detalles nuevos. Se conserva la revisión histórica existente.
https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14305291199
'''
(w/'delivery/Informe_Chocobo_HF9_QA13_20261014.txt').write_text(report)
(root/'INFORME_ES.md').write_text('# QA13: validación sintética autorizada\n\n'+report)
(root/'README.md').write_text('''# Chocobo English v1.1 + HF9 TEST · QA13

QA13 amplía pruebas y confirma el fix existente del mapa 99→30. **No cambia los bytes de HF9 ni su BPS.** Equipamiento, Atla, ascensor y guardado tienen PASS_SYNTHETIC en el alcance de `INFORME_ES.md`; sus causas históricas no reproducidas se identifican por separado.

Aplicar `patches/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps` directamente a JP Rev2 CRC32 `CCAA4853`, sin parches intermedios. No se distribuyen ROM, BIOS ni emulador.

Construir: `python3 build.py JP.ws --out build`. Python3, sin dependencias externas. BPS independiente: `python3 tools/verify_independent_bps.py JP.ws`.

Verificar esta revisión: `python3 qa13/verify_scope.py --runs evidence/qa13_runs --out qa13/revalidation.json`.

Reproducción en emulador y acceso sintético: `docs/QA13_REPRODUCCION.md`. Resultados y descartes: `docs/QA13_RUN_INDEX.json`; `docs/QA13_VALIDATION.json`. Pendientes vigentes: `docs/issue_register.json`. Historia completa preservada, incluidos QA12 y el logo aportado en `assets/title/user_v01`.

No se concede aprobación global de maquetación, lingüística, hardware ni glifos del logo. Los lanzadores Windows/macOS permanecen conservados, sin prueba nueva en esos sistemas.
''')
(root/'CONTEXTO_CONTINUACION.md').write_text('''# Continuación después de HF9 / QA13

Autoridad: manifest.json, docs/issue_register.json y docs/QA13_VALIDATION.json. ROM/BPS idénticos a HF9 QA12; hash final c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284. No crear HF10 sólo por esta revisión.

El usuario autorizó expresamente pruebas sintéticas y PASS_SYNTHETIC para los pendientes antes llamados naturales. Equipamiento, Atla, ascensor/99→30 y guardado tienen aceptación funcional sintética en el alcance documentado. No reabrirlos por falta de adquisición natural. Causas históricas de equipamiento, Atla y reset espontáneo siguen sin reproducirse; no presentarlas como fixes nuevos.

Equipamiento: bolsa nativa18, autoordenada al abrir; resolver ID después del ordenamiento. Seis casos idénticos en HF9/EN/JP regresan al campo0011, cero cruces en cuatro stores/cero escrituras175AC..17F8F. Tabla de fusión117x10 en6D3F; byte0=slot, bytes8/9=propiedades. Tres ciclos guardado/carga fría (equipo D1F1→2, D3F30→31 y32→33), seis copias exactas de2516bytes, commits válidos. No repetir pruebas de escritura parcial HF4 ya cerradas sin un riesgo nuevo.

Atla: bolsa llena de fusionados malditos y HP1, sin editar historia/puntero del rescate. Hitos9A1C/9D07/9E44 y bandera18; JP también alcanza el rescate. HF9: combate asistido→créditos→pueblo→movimiento. No conocemos condiciones exactas de Yahoo; no confundir variante de estrés con reproducción histórica exacta.

Hallazgo principal: llamador nativo de ascensor ROM1998D7 configura E013,1FAE0A,1FB0FE,1FB3=0. Estado05 era un observador incompleto. E0 corresponde al bancoROM00, NO1E. Cadena HF9 fría99→Telep→pueblo→ascensor sintético30 completa; mapa normal0000 y control. JP mismo estado seleccionaA216 (mapa99). Intervenir sólo caché753A..753E al consumidor4D39B corrige JP a0000. Primera lectura: piso29/caché98; el incremento posterior llega30. Fix HF6 ya incluido en HF9 resuelve esta causa. Una escritura de caché al entrar al menú se sobrescribe y NO constituye control causal válido.

JP caminó1800frames por el mapa erróneo y mantuvo guardado intacto; carga fría posterior vuelve99 con2516bytes exactos. No se reproduce el freeze posterior del foro ni borrado. Diferenciar selección de mapa de pérdida de datos.

El menú de escalera puede invocarse sintéticamente por E00A/puntero1950 con1FAE0A y1FB0FF; se pulsan Down/A para Save and go on. No presentar estas entradas como escaleras alcanzadas caminando. Los intentos de reubicar tile031D no abrieron el menú en estos estados y están excluidos. Crear savestates sólo desde callbackCPU, nunca directamente desde endFrame.

Pendientes fuera del alcance funcional aceptado: maquetación/lingüística global; revisión formal independiente de glifos del logo del usuario. No rediseñar el arte, no volver a HF7. Incidente de cartucho físico cerrado por causa eléctrica del usuario. Reproducción portable y estados incluidos en docs/QA13_REPRODUCCION.md y evidence/qa13_fixtures. No repetir inventarios ya cubiertos sin un caso nuevo.
''')
(root/'CHANGELOG.md').write_text('# QA13 · misma ROM HF9\n\nPruebas de bolsa llena, rescate de Atla bajo estrés, llamador completo del ascensor, cadena99→30, control causal JP de caché, tres nuevos ciclos de guardado/carga fría y estados PASS_SYNTHETIC autorizados. No hay edición binaria nueva. Historial de correcciones HF1–HF9 conservado en docs/history/.\n')
manifest=json.loads((root/'manifest.json').read_text());manifest.update(audit_revision='QA13_SYNTHETIC_CLOSURE_AND_ELEVATOR_CAUSAL_CONTROL',rom_changes_in_QA13=0,new_bps_required=False,native_save_load='PASS_SYNTHETIC_THREE_NEW_NATIVE_SAVE_COLD_LOAD_CYCLES_EXACT_2516_BYTES',natural_save_loss_trigger='NOT_REPRODUCED;SCOPED_SYNTHETIC_SAVE_INTEGRITY_PASS',equipment_freeze='PASS_SYNTHETIC_FULL_BAG_RETURN_AND_PERSISTENCE;HISTORICAL_CAUSE_NOT_REPRODUCED',atla_rescue='PASS_SYNTHETIC_FULL_BAG_LOW_HP_RESCUE_ASSISTED_BOSS_ENDING_VILLAGE',teleport99_to30='PASS_SYNTHETIC_LINKED_RUNTIME_CHAIN_NATIVE_ELEVATOR_RETURN',floor_map_cause='PASS_SYNTHETIC_JP_CACHE_CONSUMER_COUNTERFACTUAL',synthetic_acceptance_authorized=True)
(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
issues=json.loads((root/'docs/issue_register.json').read_text())
changes={
'EN-01':('PASS_SYNTHETIC','Six full-bag cases on HF9/EN/JP: sorted target resolution, fused/cursed/unidentified +/-99, native Check and field return, no watched overrun or persistent write. HF9 full bag and synthesis metadata survive native save/cold load.','NOT_REPRODUCED'),
'JP-01':('PASS_SYNTHETIC','Complete native elevator dispatch after synthetic caller entry; HF9 destinations30/32/99. Native save32 and cold load33/event0010 exact. Existing HF6 cache fix retained.','STALE_CACHE_MAP_SELECTION_REPRODUCED_SYNTHETICALLY;NATURAL_SAVE_ERASURE_NOT_REPRODUCED'),
'JP-03':('PASS_SYNTHETIC','Cold99 -> native Telep -> town -> synthetic elevator caller/destination -> native confirmation and floor30/event0000; bounded walking. JP selectsA216; cache refresh at consumer makes JP select0000. No intermediate saved-data reentry container.','STALE_CACHED_DIGITS_CAUSE_WRONG_MAP;POSTER_REPORTED_LATER_FREEZE_NOT_REPRODUCED'),
'JP-04':('PASS_SYNTHETIC','Full fused cursed bag and HP1 before exact D2 rescue, no story/pointer edits in rescue. Rescue flags pass on HF9/JP. HF9 assisted boss -> credits -> village movement. Stress variant, not proven identical to historical failing state.','HISTORICAL_TRIGGER_UNKNOWN'),
'SAVE-01':('PASS_SYNTHETIC','Three new HF9 native writes and fresh-process cold loads: six exact2516-byte copies, valid CRC/complement/commit, full inventory/synthesis retained. JP wrong-map traversal does not overwrite stored data and cold-restarts successfully. HF4 interruption evidence retained, not rerun.','NATURAL_RESET_NOT_REPRODUCED;PARTIAL_WRITE_ACCEPTANCE_FIXED_IN_HF4')}
for row in issues:
 if row['id'] in changes:
  status,scope,cause=changes[row['id']];row.update(status=status,scope=scope,functional_validation='PASS_SYNTHETIC',historical_cause=cause,acceptance='USER_AUTHORIZED_SYNTHETIC;NATURAL_ACCESS_NOT_REQUIRED_FOR_THIS_SCOPE',binary_change_in_QA13=False)
(root/'docs/issue_register.json').write_text(json.dumps(issues,indent=2)+'\n')
with (root/'docs/issue_register.csv').open('w',newline='') as f:
 keys=['id','status','scope','functional_validation','historical_cause','acceptance','binary_change_in_QA13'];wr=csv.DictWriter(f,fieldnames=keys);wr.writeheader();wr.writerows(issues)
g=json.loads((root/'docs/quality_gates.json').read_text());g.update(audit_revision='QA13',save_protected_normal_load='PASS_SYNTHETIC_THREE_NEW_HF9_SAVE_COLD_LOAD_CYCLES_2516_BYTES',natural_forum_save_reset_cause='NOT_REPRODUCED;FUNCTIONAL_SAVE_SCENARIOS_PASS_SYNTHETIC',teleport99_to30='PASS_SYNTHETIC_LINKED_RUNTIME_CHAIN_NO_INTERMEDIATE_SAVE_CONTAINER',actual_elevator_ui='PASS_SYNTHETIC_CALLER_AND_DESTINATION_WITH_NATIVE_CONFIRMATION_AND_RETURN',atla_rescue='PASS_SYNTHETIC_FULL_BAG_LOW_HP_RESCUE_ENDING_VILLAGE',equipment_cause='NOT_REPRODUCED;SIX_FULL_BAG_SCENARIOS_PASS_HF9_EN_JP',qa13_elevator_cause='PASS_SYNTHETIC_JP_CACHE_COUNTERFACTUAL',qa13_checks=122,qa13_binary_changes=0,final_approved=False)
(root/'docs/quality_gates.json').write_text(json.dumps(g,indent=2)+'\n')
ap=json.loads((root/'docs/approval_matrix.json').read_text());ap.update(scope='HF9 unchanged; QA13 authorized synthetic functional acceptance',FUNCTIONAL_APPROVED='PASS_SYNTHETIC_SCOPED_EQUIPMENT_ATLA_ELEVATOR_SAVE',historical_causes='ELEVATOR_WRONG_MAP_CACHE_CAUSE_SUPPORTED;EQUIPMENT_ATLA_NATURAL_SAVE_RESET_UNREPRODUCED',FINAL_APPROVED=False)
(root/'docs/approval_matrix.json').write_text(json.dumps(ap,indent=2)+'\n')
print(root)
