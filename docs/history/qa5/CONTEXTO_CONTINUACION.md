# Continuidad HF3 / QA5

ROM y BPS HF3 byte-idénticos; no generarHF4 sin cambios. Ver INFORME_ES.md, qa5/save_code.txt y evidence/qa5_provenance.json.

Guardado: bloque2516bytes6BD8→75B6; firma n_c1 en75B0; firma A_C1 en75AC; validez75B4. Cambiar75B0 oculta partida sin borrar payload. Cambiar765B nivel1→2 se acepta. Guardar/cargar no borra firma normal. Rutina explícita18C813 borra firma. Rango190333..190401 igualJP/EN. Lafoss bloqueaJP/EN pero no toca bloque existente; coldload posteriorPASS.

Fixture D3coherente piso33 funciona con flags730a8000/730c4. Las inicialesD2/D3 pasan aD1 y NO validan escenas tardías. D2piso60 blanco: bucle4000:8393 espera4B54; filtroEAFB retorna0 cuando0647=0. ScriptD34E escribe7301=1. Seguir banco649B/puntero64A1, completar condiciones coherentes antes de parchear. No confundir bloqueo de estado sintético incoherente con reporte naturalJP01/02.

Chat completo Analizar bloqueo de Chocobo no recuperable en esta sesión; PDF y fuentesS02/S03/S06/S07 revisados. Atla fuente inaccesible. Fallo físico eléctrico fuera del alcance. No reabrirlo.

Las ejecuciones con timeout están excluidas. save_write_trace_recorded.lua es plan original de q5_save_trace, cuyo nombre de trabajo fue reutilizado. Próximo: coherenciaD2, ascensor/eventos, fuente/rana, warp99→30/Atla; luego Lafoss completo y traducción restante.
