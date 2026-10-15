CHOCOBO — HF9 TEST / QA12 — 14 de octubre de 2026

Se corrigieron cuatro defectos visibles heredados de la traducción inglesa:
1. La propiedad contra no muertos mostraba «Skill Strong on dead o,af». Ahora usa «Skill Strong to Undead!», con los glifos ya empleados por ZombieKiller.
2. El ataque de tres direcciones mostraba «Skill3pronged hit o,af». Se termina la cadena después de «hit».
3. La propiedad de fuego de las sillas mostraba «Fire typeaf». Ahora coincide con «Fire type» de las garras.
4. La carta de sueño mostraba «Sleepel Card». Se quitó el glifo sobrante: «Sleep Card».

Los significados se contrastaron en la ROM japonesa mediante siete casos de control. Se conservan el logo entregado, animación, fuente, punteros, código de juego y fixes anteriores. HF9 modifica 19 bytes respecto de HF8: 17 bytes de texto y dos de checksum.

Validación y cobertura
Se exploraron 163 identificadores adicionales (01–64 y C1–FF) mediante inventario sintético y menú nativo: todos conservaron el objeto y regresaron del menú. Incluyen 125 nombres no vacíos y 38 vacíos; no se afirma que todos sean objetos obtenibles. Sumados a los 92 IDs revisados en QA10, cubren los IDs 01–FF en esas superficies, no todos los textos del juego.

Se identificó el registro nativo de propiedades fusionadas. La bandera 10 activa un registro de diez bytes vinculado al espacio de la bolsa; sus bytes 8/9 contienen códigos de propiedad. No se guardan en el campo auxiliar del objeto. Las familias 6 y 7 contienen 57 y 39 descripciones no nulas.

En el hash final HF9 se ejecutaron 49 parejas que cubren las 96 descripciones, más nueve casos dirigidos que incluyen los textos corregidos en ambas posiciones, la carta y dos equipos malditos con nivel -99. Todos terminaron sin apagar la CPU, conservaron el registro de inventario y regresaron al menú. No hubo cruces del límite en los cuatro puntos de copia vigilados ni escrituras en 175AC–17F8F. Son pruebas sintéticas con controles nativos; no son fusiones adquiridas jugando ni todas las combinaciones posibles.

Comparación de 147 capturas nativas HF8/HF9 de propiedades: 144 idénticas; las otras tres cambian únicamente en la línea corregida. Se revisaron las pantallas completas a resolución nativa. Censo de 2.333 recursos en 19 familias: sin candidatos que pierdan el terminador antes del siguiente slot; esto no aprueba su traducción ni maquetación global.

Build fijado a hash, aplicación BPS independiente y 11 pruebas existentes de infraestructura: PASS. Fuentes acumulativas y BPS directo desde la JP incluidos. Segundo emulador y hardware: sin validar.

Qué sigue abierto
• Maquetación y revisión lingüística global, especialmente diálogos, ventanas y variantes fuera de los menús examinados.
• Disparador histórico del bloqueo al consultar equipamiento. No se reprodujo con registros de propiedad válidos. Seis casos con los antiguos terminadores defectuosos de la traducción también regresaron; por eso no se presentan como causa confirmada del congelamiento.
• Obtención y combinación natural de equipo, inventarios completos y el estado exacto que falla en los reportes.
• Variante histórica de Atla: el rescate exacto D2F60 ya tiene PASS sintético acotado QA10; su congelamiento original continúa sin reproducirse.
• Ascensor continuo, ruta natural 99→30 y causa natural del reset del guardado. Se conservan los fixes y pases acotados anteriores.
• Revisión formal independiente de legibilidad del logo aportado. Su integración y fidelidad de píxeles siguen verificadas en QA11.

Se excluyen expresamente de la cobertura válida dos pruebas diagnósticas: un selector de menú inicialmente incorrecto y una primera construcción de propiedades que usaba IDs de objetos fuera del rango permitido. Esta última produjo desbordamientos artificiales y no demuestra un fallo alcanzable jugando. Los registros se conservan etiquetados para no confundirlos con un PASS ni con la causa del fallo histórico.

Identidad
JP SHA-256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF9 SHA-256: c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284
HF9 CRC32: 4CA9F7B4; checksum WS: E8BA.
BPS SHA-256: 3021df81f13b79e3b5ca5df86e65cadda6c886847e353493025b4052723ab950
Estado inicial de pruebas SHA-256: 2cb9e29b3749ce0caf9628ff93f8c5b52ebe5eb7212627175290a38d9adb5f82.
Entorno: Linux x86_64, Mesen 2.1.1. TEST, sin aprobación global ni causa histórica cerrada. Incidente físico eléctrico fuera del alcance ROM.
