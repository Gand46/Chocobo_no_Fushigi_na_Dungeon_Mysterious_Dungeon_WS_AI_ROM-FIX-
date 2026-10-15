CHOCOBO — HF6 TEST / QA9 — 14 de octubre de 2026

Se incorpora una corrección de la caché decimal del piso. Reproduce y corrige dos resultados concretos: el bucle de carga de F99 con caché desactualizada y la asignación de un mapa de jefe a F30 al reconstruir la entrada con el estado dejado por Telep desde F99. La versión sigue siendo TEST; no es una aprobación global.

RESULTADOS Y PENDIENTES

• Pisos/ascensor: corregida la consulta de dígitos obsoletos en los selectores de D3. Doce destinos sintéticos —11,22,33,44,55,66,77,88,98,99,100 y30— alcanzan una escena de piso. No todos son pisos de jefe: el código nativo omite el evento de77. La entrada continua por el ascensor todavía no queda aprobada.
• Telep99→30: se ejecutó Use con Telep Card0B en F99 y se regresó al pueblo. Con ese bloque vivo se preparó una reentrada sintética a30 y se utilizó el cargador nativo. HF5 asigna el estado de mapa A217; HF6 asigna0000 y muestra un piso ordinario. Es PASS sintético de la reconstrucción y de la asignación del mapa. No equivale a recorrer el ascensor de forma continua ni demuestra el congelamiento posterior al caminar citado en el foro.
• Fuente/rana: mapeados los contadores7514/7515 y flags54..59. Se probaron dos configuraciones coherentes antes del final:15 Geyser+5 Frog y45 Geyser+15 Frog, con sus flags acumulados. Ambas completan E0:ABE2 en HF5; la variante completa también lo hace en HF6 y en el control JP. Se conserva evidencia de control posterior. No se ha reproducido el bloqueo del foro ni aplicado un parche especulativo a esta escena.
• Maquetación global: se revisó visualmente el selector de piso y se conserva el censo previo de2.333 entradas / 19 familias. No se detectó un nuevo defecto de maquetación en esa pantalla. Continúa pendiente revisar globalmente diálogos, tiendas, eventos y créditos en sus consumidores reales.
• Título: permanece japonés. Los411 tiles nativos y su cargador siguen identificados; falta diseñar e integrar el arte inglés respetando el estilo del logotipo. Esta versión no sustituye el título por una fuente genérica.
• Equipamiento: no se ha reproducido la causa del bloqueo; siguen vigentes los ensayos acotados anteriores. No se añade un fix de equipamiento sin un disparador demostrado.
• Atla: el rescate exacto del testimonio continúa sin validar. La fuente Yahoo no pudo consultarse de nuevo. Las escenas ya completadas no se renombran como prueba de ese incidente.

CAUSA Y CAMBIO CONCRETO

El piso autoritativo reside en7303 y sus cinco dígitos decimales en753A..753E. El selector de eventos consulta estos últimos. Si pertenecen a otro piso, puede omitir un mapa especial o seleccionar uno ajeno. En la carga sintética de F99 con caché61, omite el evento y llega a148393: solicita una colocación aleatoria hasta que4B54 sea distinto de cero. La probabilidad0647 vale cero;1EEAFB rechaza cada intento. La copia del guardado, en cambio, ya había concluido íntegramente.

HF6 recalcula los dígitos mediante la rutina original9000:6E1C solo cuando el opcode34 lee753A..753E dentro de los selectores E1:639C..69FF. El gancho está en14D398 y el código nuevo en14FDA8..14FDD9. Preserva registros y flags, vuelve al consumidor nativo y deja intactos los valores temporales del menú del ascensor. No fuerza la probabilidad del mapa, no inventa un evento y no salta las escenas.

Hay53 bytes distintos frente a HF5:51 de contenido y2 de checksum. Se conservan acumulativamente los arreglos de texto, Whistle, Lafoss y protección del guardado de HF1–HF5.

VALIDACIÓN BASADA EN DATOS Y LÍMITES

Las pruebas distinguen adquisición/preparación sintética de ejecución nativa. Las fixtures antiguas modificaban el número de piso conservando la caché61 de otro contexto. Esto explica sus pantallas blancas; por sí solo no demuestra que una partida natural produzca esa incoherencia. Un control nuevo coloca una escalera junto al personaje de F98 y el juego ejecuta Save and go on. El guardado nativo contiene piso98/caché98 y carga correctamente F99 tanto con HF5 como con HF6. Por tanto, no se presenta ese caso como una corrupción del guardado original.

En la prueba de Telep, la salida99→pueblo es nativa, con una carta inyectada en la bolsa. La reentrada utiliza el bloque realmente dejado en el pueblo, conservando su caché99; se cambia D3 y piso29 en el contenedor guardado para que el cargador entre a30. Cambian el contenedor y esos campos, no se falsifica una pulsación del ascensor. La diferencia A217→0000 demuestra el efecto de la corrección en ese estado; la ruta continua sigue pendiente.

Los intentos de invocar directamente los guiones del ascensor se conservaron como diagnósticos incompletos y se excluyeron del PASS. También se excluye como corrección la sonda que cambiaba0647a1: liberaba el bucle, pero no garantizaba recuperar el mapa previsto. Las primeras hipótesis de flags4D/12 no correspondían a fuente/rana.

Build directo desde JP, checksum, aplicador BPS independiente, consistencia histórica de recursos y11 pruebas de infraestructura: PASS. QA9_VERIFICATION.json comprueba los offsets permitidos, los destinos, los estados de mapa y las copias nativas exactas de2.516 bytes. Segundo emulador, hardware y recorrido natural completo no están aprobados. El bloqueo eléctrico del cartucho permanece cerrado y fuera del alcance de esta corrección.

APLICACIÓN

Aplicar Chocobo_EN_v1.1_HF6_TEST_JP_CCAA4853.bps directamente a la ROM japonesa limpia CRC32 CCAA4853, sin encadenar HF5. Los fuentes reconstruidos son editables y acumulativos; no son el código fuente original del juego. No se incluyen ROM ni BIOS.

HF6 conserva el formato de guardado protegido HF4/HF5. Para volver a una revisión anterior aHF4, exportar una copia con tools/chocobo_save.py --export-legacy; no sobrescribir el guardado de trabajo. La protección rechaza bloques incompletos y no recupera automáticamente una generación sobrescrita.

FUENTES EXTERNAS DEL CASO

Los siguientes enlaces son testimonios, no pruebas de causalidad del código:
https://wazap.com/cheat/セーブデータ破損？バグ/570082/ — pisos y comentario2729953 de Telep99→30.
https://wazap.com/cheat/クリア不能バグと対処法/570080/ — fuente/rana antes del segundo final.
https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14305291199 — referencia retrospectiva de Atla; inaccesible en esta revisión.
Chat compartido revisado en QA6: https://chatgpt.com/share/6acebdec-2b5c-83e9-833e-60560c52d788

IDENTIFICACIÓN
JP SHA256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF6 SHA256: 87ecaab08786651ee9431d6e386b0b73147e759aee282c053f6a75249e820d73
HF6 CRC32: 37109106; checksum WS: EBA8
BPS SHA256: a92cf352b84318ffb7f0c168ea7515da961cd044589500169e9db92e384be418
