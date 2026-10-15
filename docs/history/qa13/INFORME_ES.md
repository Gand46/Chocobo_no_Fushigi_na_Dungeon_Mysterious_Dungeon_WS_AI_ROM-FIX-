# QA13: validación sintética autorizada

Chocobo English v1.1 + HF9 TEST — revisión QA13
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
