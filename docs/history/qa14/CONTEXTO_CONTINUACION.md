# Continuación después de HF10 / QA14

Autoridad: manifest.json, docs/issue_register.json, docs/QA14_VALIDATION.json y docs/QA14_PLAN_ITERACIONES.json. HF10 sí cambia la ROM: 370 bytes del título/checksum frente a HF9. Hash final aacb4fc13587eda56923548f8fad9f8dac83ff24d4ddb1a0372cddcb3475f39f. BPS acumulativo contra JP CCAA4853.

TR-03: PASS_VISUAL_CONTEXT_MASKED_RUNTIME. Dibujo principal recibido conservado; subtítulo recompuesto como glifos nativos. 23 caracteres del título principal y 13 del subtítulo revisados. Mismo revisor, no experimento humano independiente. 1001 cuadros de HF10: píxeles fuera del subtítulo idénticos a QA11; entrada al menú comprobada. No rediseñar el logo ni repetir esta prueba sin cambio concreto. user_v01 preserva el arte recibido y QA11; user_v02_subtitle es la fuente compilada actual.

Siguiente acción: iteración 1 de docs/QA14_PLAN_ITERACIONES.json. Definir universo visible de texto antes de conceder cobertura global. Censo actual: getter de 19 familias/2333 entradas/1970 no vacías estructurales. No prueba totalidad de diálogos; familia4 semánticamente no clasificada. 255 IDs de objetos y 96 propiedades de QA10/QA12 son unidades distintas; no restarlos de2333 ni repetir su evidencia vigente.

Dos registros abiertos: TR-01-M maquetación (4 iteraciones base:1,2,3,6) y TR-01-L lingüística (5:1,2,4,5,6). Tres compartidas, total6; previsión6–8 provisional, nunca garantía de máximo8. Recalcular tras inventario. No aprobar fidelidad por tamaño ni presentación por texto fuente.

Los cuatro frentes funcionales aceptados en QA13 siguen PASS_SYNTHETIC por código no relacionado con el título idéntico. No reabrirlos por falta de recorridos naturales. Causas históricas de equipamiento, Atla y reset espontáneo siguen sin reproducirse. Detalles técnicos completos preservados en docs/history/qa13/CONTEXTO_CONTINUACION.md. Cartucho físico fuera de alcance por causa eléctrica establecida por usuario.

Entorno QA14: extraer Mesen completo (83367840 bytes; hash en manifest) y crear settings.json con {} junto al ejecutable para modo portable/testRunner sin pantalla. La primera extracción local quedó parcial; no era un fallo de ROM. Se conservaron sus fallos como diagnóstico. No repetir instalación de Xvfb: no fue necesaria.

Ahorro de tokens: no medido. No hay agentes adicionales.
