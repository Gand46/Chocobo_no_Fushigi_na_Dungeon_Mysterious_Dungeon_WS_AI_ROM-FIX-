# Chocobo English v1.1 + HF10 TEST · QA14

HF10 mejora la legibilidad del subtítulo «for WonderSwan» con una fuente del título en cuadrícula nativa. Conserva el dibujo principal aportado. 36 caracteres revisados (23 sin cambios y 13 corregidos), 1001 cuadros nativos y transición al menú comprobados. Revisión contextual del mismo agente, sin segundo revisor independiente.

Aplicar `patches/Chocobo_EN_v1.1_HF10_TEST_JP_CCAA4853.bps` **directamente a JP Rev2 CRC32 CCAA4853**, sin parches intermedios. No se distribuyen ROM, BIOS ni emulador. La versión sigue siendo TEST.

Construir: `python3 build.py JP.ws --out build`. Python 3, sin dependencias externas para el build. Aplicador independiente: `python3 tools/verify_independent_bps.py JP.ws`.

Verificar QA14: `python3 qa14/verify_scope.py --japanese-rom JP.ws --out revalidation.json` (Pillow y NumPy). Reproducción: `docs/QA14_REPRODUCCION.md`. Fuente artística recibida preservada en `assets/title/user_v01`; integración actual en `assets/title/user_v02_subtitle`.

Maquetación y revisión lingüística global permanecen abiertas y separadas. Plan base: 6 iteraciones coordinadas, previsión provisional 6–8, recalculada tras el censo completo. Detalle en `docs/QA14_PLAN_ITERACIONES.md` y `docs/issue_register.json`. Los PASS_SYNTHETIC de QA13 se heredan por identidad del código no relacionado con el título.

Autoridad actual: `manifest.json`, `INFORME_ES.md` y `docs/QA14_VALIDATION.json`. Los informes anteriores conservan su alcance y versión históricos. Los lanzadores Windows/macOS no se han probado de nuevo.
