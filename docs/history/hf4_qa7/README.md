# Chocobo English v1.1 + HF4 TEST — QA7

Versión experimental del 14 de octubre de 2026 (UTC). Traducción japonesa → inglés, con las correcciones acumulativas HF1–HF4. No es una versión final ni RC. No incluye ROM ni BIOS.

HF4 corrige la aceptación de escrituras incompletas del guardado: invalida las cabeceras antes de copiar y publica una marca de finalización después de comprobar el bloque con CRC16. También detecta alteraciones del bloque protegido. No restaura datos sobrescritos ni demuestra que se haya resuelto la causa natural de los resets comentados en foros.

## Aplicación

Aplica `patches/Chocobo_EN_v1.1_HF4_TEST_JP_CCAA4853.bps` directamente a una copia limpia de la ROM japonesa de 2.097.152 bytes, CRC32 **CCAA4853**, SHA-256:

`38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`

No se encadena sobre un parche anterior. La salida esperada tiene CRC32 **12E75051**, checksum WonderSwan **06C5** y SHA-256:

`1ec449933e812c8e4f5e83b882db17b4c5f1ce3b5ea85527d9a1dd2a0891060d`

## Guardados y compatibilidad

HF4 carga partidas antiguas y las protege al volver a guardar. Las partidas antiguas no tienen CRC: su carga compatible no certifica su integridad. Una partida HF4 protegida no es reconocida directamente por JP, EN v1.1 ni HF1–HF3. Para volver a una versión anterior, exporta una copia verificada:

```sh
python3 tools/chocobo_save.py partida_HF4.sav
python3 tools/chocobo_save.py partida_HF4.sav --export-legacy copia_legacy.sav
```

La herramienta requiere SRAM cruda de 32 KiB; no acepta savestates. Rechaza la exportación de datos protegidos inválidos y nunca sobrescribe el archivo original ni un destino existente. La copia exportada pierde la protección CRC. Se verificó su carga en frío en HF3, conservando exactamente los 2.516 bytes de la partida.

El juego conserva un único bloque de partida. Si se interrumpe su sobrescritura, HF4 puede rechazarlo y mostrar el mensaje nativo «There is no data.». No existe recuperación automática del bloque anterior. Conserva una copia de tu guardado antes de probar esta versión experimental.

## Reconstrucción y comprobación

Solo hace falta Python 3 para el build acumulativo; no se necesita ensamblador para usar los fuentes emitidos:

```sh
python3 build.py /ruta/JP.ws --out build
python3 -m unittest discover -s tests -v
python3 tools/verify_evidence.py /ruta/JP.ws
python3 qa7/verify_matrices.py evidence/qa7_runs
```

`src/corrections.json` contiene precondiciones y rangos exactos. `src/save_guard.s` es el ensamblador editable de HF4. Para regenerar su receta desde una HF3 identificada, usa `tools/generate_save_guard.py HF3.ws --out desarrollo` con GNU binutils. Los fuentes reconstruyen el parche; no son el código fuente original del juego.

## Validación y límites

- 7.606 prefijos de escritura comprobados con el validador real ejecutado por la CPU emulada y un oráculo CRC independiente: ninguna mezcla de partidas fue aceptada.
- 144 alteraciones de un bit rechazadas, con control positivo válido. Borrado selectivo de cabeceras: máscaras 3 → 2 o 1 preservadas.
- Guardado normal nativo, reinicio del proceso, carga fría de partidas antiguas/protegidas y comparación exacta del bloque: PASS.
- Guardado alternativo: escritura y validador probados mediante redirección explícita; reanudación completa de su evento natural: NOT_VALIDATED.
- Lafoss y silbato: regresión acotada en HF4; recursos previos sin cambios. La animación y semántica completas de Lafoss siguen abiertas.
- Seis bytes reservados de SRAM: no se encontraron usos previos en el análisis y rutas acotadas descritos; no es una prueba exhaustiva de todos los eventos.
- Segundo emulador, hardware real, eventos tardíos y aprobación lingüística/visual global: NOT_VALIDATED.

Los resultados son sintéticos donde se indica; no prueban una reproducción natural de los foros. El bloqueo eléctrico del cartucho está cerrado y fuera del alcance de la ROM. Revisa `INFORME_ES.md`, `docs/HF4_SAVE_FORMAT.md`, `docs/issue_register.csv` y `docs/quality_gates.json`. Los informes históricos se conservan con su versión y no sustituyen este estado.
