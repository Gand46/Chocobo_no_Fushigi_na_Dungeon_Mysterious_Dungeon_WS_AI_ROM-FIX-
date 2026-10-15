# QA17 / Maquetación global, iteración 3 de 4

HF12 TEST integra 11 correcciones de recursos únicos (13 referencias, porque G16:M034/035/036 comparten puntero). Son 203 bytes de contenido y 2 de checksum respecto de HF11. El parche es acumulativo y se aplica directamente a la ROM japonesa CRC32 CCAA4853. No se modificaron el código ejecutable, los punteros, la fuente ni el logo.

29 pruebas sintéticas aprobadas en la compilación final, con 0 glifos visibles descartados. Se archivan 78 ejecuciones en total: las pruebas de diagnóstico, compilaciones intermedias y un timeout de instrumentación están excluidos del PASS. Ninguno se presenta como recorrido natural.

De las 13 alertas heredadas: 9 corregidas, 3 sólo afectan relleno vacío y 1 sigue pendiente de consumidor real (G16:M064). También se corrigió la unión «Price65535» mediante «Cost 65535» y la unión del nombre del objeto con «Level», ahora en una línea aparte. Hay 14 casos de variables para 7 punteros únicos / 9 referencias y 14 pantallas de créditos identificadas C5..D2. Las confirmaciones finalizan los mensajes; los créditos regresan al pueblo.

Las variables usan 0 y 65535 como extremos del formateador de 16 bits; 65535 no se declara un nivel alcanzable. Los nombres probados son Ore (1 celda) y Double KnockTalon (9 celdas), máximo ordinario de esta familia. Se excluye el recurso compuesto de moneda I012. FFF8 selector1 usa un buffer preparado con palabras exactas de la ROM: valida el consumidor, no la preparación natural del buffer. M035/M036 se cubren estructuralmente por identidad del puntero M034, no por rutas naturales separadas.

Los tres casos de relleno más tres variantes dinámicas máximas consumen un espacio invisible al avanzar: 6 eventos, 0 pérdidas visibles. No se ocultan ni se contabilizan como fallos corregidos. El recurso compuesto G16:M064 sólo falla al forzarlo por un consumidor que puede no corresponderle, y por eso queda NOT_VALIDATED.

## Cambios

- G01:M039: recuperar el terminador antes de G01:M040; conservar pausa y reducir un punto de la elipsis. M040 se comprobó por separado y sus bytes permanecen intactos.
- G03:M012: eliminar el sufijo «ff» residual, cotejando el agradecimiento al hermano con el japonés.
- G04:M031: saltos y pausa entre el nombre coloreado y la frase de la mazmorra.
- G04:M034: ambas confirmaciones de precio completas, 1000/500 Gil; eliminar residuos.
- G04:M048: «What is it? / Another Teleport Box?» completo y sin residuos.
- G06:M099: mover el salto; conservar todos los glifos, color y espera. La gramática heredada sigue pendiente de revisión lingüística.
- G08:M020: nombres / nacimiento / trillizos completos, con pausa y limpieza entre páginas.
- G16:M004: aviso y texto de guardado completos en dos páginas. Hacer legible el aviso no demuestra corrupción ni causa del reset; su formulación inglesa requiere revisión lingüística frente al japonés.
- G16:M070: tres páginas legibles, sin cortar «recommend» ni «Wanderer».
- G00:M253: separar etiqueta y cifra con «Cost».
- G16:M034/035/036: nombre en primera línea; «Level» y cifra en segunda.

## Pendientes concretos para M4

1. G16:M064: identificar el consumidor/caller del texto compuesto de puntos y precio antes de intervenirlo.
2. TR-01-M2-C01: identificar el caller válido de preset32 y su segunda página. La pregunta compartida F00:I053 no se cambia sin resolver sus usos.
3. Reconciliar la cobertura por contextos reales y la regresión de maquetación. El censo tiene 3488 referencias narrativas y 2333 entradas getter, pero esos totales no equivalen a aprobaciones visuales. No se ha completado el denominador de todos los contextos.

Queda 1 iteración base de maquetación; no es garantía de aprobación global. La revisión lingüística global es un bloque separado y permanece abierta. Se conservan los PASS sintéticos funcionales previos; las causas históricas exactas de equipamiento, Atla y reset de guardado no fueron reproducidas nuevamente en M3. El incidente eléctrico físico sigue fuera del alcance de la ROM.

Estado: TEST, no RC ni FINAL_APPROVED. Segundo emulador y hardware no validados. Los detalles verificables están en docs/QA17_VALIDATION.json, docs/QA17_RUN_INDEX.json, qa17/visual_readings.json y qa17/alert_resolution.csv.
