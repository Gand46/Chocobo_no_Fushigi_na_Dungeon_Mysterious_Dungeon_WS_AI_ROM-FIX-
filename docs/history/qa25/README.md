# Chocobo English v1.1 HF19 TEST — QA25

Esta es la fuente acumulativa vigente. QA24 revisa con Astra las 11 reservas de HF18. Corrige cuatro recursos story (dinero, depuración y dos sufijos temporales) y dos etiquetas del bestiario. El cierre es **lingüístico y visual sintético de recursos**; no es aprobación global ni recorrido natural.

QA25 añade una auditoría de distribución de texto **sin cambiar la ROM ni el BPS**. El informe `QA25_HF19_Auditoria_Distribucion_Texto.html` y `qa25/README.md` explican el barrido de los 886 recursos literales, la revisión de 128 capturas históricas de 99 alertas y seis repartos candidatos aún no aplicados. Ninguna alerta por sí sola prueba un error visual.

- V1–V5: 886 referencias literales revisadas; 886 aprobaciones de recurso acotadas tras QA24.
- QA24: 23 sesiones nativas, 5.625 cuadros, 0 glifos no blancos descartados; 176 controles y 13 pruebas del proyecto.
- Delta HF18 → HF19: 97 bytes; fuente, motor y código preservados.
- Informe autocontenido: `QA24_HF19_Informe_Consolidado_V1-V5.html` (946 imágenes y 886 fichas).
- Estado vigente: `docs/approval_matrix.json`, `qa24/resolution.json`, `PROJECT_CONTEXT.md`. Los informes QA19–QA23 y notas previas son históricos.

## Reconstrucción

Se necesita Python 3.10+ y la ROM japonesa limpia de 2.097.152 bytes, CRC32 CCAA4853, SHA256 `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`. No se incluye ROM, BIOS ni emulador.

Windows: `BUILD.bat "C:\ruta\Japanese.ws"`.

Windows/Linux/macOS: `python3 build.py /ruta/Japanese.ws --out build` (usar `py -3` en Windows). No requiere paquetes anteriores.

Regeneración semántica independiente: definir `CONTINUITY_INPUT_JP` con la ruta absoluta de la JP y ejecutar `python3 qa24/release_build.py`. Reconstruye HF18 desde recetas heredadas incluidas, regenera las dos etiquetas F17 desde texto editable, regenera cuatro cambios story y exige igualdad byte por byte con la receta canónica.

Fuentes editables: `qa24/story_repairs.json`, `qa24/getter_translations.json`, sus regeneradores; fuente acumulativa `src/corrections.json` y `src/legacy_translation_ranges.json`. Para hacer una nueva corrección, regenerar los edits, integrar con `qa24/compose_cumulative.py` y actualizar conscientemente hashes y validación; editar sólo un JSON de traducción no modifica automáticamente el parche publicado. El código original del juego no se atribuye a este proyecto.

## Pruebas

- `python3 -m unittest discover -s tests -v`.
- Con `CONTINUITY_INPUT_JP`: `python3 qa24/verify_scope.py`.
- Auditoría QA25: seguir `qa25/README.md`. Su informe no modifica el parche; las seis alternativas necesitan una siguiente prueba de reflujo en ROM de trabajo.
- Mesen 2.1.1 SHA256 `ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41`, perfil portable con `settings.json` cuyo contenido sea `{}`. No necesita Xvfb.
- Repetir un caso: definir `LAYOUT_OBSERVER` con ruta absoluta a `qa21/layout_observer.lua`; ejecutar `python3 qa21/run.py ROM ESTADO PLAN SALIDA --mesen EJECUTABLE --timeout 15`. `SALIDA` debe ser nueva. Estado de diálogo: `evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss`; los planes exactos y hashes están en cada carpeta `evidence/qa24_runs/`. Para bestiario, la orden y el estado usado constan en `run.json`; reconstruir rutas desde el paquete y conservar los hashes.
- Un solo proceso por perfil Mesen; no reutilizar SRAM concurrentemente. Los scripts históricos con rutas de sesión son procedencia, no la receta actual.

## Límites que permanecen

Las 11 reservas no requieren una decisión manual de traducción, pero quedan pendientes las rutas naturales y composiciones anfitrionas indicadas en `qa24/resolution.json`. Los dos sufijos se aprobaron aislados; no se probó cantidad máxima ni singular/plural de su anfitrión. El dinero 9.999.999 es extremo del formateador, no máximo alcanzable acreditado. Ruin Cannon usa una fila de bestiario sintética y no se atribuye a Omega. Sin revisión global de todos los 2.333 getters y gráficos, sin hardware ni segundo emulador. `FINAL_APPROVED=false`.

El BPS `patches/Chocobo_EN_v1.1_HF19_TEST_JP_CCAA4853.bps` se aplica directamente a la JP limpia. SHA-256 ROM HF19 `f27e69f65e134b161c1f3ce263c3ed78a8ae247997c95d7383c43c4a78c8962f`; BPS `c1984adda38b7d34291c1d65ba4da0df79ccc5ddb08c384787725188e53e648a`.

La entrega formal usa `tools/continuity.py release`: dos reconstrucciones independientes desde ZIP, BPS roundtrip e inventario. La integridad sólo acredita la herencia desde la adopción del proyecto, no material perdido antes de ella.
