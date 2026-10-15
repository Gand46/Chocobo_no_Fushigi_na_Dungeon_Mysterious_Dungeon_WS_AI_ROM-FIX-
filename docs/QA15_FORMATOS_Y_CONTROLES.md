# QA15 · Ventanas, saltos y variables

Alcance: análisis estático del motor y muestras nativas. Las celdas de16 px suelen contener dígrafos; contar caracteres Unicode no mide el ancho real.

## Ventanas de interfaz

Tabla ROM183F70:141 registros de6 bytes, termina1842BE. Inicializadores1842D0..1843EA y consumidores de filas186D46..186E60 tienen el mismo denominador.79 geometrías distintas;16 consumidores por defecto. Son configuraciones, no141 pantallas aprobadas. Campos: x, parámetro y, ancho, byte3 desconocido, modo, alto. Modo4 se interpreta como coordenadas; modo1 usa anclaje especial y necesita contexto. Ancho interior=(ancho-2)*8. Filas nominales=(alto-2)/2; excepciones0D→6,19/1B→8.

Buffer común:11 filas×52 bytes, SRAM6057..6292; offset de fila6293. Glifo normal avanza16 px; bit8000 avanza8 px;4000 selecciona icono en el consumidor de dibujo;2000 se omite en los bucles comunes. FFFF termina; no transportar esta semántica sin más al motor narrativo.

## Motor secundario

Entrada150E6F; grupo648F, mensaje648E, banco6493, puntero6486, índice6482. Raíz en banco+2, tabla por grupo, tabla por mensaje. Catorce grupos no nulos del dominio0..16;12/13/15 vacíos. La tabla de32 selectores de banco no acredita32 grupos de diálogo: después del16 hay otras estructuras, incluidas animaciones. Grupo14 y recursos compuestos requieren confirmar consumidor;3488 referencias no equivalen a3488 conversaciones.

Lector15113B, palabra devuelta en151158. Despacho de controles150FD8. Columna6499, línea6491, límite6495. Capacidad13 celdas de16 px=208 px. Si llega un glifo cuando columna==13,150FFB..15110D avanza la línea después de haberlo consumido: ese glifo se pierde. Confirmado para00DD y0106 mediante selectores inyectados, sin fabricar cadenas ni píxeles.

| Control | Efecto observado en código | Validación M1 |
|---|---|---|
| FFF0 | velocidad6490=0 | STATIC_ONLY |
| FFF2 | pausa/espera, estado bit04 | runtime en la corrección |
| FFF4 + argumento | sustitución numérica, buffer6440; selectores bajos0/1 | STATIC_ONLY;9 recursos dinámicos junto conFFF8 |
| FFF5 / FFF6 | temporización25/4B | STATIC_ONLY |
| FFF8 + argumento | sustitución; selector0 usa byte64CB | STATIC_ONLY |
| FFFA + argumento | paleta | STATIC_ONLY |
| FFFB + argumento | llamada de sonido | STATIC_ONLY |
| FFFC | espera/estado | STATIC_ONLY |
| FFFD | reinicio de caja | STATIC_ONLY |
| FFFE | nueva línea, con desplazamiento al agotar filas | runtime |
| FFFF | fin de mensaje o retorno de sustitución | runtime |

FFF1/3/7/9 apuntan a retornos en este despacho. No se inventa significado adicional. Las variantes contextuales de controles y argumentos siguen pendientes.

## Variables

187B15 compone nombre+signo+nivel desde0576; signo ocupa16 px y dos cifras usan8 px cada una. Formateadores188100/18810D/18812F: una cifra16 px, dos/tres cifras8 px. Cantidades y otros campos pueden reservar columnas24/25. Muestra sintética de ítem9D nivel+99: nombre, icono y modificador caben; no prueba todos los límites ni combinaciones. Los9 recursos conFFF4/FFF8 están listados en el censo; falta cubrir sus rangos y ventanas reales.

## Corrección del censo anterior

F00:I075 yF00:I076 comparten colas. Leer hasta el siguiente puntero truncaba su medición; ahora se sigue hastaFFFF con límite del banco y guarda explícita. HF11:2333 referencias,1972 no vacías estructurales,13805 palabras contando controles y terminadores. Familias4/16 contienen iconos;9/18 incluyen recursos numéricos. No contar estos registros como frases traducidas. La tabla secundaria tiene3488 referencias,3472 punteros distintos,886 entradas con celdas literales,2421 sólo controles no vacías y181 vacías. Aún no hay unión completa por recurso+contexto ni cobertura global visual.
