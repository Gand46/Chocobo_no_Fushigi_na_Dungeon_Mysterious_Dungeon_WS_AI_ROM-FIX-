# Resultado QA16 / M2

16 PASS_SYNTHETIC acotados; 36 ejecuciones archivadas. La ROM y el BPS HF11 permanecen idénticos. Estado, magia, inventario y compra/venta están vinculados a sus consumidores. Se verificaron 97 vínculos ventana/familia/recurso en 12 tipos de ventana, con 343 comprobaciones de integridad, procedencia, transacciones y reconstrucción. No son 343 recorridos ni una aprobación visual global.

Candidato M2-C01, preset 32 / F00:I053: la segunda página forzada recorta una pregunta de pisos. Falta un caller válido. No se otorga PASS ni se cambia la ROM por esa prueba. No es una regresión introducida en M2.

Los valores y las transacciones exactos están en `docs/QA16_VALIDATION.json` y `docs/QA16_RUN_INDEX.json`. Las lecturas visuales están en `qa16/visual_readings.json`; el informe con capturas, en `qa16/Chocobo_QA16_M2_Informe.html`.

M3 y M4 siguen pendientes. Las 13 alertas narrativas de M1 y la revisión lingüística no se cierran aquí. M2 es una iteración ejecutada con alcance acotado, no un barrido exhaustivo de todas las variantes de interfaz.

QA16 final: `magic_display99` sustituye al ensayo `magic_boundaries` en la lista de PASS. Los valores 99 se muestran completos (Lv.99, ATB99 y NEXT99P). El ensayo anterior con 255 se conserva como diagnóstico excluido porque supera el formato de dos cifras. No demuestra un defecto alcanzable de la ROM.
