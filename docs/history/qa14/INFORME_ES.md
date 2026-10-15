Chocobo — HF10 TEST / QA14 — 14 de octubre de 2026

RESULTADO
Legibilidad del logo: PASS_VISUAL_CONTEXT_MASKED_RUNTIME en el alcance revisado.
El dibujo principal entregado por el usuario se conserva. Se corrigió únicamente
la representación de «for WonderSwan», mediante una fuente del título definida
en la cuadrícula nativa. No cambia la fuente compartida del juego ni el texto.

La primera lectura aislada de HF9 produjo 33 coincidencias de 36 y tres lecturas
ambiguas en el subtítulo: o→a, r→n y a→r. Los primeros dos juegos de recortes
estaban mal delimitados y se conservaron como diagnósticos, no como pruebas
válidas de un defecto. Las dudas persistentes motivaron mejorar la legibilidad;
no se afirma que el diseño aportado tuviera esas palabras mal escritas.

La revisión final combina 23 caracteres del título principal sin modificar y 13
del subtítulo corregido. El subtítulo se leyó en orden mezclado, sin contexto
de palabra, a escala nativa y con ampliación entera. Resultado 13/13. Las parejas
o/r/n del subtítulo son idénticas en píxeles. Es revisión del mismo agente,
no un segundo revisor humano ni un experimento ciego independiente.

VALIDACIÓN
Mesen 2.1.1, ROM final HF10, arranque sin savestate, sin escrituras sintéticas de
memoria: SCRIPTED_NATURAL. Se capturaron 1.001 cuadros del título (300..1300).
Los píxeles exteriores a la franja del subtítulo (x65..158,y109..120) coinciden
exactamente con QA11. También se comprobó la transición al menú con botones.
El subtítulo coincide con sus fuentes compiladas en los 1.001 cuadros. La animación,
el dibujo principal y el prompt conservan sus píxeles. No se declara hardware.

370 bytes cambian frente a HF9: recursos gráficos/mapa del título y checksum.
Código de animación, tiles 328..391 y código no relacionado con el título idénticos.
Build fijado por SHA-256, BPS ida/vuelta y aplicación independiente: PASS.
HF10: aacb4fc13587eda56923548f8fad9f8dac83ff24d4ddb1a0372cddcb3475f39f
BPS: 841a0d53581caf9ed46bc113880a62ff905b8f5fcc887df89f0f017a4bdfe7c5
Checksum E1F6. Aplicar BPS directamente a JP CRC32 CCAA4853.
No aplicar sobre HF9 u otra ROM ya traducida. Sigue siendo una versión TEST.

DOS TAREAS SEPARADAS
TR-01-M / MAQUETACIÓN GLOBAL: tamaños, recortes, saltos, ventanas, paginación,
variables y glifos visibles. Base: 4 iteraciones (1,2,3,6).
TR-01-L / REVISIÓN LINGÜÍSTICA GLOBAL: fidelidad japonés→inglés, gramática,
naturalidad, terminología y coherencia contextual. Base: 5 iteraciones (1,2,4,5,6).
Las iteraciones 1, 2 y 6 son comunes:4+5−3=6 iteraciones distintas pendientes.
La iteración actual del logo está terminada y no se vuelve a contar.

PLAN BASE DE SEIS ITERACIONES
1. Censo común: clasificar 19 familias; localizar diálogo/eventos/créditos fuera
   del getter; fijar IDs, contextos, glosario y denominador. Recalcular estimación.
2. Interfaces e inventario: cerrar maquetación y revisión lingüística de menús,
   nombres, descripciones y propiedades en los contextos que faltan.
3. Maquetación: diálogos, tiendas, tutoriales, escenas tardías y créditos;
   saltos, ventanas, paginación y variables en consumidores nativos.
4. Lingüística: diálogos principales, relato, voz y terminología JP/EN.
5. Lingüística: ramas tardías, variantes, ayudas, textos especiales y créditos;
   reconciliación del glosario y comprobación contextual.
6. Cierre conjunto: integrar correcciones, volver a validar visualmente los
   textos cambiados, conciliar cobertura y generar el BPS acumulativo.

PREVISIÓN: 6 iteraciones como base; 6–8 como rango de planificación provisional.
Reserva 7 si aparecen recursos/contextos adicionales; reserva 8 para correcciones
que requieran otra pasada. No es una garantía de terminar en 8: el censo de la
iteración 1 puede justificar revisar el total. No se conocen aún todos los diálogos.

BASE REAL DE LA ESTIMACIÓN
El getter censado contiene 2.333 entradas en 19 familias; 1.970 son estructuralmente
no vacías. Las 13.742 palabras de 16 bits incluyen controles/terminadores y NO son
palabras inglesas. Algunas familias aún requieren identificación semántica;
la familia 4 no se da por texto visible. Este censo no cubre demostrablemente todos
los diálogos y scripts. No se publica un porcentaje global de traducción revisada.

QA10/QA12 cubren 255 IDs de objetos y 96 descriptores de propiedades, con sus límites
de versión/contexto. No son unidades directamente restables de 2.333. Reutilizar su
evidencia válida; revisar únicamente huecos, nuevas variantes y textos cambiados.

CIERRE EXIGIDO
Maquetación: cada recurso/contexto del universo definido debe tener evidencia
visual nativa o exclusión justificada; ningún recorte o fallo tipográfico abierto.
Lingüística: cada entrada visible debe tener revisión de sentido JP/EN y contexto,
con glosario coherente. Una comprobación estructural o un PASS visual no prueban
fidelidad de traducción. Todo cambio lingüístico debe volver a pasar maquetación.
Se permite acceso sintético documentado conforme a la autorización del usuario.

CONTINUIDAD
Se mantienen los PASS_SYNTHETIC funcionales de QA13 por identidad del código no
relacionado con el título; no se ejecutaron de nuevo esas baterías. No se reabren
por falta de acceso natural. Las causas históricas no reproducidas siguen con
esa clasificación; no se presentan como correcciones nuevas.

Fuentes, observaciones literales, intentos descartados, capturas, scripts y plan
estructurado se incluyen en el paquete QA14. Los recursos originales user_v01
se preservan; la compilación actual usa user_v02_subtitle. El paquete no incluye
ROM, BIOS ni ejecutable de emulador. Ahorro de tokens: no medido.
