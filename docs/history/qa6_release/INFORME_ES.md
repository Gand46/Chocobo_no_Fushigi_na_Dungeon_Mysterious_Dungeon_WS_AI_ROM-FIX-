# Chocobo HF3 TEST — QA6: validación del guardado desde los datos

13 de octubre de 2026. Auditoría y herramientas nuevas; ROM y BPS HF3 sin cambios.

## Resultado

Se implementó un validador de sólo lectura y se contrastó con las operaciones reales de guardado y carga de Mesen 2.1.1. El resultado nuevo es una debilidad de la sobrescritura: un contenido parcialmente actualizado puede mantener una firma válida y cargar con datos de dos momentos distintos. La prueba es controlada; todavía no identifica el disparador natural de las pérdidas descritas en foros.

La validación también detectó y corrigió un error en el estado artificial de QA5: se había usado la máscara 8000 en vez de 0080 en la dirección 730A. La pantalla blanca de ese estado desaparece al corregir la bandera. Se accede a la escena de la segunda mazmorra, piso 60, y el diálogo avanza con A. Esto corrige la prueba, no la ROM, y no demuestra haber resuelto el reporte sobre la fuente/rana y el segundo final.

## Chat compartido revisado

Se recuperó la versión pública de «Analizar bloqueo de Chocobo»:
https://chatgpt.com/share/6acebdec-2b5c-83e9-833e-60560c52d788

Se extrajeron 58 mensajes textuales visibles de usuario y asistente. Se contrastó el informe final y los pasajes sobre software del resto de esos mensajes. El catálogo coincide con las diez incidencias del PDF: TR-01..03, EN-01..03 y JP-01..04. No se encontró otra incidencia de software distinta en esos textos. Algunos resultados de complementos aparecen censurados en el enlace y no pudieron examinarse; las imágenes adjuntas no se volvieron a descargar. Metadatos y alcance: qa6/chat_review.json. El HTML completo y los datos de sesión de la página no se incluyen en las fuentes.

Dos conclusiones antiguas quedan actualizadas: la diferencia entre CRC32 6E8CA148 y AC2E344C ya se explicó en QA5 mediante los dos bytes de checksum de la ROM; no identifica otra traducción ni corrupción. Las escalas históricas de sospecha del cartucho no son un diagnóstico vigente: el usuario estableció su causa eléctrica y ese incidente sigue cerrado fuera del alcance de ROM.

## Método nuevo

1. Identificar el archivo como SRAM cruda de 32.768 bytes. No aceptar ROMs, estados de emulador ni archivos truncados.
2. Separar firma, contenido guardado y memoria de trabajo. Las firmas n_c1/A_C1 reconocen una partida, pero apuntan al mismo bloque y no son una suma de integridad ni dos respaldos.
3. Comparar los 2.516 bytes almacenados con una referencia confiable de la misma generación. El SHA-256 es calculado por la herramienta externa; no es un checksum que el juego ya almacene. Un guardado posterior legítimo puede diferir y debe establecerse su procedencia.
4. Capturar la copia nativa en sus límites exactos: antes/después de guardar, y justo después de copiar los datos al cargarlos. Comparar todos los bytes antes de las modificaciones propias de la entrada a la escena.
5. Decodificar campos observados y contrastar relaciones confirmadas, como el selector de mazmorra frente a las banderas. Las condiciones completas de historia, inventario y eventos aún no están modeladas. No declarar jugabilidad válida sólo porque coincidan firmas o hashes.
6. Cuando existen dos generaciones conocidas, comprobar si una muestra coincide con un prefijo nuevo y un resto antiguo. La mezcla es un patrón compatible con escritura interrumpida; la traza nativa aporta la evidencia causal de esta prueba concreta.

### Distribución observada

| Zona SRAM | Función observada |
|---|---|
| 6BD8..75AB | Contenido activo que se copia al guardar; 2.516 bytes |
| 75AC..75AF | Firma alternativa A_C1 |
| 75B0..75B3 | Firma normal n_c1 |
| 75B4 | Caché de validez calculada durante la carga |
| 75B5 | Fuera del contenido copiado; función no establecida |
| 75B6..7F89 | Único bloque almacenado por las rutinas observadas |

El hash del archivo completo cambia durante el arranque aunque el contenido guardado y sus firmas permanezcan intactos: la SRAM también contiene memoria de trabajo. En las pruebas nuevas, 75B4 cambia de 00 a 01. El validador excluye esa caché de la comparación de persistencia para evitar un falso diagnóstico de corrupción.

## Pruebas y resultados

| Prueba | Resultado comprobado | Alcance |
|---|---|---|
| Guardado nativo observado | Copia exacta de 2.516 bytes; después escribe cuatro bytes de firma | Datos de entrada controlados, acción Save nativa desde un estado con procedencia |
| Carga completa HF3 | 2.516/2.516 bytes coinciden en cada una de las dos llamadas nativas | Proceso nuevo; ningún savestate usado para cargar |
| Carga de mezcla HF3 y JP | Ambos aceptan la muestra parcial; Lv2, HP29/30 | Datos artificiales; demuestra aceptación, no una pérdida natural |
| Marcador dañado de QA5 | Firma no reconocible, contenido intacto | Distingue partida oculta de payload borrado |
| Nivel cambiado de QA5 | Firma válida; diferencia detectada frente a referencia | Un valor plausible no prueba integridad |
| Estado D2 erróneo de QA5 | Datos cargados exactamente, pero selector 2 y banderas discrepan | El propio estado de prueba explica el cambio 2→1 |
| Estado D2 corregido | Mantiene mazmorra2 y alcanza escena del piso60; diálogo avanza | Acceso sintético; segundo final y fuente/rana no validados |

Verificación reproducible: 35 comprobaciones PASS, incluidas diez copias nativas de carga de 2.516 bytes cada una, repartidas en cinco arranques en frío. No son 35 incidencias del juego corregidas ni una medida de cobertura global. Se ejecutaron siete sesiones nuevas, todas completadas dentro de sus límites; no se usa un timeout como resultado del juego.

### Sobrescritura interrumpida: evidencia nueva

La generación A procede del guardado nativo temprano de HF3. Para obtener una generación B distinguible se cambian artificialmente nivel 1→2, HP30→29 y el contador capturado desde WRAM050E a 1234 hexadecimal. No se presenta como progreso natural. Se pulsa Save y se deja trabajar a la rutina original.

Se captura la SRAM tras la escritura número 200 del bloque. El proceso original termina normalmente; la interrupción se simula usando esa captura como archivo SRAM en otro proceso. No se afirma haber hecho una prueba física de corte de energía.

La muestra conserva exactamente los primeros 200 bytes de B y los restantes 2.316 de A. Nivel y HP son nuevos; el contador guardado todavía es antiguo (18 en vez de 4.660). La firma n_c1 anterior permanece válida. La traza sólo registra las cuatro escrituras de firma después de completar las 2.516 del bloque: no se invalida antes de sobrescribir.

La muestra carga en frío tanto en HF3 como en la japonesa original. Este caso demuestra que la sobrescritura no es atómica y el cargador observado acepta esa mezcla. No demuestra que el menú de equipo, Lafoss, ascensor o un evento provoquen esa interrupción. Tampoco demuestra que ese ejemplo concreto cause un bloqueo posterior.

Los rangos de guardado/carga 190333..190401, de banderas 18C88E..18C8CA y de selección de mazmorra 0158E2..015906 son idénticos entre JP, EN y HF3. Sus hashes constan en qa6/code_identity.json. La debilidad observada está presente en código heredado; no se atribuye a una modificación introducida por HF3.

### Corrección de la prueba QA5

El script del banco E1 escribe la mazmorra en 7301. La bandera 0F corresponde a word[7309] bit15, equivalente a byte[730A] bit7. La rutina nativa 18C88E también utiliza la máscara 0080 en word[730A]. QA5 había empleado 8000, que activa otro bit.

Se retira de la prueba ese bit incorrecto y se añade el correcto. La rama ahora selecciona E1:58F9 (mazmorra2), llega a la escena de piso60 y avanza el diálogo. La captura anterior que parecía una congelación no acreditaba un fallo natural y queda expresamente reclasificada como defecto del estado artificial. Los informes QA5 originales se conservan como historial, con esta rectificación como estado vigente.

## Estado de las incidencias

| ID | Estado vigente |
|---|---|
| TR-01 | Diez recursos corregidos; revisión global de texto/desplazamientos pendiente |
| TR-02 | Silbato corregido en HF3, con el alcance sintético ya documentado |
| TR-03 | Título sigue en japonés |
| EN-01 | Bloqueo/guardado desde equipo no reproducido; nuevo método preparado para localizar el primer dato divergente |
| EN-02 | Protección Lafoss evita el bucle inválido; efecto completo y animación pendientes; pérdida de guardado no observada en las pruebas previas |
| EN-03 | Dos órdenes de uso de DispelDrink funcionan en pruebas con adquisición artificial; compra natural pendiente |
| JP-01 | Ruta exacta de pisos de evento/ascensor pendiente; la pantalla blanca de la fixture D2 queda explicada y corregida |
| JP-02 | Escena del piso60 accesible sintéticamente; comparación del final con/sin fuente/rana aún pendiente |
| JP-03 | Teletransporte99→30 pendiente |
| JP-04 | Rescate de Atla pendiente |

La falta de atomicidad se registra como hallazgo técnico SAVE-01, no como una undécima causa independiente confirmada de los reportes. No hay corrección general de la pérdida de guardado incorporada a la ROM.

## Herramienta y reproducción

tools/validate_chocobo_save.py usa únicamente Python 3 y nunca escribe el archivo examinado. Emite JSON; la terminación normal de la herramienta no significa que la partida sea jugable: deben leerse los estados por comprobación. Un error de formato termina con error de argumentos.

Inspección:
python3 tools/validate_chocobo_save.py partida.sav

Comparación con un respaldo de la misma partida guardada:
python3 tools/validate_chocobo_save.py partida.sav --reference respaldo.sav

Clasificación de la mezcla incluida en estas fuentes:
python3 tools/validate_chocobo_save.py evidence/qa6/q6_save_overwrite/cut_0200.sav --reference evidence/qa6/q6_save_overwrite/generation_A.sav --next-reference evidence/qa6/q6_save_overwrite/generation_B.sav --loaded-copy evidence/qa6/q6_cold_interrupted/load_2_copied.sav

Revalidar las evidencias sin emulador:
python3 qa6/verify_data_validation.py --runs evidence/qa6 --fixtures qa5/save_fixtures

Repetir una carga real con Mesen en un perfil portátil aislado:
python3 qa6/run.py /ruta/Chocobo_EN_v1.1_HF3_TEST.ws - qa6/load_data_trace.lua /ruta/nueva_salida --mesen /ruta/perfil/Mesen --input-save evidence/qa6/q6_save_overwrite/cut_0200.sav --timeout 25

El parámetro --input-save reemplaza sólo el archivo SRAM del perfil de pruebas indicado. Los datos originales incluidos en evidence se conservan. Las capturas --loaded-copy deben tomarse en 9000:033F; una captura tomada después de avanzar la escena puede diferir legítimamente y no sirve para esa comprobación exacta.

## Continuación concreta

Usar estados de progreso trazables para capturar datos antes de guardar, después de guardar y al cargar en las rutas de equipo y ascensor. Comparar fuente/rana con dos ramas que compartan el resto del progreso. La herramienta identifica la primera divergencia, pero la semántica de todas las banderas sigue pendiente.

Una protección dentro de la ROM requerirá definir integridad, comportamiento ante una escritura incompleta, almacenamiento utilizable y compatibilidad con partidas antiguas. No basta con reponer una firma ni con saltar un bucle: ambas acciones podrían aceptar un estado incoherente.

## Identidad del build

Base japonesa Rev2: 2.097.152 bytes; CRC32 CCAA4853; SHA-256 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728.
HF3 vigente: CRC32 302765E7; checksum WonderSwan A43B; SHA-256 85a8be61fdac2feb777ed1726235b46b36f8950265a1788e7d7c9a0bc90f4b11.
BPS acumulativo JP→HF3: SHA-256 c2599e33c45d8e5430cc1d6f85eae06bc42dc7d7e5639e6a761f706e214ecef1.

No se crea HF4 ni un BPS nuevo, porque no hay cambios binarios. El paquete incluye el BPS HF3 acumulativo existente, las fuentes completas anteriores y esta auditoría. Sigue siendo TEST, no RC/final. No se incluyen ROM comercial, BIOS ni binarios del emulador. Ahorro de tokens: no medido.
