# Estado vigente — HF13 TEST / QA18 M4

Juego: Chocobo no Fushigi na Dungeon (WonderSwan). Japonés a inglés. M4/4 ejecutada; cero iteraciones base restantes, sin convertirlo en aprobación global.

Target SHA256 a6bb2ee9e1d973f92aa7eac1a158f2873cde185075fc8a3b042dbe1f1dcb303f; BPS SHA256 33a916387401d4ce329f7123bc503853290bbf5c516d24397f2f21473f0ac52d; JP CRC CCAA4853. Nunca tomar la base por fecha/nombre sin contrastar hash.

Nuevo: cinco recursos (qa18/edits.json),147 bytes de texto+2 de checksum. SlotPoints: entrada sintética al script E0:59B5, ventana1 de una línea, tres páginas con pausas; secuencia fo lot corregida con S/lo/t-space del mismo recurso. Cuatro mensajes adicionales con páginas/espaciado ajustados. Siete sesiones finales,7.500 cuadros,14 lecturas,259 comprobaciones. QA17 histórico revalidado790;11 unit tests PASS.

Pendientes reales: TR-01-M2-C01 preset32/F00:I053 (sin caller válido); revisión visual global de consumidores fuera de la matriz; TR-01-L lingüística. G06:M073 conserva una frase incompleta tras to: no aprobar semántica. M3 ya señaló G06:M099 yG16:M004. No repetir diagnóstico de cartucho físico ni convertir causas históricas desconocidas en bloqueos funcionales: los PASS sintéticos anteriores de equipamiento/Atla/ascensor/99→30/guardado siguen limitados a sus pruebas.

Fuentes y evidencia acumulativas: consultar qa18/coverage_summary.json,story_coverage.csv,context_resolution.json,gates.json,verification.json y docs/QA18_RUN_INDEX.json. Veintitrés diagnósticos excluidos; no usar pre_final ni candidate como evidencia de HF13 final. Los planes finales son los siete nombres final_* del índice.

Antes de continuar, recuperar este paquete completo y verificar manifest.json. No fabricar un nuevo BPS si no cambia la ROM. La cobertura de26 punteros de diálogo,12 ventanas/97bindings y9 referencias dinámicas es acotada: no afirmar que los886 diálogos literales y141presets fueron leídos en pantalla. Es posible seguir con otra etapa, pero no prometer una cantidad de iteraciones sin definir sus consumidores y casos.
