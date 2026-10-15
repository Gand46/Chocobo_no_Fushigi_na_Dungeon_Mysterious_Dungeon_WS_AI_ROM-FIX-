# Chocobo — QA18 / Maquetación M4 de 4

HF13 TEST • 14 de octubre de 2026 • Japonés → inglés

La cuarta iteración está ejecutada: cinco recursos corregidos y siete pruebas finales con **PASS_SYNTHETIC_SCOPED**. Las cuatro iteraciones del plan han terminado. Esto cierra el lote M4 y los defectos demostrados de su alcance; **no concede aprobación visual exhaustiva a toda la ROM**.

| Recurso | Contexto | Corrección |
|---|---|---|
| G16:M064 | Intercambio de puntos | Tres páginas con pausa; recuperación de letras recortadas y sustitución de «fo lot» por «Slot». |
| G00:M015 | Disculpa | Pausa tras «Oh, sorry.»; la frase siguiente queda completa en dos líneas. |
| G06:M012 | Camilla y la mazmorra | Tres páginas sin desplazamiento prematuro; espacio entre «Camilla’s» y «Dad». |
| G06:M073 | Aviso del libro | «to» comparte línea con un separador; la advertencia final tiene página propia. Persiste una omisión de traducción. |
| G09:M191 | Vacilación | Los puntos suspensivos se completan antes de la pausa y se limpia la ventana para la frase siguiente. |

## Validación

- 7 sesiones finales, 7.500 cuadros nativos, 14 lecturas de capturas y 259 comprobaciones reproducibles.
- Cero glifos no vacíos perdidos en las siete sesiones. También pasan las regresiones de Cost65535 y nombre largo/Level65535.
- 147 bytes de contenido y 2 de checksum cambiados frente a HF12. Código, fuente, logo, tablas de punteros y recursos del getter idénticos.
- BPS aplicado mediante un decodificador independiente a la ROM japonesa limpia: igualdad de todos los bytes y SHA-256.
- 11 pruebas del proyecto aprobadas. 790 comprobaciones QA17 repetidas sobre su HF12 histórico; sus 29 sesiones conservan su alcance original y no se presentan como nuevas ejecuciones HF13.
- 30 sesiones archivadas: 7 aprobadas y 23 diagnósticas excluidas, incluidas compilaciones candidatas y entradas de script descartadas. Ninguna diagnóstica cuenta como PASS.

## Ventanas, saltos, recortes y variables

El censo completo de las tablas verificadas contiene 3.488 referencias de diálogo (3.472 punteros), 886 referencias con texto literal, 2.421 no vacías compuestas sólo por controles, 2.333 entradas del getter y 141 presets de ventana (79 geometrías incluyendo modo). No hay cadenas sin terminador en esas tablas.

El barrido de ancho sólo conserva G01:M031, G06:M022 y G09:M063: sus excesos son relleno 0000, comprobado en M3; no requieren recortar texto. El nuevo barrido de líneas explícitas entre pausas no deja candidatos verticales. Es un análisis estructural: no cubre por sí solo cualquier altura elegida por un consumidor ni toda combinación contextual de variables.

La matriz M2–M4 acredita 26 punteros de diálogo probados como objetivo (28 referencias contando alias, sin atribuirles un caller independiente), 12 ventanas del getter y 97 enlaces ventana/familia/índice. Las 9 referencias dinámicas comparten los 7 punteros probados en M3; sus bytes y consumidores se conservan en HF13. Las 14 páginas de créditos mantienen su comprobación M3. **Estas cifras no son un porcentaje de aprobación global**: falta revisión visual de los demás contextos reales.

## Pendientes concretos

1. **Preset32 / F00:I053:** el recorte aparece al forzar una segunda página. No se encontró una llamada nativa válida en esta investigación acotada. Dos aparentes llamadas resultaron ser argumentos de otras instrucciones. Se conserva como candidato no confirmado, sin afirmar que sea inalcanzable ni modificar la pregunta compartida sobre pisos.
2. **Cobertura visual global:** ampliar la matriz de consumidores y escenas antes de marcar TR-01-M como aprobado globalmente. Ejecutar cuatro iteraciones no prueba todas las 886 referencias con texto ni los 141 presets.
3. **Revisión lingüística separada:** G06:M073 termina «will revert your level to» sin complemento; conserva una omisión anterior. También siguen vigentes las observaciones lingüísticas de M3 (incluida la redacción del aviso de guardado). La maquetación de estas frases no certifica su traducción.

El acceso a los mensajes fue sintético: savestate más sustitución de selector o puntero de script; dos casos añaden valores extremos. El script de puntos se ejecuta con sus instrucciones y ventana originales, pero su entrada natural, la transacción económica y la persistencia del guardado no se validaron aquí. La rutina 7B que repite ese script se conserva.

## Artefactos y reproducción

BPS acumulativo directo desde JP CRC32 **CCAA4853**. No se aplica sobre HF12 ni sobre una ROM inglesa. Fuentes completas reconstruidas y editables, evidencia histórica y nueva, planes Lua, estados compatibles, verificador y manifiesto incluidos. No se distribuye ROM ni BIOS.

```sh
python3 build.py /ruta/original-japonesa.ws --out /ruta/build-hf13
python3 qa18/verify_scope.py --japanese-rom /ruta/original-japonesa.ws --out /ruta/verificacion-qa18.json
python3 -m unittest discover -s tests
```

Para repetir una sesión con Mesen compatible, use qa18/run.py, qa18/driver.lua, el plan y la ruta de estado indicados en provenance.json de cada sesión, con LAYOUT_OBSERVER apuntando a qa18/layout_observer.lua. Las inyecciones operan en memoria del emulador y no son cambios de ROM.

SHA-256 JP: `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`

SHA-256 HF13: `a6bb2ee9e1d973f92aa7eac1a158f2873cde185075fc8a3b042dbe1f1dcb303f`

SHA-256 BPS: `33a916387401d4ce329f7123bc503853290bbf5c516d24397f2f21473f0ac52d`

Checksum WonderSwan: **0903**. Estado de publicación: **TEST**, no RC ni FINAL_APPROVED.
