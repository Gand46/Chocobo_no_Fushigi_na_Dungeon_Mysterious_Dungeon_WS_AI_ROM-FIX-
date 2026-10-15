CHOCOBO — HF11 TEST / QA15
MAQUETACIÓN GLOBAL · ITERACIÓN 1 DE 4 · 14-10-2026

Resultado
Se completa M1 como inventario acotado y una corrección comprobada. La maquetación global y la revisión lingüística continúan abiertas. Quedan 3 iteraciones base de maquetación; la estimación depende de cerrar los contextos todavía desconocidos.

Corrección aplicada
G05:M002: el motor admitía 13 celdas por línea y consumía el glifo «go» como celda 14 sin dibujarlo. El siguiente salto explícito provocaba otro avance y borraba la primera línea antes de confirmar. HF11 mueve ese salto delante de «go»:
Using it, you can easily
go from 2F to 1F!
Se conservan todos los glifos, su orden, el tamaño, el terminador y las pausas. Sólo cambian 6 bytes en065220..065225; código, punteros, fuentes y el resto de la ROM son idénticos a HF10. El checksum E1F6 permanece igual porque es una permutación de los mismos bytes.

Prueba: PASS_SYNTHETIC, SAVESTATE + POINTER_INJECTION. Se seleccionó el recurso dentro del consumidor nativo, sin dibujar texto artificial. Antes se registró la pérdida de0106 en columna 13. Después aparece en línea 1/columna 0, no hay avance automático por exceso, ambas líneas se leen completas y A consumeFFFF y permite continuar.500 cuadros; proceso completado con salida0. Esto no acredita llegada natural al diálogo ni fidelidad de toda la traducción.

Inventario y cobertura
•141 configuraciones de ventana,79 geometrías distintas.14 IDs observados, incluido0; no son14 interfaces exhaustivamente aprobadas.
•19 familias del getter:2333 referencias,1972 no vacías estructurales. Corregida la medición de dos entradas con colas compartidas. Iconos y números se separan del texto.
•14 grupos secundarios:3488 referencias,3472 punteros distintos;886 entradas con celdas literales. El resto son entradas vacías o sólo controles. No equivalen a3488 diálogos únicos ni constituyen por sí solas el universo visible completo.
•24 vínculos ventana/familia/índice observados en cuatro familias. Cuatro IDs de mensaje observados; acceso y procedencia están registrados por ejecución.
•Controles de pausa, salto, fin, formato y sustitución catalogados.9 recursos con sustituciones numéricas localizados. Muestra sintética de inventario con +99 legible; no aprobación de todos los valores.

Pendientes concretos
HF10 produjo 14 alertas por más de13 celdas literales. HF11 resuelveG05:M002. Quedan 13 alertas: G01:M031, G01:M039, G03:M012, G04:M031, G04:M034, G04:M048, G06:M022, G06:M099, G08:M020, G09:M063, G16:M004, G16:M064 yG16:M070.
G03:M012 se reprodujo sintéticamente: se pierde el tercer00DD y queda un sufijo visible de letras f. Requiere maquetación y revisión del texto de origen. Las otras 12 son candidatas estáticas, NO12 fallos confirmados. Algunas exceden por relleno yG16:M064 parece un recurso compuesto de tienda; hay que verificar consumidor y desplazamiento antes de modificarlo. El detalle exacto está enqa15/layout_alerts_remaining.csv.
Faltan vínculos de muchas ventanas y familias, variantes de variables, consumidores especiales y el mapeo completo de créditos. Los créditos vistos no se atribuyen al getter sin evidencia. La cobertura anterior de objetos/propiedades se conserva; no se suma a estos denominadores como si fueran la misma unidad.

Siguientes 3 iteraciones
M2: interfaces, inventario, estados, tiendas y límites de variables; cubrir contextos restantes y corregir defectos demostrados.
M3: diálogos, tutoriales, eventos, créditos, paginación y13 alertas; coordinar los cambios que necesiten revisión lingüística.
M4: integración, regresión de textos modificados, conciliación de cobertura y cierre verificable.
No se concede PASS global ni se promete que lo desconocido ya esté cubierto por ese número de iteraciones.

Entrega
Parche BPS acumulativo: aplicar directamente a la ROM japonesa CRC32 CCAA4853, sin parches intermedios. Fuentes editables, herramientas, censos, capturas, registros y continuidad incluidos. No se incluye ROM, BIOS ni emulador. La versión sigue siendo TEST.
ROM HF11 SHA256:83de8ad93ddfab014670c9ddeea0e71656da55a0f429512e4182e3c280d759bf
BPS SHA256:87a48858a65e66f4f11b3865869f1c0df499317b56fbeae19f2335fcfff9e183

Limitaciones y diagnósticos
El primer intento HF11 obtuvo capturas pero terminó por timeout y no se acepta como PASS. La repetición final completó500 cuadros, confirmó continuación y no registró error de volcado; la causa exacta del intento inicial no se atribuye a la ROM. Los ensayos iniciales sin lecturas narrativas no cuentan como cobertura de diálogos. Se corrigió además un valor fijo desactualizado de la prueba de manifiesto, para que compruebe4310 bytes respecto a la base inglesa. Los PASS funcionales QA13 y el logo QA14 se heredan por identidad de todos los bytes ajenos al recurso modificado.
Ahorro de tokens: no medido. Sin subagentes. Una sola revisión visual con contexto de fuente; no estudio humano independiente.
