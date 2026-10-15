# Continuidad HF3 / QA6

ROM/BPS HF3 sin cambios: CRC302765E7. Estado vigente en INFORME_ES.md; QA5 queda como historial en docs/history/qa5.

Usuario: cartucho físico resuelto por causa eléctrica, fuera de ROM. Objetivo: parche acumulativo japonés→inglés con fixes; investigar guardado desde datos y fallos originales.

Chat compartido recuperado: https://chatgpt.com/share/6acebdec-2b5c-83e9-833e-60560c52d788. 58 mensajes textuales visibles; diez incidencias, ninguna nueva distinta. Hay salida de complementos censurada. Sólo metadatos/software se incluyen en qa6/chat_review.json; no HTML de sesión.

Nuevo tools/validate_chocobo_save.py: sólo lectura, 32768 bytes; separa firmas75AC..75B3, caché75B4 y payload75B6..7F89. Comparación confiable por generación, mezcla prefijo nuevo/resto antiguo y copia de carga exacta. No repara archivos ni certifica todos los eventos. 35 comprobaciones PASS; diez copias de2516bytes en cinco cargas frías; siete sesiones completadas.

SAVE-01: guardar190367 copia primero y sólo después reescribe n_c1; no invalida firma antigua. Captura tras200 escrituras conserva200bytes nuevos+2316antiguos y se acepta en frío JP/HF3. B artificial cambia nivel, HP y contador. No es aún causa demostrada de los foros. No añadir guard global ni checksum sin diseñar compatibilidad/espacio/recuperación.

Rectificación QA5: máscara de word730A debe ser0080, NO8000. La bandera script0F es word7309 bit15. RamaE1:58F2 asignaD1,58F9D2,5900D3; registroescritura scriptpuntero58FD muestraD2. qa6/dungeon2_before_60_correct_flag.sav elimina biterróneo730B80 y pone730A80. Carga exacta, D2/60 escena de jefe, diálogo avanza. Pantalla blanca anterior era defecto de fixture. Fuente/rana/segundofinal todavía no validado; D3 requiere validar progreso completo también.

Reproducción de copias: puntos9000:0373/037F/038B para guardar;9000:0333/033F/0359 al cargar. Los cambios de SRAM de trabajo/caché no son pérdida del payload. Run QA6 registra input_save y salida nativa; primer run q6_save_overwrite tiene provenance.json para SAVE_FIXTURE.

Siguiente: partir de progreso trazable para fuente/rana y ascensor; comparar datos en los mismos puntos, vigilar primera escritura divergente. EN01 equipo, JP01 ascensor, JP02 final, JP03 99→30 y JP04 Atla abiertos. Lafoss efecto completo, título y revisión global de texto pendientes. BPS anterior y fixes silbato/Lafoss permanecen.
