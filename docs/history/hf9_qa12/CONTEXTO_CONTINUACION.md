# Continuación tras HF9 / QA12

Autoridad actual: `manifest.json` y `build.py` de HF9. SHA256 final: `c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284`; CRC32 `4CA9F7B4`; checksum `E8BA`. BPS acumulativo sobre JP `CCAA4853`. Los cuatro fixes están en `localization/hf9_text_repairs.json`. Cambian 19 bytes respecto de HF8, incluidos dos de checksum. Logo y lógica intactos.

QA12 examinó 163 IDs adicionales al rango 65..C0 de QA10: 125 nombres no vacíos y 38 vacíos. No confundir 255 IDs inspeccionados con 255 objetos obtenibles ni con aprobación global. Check es familia 1, índice 4; el índice 6 es Equip. La primera corrida `q12_item_layout` está excluida y fue sustituida por `q12_item_check_fixed`.

La bandera 0x10 del inventario activa la tabla de síntesis SRAM 6D3F: 117 registros de diez bytes. Byte 0 = espacio de bolsa; bytes 8/9 = códigos de propiedades. Talon usa familia 6, rango 0..57; Saddle usa familia 7, rango 0..39. Aux no es la propiedad. Lectores ROM 19B16A y 19B243; compositor 184AAF..184B07. `qa12/property_all` copia estadísticas base y usa códigos válidos. La primera `q12_fused_records` utilizaba IDs de objetos; sus 206 cruces artificiales no prueban el fallo original.

En el hash final: 49 parejas cubren 96 descripciones; nueve casos críticos cubren los fixes en ambas posiciones, Sleep Card y dos equipos malditos con nivel -99. No hubo cruces en cuatro stores vigilados ni escrituras en 175AC..17F8F; el menú regresó y se conservó el inventario. De 147 capturas comparadas, 144 son idénticas y tres cambian sólo la línea corregida. No se adquirieron fusiones jugando ni se probaron todas las parejas. Siguientes pruebas útiles: producción natural de un registro fusionado, bolsa completa/dos selecciones y estado exacto del reporte. No repetir barridos básicos sin un riesgo nuevo.

Pendientes: maquetación global; causa histórica del bloqueo de equipo; variante histórica de Atla (rescate exacto D2F60 ya tiene PASS sintético QA10); ascensor continuo, ruta natural 99→30 y causa natural del reset. Logo vigente en `assets/title/user_v01`: integración QA11 conservada, revisión formal independiente de glifos pendiente. No rediseñar el arte del usuario. Incidente eléctrico físico fuera del alcance ROM. No repetir guardado, Lafoss, eventos o título ya comprobados sin un cambio concreto.

Comandos y límites: `docs/QA12_METODO_Y_LIMITES.md`. Las evidencias originales conservan sus hashes. QA12 no concede aprobación final/global. Ahorro de tokens no medido.
