CH O C O B O — HF7 TEST / QA10 — 14 de octubre de 2026

Cambios reales
• Título traducido al inglés: CHOCOBO'S MYSTERY DUNGEON / FOR WONDERSWAN. Conserva el arte superior y los64tiles de animación. Se corrigieron la interferencia de la animación, el espaciado y la legibilidad de glifos pequeños detectadas durante QA.
• TitanSaddle: eliminada una w sobrante en el nombre mediante el terminador correcto, sin tocar la fuente ni el objeto.

Validación de los cuatro pendientes
Título: integrado y visible; animación,36glifos aislados y transición al menú revisados.
Maquetación: revisión acotada de92IDs de equipamiento (90objetos y2reservados), con trazas del consumidor real; TitanSaddle corregido. La maquetación global sigue pendiente.
Equipamiento:92consultas nativas Check y salida completadas. Ningún cruce en los dos stores vigilados ni escritura al bloque persistente. No se encontró el disparador del bloqueo histórico; no se añade un fix especulativo.
Atla: identificada y recorrida la escena previa al jefe deD2F60, E0:9A1C..9E4D, extracción/transformaciones9D07..9E0F y bandera18 en9E44. PASS sintético de esta ruta. Rescate sin pokes; combate posterior asistido, créditos, regreso y movimiento verificados. La variante exacta del testimonio de congelamiento sigue sin reproducirse y no se modificó su código.

Build
JP SHA256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF7 SHA256: 116cd3df2828e97c890049619f6f43bf10102490f0c709a3dc836ec54a6a065a
CRC32: 8BA15CB0; checksumWS: 241D.
Cambios frente aHF6: 3304 bytes, incluido checksum.
BPS SHA256: ff15284cbfc0512d972d82c59b52c35f3edbe2172578d128cf17f4a9c2d91017
BPS directo desde JP CCAA4853, reconstrucción reproducible, comparación exacta y aplicador independiente.11pruebas de infraestructura. Emulador Mesen2.1.1, Linuxx86_64. No prueba en hardware ni segundo emulador.

Límites y continuidad
Sigue siendo TEST. No hay aprobación global. Los92casos y la cadena Atla conservan el hash de su candidata; el último ajuste sólo cambia gráficos/mapas del título y checksum. La fuente y el código de esos consumidores permanecen idénticos; el paquete justifica esa reutilización y contiene pruebas finales de título/TitanSaddle.
No se reabrieron aquí ascensor/teletransporte/fuente-rana; sus límites deQA9 se mantienen. El fallo eléctrico del cartucho continúa cerrado fuera del alcance ROM.

Fuentes externas consultadas
https://retroachievements.org/game/16362 — testimonio de Chauckles sobre Check/equipamiento, sin objeto ni guardado preciso.
https://retroachievements.org/forums/topic/14392 — aviso general de congelamiento/guardado y revisiónJP.
https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14305291199 — inaccesible; se conserva la reseña histórica, no una nueva verificación.
https://sekaijyusaya.hatenablog.com/entry/2026/05/03/002434 — orientación narrativa deD2; imágenes dePS, no evidenciaWS.

Consultar docs/QA10_REPRODUCTION.md y QA10_RUN_INDEX.json para comandos, estados, hashes y exclusiones. Fuentes completas acumulativas; no contiene ROM, BIOS ni emulador. Ahorro de tokens: no medido.
