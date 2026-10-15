# Continuación — partir de HF14 / QA19 V1

Solicitado: aprobación visual/lingüística global, validación 1 de 5. V1 ejecutada; quedan V2–V5, no una supuesta aprobación global completa.

Prioridad siguiente: V2 (248 referencias de G00–G05), leer japonés/inglés y comprobar los consumidores reales de menú y guardado, incluidos G16:M000, M003 y M004. No volver a correr indiscriminadamente las pruebas de las causas históricas. Usar five_validation_plan.json para evitar duplicar cobertura.

G16:M073 necesita frase anfitriona; mantiene contexto pendiente. preset32/F00:I053 sigue sin consumidor válido, no confundir pruebas forzadas con bug natural. Los tres candidatos horizontales estáticos siguen siendo G01:M031, G06:M022 y G09:M063; conservan el análisis histórico y no son fallos nuevos demostrados.

Reanudar desde checkpoints en evidence/qa19_runs/release2_*; base general evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss, consumidor Slot evidence/qa16_runs/shop_enter/checkpoint.mss. Mesen y driver fijados en manifest/run.json. Una sola instancia de Mesen a la vez. No usar código de salida como PASS: exigir target_completed, FFFF exterior (estado sin bit40), páginas leídas e integridad de las variables. La pausa lleva bit80; en el automatismo comparar estado & 7F.

En text_codec.py, los glifos de una letra del lado derecho se reservan para prefijos sin digrafo; los finales usan el lado izquierdo. La fila y es irregular y «yo» fue sustituido en la fuente. No inferir automáticamente todo el mapa por aritmética. Las frases entregadas están verificadas visualmente.

La versión se mantiene TEST. PASS sintético autorizado por el usuario no prueba recorrido natural, segundo emulador o hardware. Mantener entregas de fuentes acumulativas completas + BPS directo JP + evidencia, sin ROM. Conservar límite de emergencia de 40 minutos por turno; guardar checkpoint antes de cortar.
