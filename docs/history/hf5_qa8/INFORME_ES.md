# Chocobo — HF5 TEST / QA8

Continuación del 14 de octubre de 2026, UTC. Traducción japonesa → inglés. Compilación experimental, no RC. Se incorporan tres correcciones concretas: proyectil de Lafoss, acceso al daño nativo de las dos últimas perlas y un terminador de texto adicional. Son seis bytes de contenido y un byte de checksum respecto a HF4.

## Estado de los ocho pendientes

| Frente | Resultado de esta iteración | Pendiente concreto |
|---|---|---|
| Maquetación global, TR-01 | Corregida una lectura fuera del espacio de una cadena. Censo de 2.333 entradas en 19 familias: un candidato antes, cero después | Aprobación visual del resto de diálogos, tiendas, créditos y eventos; el censo no cubre todo el guion ni mide anchura global |
| Título japonés, TR-03 | Identificados consumidor y 411 tiles nativos; extraídos los recursos editables | Diseñar e integrar el título inglés conservando el estilo original; sigue japonés |
| Equipamiento, EN-01 | Cuatro casos adicionales de descripción con bolsa de 18 objetos y nivel +99, incluido el último espacio, sin bloqueo ni escrituras persistentes observadas | Reproducir el disparador natural y determinar su causa; no hay fix nuevo de equipamiento |
| Lafoss, EN-02 | PASS sintético de la acción nativa Kick: proyectil, impacto de 1.000 puntos con defensa cero, muerte del enemigo, consumo y continuación | Otras combinaciones de combate, adquisición natural y hardware no están aprobados; el caso Kick reproducido sí queda corregido |
| Pisos/ascensor, JP-01 | Ampliados los pisos sintéticos. La carga del 99 queda blanca también en JP con la misma fixture mínima; el bloque de datos se copia íntegro | Aislar la condición de reconstrucción del evento y probar el ascensor real antes de modificar código |
| Segundo final y fuente/rana, JP-02 | PASS sintético de la ruta base: jefe asistido, créditos, escenas del pueblo y desplazamiento normal posterior | Comparar la ruta con la fuente limpia y la rana invocada antes de finalizar D2; ese fallo no queda corregido |
| Teletransporte 99→30, JP-03 | Identificada Telep Card, ID 0B; obtenidos estados D3 posteriores al segundo final, incluidos 98 y 30 | Conseguir el 99 por una transición trazable, usar Telep Card y regresar al 30; la secuencia exacta sigue sin validar |
| Rescate de Atla, JP-04 | Avanzada una secuencia de D1 F30 hasta volver al pueblo | Identificar y reproducir el rescate concreto; no se equipara cualquier escena de D1 al incidente de Atla |

## Correcciones implementadas

Lafoss tenía dos fallos distintos. El selector del proyectil enviaba el objeto FF a una entrada FFFF sin modelo. HF5 asigna el modelo de perla 0AF8 usado por los objetos vecinos. La comprobación exhaustiva de los 256 IDs demuestra que solo cambia FF. Se conserva la protección de HF2 como respaldo.

La rutina de daño excluía FE y FF mediante un límite superior FE. Sin embargo, el inicializador contempla las 16 perlas F0–FF y el juego ya contiene un cálculo de 1.000 puntos para FE/FF. HF5 amplía el límite a 100 hexadecimal: activa esa implementación existente, sin insertar un daño inventado. La traza pasa de un valor residual de 3 a 1.000; con defensa 200 aplica 800, y con defensa 2.000 aplica 1 según el código nativo. La prueba FE también pasa de 3 a 1.000. No se generaliza una cifra fija a todas las defensas.

La entrada 81 de la familia 0 había perdido FFFF. Se restaura dentro de sus ocho bytes originales. El consumidor ahora lee cuatro palabras, frente a cinco que alcanzaban la siguiente entrada. Las capturas son idénticas: se conserva la etiqueta visible «3». Es una corrección de límites, no una demostración de un desbordamiento visible.

## Validación y límites

Se ejecutó Mesen 2.1.1 en Linux. Las pruebas de inventario, recursos y eventos usan estados e inyecciones explícitas. El segundo final parte del estado D2 sintético de QA7; para superar el combate se redujo la vida del jefe a 1 y se mantuvo la del personaje en 500. Después se siguieron las escenas con entradas normales, sin saltar instrucciones del evento. Las capturas y cambios de guion documentan créditos, pueblo y movimiento posterior. Esto no valida todavía la variante fuente/rana descrita en el foro.

La fixture D3 antigua necesitaba la máscara 0080, no 8000, igual que D2. La corrección de esa fixture mejora la investigación y no es un cambio de ROM. Algunas pantallas blancas persisten; no se consideran prueba de corrupción del bloque guardado. Los estados con progreso insuficiente incluso devolvían el piso 30 al pueblo; al usar el progreso producido por el segundo final se carga un piso 30 visible. Por eso no se da por probada la causa del foro con una fixture incompleta.

HF5 conserva byte a byte el código de guardado HF4. Se realizó un guardado nativo nuevo y una carga en proceso nuevo: nivel 3, HP 28, los 2.516 bytes del bloque recuperados exactamente. Las matrices HF4 de 7.606 prefijos y 144 mutaciones se conservan como evidencia histórica del mismo código, no como pruebas repetidas en esta iteración. No hay recuperación automática del bloque anterior ni identificación de la causa natural de los resets.

Build directo desde JP, reaplicación con aplicador BPS independiente, checksum y 11 pruebas de infraestructura: PASS. El caso de equipamiento 93/espacio 9 seleccionó otro objeto y se excluye del conteo de cuatro casos válidos. La sonda Flare no alcanzó al enemigo y no cuenta como regresión de daño aprobada. Un primer intento de guardado apuntó a un archivo inexistente; se descarta y se sustituye por q8_save_final/q8_cold_saved.

La maquetación global, el título, fuente/rana, ascensor, teletransporte, Atla, segundo emulador y hardware siguen abiertos. El fallo eléctrico del cartucho permanece cerrado y fuera del alcance de la ROM.

## Aplicación y compatibilidad

Aplicar el BPS HF5 directamente a la ROM japonesa limpia de 2.097.152 bytes, CRC32 CCAA4853. No encadenarlo sobre HF4. Se incluyen todas las correcciones anteriores y los fuentes editables reconstruidos; no son el código fuente original del juego. No se distribuyen ROM ni BIOS.

HF5 comparte el formato de guardado protegido HF4. Carga partidas antiguas y las protege al guardar; para volver a JP/EN/HF1–HF3 se debe exportar una copia con tools/chocobo_save.py --export-legacy. Las versiones anteriores no reconocen directamente la cabecera protegida. El exportador verifica integridad y no sobrescribe el original. Mantener una copia del guardado al probar esta versión TEST.

Referencias externas de los casos, tratadas como testimonios y no como demostraciones del código:
- https://wazap.com/cheat/セーブデータ破損？バグ/570082/ — pisos, ascensor y comentario de teletransporte.
- https://wazap.com/cheat/クリア不能バグと対処法/570080/ — segundo final y fuente/rana.
- Chat compartido revisado en QA6: https://chatgpt.com/share/6acebdec-2b5c-83e9-833e-60560c52d788

## Identificación exacta

JP SHA-256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF5 SHA-256: 312f688f627f0c5ccf430c35c9632033344fc0397aa25c6f0db9d99a3630f9c8
HF5 CRC32: 3887C0CF; checksum WS: 06CA
BPS SHA-256: 1fd0c2c34329d4f1961b311ad7b6fff8403331825d71f5057795de2029fee665
