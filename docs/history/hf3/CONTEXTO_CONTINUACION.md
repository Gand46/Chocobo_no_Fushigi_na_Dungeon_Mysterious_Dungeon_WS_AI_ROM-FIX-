# Continuidad — HF3 TEST, 2026-10-13

Autoridad: manifest.json, INFORME_ES.md, docs/issue_register.csv y src/corrections.json. Original CCAA4853; HF3 302765E7 / SHA 85a8be61fdac2feb777ed1726235b46b36f8950265a1788e7d7c9a0bc90f4b11. BPS acumulativo original→HF3. No repetir HF1–3 ni afirmar RC.

El usuario estableció causa eléctrica del bloqueo físico. Cerrado fuera de ROM; no reabrir esa incertidumbre.

Silbato reparado: tiles0..36 preservados; tres sólidos2/1/3 agregados; normalización18celdas de paleta al píxel equivalente. Nuevos recursos10C800/13FC60, punteros100078/130040. 2399frames comparados, 2204idénticos,192sólo18celdas,3transición638–640 revisados. Recurso y modelo original demostrados por trazas. Ver docs/whistle_comparison.json, evidence/qa4.

Lafoss: protección HF2 conservada, nuevo origen del modeloFFFF en selector4000:226C, tablaROM14229F, itemSRAM6B14=FF, llamada4000:2252→5000:432C. No usar Flare sustituto ni declarar daño/animación completos. q4_lafoss_origin guarda pila. El efecto completo sigue abierto.

Dispel HF3 antes/después de equipar maldición: bebida59→64, equipo09→01; adquisición artificial. GuardadoHF3 nativo y carga en nuevo proceso sin savestate PASS básico. No extiende aprobación a eventos avanzados. Evidencia conserva estadoHF1 temprano de origen y cadena del .sav.

Pendientes: TR01 revisiónglobal, TR03título, EN01casosavanzados, EN02efectocompleto, EN03compranatural, JP01ascensor/eventos/guardado, JP02finalsegunda, JP03warp99→30, JP04Atla. Faltan estados de progreso trazable para JP01–04; no inventarlos ni marcar PASS. Segundo emulador/hardware siguen pendientes. Priorizar Lafoss y progreso avanzado comprobable. Corte universal40min, no bucles de navegación largos.

Arnés: conservar eliminación callback final ANTES de emu.stop; PNGloaded y frame1 pueden ser inválidos antes de primer render. La bolsa puede ignorar pulsos durante ataques. Comprobar selección real de objeto, no inferirla de los botones enviados.
