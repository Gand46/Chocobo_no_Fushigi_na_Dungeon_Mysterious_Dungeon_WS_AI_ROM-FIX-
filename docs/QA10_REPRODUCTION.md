# QA10: reproducción y alcance

HF7 es TEST, no RC. Build actual y BPS identificados en manifest.json. Python3 para build; Pillow sólo para hojas de inspección. Mesen2.1.1 Linux x86_64 SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. No se redistribuye ROM, BIOS ni emulador.

## Título

El cargador154A27 copia411tiles2bpp desde155155..156B04 a WRAM2000. Mapas nativos: descriptorC0 BG1800, base3C; descriptorC4 BG1000, baseC2. El mapa0 se recompone en150034..1501B6; puntero150032 dirige mapa1 a15FD58. Compresión nativa LZ, ver generate_whistle_fix.decode/encode. Todas las escrituras exigen preimagen y no solapan Walking15FD00. La animación usa tiles328..391 y una ventana6x6 que termina en y63. Se conservan esos64tiles y el dibujo superior; letras grandes comienzan y65. Una candidata y60 fue rechazada porque la animación pisaba algunas letras. La capa BG2 conserva la paleta transparente4; una candidata sin ese bit fue rechazada por banda negra.

Texto: CHOCOBO'S / MYSTERY DUNGEON / FOR WONDERSWAN. Extensión gráfica propia del logotipo: contorno negro, cara clara, sombra y cuadrícula de píxeles nativos; rótulo pequeño sólido con jerarquía de PUSH BUTTON. No se usa una fuente de sistema ni se cambia la fuente compartida de diálogos. Referencia nativa: evidence/qa8_runs/q8_title_reference y qa8/title_assets. Fuente editable: tools/generate_title_fix.py y assets/title/canonical_glyphs_and_layout.json. Regeneración opcional desdeHF6: python3 tools/generate_title_fix.py HF6.ws --out title_edits.json --source-out title_source.json. El build normal usa src/corrections.json y no requiere HF6.

Revisión de glifos: qa10/glyph_sheet.py extrae capturas reales con etiquetas numéricas. Las primeras pruebas registraron O parcialmente sobrescritas, N/A pequeñas ambiguas; se corrigieron posición, separación, contraforma y rótulo pequeño. glyph_review_initial.json conserva el fallo inicial. glyph_review_final.json documenta36lecturas; vista nativa completa y zoom2x diagnóstico. OCR no utilizado.

## Equipamiento y maquetación

qa10/equipment_suite/run_suite.py ROM ESTADO OUT --mesen MESEN --suite equipment --timeout220. Estado inicial q3_dungeon SHA2cb9e29b3749ce0caf9628ff93f8c5b52ebe5eb7212627175290a38d9adb5f82. Se reemplaza una ficha de bolsa por{1,ID,0,0,0}. IDs65..C0:92consultas;90objetos con nombre y2entradas vacías9B/9C. Para cada caso se confirmó family2/indexID en text_reads.csv, abrir Check y salir con B. Son SYNTHETIC_STATE más entradas nativas, no adquisición natural. El watcher vigila únicamente37AFF/37B7D con DI>=23C y el bloque persistente175AC..17F8F: no cubre toda la memoria ni todas las combinaciones de equipo fusionado.

TitanSaddle corresponde family3/indexA4, slot16F1CA..16F1D7. Palabras0342 0279 0343 0005 0310 0078 FFFF. El0078 es la w sobrante y pasa aFFFF; elFFFF siguiente queda como relleno. El menú real confirma TitanSaddle. La sospecha de recorte de GilTalon en la hoja de conjunto se descartó al abrir la captura individual: el texto completo cabe; no se modifica.

No confundir estas90descripciones con todas las ventanas del juego ni con sus páginas de propiedades. El bloqueo EN01 no se reprodujo. Próxima investigación útil: fichas de equipo fusionado y su estructura auxiliar, con un guardado que reproduzca el fallo; evitar repetir los92casos básicos.

## Atla: escena concreta y límites

Estado previo q7_d2_dialogue_progress SHA6d67f049fe57904e6b2de8578de2e651d9f50fba2eb485fc098c2a37adde7ed0, derivado de la fixture sintética D2F60 documentada en QA6. qa10/atla_rescue_final.lua sólo envía A, captura y observa: no escribe memoria, no altera punteros y no reduce HP. Ruta E0:9927..9E4D, con transición9A1C, transformación9AC9..9BD5, cambio de escena9CD0, personajes9D07/9D0D, transformación9D65..9E0F, salida9E3A/9E3D, bandera global18 activada por opcode70 en9E44. Al final: D2,piso60,730C pasa80→81 y comienza el combate. Capturas y estados de9D07/9E44 permiten retomar exactamente ese tramo. No es la escena de D1F30.

Cadena q10_final_atla_rescue -> q10_final_atla_boss -> q10_final_atla_ending -> q10_final_atla_walk. La segunda etapa sí usa asistencia explícita: HPjefe5A32=1 y HP/máximo jugador500, mantenimiento cada60frames. La escena de rescate se completó antes de aplicar esa ayuda. Créditos, pueblo y movimiento posterior documentados. El máximo524 posterior procede del desarrollo del juego, no de una nueva afirmación de guardado.

La variante retrospectiva que congelaba según Yahoo sigue sin pasos exactos. La escena ensayada pasa, pero eso no corrige ni descarta aquel fallo. No hay modificación binaria de Atla. Se cotejan iguales enJP/HF7 los guiones009900..009EFF, el creador de actores14DD50..14DDB5 y el manejador de banderas140000..14008B. El blog de juego consultado sobreD2 aporta orientación narrativa y es dePS; no acredita el comportamiento deWS.

## Reutilización entre candidatas

run.json fija los hashes de cada ejecución. La matriz92 usa53f7309816536ac970f5fe5e02b6e2e2e9d358e5367ce9786450a7d3701d5f78. La cadena completa Atla usa31d1a3ddeccb2aaf58c2e903aadf6390c2a36ccfe81a2f31c37c0d156bd4c681. La entrega final cambia respecto de esa candidata únicamente mapas/tiles exclusivos del título y checksum. Código, textos de eventos, TitanSaddle y guardado son idénticos; se reutiliza esa evidencia con este límite explícito. q10_release_title_verified y q10_release_items_verified usan la ROM final. No se transfiere una aprobación global.

q10_atla_rescue fue un fallo del observador: createSavestate desde endFrame bloqueó la captura al llegar al primer hito. Se corrigió al registrar un callback de ejecución de un solo uso. No cuenta como bloqueo del juego. q10_atla_rescue2/3 y final_atla_rescue son los controles corregidos. Otras candidatas de título se conservan como diagnóstico, no como entrega.
