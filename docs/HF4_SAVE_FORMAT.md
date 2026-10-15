# Formato protegido HF4 y reproducción QA7

## Distribución de SRAM

| Rango | Función |
|---|---|
| 6BD8–75AB | Datos vivos; 2.516 bytes |
| 75AC–75AF | Cabecera alternativa A_C1 legacy / A_C4 protegida |
| 75B0–75B3 | Cabecera normal n_c1 legacy / n_c4 protegida |
| 75B4 | Máscara de validez calculada; no es checksum |
| 75B5 | Byte sin semántica confirmada; no modificado |
| 75B6–7F89 | Copia persistente; 2.516 bytes |
| 7F8A | Máscara de cabeceras comprometida: normal1, alternativa2 |
| 7F8B | Confirmación A5; cero durante escritura |
| 7F8C–7F8D | CRC16, little endian |
| 7F8E–7F8F | Complemento del CRC, little endian |

CRC16-CCITT-FALSE, polinomio1021, inicialFFFF, sin reflexión ni xor final; cubre 75B6–7F8A inclusive (2.517 bytes). No es autenticación ni protección contra modificaciones deliberadas. Seis bytes de cola reservados tras el bloque nativo; el análisis de disponibilidad está acotado, no exhaustivo.

## Secuencia

1. Reconocer cabeceras existentes y la modalidad solicitada.
2. Poner commit=0 y registrar máscara; invalidar el sufijo de ambas cabeceras antes de copiar datos.
3. Ejecutar el cuerpo nativo de copia de la modalidad elegida. Las constantes de firma usan sufijo4.
4. Calcular y guardar CRC/complemento; reconstruir cabeceras protegidas solicitadas.
5. Escribir A5 como último paso. Solo entonces el bloque protegido es admisible.

El validador acepta las firmas legacy1 sin CRC para conservar compatibilidad. Una firma protegida4 exige A5, CRC/complemento correctos y que sus bits estén incluidos en la máscara comprometida. El subconjunto conserva la operación nativa que borra una cabecera. Un CRC de 16 bits tiene límites de detección; no se promete detectar cualquier corrupción imaginable.

Hooks ROM: 190367 (normal), 19038C (alternativo), 1903B8 (validación); constantes1903FD y190401; cueva19FA80–19FBA8. Las precondiciones y los 297 bytes ensamblados están en src/corrections.json y src/save_guard.s. El código conserva registros/banderas alrededor de la protección; mantiene los cuerpos nativos. PUSHA y las instrucciones empleadas se validaron en el núcleo WS de Mesen.

## Procedencia y ensayos reproducibles

Mesen SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Los run.json registran ROM, estado, plan y controlador, con rutas originales como metadatos históricos. Los scripts requieren una instalación compatible de Mesen; el ejecutable no se incluye.

`qa7/run.py` usa un proceso nuevo y perfil aislado; `--input-save` copia SRAM cruda al nombre de la ROM. El acceso al menú Save se hace desde un savestate registrado; los valores vivos nivel/HP/contador se inyectan explícitamente. La copia y firma posteriores las escribe el juego. La persistencia se verifica en otro proceso sin savestate.

Valores de save_trace.lua: q7_save_new y q7_save_final_native usan SAVE_LEVEL=2, SAVE_HP=29, SAVE_COUNTER=4660 y fixture baseline. q7_save_rewrite usa 3,28,9029 y generation_B anterior. q7_alternate_save usa 3,28,9029 con el arnés alternativo; su cuerpo original no toma el contador por la misma ruta que el normal. Los CSV y SRAM capturados son la fuente de comparación, sin inferir identidad por el nombre del archivo.

El arnés `qa7/make_matrix_rom.py` preserva DS, configura DS=1000 y llama al validador final9000:FB72. `matrix.lua` reconstituye cada prefijo de writes.csv y lee75B4. `crc_matrix.lua` muta ocho posiciones del payload (64 casos), cuatro bytes de cabecera normal (32) y seis de metadatos (48). No se ensayaron todos los bits del payload. `selective_matrix.lua` usa la fixture de ambas cabeceras. `make_alternate_rom.py` reproduce la redirección explícita al escritor alternativo; no representa adquisición natural del evento.

Comprobación autónoma de evidencia:

```sh
python3 qa7/verify_matrices.py evidence/qa7_runs
```

Para repetir una matriz, genera su ROM de prueba desde la HF4 reconstruida (nunca la uses para jugar):

```sh
python3 qa7/make_matrix_rom.py build/Chocobo_EN_v1.1_HF4_TEST.ws 2534 matrix_new.ws
MATRIX_SOURCE="$PWD/evidence/qa7_runs/q7_save_new" python3 qa7/run.py matrix_new.ws - qa7/matrix.lua resultado --mesen /ruta/perfil/Mesen --timeout 25
```

Reescritura usa2534 casos y q7_save_rewrite; alternativa2538 y q7_alternate_save; CRC145 con crc_matrix.lua y q7_save_new; borrado selectivo3 con selective_matrix.lua y q7_alternate_save. Los perfiles y directorios de resultado deben ser independientes. MATRIX_SOURCE, SAVE_FIXTURE y demás variables son entradas explícitas; no están implícitas en un hash del plan.

No conceder PASS a los grupos q7_native_matrix_new, q7_matrix_*_final ni q7_matrix_debug: DS=0 en la primera llamada de inicio los hacía mirar otra memoria. q7_matrix2_crc tampoco completó sus145 casos antes del límite300; el grupo aprobado termina con q7_matrix2_crc_complete, tras ampliar a3000. Se preservan para auditar el descarte.

La carga fría normal y legacy verifica dos copias nativas (previsualización y carga confirmada) y compara los2.516 bytes. La fixture de ambas cabeceras no alcanza una reanudación jugable ni en HF4 ni en el comparador HF3 convertido; su CRC correcto no valida su semántica de evento. No usar esas pantallas como aprobación del guardado alternativo completo.
