# Chocobo’s Mystery Dungeon — WonderSwan title localization

**v0.1 · ART-REVIEW · 2026-10-14**

Diseño inglés del título a **224 × 144 píxeles**, con cuatro tonos, elaborado a partir del GIF japonés aportado y del lettering de la referencia de Switch. Este paquete contiene recursos gráficos editables y una reproducción offline de la animación. **No modifica una ROM ni constituye una versión jugable.**

## Resultado

- `Chocobo’s Mystery Dungeon`, con subtítulo `for WonderSwan`.
- 91 cuadros PNG y GIF, 6 estados distintos, 4 poses de Chocobo, 6.070 ms.
- Tiempos originales de 60/70 ms, incluido el parpadeo de `PUSH BUTTON`.
- Píxeles móviles y primeras 56 filas idénticos al original en todos los cuadros.
- Rótulo fijo: el GIF de referencia no anima las letras. Reutilizar el mismo rótulo evita vibración o deformación entre cuadros.
- Exportación de 315 patrones de 8 × 8 a 2bpp: 5.040 bytes; seis mapas de 1.008 bytes, más deltas de mapas.

`EVERY BUDDY!` se utiliza únicamente como referencia visual de lettering. Ese subtítulo no forma parte del título japonés de esta entrega y no se incorpora.

## Archivos

| Ruta | Uso |
|---|---|
| `assets/` | PNG nativos editables, máscara binaria y configuración de composición |
| `authoring/` | Maestros de diseño generados; no son recursos nativos de la consola |
| `references/` | GIF original y referencia gráfica suministrada |
| `tools/prepare_assets.py` | Conversión determinista de maestros a los PNG nativos |
| `tools/build.py` | Compilador de cuadros, GIF, recursos 2bpp y comprobaciones |
| `build/frames/` | Los 91 cuadros ordenados, sin omitir cuadros sostenidos |
| `build/unique/` | Los seis estados visuales distintos |
| `build/timeline.csv` | Orden, tiempos, pose, parpadeo, estado y hash por cuadro |
| `build/tiles/` | Patrones 2bpp, mapas neutros y deltas; no son direcciones del juego |
| `build/Chocobo_WS_Logo_EN_Frame_Viewer.html` | Visor offline, comparación y avance cuadro a cuadro |
| `build/validation.json` | Resultados técnicos y límites de validación |
| `docs/ESTADO_Y_DISENO.md` | Decisiones, revisión, limitaciones y siguiente paso |

## Reconstrucción

Python 3.10 o posterior. Dependencias probadas: Pillow 12.3.0 y NumPy 2.3.5.

```text
python -m pip install -r requirements.txt
python tools/build.py
```

En Windows puede usarse `BUILD.bat`; en macOS, `BUILD.command` (requiere Python y las dependencias). En Linux basta el comando Python. La ejecución se comprobó en Linux x86_64; los lanzadores de Windows/macOS se entregan sin prueba en esos sistemas.

Los PNG de `assets/` son la fuente editable preferida: puede cambiarse su dibujo píxel a píxel conservando los índices 0–3 y la máscara. `python tools/prepare_assets.py` regenera esos PNG desde los maestros y **sobrescribe cualquier edición manual de los assets**. No lo ejecute después de retocar los píxeles salvo que quiera reconstruirlos.

El build no requiere red, Mesen, Wonderful, BIOS ni ROM. Las llamadas de generación de imágenes ya realizadas no forman parte de la reconstrucción.

## Estado de integración

**INTEGRATED = NOT_VALIDATED · RUNTIME_CONFIRMED = NOT_VALIDATED · FINAL_APPROVED = false.**

Los recursos caben en un banco de exportación independiente de 512 patrones. Esto **no demuestra** disponibilidad de VRAM, compatibilidad de compresión, asignación de paletas, distribución por capas ni tiempos de carga del juego. Deben resolverse al integrar.

No se entrega BPS porque no hubo modificación de ROM. Una entrega integrada futura deberá partir de la revisión japonesa identificada por hash, incorporar las fuentes acumulativas de traducción vigentes, localizar los recursos/consumidores reales del título y verificar el BPS acumulativo desde esa base.

No se incluyen ROM, BIOS, emulador ni archivos de otros proyectos. Las referencias y el arte derivado conservan los derechos de sus titulares; este paquete no concede una licencia sobre ellos.
