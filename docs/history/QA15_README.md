# Chocobo English v1.1 + HF11 TEST · QA15/M1

HF11 corrige el salto de G05:M002: conserva «go» y las dos líneas completas. Cambio acotado de6 bytes respecto a HF10; PASS_SYNTHETIC con consumidor nativo y confirmación. Maquetación global y revisión lingüística permanecen abiertas.

Aplicar `patches/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps` directamente a la ROM japonesa CRC32 CCAA4853. No incluye ROM, BIOS ni emulador.

Construir: `python3 build.py JP.ws --out build`. Python3, sin dependencias externas para construir. Verificación independiente BPS: `python3 tools/verify_independent_bps.py JP.ws`.

Verificar alcance actual: `python3 qa15/verify_scope.py --japanese-rom JP.ws --out validation.json`. Rehacer censo: `python3 qa15/inventory_layout.py --rom build/Chocobo_EN_v1.1_HF11_TEST.ws --label HF11 --jp JP.ws --out census`.

Autoridad actual: manifest.json, docs/issue_register.json, docs/QA15_VALIDATION.json y docs/QA15_PLAN_MAQUETACION.json. Véanse INFORME_ES.md, docs/QA15_FORMATOS_Y_CONTROLES.md y qa15/layout_alerts_remaining.csv. Informes QA14 y anteriores conservan alcance y versión históricos; su manifiesto está preservado en docs/history/qa14.

M1 terminada con inventario acotado y un arreglo. M2/M3/M4 pendientes;13 alertas abiertas, una reproducida y12 estáticas. La estimación de3 iteraciones restantes es provisional. El universo por recurso+contexto todavía contiene desconocidos explícitos. No equivale a aprobación global.
