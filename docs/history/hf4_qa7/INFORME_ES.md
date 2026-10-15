# Avance de correcciones — HF4 TEST / QA7

Se implementó una corrección real de SAVE-01: la ROM deja de aceptar un bloque protegido parcialmente escrito y verifica su integridad antes de cargarlo. HF4 incorpora la traducción inglesa y todas las correcciones previas. Cambia 308 bytes respecto a HF3; el código añadido ocupa 297 bytes y reserva seis bytes de SRAM.

## Qué quedó comprobado

| Ensayo | Resultado |
|---|---|
| Primera escritura sobre guardado antiguo | 2.534 puntos, incluido el estado inicial; solo se admite el bloque antiguo intacto o el nuevo completo |
| Reescritura de guardado protegido | 2.534 puntos; ningún bloque mezclado aceptado |
| Escritura alternativa redirigida artificialmente | 2.538 puntos; ningún bloque mezclado aceptado |
| Corrupción de datos, cabecera y metadatos | 144 alteraciones de un bit rechazadas; control sin alteración aceptado |
| Borrado de una de las dos cabeceras | La otra mantiene su validez: 3 → 2 y 3 → 1 |
| Guardado normal y carga con proceso nuevo | PASS; bloque de 2.516 bytes copiado exactamente |
| Guardado antiguo cargado en HF4 | PASS con comparación exacta de datos |
| Exportación de copia HF4 a formato anterior | PASS; carga fría en HF3 y datos idénticos |
| Parche acumulativo y checksum | PASS; reaplicación independiente byte a byte, 11 pruebas de infraestructura aprobadas |

El oráculo independiente utiliza `binascii.crc_hqx`; las decisiones del juego proceden del código de HF4 ejecutado por la CPU de Mesen. Las matrices de interrupción inyectan prefijos del flujo de escrituras nativas observado. Esto es un PASS sintético, no una prueba física de cortar la alimentación.

Las primeras matrices no configuraban DS=1000 y rechazaban incluso el control válido: se descartaron. La primera matriz CRC corregida finalizó por límite de cuadros antes de completar los casos y también se descartó. Solo cuentan `q7_matrix2_new`, `q7_matrix2_rewrite`, `q7_matrix2_alternate` y `q7_matrix2_crc_complete`. Un archivo `completed.txt` por sí solo no concede PASS; el verificador exige cantidad, controles y resultados exactos.

El flujo de escritura normal de la revisión final coincide byte a byte con el de la primera sonda. La diferencia posterior del validador permite borrar una cabecera sin invalidar la otra; todas las matrices aprobadas ejecutan el validador final. El arnés alternativo cambia únicamente la entrada de llamada y el checksum; su procedencia queda registrada. Las ROM de arnés no se distribuyen como versiones jugables.

## Límites que permanecen

La SRAM tiene un único bloque persistente identificado. La protección evita cargar una mezcla de datos y detecta corrupción cubierta por CRC; no recupera la partida anterior si ya se sobrescribió. Las partidas legacy carecen de comprobación retrospectiva. Tampoco se identificó la causa natural exacta de los resets de los foros.

Los guardados protegidos usan un formato nuevo y requieren exportación de una copia para versiones anteriores. La carga normal protegida está aprobada en el ensayo; la reanudación natural del guardado alternativo sigue pendiente. La fixture artificial con ambas cabeceras llega a una pantalla vacía tanto en HF4 como tras convertirla y cargarla en HF3: se conserva como prueba no aprobada del evento, no como un éxito ni como evidencia de una nueva regresión.

La reserva SRAM 7F8A–7F8F no mostró referencias literales en el barrido acotado ni accesos durante las rutas HF3 de D2 y Lafoss observadas. Las referencias indexadas y otros eventos requieren ampliar cobertura. Esta limitación mantiene el estado TEST.

## Pendientes del PDF

| ID | Pendiente concreto |
|---|---|
| TR-01 | Revisión global de desbordamientos y maquetación; diez recursos ya corregidos se conservan |
| TR-03 | Traducir el título gráfico japonés |
| EN-01 | Reproducir la causa natural del bloqueo/reset asociada al equipamiento |
| EN-02 | Restaurar y validar animación y efecto completos de Lafoss; el bloqueo ya tiene protección |
| JP-01 | Reproducir la ruta exacta de pisos de evento/ascensor |
| JP-02 | Completar el segundo final y validar fuente/rana; se avanzó 1.200 cuadros adicionales del diálogo D2 sin cerrar esa ruta |
| JP-03 | Validar la ruta de teletransporte 99 → 30 desde un estado trazable |
| JP-04 | Validar el rescate de Atla desde antes del evento |

TR-02, silbato: corrección sintética conservada y regresión acotada en HF4. EN-03, Dispel: ensayos previos de ambos órdenes sin fallo reproducido; no se inventa otra corrección. SAVE-01: aceptación de escrituras incompletas corregida en el alcance anterior; recuperación y causa natural no resueltas. El fallo eléctrico del cartucho permanece cerrado y fuera del alcance.

## Entrega

BPS directo desde JP CCAA4853, fuentes acumulativos editables, validador/exportador de guardados, ensamblador, recetas, hashes, capturas, estados y resultados. No contiene ROM ni BIOS. La compilación sigue siendo HF4 TEST, no una aprobación final del juego.
