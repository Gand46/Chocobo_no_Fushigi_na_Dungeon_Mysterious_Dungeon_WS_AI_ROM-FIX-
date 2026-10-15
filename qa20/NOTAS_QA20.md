# QA20 — validación visual/lingüística 2 de 5

Autoridad: fuentes completas HF14/QA19, ZIP SHA-256 0a6d7e96978db234f801a8bf8936a06f4872c8bb773212256878762912bc96e4. Se verificaron las 49.807 entradas del inventario recibido antes de editar. La autoridad de continuidad se adoptó sin atribuirle retrospectivamente una reconstrucción que no existía en sus metadatos.

Se revisaron 248 referencias G00–G05 de la partición V2 leyendo los glifos japoneses originales junto al inglés HF14, y el inglés final en el motor nativo. Hay 74 referencias corregidas; 242 obtienen PASS sintético acotado. Los seis casos restantes se leen pero no se aprueban en contexto: G00:M252–255 y G04:M033–034. Las escenas sintéticas usan un checkpoint de introducción de jefe como vehículo del motor, por lo que su fondo y personaje no identifican al hablante de cada mensaje.

## Método y lecturas

- audit_00.png…audit_24.png: comparación bilingüe estática del corpus completo. No se cuentan como sesiones japonesas de juego.
- baseline_contact_00.png…baseline_contact_12.png: lectura directa de HF14, incluidas pausas y final del mensaje.
- final_review_00.png…final_review_04.png y checked_review_00.png: lecturas directas de las frases corregidas, con ajustes posteriores registrados. Los nombres «final» de la tanda intermedia no convierten esa ROM diagnóstica en la entrega.
- release_G* contiene la nueva ejecución completa de las 248 referencias con el SHA de HF15. visual_readings.json identifica cada captura y su lectura directa o identidad exacta de píxeles con una captura ya leída. Los seis casos reservados siguen excluidos del PASS aunque alcancen el terminador.
- release_menu_empty, release_menu_saved, release_save_native y release_load_saved: arranque en frío sin/con SRAM, confirmación de carga, menú nativo de escalera/guardar y carga en frío del guardado recién generado. release_consumers_00/01 y release_load_saved.png documentan su lectura directa.

Los menús principales observados usan recursos getter (familias F00/F05), no los mensajes cortos de G16 forzados en V1. No se atribuye cobertura de consumidor a G16 por parecido del texto. G16:M000, G16:M003 y G16:M004 conservan la lectura sintética de V1, pero su consumidor propio sigue pendiente. La búsqueda de comandos directos 28 10 03 / 28 10 04 no halló coincidencias; esto no demuestra que el recurso sea inaccesible, pues puede seleccionarse mediante código o tablas. No se fuerza una conclusión de recurso sin uso. El guardado de esta fase prueba acceso al menú, regreso al juego y carga fría posterior; no sustituye los controles de integridad o interrupción históricos ni un nuevo ciclo exhaustivo de cargar/comparar 2516 bytes.

## Cambios

Se restauran relaciones causales, sujetos, matices de preocupación/curiosidad y textos omitidos. Ejemplos: maceta frente a planta, objetos/orbes, posesión del padre, el alcalde como causa de preocupación y la instrucción de mejorar/fusionar equipo. Se reparan palabras parcialmente ausentes que no provocaban un desbordamiento detectable. Cada razón concreta está en translations.json y linguistic_review.json.

Los 74 nuevos bloques se alojan en el banco 1B, intervalo 1B:DCD0–1B:EE88 exclusivo del final. Todo 1B:DCD0–1B:FFFF era FF en JP y HF14; la nueva escritura usa 4536 bytes. Se redirigen 74 punteros de 16 bits dentro del mismo banco. La diferencia real es de 4279 bytes, incluido checksum. Los textos anteriores permanecen conservados. No hay cambios de motor, tamaño, fuente compartida, gráficos del título, guardado o jugabilidad.

text_codec.py conserva los digrafos nativos y prefiere una media celda inicial a un hueco interno cuando falta un digrafo. No es un mapa universal certificado: cada frase nueva debe leerse visualmente. La única secuencia nominal especial es «Camilla's Dad»: C1 000E 007A 0198 0275 00C2 0005, tomada de los recursos previos G01:M021/G04:M031 y leída en los glifos existentes. カミラパパ designa al padre de Camilla, no a Camilla y su padre como dos sujetos. El resaltado se conserva mediante FFFA:6/0. El envoltorio usa un máximo de 13 celdas por línea, dos líneas y pausa/limpieza; no altera controles de variables porque no se reescriben recursos dinámicos.

## Reserva y continuidad

G00:M252–255 son textos de depuración/variables sin consumidor válido en esta prueba. G00:M255 descarta dos glifos no vacíos y sigue leyendo el buffer ajeno al llegar al límite de 2400 cuadros; no alcanza el terminador. Queda excluido. Las otras 247 referencias sí lo alcanzan, incluidas las 242 aprobadas. G04:M033–034 son recursos compuestos de forja con preguntas/precios que requieren su consumidor, no solo la ventana de dos líneas. G16:M073 sigue pendiente de la frase anfitriona (V1). preset32/F00:I053 conserva su reserva de alcance nativo (M2).

V3 conserva las 207 referencias previstas de G06 restante, G07, G08, G10 y G11. V4: 194 de G09. V5: 154 de G14 y revisión transversal/reservas. No se añade automáticamente una sexta validación. La aprobación global sigue abierta; el conteo de 886 referencias literales no cubre por sí solo todos los getters, menús, variables, gráficos o recorridos.

No se usó un segundo emulador, hardware físico ni segundo revisor independiente. El incidente eléctrico del cartucho queda fuera de la ROM. Las causas históricas no reproducidas permanecen con sus límites anteriores.

## Reproducción

build.py y src/corrections.json constituyen la reconstrucción acumulativa canónica desde JP limpio. qa20/rebuild_translation_edits.py reconstruye primero HF14 desde las recetas previas incorporadas y regenera las frases sin necesitar un ZIP histórico externo. Cambiar translations.json exige reintegrar sus edits y repetir la validación; no altera automáticamente el builder canónico.

Los scripts de exploración prepare_candidate.py/render_audit.py conservan las rutas de la sesión como procedencia. Para reconstrucción portable usar build.py, qa20/rebuild_translation_edits.py y qa20/verify_scope.py. Para repetir una sesión con una instalación compatible de Mesen: definir LAYOUT_OBSERVER con la ruta absoluta de qa20/layout_observer.lua, llamar qa20/run.py ROM CHECKPOINT PLAN SALIDA --mesen EJECUTABLE. El checkpoint de diálogo está incluido en evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss. Los planes exactos se conservan en evidence/qa20_runs/release_*/plan.lua. No ejecutar varias sesiones simultáneas con el mismo directorio de SRAM.

Las tandas baseline_, candidate_, final_ y checked_ son antecedentes diagnósticos o de lectura; release_* es la evidencia de ejecución sobre el binario distribuido. Dos intentos de localizar el checkpoint de guardado fallaron antes de ejecutar; no cuentan como pruebas. El archivo válido utilizado es evidence/qa13_runs/q13_equipment_checkpoint/fullbag_checked_checkpoint.mss.
