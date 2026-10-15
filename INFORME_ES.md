# Chocobo English v1.1 HF16 TEST — QA21, validación 3/5

V3 ejecutada con reservas: **207 referencias revisadas, 64 diálogos corregidos, 205 aprobaciones sintéticas acotadas y dos reservas**. También se corrigieron dos etiquetas de propiedades de equipo. La aprobación visual/lingüística global sigue abierta: quedan V4, V5 y los contextos pendientes.

## Resultado comprobado

- 207 selecciones sobre la ROM final; 207 alcanzan el terminador, 60714 cuadros y 284 capturas registradas. Ningún glifo no vacío descartado en las 205 referencias aprobadas.
- Complemento: cuatro recorridos de inventario/estado y seis configuraciones de equipo fusionado, en cinco sesiones finales y cinco japonesas de comparación. 13641 cuadros finales; 100 imágenes de comparación leídas. Cantidades 1/99, equipo ±99, dinero de ocho cifras, nombres sin identificar y ocho propiedades.
- 3365 controles del lote y 98 del complemento; 11 pruebas del proyecto aprobadas. Builder acumulativo, regenerador editable y aplicación BPS independiente producen exactamente la misma ROM.
- 64 bloques nuevos y 64 punteros en el banco 06: 06:E588–06:F708, final exclusivo, 4480 bytes. Dos propiedades se corrigen en su espacio original, sin mover sus punteros. 4258 bytes distintos frente a HF15, incluido checksum.
- Motor, fuente compartida, título, lógica de guardado y tamaño de ROM conservados. Los getters cambian únicamente en F06:I019 y F06:I022.

## Correcciones

Se recuperan sujetos, cantidades, causas, despedidas e instrucciones omitidas. Se repara una frase ilegible sobre el crecimiento del pueblo y la repetición de Item File. La explicación del cristal vuelve a incluir su división y expansión. Se mejora la gramática, la posesión de los personajes y el tratamiento Professor en este grupo. Las propiedades ahora dicen Strong vs undead y Strong vs poison foes: eficacia contra tipos de enemigos, no resistencia al estado veneno.

Detalle: qa21/translations.json (64 diálogos), qa21/getter_translations.json (dos propiedades), qa21/linguistic_review.json y QA21_V3_Informe.html. La tipografía conserva sus medias celdas, glifos y resaltados nativos.

## Reservas y límites

G06:M100 requiere su consumidor de depuración. G11:M011 es el fragmento de un número de plantas: falta la ventana compuesta y su cantidad real. Tener una captura aislada no los aprueba. La muestra de inventario no equivale a revisar todos los objetos ni los 2333 getters.

Se mantienen las seis reservas de V2: G00:M252–255 y G04:M033–034. También G16:M073, preset32/F00:I053 y los consumidores propios G16:M000/M003/M004. No se atribuyen etiquetas de G16 a menús con texto parecido. No se acredita recorrido natural completo, hardware, segundo emulador o segundo revisor.

Los 3787 controles históricos de QA20 se repitieron sobre HF15 preservado; no son nuevas sesiones V2 sobre HF16. Las matrices de guardado y las causas históricas no reproducidas mantienen sus límites anteriores.

| Validación | Referencias | Estado |
|---|---:|---|
| V1 | 83 | 82 aprobaciones acotadas; una reserva. |
| V2 | 248 | 242 aprobaciones acotadas; seis reservas. |
| V3 | 207 | 205 aprobaciones acotadas; dos reservas; complemento de inventario. |
| V4 | 194 | Siguiente: G09, diálogos extensos y opciones. |
| V5 | 154 | G14 y revisión transversal, gráficos, créditos, terminología y reservas. |

No se añade automáticamente una sexta fase ni se declara aprobación universal por contar las 886 referencias literales.

## Aplicación y reconstrucción

Aplicar **Chocobo_EN_v1.1_HF16_TEST_JP_CCAA4853.bps** directamente sobre una ROM japonesa limpia, CRC32 **CCAA4853**. Es acumulativo; no se aplica sobre una ROM inglesa ni sobre HF15.

```bash
python3 build.py '/ruta/Chocobo_JP.ws' --out '/ruta/salida_hf16'
python3 qa21/rebuild_translation_edits.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/frases_qa21'
python3 qa21/verify_scope.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/verificacion_qa21.json'
python3 -m unittest discover -s tests -v
```

El regenerador recompone HF15 con las recetas incorporadas y el snapshot docs/history/qa20/corrections.json; después genera los textos y propiedades QA21. No necesita recuperar un ZIP anterior. Cambiar un JSON de traducción requiere reintegrar los edits y repetir la validación; no modifica automáticamente el BPS.

Son fuentes acumulativas editables reconstruidas, no el código fuente original del juego. Se conserva el historial, la evidencia y los checkpoints. No se incluye ROM comercial, BIOS ni emulador. HF15 queda intacto en patches/historical. Los informes de dos reconstrucciones desde extracciones nuevas están en .continuity/reports.

## Integridad

- JP SHA-256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
- HF16 SHA-256: 14abf199753631e907e80092ce50f4e48d7eb139f31964cdc8897b9d6bf51c00
- HF16 CRC32: 20FF7B24; checksum WS: 6555.
- BPS SHA-256: 5f1c59ee00a6e564ff007518aa86e46b40eb9f94dc0f410fd702df0db8a6e78a
