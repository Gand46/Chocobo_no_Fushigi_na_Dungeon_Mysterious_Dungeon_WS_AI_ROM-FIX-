# QA12 — método, procedencia y límites

## Reproducir

Tras reconstruir HF9, proporcionar un Mesen 2.1.1 privado:

`python3 qa12/property_all/run_suite.py build/Chocobo_EN_v1.1_HF9_TEST.ws evidence/qa12_fixtures/checkpoint.mss runs/property_final --suite equipment --mesen /ruta/Mesen --timeout 150`

Para las nueve regresiones concretas, reemplazar `property_all` por `critical_check`. Una instancia por perfil/directorio Mesen, sin compartir Saves entre procesos.

El estado inicial procede de q3_dungeon, identificado por SHA256 en QA12_RUN_INDEX.json. Es sintético. El observador carga el estado en un callback único de CPU, escribe un registro de bolsa en 6C9F y, cuando corresponde, un registro de síntesis en 6D3F. Conserva estadísticas del objeto base y añade códigos de propiedad válidos. El resto usa botones del menú nativo, sin inyectar punteros ni sustituir retornos del getter.

Bolsa: cantidad, ID, nivel, aux, flags. Talones: ROM 19B663, 54 entradas de 15 bytes, propiedad base en byte 14. Sillas: ROM 19B98D, 36 entradas de 14 bytes, propiedad base en byte 13. Bandera 0x10: tabla SRAM 6D3F de 117 registros de diez bytes. Byte 0 vincula el espacio de bolsa, no el ID; bytes 8/9 son propiedades. Familia 6: tabla 15C918, 58 entradas. Familia 7: tabla 15CF54, 40 entradas. Código 0 = ausencia. Se cubren las 96 entradas no nulas en 49 parejas, no todas las combinaciones.

Vigilancia: stores CPU 37AFF, 37B7D, 37BC1 y 37BFD con DI >= 023C, donde el buffer 6057 alcanzaría el puntero 6293; escrituras CPU 175AC..17F8F. La ausencia de hits sólo cubre esos puntos/rango durante los recorridos. No es prueba general de persistencia. Se comprueban getters de familias 6/7, salida sin powerOff, estado de menú 0004 e inventario conservado.

`python3 qa12/verify_scope.py --hf8 /ruta/HF8.ws --hf9 build/Chocobo_EN_v1.1_HF9_TEST.ws --runs evidence/qa12_runs --out /ruta/validation.json`

Pillow sólo se requiere para comparar capturas. Verifica 19 bytes dentro de cuatro slots y checksum, hashes finales, coberturas, retornos y 147 capturas. No aprueba el juego natural. El build normal no requiere Pillow.

## Exclusiones

- `q12_item_layout`: buscaba acción 6 (Equip), no 4 (Check), y consumió algunos objetos. Excluida. La repetición corregida es `q12_item_check_fixed`; sus 163 casos conservan inventario y muestran el getter esperado.
- `q12_fused_records`: usó IDs de objetos como códigos de propiedad, fuera de los límites. Produjo 206 hits de buffer con datos inválidos. No reproduce el congelamiento reportado.
- `q12_fusion_probe`: probó flags/aux sin registro vinculado; no cubre propiedades fusionadas.
- `q12_property_all_hf9`: candidato anterior al arreglo Sleep Card, con hash diferente del final. La corrida final es `q12_property_final_hf9`; no se reescriben metadatos antiguos.
- `q12_legacy_fused`: seis parejas de propiedades 11/12/13 en English v1.1. Muestra concatenación por terminadores históricos, pero todos los casos regresan. No demuestra la causa histórica del bloqueo. HF1 ya había corregido esos terminadores.

## Alcance

Siete casos JP verifican significados y textos originales. HF9 los corrige sin modificar fuente, punteros, código o logo. No se prueban adquisición natural de fusiones, efectos de combate, todas las combinaciones ni el guardado real que falló. Guardado, Lafoss, Atla y logo conservan pruebas anteriores y límites por identidad de bytes; no se presentan como reejecutados.

Se revisó nuevamente el reporte público en https://retroachievements.org/game/16362 . Describe congelamiento al consultar equipo y pérdida de guardado, sin precisar objeto, combinación ni estado reproducible en el contenido consultado. Es una pista, no causalidad demostrada. Estas pruebas no cierran EN-01 ni la causa natural de SAVE-01.
