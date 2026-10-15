# Chocobo WonderSwan — HF3 TEST, 13 de octubre de 2026

El bloqueo del cartucho físico queda cerrado fuera del alcance de ROM: el usuario confirmó una causa eléctrica distinta. Esta fase se centra en los defectos de la ROM japonesa y su traducción inglesa. No se atribuyen las fotografías físicas a un fallo del parche.

## Resultado nuevo

Se reparó el silbato (TR-02). La ROM japonesa carga 37 tiles del gráfico, pero su mapa referencia el tile 38 en 18 celdas. La zona sin cargar conserva un glifo del menú, por eso el residuo cambia entre japonés e inglés. La fuente comprimida está en ROM 105B76 (592 bytes descomprimidos); el mapa está en 130C48 (2048 bytes). La traza real confirma esos punteros y la escritura de 3800 hasta 3A4F, dejando 3A50 con texto.

La reparación conserva íntegros los tiles 0–36. Añade tres tiles de color uniforme: índices 37/38/39 con píxeles 2/1/3. Las 18 celdas usan seis veces el color 2, ocho el 1 y cuatro el 3. Esto no es una elección artística: las paletas originales [5,1,3,6], [5,6,1,3], [5,3,6,1] y los bordes vecinos demuestran las equivalencias del color 2. Se incorporan esas equivalencias al gráfico porque la rutina nativa 5000:4935 sustituye la paleta de todo el mapa durante la animación.

Recursos nuevos: 333 bytes en 10C800 y 419 en 13FC60, ambos en relleno FF comprobado del mismo banco. Punteros 100078 y 130040 actualizados. No se cambia código ejecutable en HF3, ni la tipografía. Se mantienen todas las correcciones HF1 y la protección HF2.

## Validación efectuada

- Once pruebas unitarias y aplicación BPS con decodificador independiente: PASS. Regeneración de los cuatro edits del silbato: coincidencia exacta.
- Constructor desde la japonesa CCAA4853: resultado reproducible, checksum correcto, cero offsets inesperados; BPS acumulativo original→HF3.
- Silbato: inventario inyectado, selección y uso mediante menú nativo, mismo estado de mazmorra HF1. Se comparan 2399 capturas decodificables (fotogramas 2–2400); 2204 son idénticas. En 192 las diferencias quedan dentro de las 18 celdas reparadas. Tres fotogramas (638–640) muestran diferencias de transición de carga fuera de esas celdas; se revisaron y conservan en evidencia. No se afirma identidad temporal absoluta. Se excluye el primer PNG inválido anterior al primer render del emulador.
- RAM en fotograma 720: los 37 tiles originales son idénticos; los tres nuevos contienen los colores esperados; las diferencias del mapa se restringen a las 18 celdas. El silbato se consume y el juego vuelve a responder a las acciones.
- Lafoss y Flare: consumidos mediante menú; el mundo continúa y responde al movimiento. La protección Lafoss no reconstruye su animación o potencia completa.
- Lafoss: nueva traza localiza el origen en 4000:226C. El selector de modelo usa el ID FF de SRAM 6B14 y devuelve FFFF desde la tabla 14229F antes de llamar al dibujado desde 4000:2252. Es una ausencia en la selección gráfica original, no un glifo de traducción. No se sustituye por Flare ni se inventan daños.
- DispelDrink: las dos órdenes, adquirido antes y después de equipar la montura maldita, funcionan en HF3 bajo adquisición artificial. Equipo 09→01 y bebida 59→botella 64: se retira el equipo, permanece su maldición. La compra natural sigue sin comprobarse.
- Guardado básico: acción nativa en HF3 y carga del .sav en un proceso nuevo sin savestate; vuelve a la casa con HP 30/30 y permite moverse. No acredita guardado en eventos avanzados.
- 30 acciones nativas de equipo y diez recursos de texto reejecutados en HF3. Son pruebas acotadas con inventario sintético.

## Pendientes validados como abiertos

| ID | Estado al cierre |
|---|---|
| TR-01 | Diez recursos corregidos; falta revisar disposición y legibilidad del guion completo. |
| TR-02 | Reparado y validado en la secuencia de Mesen descrita; hardware y segundo emulador pendientes. |
| TR-03 | Pantalla de título sigue en japonés. |
| EN-01 | No reproducido en pruebas acotadas de equipo; no cerrado globalmente. |
| EN-02 | Protección contra bloqueo pasa; animación y semántica completa de Lafoss pendientes. |
| EN-03 | No reproducido en las dos órdenes sintéticas; adquisición natural pendiente. |
| JP-01 | Ascensor/pisos de evento/pantalla blanca: falta estado previo trazable y reproducción. |
| JP-02 | Final de segunda mazmorra: falta estado previo trazable y reproducción. |
| JP-03 | Teletransporte 99→30: falta ruta y estado previo trazable. |
| JP-04 | Rescate de Atla: falta estado previo trazable y reproducción. |
| HW-USER | Cerrado fuera del alcance de ROM por causa eléctrica confirmada por el usuario. |

El material disponible sólo acredita progreso temprano y guardado básico. No se convierten estados inventados de final de juego en pruebas de los eventos JP-01–04. La siguiente prioridad es obtener progreso trazable hasta esos eventos y revisar Lafoss desde el selector ya localizado. Esta entrega sigue siendo TEST, no RC ni traducción completa. Segundo emulador y hardware no validados.

## Aplicación y reproducción

Aplicar sólo `patches/Chocobo_EN_v1.1_HF3_TEST_JP_CCAA4853.bps` a la japonesa limpia de 2097152 bytes, CRC32 CCAA4853. No aplicar encima de HF1/HF2 ni de la traducción previa. Salida CRC32 302765E7, checksum A43B; SHA-256 en manifest.json. No se distribuye ROM comercial.

```sh
python3 build.py /ruta/JP.ws --out /ruta/salida_nueva
python3 -m unittest discover -s tests
python3 tools/verify_evidence.py /ruta/JP.ws
python3 tools/verify_independent_bps.py /ruta/JP.ws
```

Ejemplo de repetición del silbato: `python3 qa4/run.py /ruta/HF3.ws evidence/qa3/q3_dungeon/checkpoint.mss qa4/whistle_validation.lua salida_nueva --mesen /ruta/Mesen --timeout 25`.

Mesen 2.1.1 Linux x64: SHA-256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Los scripts exigen acceso Lua de I/O para escribir evidencia. Los estados y adquisiciones artificiales se identifican en qa4_provenance.json. Los informes previos quedan en docs/history/hf2; no sustituyen el alcance actualizado. Los registros históricos conservan los resultados anteriores para auditoría.
