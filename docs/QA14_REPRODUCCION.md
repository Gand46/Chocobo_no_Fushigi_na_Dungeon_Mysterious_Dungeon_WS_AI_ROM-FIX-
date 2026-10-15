# Reproducción QA14

Usar JP SHA-256 del manifest. El paquete no contiene ROM/BIOS/Mesen. Mesen 2.1.1: SHA-256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41, 83367840 bytes. Preparar un directorio portable propio, con settings.json conteniendo `{}` y un Saves vacío. El perfil y los archivos de prueba son desechables. En este entorno el ejecutable se ejecutó desde /tmp.

```sh
python3 build.py JP.ws --out build
python3 tools/verify_independent_bps.py JP.ws
python3 qa11/run.py build/Chocobo_EN_v1.1_HF10_TEST.ws - qa11/title_animation.lua out_title --mesen /ruta/perfil/Mesen --timeout 45
python3 qa11/run.py build/Chocobo_EN_v1.1_HF10_TEST.ws - qa11/title_menu.lua out_menu --mesen /ruta/perfil/Mesen --timeout 35
python3 qa14/verify_scope.py --japanese-rom JP.ws --out revalidation.json
```

El verificador compara la evidencia empaquetada:1001 cuadros frente a QA11, fuente del subtítulo, identidad de dibujo principal, pares de glifos y diff binario. No equivale a una nueva lectura humana de cada glifo. Para una ejecución nueva, conservar su salida separada y comparar sus cuadros con evidence/qa14_runs.

Regenerar recursos artísticos (Pillow/NumPy): `python3 tools/integrate_title_assets.py JP.ws --out title_edits.json --report title_report.json`. El comando usa user_v02_subtitle; no escribe corrections.json salvo --write-source. El build ordinario usa los rangos comprobados, sin dependencias gráficas.

Método de las dos corridas finales: SCRIPTED_NATURAL, sin estado inicial ni pokes de memoria. title_animation captura300..1300; title_menu pulsa A/Down/Up. Los checkpoints resultantes pertenecen al hash HF10 y se incluyen sólo como evidencia de esos arranques; no prueban recorridos completos.

Los primeros dos juegos de recortes en qa14/ son diagnósticos de segmentación. glyph_review.json conserva33/36 del diseño anterior; únicamente los23 caracteres de sus bandas0/1 se transfieren por identidad exacta del dibujo principal. hf10_visible_transcription.json registra la lectura del nuevo subtítulo antes de comparar la clave. hf10_subtitle_review.json registra13/13. La misma persona/agente conoce el proyecto: es lectura con contexto de palabra oculto, no una segunda revisión independiente.
