# Chocobo English v1.1 — HF1 TEST
## Auditoría específica y primera reparación reproducible · 13 de octubre de 2026

**Resultado:** parche BPS acumulativo real, de la base japonesa a la traducción inglesa v1.1 con diez recursos de texto corregidos. Esta entrega es **TEST**, no RC ni reparación certificada de todos los bloqueos del PDF.

El PDF adjunto distingue diez entradas documentales y advierte que no son diez defectos confirmados o independientes (página 1). Se conserva esa distinción: **diez recursos corregidos no equivalen a las diez incidencias del informe resueltas**. Los reportes críticos de guardado, eventos y uso de perlas siguen abiertos donde no existe reproducción suficiente.

## 1. Aplicación e identidad

Aplicar `patches/Chocobo_EN_v1.1_HF1_TEST_JP_CCAA4853.bps` **directamente a la ROM japonesa**, sin aplicar antes el IPS. Salida de 2.097.152 bytes, extensión `.ws`.

| Imagen | CRC32 | Checksum WS |
|---|---|---|
| Japonesa aportada, base aceptada | CCAA4853 | 3321 |
| Japonesa + IPS literal | AC2E344C | 3321, incorrecto para su nuevo contenido |
| Inglesa adjunta, checksum normalizado | 6E8CA148 | 13E3 |
| **HF1 TEST** | **F576EF15** | **F9B9** |

La diferencia de CRC citada en la página 7 del PDF queda explicada: aplicar el IPS produce la variante AC2E344C y corregir solo sus dos bytes finales produce exactamente la inglesa adjunta 6E8CA148. No se usa otra revisión japonesa ni se añaden cambios inexplicados.

SHA-256 de la base:
`38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`

SHA-256 de HF1:
`c5ca8fcda7d40a22215bea83b4c0f6b210d244e8ab5ac90fd8a3392a28a279cb`

SHA-256 del BPS:
`9d1f54ae38727b8a9174d2a9783fbf33713c36588c59d5b0e159f899b460d04a`

## 2. Defecto localizado y correcciones

El lector nativo devuelve palabras de 16 bits; el copiador común deja de recorrer la cadena al encontrar `FFFF`. Varias entradas inglesas perdieron ese terminador y el lector continúa por las siguientes. La prueba observa las palabras leídas y las confronta con los bytes de cada ROM; también conserva el resultado dibujado por el juego.

| Recurso | Dirección anterior | Palabras leídas EN → HF1* | Exceso anterior sobre el espacio asignado |
|---|---|---:|---:|
| Venom | `0x06C6CC` | 9 → 4 | 8 bytes |
| Tidal | `0x06C9A6` | 10 → 4 | 12 bytes |
| Poisn_B06 | `0x06CAA8` | 17 → 9 | 18 bytes |
| GilToss | `0x06CB0E` | 12 → 6 | 12 bytes |
| Walking | `0x15C894` | 19 → 10 | 26 bytes |
| IceFireLit | `0x15D04A` | 44 → 11 | 66 bytes |
| IceFireWind | `0x15D060` | 33 → 11 | 44 bytes |
| LitFireWind | `0x15D076` | 22 → 11 | 22 bytes |
| Particle | `0x15D608` | 13 → 2 | 22 bytes |
| Poisn_B19 | `0x19C708` | 17 → 9 | 18 bytes |

*Los recuentos incluyen el terminador. Para los recursos reubicados, el límite corregido es el del nuevo espacio reservado, no el espacio anterior. Los diez terminan dentro de su asignación en HF1.

Se sustituyen por `FFFF` los sobrantes finales de Venom, Tidal, Gil toss A y tres rótulos de atributos. Dos copias de la categoría de veneno/resurrección mantienen sus glifos ingleses completos y se reubican dentro del mismo banco para añadir el terminador, sin truncarlas. La frase japonesa `歩いても` se restituye como `Even walking`, conservando `FFFE` y `FFFF`: la versión anterior había introducido `Equipment w` y consumía además el mensaje siguiente. El recurso `の` de la familia 8, índice 39, pasa a espacio + `FFFF`, como las dos partículas japonesas idénticas de los índices 35 y 37 ya traducidas así en v1.1. No se altera el mensaje siguiente de cambio de nivel.

Se dejan sin modificar dos de las doce alertas previas: `0x16E6F4`, que puede utilizar la terminación de una entrada vacía adyacente, y `0x1B3AEF`, que termina con un control `FFF2`. No se ha demostrado que deban repararse sustituyendo controles o separando esos datos.

## 3. Alcance binario

HF1 modifica **71 bytes respecto de la inglesa aportada**, repartidos en catorce operaciones explícitas y la actualización del checksum. El BPS acumulativo incluye además la traducción previa: la diferencia total contra la japonesa es **62.330 bytes**. No confundir estos dos contadores.

Se cambian intencionalmente tres punteros cercanos: `0x06C478 → D800`, `0x15C44C → FD00`, `0x19C0D8 → FA60`. Sus destinos son `0x06D800`, `0x15FD00` y `0x19FA60`: el constructor exige que los bytes originales de esos destinos sean `FF` y conserva el banco de cada tabla. Se verifican todas las preimágenes; el conteo de offsets inesperados es cero.

No se cambia tamaño, mapa de cabecera, configuración de SRAM/EEPROM, rutinas ejecutables, gráficos de la fuente, animaciones ni flags de historia con esta reparación. Esto describe los cambios de HF1; la traducción v1.1 anterior sí había modificado fuentes y otros recursos. La ausencia de cambios de código no es una garantía automática de ausencia de regresiones de datos.

## 4. Pruebas ejecutadas

**Recursos:** diez casos en cada una de tres variantes: japonesa, inglesa v1.1 y HF1. El arnés crea un único objeto de prueba, entra con mandos al comando `Chk` y sustituye las lecturas de su descripción por las del recurso real elegido, siguiendo el puntero de la ROM correspondiente. No se inserta texto dibujado externamente ni se inventan pantallas. Las trazas validan que los valores sustituidos son los bytes reales de esa variante. Se confirma fin de lectura dentro del nuevo espacio y eliminación de las concatenaciones observadas.

Este acceso es **SYNTHETIC_RESOURCE_REPLAY**, no el contexto natural de la habilidad, evento o condición. El encabezado TanTalon pertenece al objeto usado como superficie de prueba. Demuestra el comportamiento del lector/copiador y su representación en esta superficie, no que se haya completado la escena original ni que se haya reparado un bloqueo de historia.

**Inventario y equipamiento:** quince IDs, con consulta `Chk` y acción `Equ`, en las tres variantes: **90 casos**. Los objetos se introducen en un registro nativo de cinco bytes; las acciones posteriores usan entradas del mando. No se reproduce el congelamiento en esta matriz. Los quince casos de consulta terminan en estado de menú `0004`; los quince de equipamiento terminan en el menú raíz, estado `0009`, igual en las tres variantes. No se afirma que todos regresen a pantalla de juego sin menú. Los puntos de escritura observados `7AFF` y `7B7D` no registran cruces del límite vigilado. No cubren todas las escrituras posibles ni prueban persistencia del guardado.

**Arranque y regresión:** cada variante completa 22.000 fotogramas desde el inicio hasta el poblado, usando únicamente entradas de mando y su propio checkpoint entre tramos. HF1 y v1.1 terminan con la misma captura, WRAM y SRAM, byte por byte. Se preservan las rutas, hashes, seis checkpoints de procedencia conocida y copias comprimidas de memoria y cobertura. Esta igualdad es una comprobación acotada de ejecución, **no un guardado nativo seguido de carga en frío**.

**Identificación adicional:** replay independiente de nombres y descripciones de `0xFF` y `0x59`. El juego dibuja `Lafoss pearls` y `Allow cursed item removal`. Esto localiza los objetos de EN-02 y EN-03, pero no valida sus reglas o efectos. Ocho exploraciones adicionales de navegación de propiedades no alcanzaron la familia problemática; sus resultados negativos se conservan sin contarlas como cobertura de atributos.

**Construcción:** once pruebas unitarias aprobadas; reconstrucción exacta desde Japón; checksum correcto; BPS→ROM idéntico al constructor; aplicación cruzada con una implementación BPS independiente ya incluida en las herramientas aportadas. Se rechazan la inglesa como base, una japonesa con un bit alterado y una base truncada. El nuevo lanzador de QA incluido también se ejecutó contra los diez recursos.

Las capturas conservan los 224×157 píxeles que entrega `emu.takeScreenshot()` con esta configuración; no se presentan como volcado crudo de 224×144. La hoja comparativa solo dispone capturas intactas con rótulos exteriores. No se usó OCR ni generación de imágenes.

## 5. Estado de las diez incidencias del PDF

**TR-01 — Texto desplazado: `PARTIALLY_AUDITED`.** Se corrigen 10 recursos con lectura hacia entradas vecinas; no se ha censado todo el guion ni se equipara este conjunto a todos los desplazamientos del readme.

**TR-02 — Animacion del silbato: `NOT_REPRODUCED`.** No se ha aislado el defecto de animacion. No se modifican sus graficos.

**TR-03 — Titulo sin traducir: `DOCUMENTED_UNCHANGED`.** El titulo japones se conserva; no es una reparacion de estabilidad.

**EN-01 — Consulta de equipamiento: `NOT_REPRODUCED_IN_TESTED_SUBSET`.** 15 equipos x Chk/Equ x 3 variantes: 90 casos, sin reproducir bloqueo en esta matriz. El inventario fue construido sinteticamente; no cubre todas las propiedades, posiciones, maldiciones ni partidas.

**EN-02 — Lafosse Pearls: `ITEM_IDENTIFIED_FAILURE_NOT_REPRODUCED`.** La ROM dibuja Lafoss pearls para ID 0xFF. Nombre/descripcion identificados con el renderer nativo. No se ha reproducido su uso ni el bloqueo.

**EN-03 — DispelDrink inhabilitado: `ITEM_IDENTIFIED_RULE_MATRIX_PENDING`.** ID 0x59: descripcion Allow cursed item removal. Identificacion no demuestra cuando el uso deberia habilitarse.

**JP-01 — Eventos / ascensor / guardado: `NOT_REPRODUCED`.** No hay estado tardio validado para el escenario. No se modifican flags, cargador ni guardado.

**JP-02 — Final segunda mazmorra: `NOT_REPRODUCED`.** No se han obtenido las dos ramas equivalentes con/sin evento de fuente/rana.

**JP-03 — Teletransporte 99 a 30: `NOT_REPRODUCED`.** No se ha ejecutado la ruta reportada. Puede solaparse con JP-01.

**JP-04 — Rescate de Atla: `NOT_REPRODUCED`.** No se ha identificado el instante exacto del bloqueo anecdótico.

## 6. Límites y siguiente trabajo técnico

La segunda implementación de emulación no se ejecutó: la obtención del core independiente quedó bloqueada por resolución DNS (`codeload.github.com`); se conserva el error. No se atribuye ese fallo al juego. Tampoco se realizó validación en hardware. Los avisos de memoria no inicializada que Mesen emite al continuar los checkpoints aparecen en las ejecuciones comparables; no se reclasifican como una corrupción nueva provocada por HF1 ni se ocultan los registros.

Faltan una reproducción del disparador de EN-01 con el equipo exacto, uso efectivo de Lafoss en contexto válido, la matriz de DispelDrink, guardado/carga nativos y escenas tardías. La corrección de la partícula del cambio de nivel es estructuralmente demostrable; **su relación causal con el reporte de Lafoss sigue sin demostrar**. No se han alterado eventos para saltarse estos pendientes.

Utilizar copias desechables de partidas al evaluar esta versión TEST. El siguiente hito es cerrar EN-01/EN-02 en sus consumidores propios y comprobar persistencia, no conceder un PASS global a partir del arranque o del replay.

## 7. Fuentes y reproducción

El paquete incluye una receta binaria editable que reconstruye íntegramente los cambios de v1.1, el IPS de referencia con sus créditos, las nuevas correcciones editables, formato y mapa de recursos, constructor/aplicador BPS, pruebas, Lua, evidencias y checkpoints. **No se presenta la receta reconstruida como código fuente original del juego o de los autores de la traducción.** Las interpretaciones de alto nivel fuera de los recursos auditados no se inventan.

No contiene ROM comercial, BIOS, ejecutable de emulador ni archivos de fuentes tipográficas. Para reconstruir: `python3 build.py "/ruta/Japanese.ws"`; en Windows, `BUILD.bat "C:\ruta\Japanese.ws"`. Python 3.10 o posterior. El constructor no sobrescribe archivos existentes por defecto. Los wrappers Windows/macOS se entregan como conveniencia y no se declaran probados en esos sistemas; la ejecución verificada fue Linux x86_64.

Documentos y evidencia de referencia: PDF adjunto (páginas 1–7 para alcance, fichas e identidad); `docs/LEGACY_README.txt`; `src/`; `localization/corrected_resources.json`; `evidence/resource_validation.csv`; `evidence/runtime_validation.json`; `evidence/regression_summary.json`; `evidence/independent_bps_validation.json`. La hoja `evidence/screenshots/comparacion_sintetica.png` permite revisar las capturas directamente.
