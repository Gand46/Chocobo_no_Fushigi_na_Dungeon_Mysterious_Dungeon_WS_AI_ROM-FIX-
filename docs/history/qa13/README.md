# Chocobo English v1.1 + HF9 TEST · QA13

QA13 amplía pruebas y confirma el fix existente del mapa 99→30. **No cambia los bytes de HF9 ni su BPS.** Equipamiento, Atla, ascensor y guardado tienen PASS_SYNTHETIC en el alcance de `INFORME_ES.md`; sus causas históricas no reproducidas se identifican por separado.

Aplicar `patches/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps` directamente a JP Rev2 CRC32 `CCAA4853`, sin parches intermedios. No se distribuyen ROM, BIOS ni emulador.

Construir: `python3 build.py JP.ws --out build`. Python3, sin dependencias externas. BPS independiente: `python3 tools/verify_independent_bps.py JP.ws`.

Verificar esta revisión: `python3 qa13/verify_scope.py --runs evidence/qa13_runs --out qa13/revalidation.json`.

Reproducción en emulador y acceso sintético: `docs/QA13_REPRODUCCION.md`. Resultados y descartes: `docs/QA13_RUN_INDEX.json`; `docs/QA13_VALIDATION.json`. Pendientes vigentes: `docs/issue_register.json`. Historia completa preservada, incluidos QA12 y el logo aportado en `assets/title/user_v01`.

No se concede aprobación global de maquetación, lingüística, hardware ni glifos del logo. Los lanzadores Windows/macOS permanecen conservados, sin prueba nueva en esos sistemas.
