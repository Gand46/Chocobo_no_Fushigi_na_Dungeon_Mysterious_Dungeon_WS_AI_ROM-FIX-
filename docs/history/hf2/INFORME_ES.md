# Chocobo WonderSwan — HF2 TEST: reproducción y protección de Lafoss
Fecha: 2026-10-13. Estado: experimental / TEST, no RC.

## Resultado principal
Se reprodujo el bloqueo al activar la opción Kck de Lafoss (ID FF) dentro de una mazmorra en Japón, inglés v1.1 y HF1 mediante inventario sintético y el menú real. HF2 conserva las diez correcciones de texto de HF1 y añade una protección que evita el bucle observado. No reconstruye los gráficos ausentes ni certifica la potencia, todas las variantes o la fidelidad completa del hechizo.

El BPS es acumulativo: aplicar directamente al original japonés de 2.097.152 bytes, CRC32 CCAA4853. No aplicar sobre una ROM inglesa ni HF1.
Salida HF2: CRC32 A18CFFA6; checksum WS F2E4; SHA-256 605ef4467766d778d74f01edee57ed1794698fd587056b2cff1f542e61b41864.
Original: SHA-256 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728.
BPS: SHA-256 694cc67034e6e13a6c83887d0ec5dd55b3ecdd64b100903c8a0c706d635e41ce.

## Qué se reprodujo y qué se corrigió
| Incidencia | Resultado de esta iteración | Alcance |
|---|---|---|
| EN-02 / Lafoss | REPRODUCED_SYNTHETIC en JP, v1.1 y HF1; protección HF2 funciona en el escenario probado | La adquisición del objeto se inyecta. No se reconstruye su animación ni se certifica su daño. |
| TR-02 / silbato | REPRODUCED_SYNTHETIC; causa localizada en tile residual | Sigue abierto. El original también reutiliza un tile de texto; la traducción cambia el dibujo residual. |
| EN-03 / DispelDrink | NOT_REPRODUCED en las dos condiciones sintéticas de orden | Con la bebida antes/después de equipar, retira la montura maldita; no elimina su maldición. No reproduce compra/adquisición natural. |
| EN-01 / consulta de equipo | No bloqueo en matriz previa de 48 variantes de bits ni en 30 casos HF2 | Los bits arbitrarios no equivalen todos a estados naturales válidos. No se valida toda combinación de inventario ni corrupción de partidas. |
| Guardado básico | PASS_BASIC_COLD_BOOT en HF1 y HF2 con Mesen | Guardado del juego, proceso cerrado, proceso nuevo sin cargar savestate, selección de partida y movimiento. |
| JP-01 a JP-04 | NOT_REPRODUCED / pendientes | No se alcanzaron eventos tardíos, ascensor, final de segunda mazmorra, teletransporte 99→30 ni rescate de Atla. |
| TR-01 / composición global | HF1 preservado; diez recursos revalidados en HF2 | No equivale a aprobar todo el guion. |
| TR-03 / título | Japonés conservado | Sin cambios. |

## Lafoss: causa demostrada y protección
En CPU 5000:4392 se calcula el índice de un descriptor gráfico. El caso problemático entra con CX=FFFF. Tras multiplicarlo por cuatro, la dirección envuelve a ES:018C, donde DX=FFFF y AX=FFFF. El banco C2 pasa a FF y el buscador en 5000:43B3–43C4 incrementa DI/CX sin poder encontrar un límite estrictamente mayor que FFFF. La CPU sigue atendiendo interrupciones; no es un apagado. El juego queda atrapado en ese bucle y no responde a las entradas posteriores.

La traza de 2.048 instrucciones de `q3_freeze_trace_hf1` registra repetición de ese bucle. En el estado idéntico de comparación, las tres ROM terminan en el mismo patrón de espera y no consumen la perla. Flare (ID F4) sirve como control: concluye y permite continuar.

HF2 cambia el punto ROM 0x154392–0x154397 y añade un bloque de 17 bytes en 0x15FD40–0x15FD50, tras el recurso HF1 situado en FD00. El bloque comprueba CX=FFFF antes de acceder al descriptor; si coincide, salta a 44CC, la limpieza nativa que restaura el banco C2 desde la pila, normaliza DS/controles y hace RETF. Para un índice válido ejecuta los dos opcodes desplazados y vuelve a 4398. No sustituye Lafoss por Flare ni inventa una animación.

Son 24 bytes diferentes respecto de HF1, incluidos dos del checksum; 22 bytes efectivos de código/trampolín. No hay edición nueva de fuentes ni de gráficos. Los rangos escritos tienen preimagen exacta y el constructor detecta cero offsets inesperados. El resultado permite consumir la perla, continuar las acciones del mundo y responder al movimiento. Se entrega como protección experimental contra el bloqueo, no como restauración completa de Lafoss.

## Silbato: evidencia propia
Se registraron 1.500 fotogramas por variante para JP, v1.1, HF1 y HF2, desde el mismo checkpoint. En la animación, el mapa BG2 utiliza el tile 0x1A5, WRAM 0x3A50, en 18 celdas. El descompresor carga los tiles 0x180–0x1A4 y no sobrescribe 0x1A5. La traza de escrituras muestra que 3A50 fue cargado previamente por el texto; en JP contiene parte del glifo de ROM 0x1623B0. De ahí el dibujo diferente en inglés.

En el fotograma 720 las 288 diferencias de píxel entre JP/HF1 corresponden exactamente a esas 18 celdas. No se restauró ciegamente el glifo japonés porque dañaría/reintroduciría texto o perpetuaría la dependencia del contenido anterior. Falta identificar el tile esperado y corregir el consumidor/longitud del recurso con evidencia de composición. Capturas originales y trazas incluidas.

## DispelDrink: prueba de orden y semántica
Se construyó una montura TanSaddle (9D), con bit de maldición 01, y se equipó usando el menú; el registro pasó a flags 09 y la pantalla mostró E junto a Curse. En un caso el DispelDrink (59) estaba ya en la bolsa; en otro se añadió después de equipar. Se cerró sólo la ventana de estadísticas, conservando el menú para no confundir combate/animación con indisponibilidad del objeto.

Ambos casos mostraron “Cursed equips were removed.” El objeto 59 pasó a Bottle (64); la montura pasó de flags 09 a 01. Esto confirma retirada del equipo y permanencia de la maldición. HF2 repitió correctamente el caso de bebida añadida después. El orden sintético probado no reproduce el reporte; quedan adquisición natural, otras monturas/propiedades y contextos.

## Guardado y arnés de QA
La ruta inicial requería hablar con el alcalde y completar el encuentro con el moogle en casa. Una visita anterior al nido sin ese progreso no activaba el guardado.

Además, el driver heredado dejaba activo el callback de captura al llamar `emu.stop`. Podía sobrescribir el checkpoint durante la salida. Se cambió a un callback de una sola ejecución, retirándolo antes de capturar y parar. Las pruebas antiguas de carga que arrancaban desde ese checkpoint no sirven para acusar a la ROM. Se conservaron como intentos rechazados, no como fallos del juego.

Con el driver corregido se observó el diálogo Save your game?, se confirmó Yes y se conservó el archivo .sav escrito por Mesen. Después se lanzó otro proceso desde arranque, sin `QA_STATE`, se escogió Load, se confirmó continuar y se volvió a la casa con Lv 1 / HP 30/30, seguido de movimiento. HF1 y HF2 pasan esta prueba básica. No demuestra ausencia de corrupción en los eventos tardíos del PDF. Los .sav, planes, hashes y capturas están en evidence/qa3/q3_hf2_save y q3_hf2_cold; el informe run.json del cold tiene state_sha256=null.

## Validación del parche y regresión
- Build desde Japón y reaplicación BPS byte-idénticos; además, aplicación con `17_WS_Patch_Tools v0.1.1`, implementación independiente.
- Once pruebas unitarias de integridad, precondiciones, rangos, BPS corrupto/truncado y base errónea: PASS.
- Treinta casos HF2 de consulta/equipamiento, quince IDs y dos acciones: completados, sin apagado ni cruce de las dos guardas instrumentadas.
- Diez recursos HF1 revalidados en HF2 con lector/dibujado reales y trazas: completados, sin cruce de guardas.
- 120 capturas de esos casos comparadas con HF1: 55 idénticas en toda la imagen. Las otras difieren sólo en tres píxeles del HUD (x=50–52, y=5); las superficies de texto y menús comparadas permanecen idénticas. Una comprobación actual de HF1 reproduce la misma alternancia de intensidad (43/133) en esos tres píxeles, con fase distinta; no desaparece su geometría. No se afirma identidad absoluta de todas las capturas.
- Silbato HF1/HF2: 849 de 851 fotogramas del intervalo 550–1400 son idénticos; las dos diferencias de transición se conservan. No se presenta este dato como reparación del silbato.
- Flare sigue consumiéndose y permite continuar con la protección aplicada. No se exige igualdad de RAM completa: cambian tiempos/ruta de enemigos; no se declara determinismo global.
- Guardado/carga en frío HF2 y DispelDrink después de equipar: PASS de los escenarios acotados.

No se realizaron segunda implementación de emulación ni pruebas físicas. No se afirma que haya quedado corregido el bloqueo del cartucho PTS-133 del usuario. El emulador usado es Mesen 2.1.1 Linux x86_64, SHA-256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41.

## Procedencia, reproducción y límites
Las comparaciones JP/v1.1/HF1 de Lafoss y silbato reutilizan el mismo estado HF1 de mazmorra para aislar el cambio de ROM: son SYNTHETIC_STATE + SAVESTATE, no tres recorridos naturales independientes. El menú vuelve a leer sus recursos de cada ROM. El código afectado es byte-idéntico en JP/v1.1/HF1 antes de la protección. Se conservan además cargas del guardado nativo HF1 en JP/EN; la ruta inglesa adicional reproduce Lafoss. Los intentos japoneses posteriores quedaron interrumpidos por combate/muerte sin activar el objeto y no se cuentan como reproducciones.

`qa3/run.py ROM STATE PLAN OUT --timeout 25 --mesen /ruta/Mesen` ejecuta cada plan. Usar `-` como STATE para arranque en frío; usar un perfil portátil aislado con settings.json y copiar sólo el .sav del juego al nombre correspondiente de Saves. Nunca sustituir la carga nativa por loadSavestate para aprobar persistencia.
Ejemplo Lafoss: PLAN=qa3/lafoss_use.lua, STATE=evidence/qa3/q3_dungeon/checkpoint.mss. Ejemplo Dispel después: STATE=evidence/qa3/q3_dispel_equip_only/checkpoint.mss, PLAN=qa3/dispel_from_equipped.lua, variable ADD_DRINK=1. Antes: usar q3_dispel_equip y omitir ADD_DRINK. Es una fixture de inventario; no una compra natural.

Los comandos originales conservan sus rutas de ejecución; sustituirlas por la ruta local al descomprimir. `qa3_provenance.json` enlaza entradas y salidas por SHA-256. Los archivos `q3_*` son ensayos: sólo los citados como válidos sustentan las conclusiones; otros documentan rutas descartadas, errores de selección o hipótesis. `qa2_legacy` conserva el arnés anterior para trazabilidad; usar qa3 para nuevas pruebas.

## Fuentes documentales nuevas/verificadas
1. Wazap, publicación de 17/03/2016: reporta que una perla ラーフォス obtenible en cierto piso congela el juego. Es un testimonio anterior a la traducción, sin ROM/hash o emulador identificado; orientó la prueba y no se usa como prueba de causalidad.
https://wazap.com/cheat/WS%E7%89%88%E3%83%95%E3%82%A3%E3%83%A9%E3%83%8D%E3%82%B9%E3%80%81%E3%83%A9%E3%83%BC%E3%83%95%E3%82%A9%E3%82%B9%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/570084/
2. Titney, guía WS (2021): ruta inicial, lugares de guardado y observación de orden en DispelDrink. Se consultó el contenido indexado; la apertura directa respondió bloqueo de acceso. No es una reproducción controlada.
https://gamefaqs.gamespot.com/wonderswan/576610-chocobo-no-fushigi-dungeon-for-wonderswan/faqs/79455
3. PDF del usuario y README original de traducción, conservados en docs. Los estados documentales originales se preservan y el registro actual se actualiza en issue_register.csv/json.

## Próxima acción concreta
Corregir el consumidor gráfico del silbato sin restaurar caracteres japoneses; identificar la animación/efecto completo de Lafoss. Reproducir las incidencias de ascensor y pisos de evento a partir de un guardado de progreso con procedencia verificable. No repetir intentos de navegación con el driver antiguo. Ahorro de tokens: no medido.
