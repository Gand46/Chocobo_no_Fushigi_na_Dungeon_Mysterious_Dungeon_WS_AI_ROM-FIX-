# Continuación — autoridad HF15 / QA20 V2

Objetivo vigente: aprobación visual/lingüística global en cinco validaciones. V2 ejecutada con 248 lecturas bilingües, 74 referencias corregidas, 242 PASS sintéticos acotados y seis reservas. Global sigue abierto. Siguiente trabajo: V3, 207 referencias de la partición qa19/five_validation_plan.json. No repetir toda V1/V2 indiscriminadamente.

Partir de estas fuentes acumulativas HF15; validar .continuity antes de editar. build.py reconstruye desde JP CCAA4853. qa20/rebuild_translation_edits.py regenera las frases desde las recetas previas incorporadas. Leer README.md y qa20/NOTAS_QA20.md. La ROM final es 2189490744c44fb1f16f79216a4c861cb7e3ade185a86e4d05b556c1bf46dd43.

Reservas V2: G00:M252–255 (depuración/variables sin contexto coherente; M255 no termina en 2400 cuadros), G04:M033–034 (consumidores de forja). De V1/UI: G16:M000/M003/M004 aún no vinculados a consumidores propios; los menús probados usan getters, no esas etiquetas. G16:M073 requiere frase anfitriona; preset32/F00:I053 sigue sin caller válido. No inferir consumidor por texto parecido ni recurso sin uso por ausencia de una firma de script.

248 sesiones de diálogo sobre HF15: 247 terminadores alcanzados y un diagnóstico excluido. Cuatro sesiones UI adicionales; 252 en total. Sólo las 242 aprobadas están libres de descartes no vacíos y tienen lectura lingüística acotada. No usar exit=0 como PASS. Las imágenes finales son idénticas a lecturas directas previas o se leyeron directamente; visual_readings.json registra la procedencia. No hay segundo revisor.

Se ocupó 1B:DCD0–1B:EE87, 4536 bytes de área FF verificada. Nuevo fin libre 1B:EE88; verificar otra vez antes de futuras escrituras. 74 punteros del mismo banco modificados; no se cambió código o fuente. El generador del codec sigue siendo parcial; cada frase nueva exige lectura nativa, especialmente medias celdas. «Camilla's Dad» usa una secuencia ya existente; no es «Camilla and her dad».

Checkpoints: diálogo evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss; guardado evidence/qa13_runs/q13_equipment_checkpoint/fullbag_checked_checkpoint.mss. Planes exactos en evidence/qa20_runs/release_*/plan.lua. Una instancia de Mesen a la vez. Reanudar desde evidencia release_*, no desde el nombre engañoso final_* de una tanda diagnóstica.

V3 conserva sus 207 referencias; V4 194, V5 154 más transversal/reservas. No añadir automáticamente una sexta fase ni declarar aprobación universal. Los PASS sintéticos autorizados no prueban hardware o ruta natural. Mantener entrega de fuentes completas acumulativas + BPS directo JP + evidencia, sin ROM. Límite de emergencia: 40 minutos por turno; preservar checkpoint antes de cortar.
