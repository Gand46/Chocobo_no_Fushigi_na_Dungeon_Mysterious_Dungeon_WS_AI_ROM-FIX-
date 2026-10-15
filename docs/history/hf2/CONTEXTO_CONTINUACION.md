# Continuidad — 2026-10-13

Autoridad: manifest.json, INFORME_ES.md y src/corrections.json de 1.1-HF2-TEST. Original CRC CCAA4853; salida A18CFFA6. Build y BPS acumulativo verificados. No repetir HF1 ni afirmar RC.

Hecho nuevo: Lafoss FF reproduce un bucle en 5000:43B3 con CX/DX=FFFF. Protección integrada: hook154392 + bloque15FD40; restaura banco por44CC. Evita hang, NO reconstruye animación/potencia completa.

Silbato: mapa BG2 referencia1A5 en18celdas; descompresión escribe180..1A4 y deja3A50 con glifo previo. Corregir consumidor/recurso con comparación; no restaurar letraJP indiscriminadamente. Evidencia q3_whistle_trace y q3_whistle_dump_jp/hf1.

Dispel antes/después: validado con equipamiento mediante menú, flags09→01 y bebida59→botella64. Compra natural pendiente. Guardado básicoHF2→coldPASS, fuente .sav del juego. EventosJP01–04 pendientes.

Arnés: callback final debe retirarse ANTES de emu.stop. Ignorar los anteriores No data como evidencia del juego si el estado fue sobrescrito. QA3 conserva estados válidos; no usar qa2_legacy para nuevas rutas. Menús pueden ignorar pulsos durante un ataque; comprobar que realmente se abrió/activó el objeto. q3_lafoss_jp_delayed terminó por combate/muerte y NO es una reproducción adicional.

Siguiente: tile silbato y efecto completoLafoss, después ascensor/eventos desde guardado de progreso trazable. HardwarePTS133 y segundo emulador pendientes. No está identificado el causante del bloqueo físico del usuario. Ahorro de tokens no medido.
