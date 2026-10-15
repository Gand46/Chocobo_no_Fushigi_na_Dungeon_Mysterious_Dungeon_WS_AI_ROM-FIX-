# Chocobo English v1.1 HF15 TEST — QA20, validación 2/5

V2 ejecutada con reservas: **248 referencias revisadas, 74 corregidas y 242 aprobaciones sintéticas acotadas**. Seis referencias necesitan su contexto. La aprobación visual/lingüística global sigue abierta; permanecen V3–V5.

## Resultado

- 248 selecciones de diálogo sobre HF15 final: 247 alcanzan el terminador. G00:M255 agota el límite y queda excluido del PASS.
- Cuatro sesiones adicionales de interfaz: inicio sin guardado, confirmación de carga con guardado, menú de guardar/escalera y carga en frío del guardado recién creado. 252 sesiones totales, 76311 cuadros.
- 387 capturas registradas: lectura directa o identidad exacta de píxeles con páginas leídas. Una sola revisión del asistente, sin segundo revisor independiente.
- 3787 controles de integridad/alcance; 11 pruebas del proyecto aprobadas. 0 glifos no vacíos descartados en las 242 referencias aprobadas.
- Reconstrucción acumulativa, regeneración de las frases editables y aplicación independiente del BPS producen exactamente HF15.
- 4279 bytes distintos de HF14; 74 bloques y 74 punteros dentro del banco 1B. 4536 bytes de espacio previamente FF ocupados. Motor, gráficos, fuente, guardado y tamaño de ROM sin cambios.

## Qué se corrigió

Relaciones de causa y sujeto, omisiones de contenido, referencias a la maceta y al padre de Camilla, matices de preocupación/curiosidad, instrucciones de objetos y máquinas, y palabras incompletas. Se preserva la broma de las azadas antes de explicar la fusión de Talons. La paginación se adapta a dos líneas de 13 celdas usando los glifos nativos. El detalle de las 74 referencias está en qa20/translations.json y en QA20_V2_Informe.html.

## Reservas

G00:M252–255 requiere un contexto válido de depuración/variables. G00:M255 no termina en el estado forzado y descarta dos glifos no vacíos; no se aprueba. G04:M033–034 necesita ejecutar los consumidores de las preguntas y precios de forja. Leer sus recursos en la ventana común no demuestra ese uso.

Los menús reales de esta fase usan recursos getter; no se corresponden automáticamente con las etiquetas G16 de V1. Los consumidores propios G16:M000/M003/M004 permanecen pendientes de identificar/ejecutar. También permanecen G16:M073 (frase anfitriona) y preset32/F00:I053 (caller válido). No son seis reservas nuevas adicionales: las seis del lote se cuentan aparte de estos pendientes heredados/de interfaz.

No se valida recorrido natural completo, otro emulador ni hardware. Las causas históricas no reproducidas y el incidente eléctrico del cartucho conservan sus límites previos. Ver qa20/NOTAS_QA20.md para método y trazabilidad.

## Plan de cinco validaciones

| Validación | Referencias | Estado |
|---|---:|---|
| V1 | 83 | Ejecutada: 82 aprobaciones acotadas y G16:M073 pendiente. |
| V2 | 248 | Ejecutada: 242 aprobaciones acotadas y seis reservas. |
| V3 | 207 | Siguiente: resto de G06, G07, G08, G10, G11; objetos y variables. |
| V4 | 194 | Pendiente: G09 y diálogos extensos/opciones. |
| V5 | 154 | Pendiente: G14, transversal, gráficos/créditos y reservas. |

Las 886 referencias literales no abarcan por sí solas 2333 entradas getter, todos los consumidores ni gráficos. No se añade automáticamente otra validación ni se declara cierre global por el conteo.

## Uso y reconstrucción

Aplicar **Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps** directamente sobre una copia limpia japonesa con CRC32 **CCAA4853**. El BPS es acumulativo; no se aplica sobre HF14 ni sobre una ROM inglesa.

```bash
python3 build.py '/ruta/Chocobo_JP.ws' --out '/ruta/salida_hf15'
python3 qa20/rebuild_translation_edits.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/frases_qa20'
python3 qa20/verify_scope.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/verificacion_qa20.json'
python3 -m unittest discover -s tests -v
```

El regenerador editable recompone HF14 desde las recetas incorporadas y aplica las frases QA20; no necesita recuperar un ZIP anterior. El builder canónico usa src/corrections.json. Cambiar translations.json requiere reintegrar los edits, no modifica automáticamente el BPS. Los scripts exploratorios con rutas de sesión se conservan como antecedentes, no son el camino portable de reconstrucción.

## Integridad

- ROM japonesa SHA-256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
- ROM HF15 SHA-256: 2189490744c44fb1f16f79216a4c861cb7e3ade185a86e4d05b556c1bf46dd43
- CRC32 HF15: D6DCD52B; checksum WS: 54D7.
- BPS SHA-256: f69ee474103edcff58396272b293748d45db2d68da0f83ffdbde3fbfa0f26c67

Fuentes acumulativas editables reconstruidas, evidencia e historial preservados; no son el código fuente original del juego. No se distribuyen ROM comercial, BIOS ni emulador. HF14 pasa a patches/historical con su hash intacto y migración registrada. Los controles históricos QA19 pasan sobre su HF14 preservado; no se presentan como ejecución nueva de V1 sobre HF15.

Los resultados de dos reconstrucciones desde extracciones nuevas del ZIP se registran en .continuity/reports. La receta conserva BPS e informe de compilación, sin incorporar la ROM generada como artefacto del paquete.
