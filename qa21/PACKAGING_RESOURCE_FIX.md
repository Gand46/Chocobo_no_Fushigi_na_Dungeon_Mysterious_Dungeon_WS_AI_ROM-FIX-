# Espacio temporal de empaquetado

La primera operación alcanzó dos reconstrucciones coincidentes, pero falló con ENOSPC antes de cerrar el archivo. No se promovió a autoridad. Se conservó el diagnóstico. El empaquetador ahora elimina cada run_dir sólo después de copiar sus logs y artefactos y conservar sus hashes; mantiene las dos extracciones nuevas, la comparación de resultados y la extracción/verificación final. Reduce el pico de cuatro copias completas a dos, sin omitir controles.
