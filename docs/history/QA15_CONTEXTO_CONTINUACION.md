# Continuar desde HF11 TEST / QA15 M1

M1 de maquetación finalizada. Siguiente: M2 de4, interfaces y variables. Autoridad: manifest.json, docs/QA15_VALIDATION.json, docs/QA15_PLAN_MAQUETACION.json, docs/issue_register.json. No volver a usar HF10 como base de trabajo final.

HF11 = HF10 con 6 bytes reordenados en065220..065225 para G05:M002; checksumE1F6. ROM83de8ad93ddfab014670c9ddeea0e71656da55a0f429512e4182e3c280d759bf. BPS acumulativo desdeJP CCAA4853. No cambia glyph order, size, pointers, code, title or save. Prueba actual: evidence/qa15_runs/hf11_dialogue_final,500 frames,exit0,POINTER_INJECTION. hf11_dialogue_go es intento incompleto/timeout, noPASS.

Censo: qa15/census_final.141 presets(79geometrías);19 familias/2333refs/1972no-vacías;14 grupos secundarios/3488refs/886con celdas literales. No son universos únicos de pantallas/frases. MediciónF00:I075/I076 corregida por colas compartidas. Getterfamilias4/16iconos y9/18numéricas.14 IDs de ventana observados incluido0,24 vínculos getter. Los consumidores aún desconocidos y los créditos se deben mapear; no inventar cobertura a partir de tablas.

Hay13 alertas restantes enqa15/layout_alerts_remaining.csv. G03:M012 está reproducida: tercer00DD se pierde y quedan f residuales. Las12otras no son fallos confirmados; relleno y recursos compuestos necesitan contexto. No alterar automáticamente FFF2/FFFE/FFFF ni aplicar límite13 al recursoG16:M064 sin trazar consumidor. M3 atenderá diálogos/eventos/créditos y alertas.9 recursos numéricos dinámicos identificados; muestra+99 sólo prueba ese caso.

TR-01-L continúa separado y abierto. No confundir control de ancho con fidelidadJP→EN. QA13 funcional y logo QA14 se heredan por bytes idénticos fuera de6 bytes. No repetir rutas naturales ni logo como requisito de cierre sintético ya autorizado.

Reproducción Mesen: ejecutable83367840bytes/hashae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41,settings.json={} junto al ejecutable; no necesitaXvfb. qa15/run.py acepta ROM,checkpoint,plan,out,--mesen; LAYOUT_OBSERVER debe apuntar aqa15/layout_observer.lua. Estados y dependencias por hash en cada provenance.json. Observadorv1 en primeras3ejecuciones;v2 agrega motor narrativo. Driverqa15 conserva excepción de volcado en dump_error.txt; comprobar ausencia, exit0 y completed.txt. No ejecutar dos procesos sobre el mismo perfil simultáneamente.

Ahorro de tokens no medido; sin agentes adicionales. Fecha14-10-2026. Tres iteraciones base restantes, reevaluar si el contexto real excede los lotes.
