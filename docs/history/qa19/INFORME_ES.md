# Chocobo English v1.1 HF14 TEST — QA19, validación 1/5

Validación 1/5 ejecutada con una reserva de contexto. 83 referencias revisadas, 36 corregidas, 82 con aprobación lingüística acotada y G16:M073 pendiente de su frase anfitriona. El estado global continúa TEST, sin aprobación visual/lingüística universal.

## Resultado comprobado

- 84 sesiones sintéticas nativas: 83 mensajes y el consumidor de Slot Points de una línea.
- 20666 fotogramas; 101 lecturas visuales verificables; 1353 comprobaciones automáticas de integridad y alcance.
- 11 pruebas del proyecto aprobadas. Los 259 controles históricos QA18 se verifican sobre HF13 preservado, no se presentan como pruebas nuevas sobre HF14.
- 0 glifos no vacíos descartados en las sesiones aprobadas; 1 descarte de relleno vacío.
- BPS reconstruido y aplicado con implementación independiente: igualdad exacta con HF14.
- Regenerador editable de las traducciones: produce la misma ROM y el mismo archivo de cambios.

## Correcciones relevantes

| Referencia | Corrección |
|---|---|
| G16:M004 | Sesión anterior terminada anormalmente; elimina la afirmación incorrecta de corrupción de datos. No identifica una causa de pérdida de guardado. |
| G16:M012–015, M020–024, M049–050 | Restaura fuente, grado de recuperación y matices de los efectos; distingue recuperación completa de aumento del máximo. |
| G16:M032, M047–048 | Diferencia desprender equipo maldito de quitar la maldición; explicita garras equipadas y equipo desprendido. No modifica la lógica del equipamiento. |
| G16:M037, M039, M043–045 | Cansancio/desfallecimiento, bolsa llena y movimiento/fuerza; elimina texto defectuoso. |
| G16:M051, M061, M064, M066 | Conserva descenso, corrige pregunta de canje, cantidad de puntos y límite de capacidad. |
| G16:M070–071 | Completa recomendación y consejos de Nakamura, incluidos los regresos frecuentes con Teleport Card. |
| G06:M073 | Explica portada/conservar nivel y contraportada/reiniciar nivel, sin inventar una advertencia irreversible. |
| G06:M099 | El intercambio comienza normalmente en el capítulo 3; no se refiere a objetos del capítulo 3. Conserva el resaltado. |
| Otras referencias del registro | Etiquetas, naturalidad, puntuación y separación de palabras. |

Las 36 referencias incluyen equivalencias y alias: no se presentan como 36 causas funcionales distintas. El registro completo está en qa19/linguistic_review.json, con imágenes japonesas originales en qa19/audit_00.png…audit_08.png y capturas nativas finales en evidence/qa19_runs/release2_*.

## Alcance y reservas

La revisión japonesa se realizó leyendo los glifos de la ROM original; el inglés final se leyó en capturas del motor nativo. Las capturas japonesas estáticas no se cuentan como sesiones de juego. Una sola revisión del asistente; no existe aprobación independiente de otra persona.

La selección de mensajes se fuerza desde un savestate. Para cinco referencias dinámicas se inyectó el nombre largo Double KnockTalon y, cuando corresponde, 65535. Esto demuestra el renderizado del caso probado, no todos los valores, consumidores o recorridos naturales. Slot Points también se ejecutó mediante su script y ventana de una línea. El resto de menús reales, en particular New Game/Unused/aviso de sesión, entra en V2.

G16:M073 mantiene «floors or so»: la referencia japonesa contiene un matiz temporal posterior. Falta localizar y leer la frase compuesta antes de decidir la traducción final. No obtiene PASS lingüístico completo.

El candidato heredado preset32/F00:I053 sigue sin consumidor válido confirmado; no se modifica basándose solo en la segunda página forzada. Las causas históricas de equipamiento, Atla y reset del guardado conservan sus límites anteriores; esta fase no reabre ni resuelve esas causas. Las pruebas sintéticas previas siguen documentadas. El incidente eléctrico del cartucho queda fuera de la ROM.

## Cinco validaciones

| Validación | Referencias literales | Alcance principal |
|---|---:|---|
| V1 | 83 | G16 + G06:M073/M099; ejecutada, con reserva G16:M073. |
| V2 | 248 | G00–G05 y consumidores reales de menús/guardado. |
| V3 | 207 | Resto de G06, G07, G08, G10, G11; léxico de objetos y variables. |
| V4 | 194 | G09; diálogos extensos y opciones. |
| V5 | 154 | G14; revisión transversal, gráficos/créditos y reservas. |

La partición suma las 886 referencias de historia con texto literal. El inventario contiene además 2421 referencias no vacías solo de control, 2333 entradas getter, 141 presets y 79 geometrías. Los gráficos y todos los consumidores getter no quedan aprobados por sumar estas cinco filas. El cierre global dependerá de los hallazgos y su evidencia, sin añadir automáticamente otra iteración.

## Reconstrucción

Aplicar Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps directamente a una copia limpia japonesa CRC32 CCAA4853. No aplicar sobre una ROM inglesa o previamente parcheada.

```bash
python3 build.py '/ruta/Chocobo_JP.ws' --out '/ruta/salida_hf14'
python3 qa19/verify_scope.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/qa19_resultado.json'
python3 -m unittest discover -s tests -v
```

Para regenerar las frases editables:

```bash
python3 qa19/rebuild_translation_edits.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/generado_qa19'
```

qa19/translations.json contiene las páginas y líneas; text_codec.py contiene el mapa parcial de digrafos. El mapa no certifica automáticamente cualquier frase futura: cada nueva frase requiere lectura visual. El generador parte del HF13 preservado y produce candidate.ws, edits.json y allocations.json fuera del paquete. build.py es la reconstrucción acumulativa canónica basada en src/corrections.json. Para introducir cambios posteriores hay que integrar explícitamente los nuevos edits y volver a validar; editar translations.json por sí solo no altera el BPS.

## Integridad y conservación

Se usan 31 bloques nuevos deduplicados, 1416 bytes del intervalo libre verificado 06:E000–06:FF00 y 36 redirecciones dentro del mismo banco. Cambian 1355 bytes respecto a HF13, incluidos los 2 del checksum. No cambia el tamaño de ROM ni el bloque de fuente; no se modifica código de juego. Los textos anteriores quedan preservados en sus ubicaciones. El analizador de inventario ahora usa el límite verificado de 256 entradas de G16, porque su primer texto ya no marca el final físico de la tabla después de reubicarlo.

- SHA-256 ROM japonesa: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
- SHA-256 ROM HF14: 056c7fa5eec4779ce7c21a07b640fbf7e32c4cc326bd2d462259f80390248a7c
- CRC32 HF14: A66CF44F; checksum WS: 5693.
- SHA-256 BPS: 9ff11440f51e52792ad4bd531f3853347cb71e00442bf249e82fe71839dda7df

Paquete acumulativo con fuentes editables reconstruidas, historial, planes, checkpoints, lecturas y evidencia. No contiene ROM comercial ni BIOS. Las fuentes no son el código original del juego. Solo release2_* se admite como evidencia final QA19; 416 sesiones anteriores son diagnósticas y quedan excluidas, incluso las que finalizaron con código 0. Algunas candidate_* mezclaron un archivo candidato modificado durante la tanda: sus hashes no sirven como prueba de versión. Se conservan sus registros y capturas para transparencia; los dumps y checkpoints completos se conservan para las 84 sesiones finales.
