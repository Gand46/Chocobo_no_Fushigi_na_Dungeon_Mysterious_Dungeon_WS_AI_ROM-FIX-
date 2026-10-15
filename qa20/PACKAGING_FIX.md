# Corrección del empaquetador en QA20

El primer intento formal completó dos reconstrucciones binarias exactas, pero la verificación final del ZIP falló con PACKAGE_INDEX_MISMATCH: el índice contenía su propia versión anterior. No se promovió ni distribuyó ese paquete.

En tools/continuity.py, zip_tree excluye explícitamente package_index.json de los miembros que dicho índice autentica. Así cumple el contrato del extractor, que ya excluye el índice de su inventario comparado. No se omiten otros archivos ni se relajan verificaciones de hash, reconstrucción, herencia o BPS. Un ensayo de dos generaciones sobre un árbol mínimo comprueba ausencia de autorreferencia y pertenencia completa de todos los demás miembros. El paquete final vuelve a ejecutar el ciclo completo.

Se conservan intactos ROM HF15 y BPS. Los locks residuales de procesos ya terminados se diagnosticaron y apartaron antes del nuevo intento; no se terminó ningún proceso con PID reutilizado.
