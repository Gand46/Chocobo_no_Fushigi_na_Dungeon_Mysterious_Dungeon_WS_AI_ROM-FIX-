# Diseño, evidencia y continuidad

## Alcance exacto

Se localiza la pantalla representada por el GIF `1000763108.gif`. El universo comprobado es de 91 cuadros y 6.070 ms, no la totalidad de los recursos de arranque del juego. La captura PNG ampliada suministrada muestra también copyright; esos renglones no están en el GIF. No se inventó su animación ni se afirma haber validado esa variante de la pantalla.

## Dirección gráfica

El rótulo inglés conserva letras redondeadas, volúmenes desiguales y remates de plumas de la referencia inglesa. La segunda línea se revisó específicamente para abrir los huecos, distinguir `r`/`n` y separar `Mystery` de `Dungeon` antes de reducir a píxeles nativos. El rótulo mide 156 × 42 y se coloca en (34,64). El subtítulo mide 94 × 12, en (65,109). La animación conserva un título inmóvil.

Los maestros de imagen generada son material de autoría, no evidencia de resolución de consola. Los recursos finales se muestrean por vecino más cercano, se asignan a cuatro índices y se empaquetan sin suavizado. La transparencia de la capa de letras usa una máscara independiente: no añade un quinto color a la pantalla compuesta.

La paleta RGB se obtiene del GIF: `#242400`, `#9292AA`, `#B6B6AA`, `#DBDBAA`. Representa el aspecto de esa captura; no es una lectura de los registros originales de paleta LCD. La exportación 2bpp contiene índices, no esos colores RGB.

Se preservan sin alteración las primeras 56 filas, todos los píxeles que cambian entre poses y las filas 121–143. El arco inferior que estaba oculto detrás del japonés se reconstruyó gráficamente: **no es una extracción de los píxeles ocultos originales**. Se eliminó parte de la reconstrucción que duplicaba el pico dentro de la zona de animación. La pequeña marca original se reutiliza a la derecha del logo más ancho.

## Revisión visual de esta iteración

Se inspeccionaron el cuadro nativo y la lámina de los seis estados con ampliación entera. El rótulo se lee como `Chocobo’s / Mystery Dungeon / for WonderSwan`, sin recorte y con la zona de `PUSH BUTTON` libre. La tercera pose cambia el ángulo de la cabeza; la cuarta cambia los ojos. No se redibujaron las poses de forma independiente con un generador: se reutilizan sus píxeles para mantener consistencia.

Esta revisión del autor, con conocimiento del texto esperado, **no equivale a reconocimiento ciego independiente ni a aprobación visual dentro del juego**. El diseño se entrega para revisión artística y posterior integración; no se concede un PASS de legibilidad runtime con una composición externa.

| Control | Resultado y evidencia |
|---|---|
| Descubrimiento | PASS para el GIF aportado: 91 cuadros, seis estados y cuatro poses |
| Traducción del rótulo | PASS como adaptación inglesa del título y de la plataforma |
| Resolución/paleta | PASS: 224 × 144, índices 0–3 |
| Secuencia/tiempos | PASS: comparación de los 91 cuadros y sus duraciones |
| Movimiento original | PASS: igualdad de los píxeles móviles y de la máscara temporal |
| Letras estables | PASS: no se añade movimiento fuera de la máscara original |
| Codificación 2bpp | PASS: decodificación de todos los estados idéntica a los PNG |
| Reconstrucción | PASS: build reproducible desde los assets entregados |
| Revisión artística | Realizada por el autor; aprobación del usuario pendiente |
| Tipografía/legibilidad dentro del juego | NOT_VALIDATED |
| Integración / consumidor / compresión | NOT_VALIDATED |
| Mesen / hardware / regresión jugable | NOT_VALIDATED; no ejecutado |
| BPS | N/A en este paquete gráfico; ninguna ROM fue modificada |
| FINAL_APPROVED | false |

## Formato de recursos

`title_patterns.2bpp`: patrones únicos, ocho filas por patrón, dos bytes por fila. El primer byte contiene el bit 0 de los ocho píxeles y el segundo el bit 1; el píxel izquierdo ocupa el bit 7. Los mapas `map16le` contienen 28 × 18 índices sin flags, little-endian. Son un formato de intercambio documentado, no mapas listos para sobrescribir posiciones desconocidas de la ROM.

Un índice de tile no equivale a una posición definitiva en VRAM. Antes de integrar hay que reservar/reubicar los patrones, asignar bits de paleta/capa, convertir al formato del consumidor y comprobar que la animación no sobrescribe las letras. `map_deltas.json` muestra los cambios entre estados; no autoriza escrituras directas al juego.

## Continuación concreta

1. Identificar ROM japonesa y fuentes de la traducción activa por SHA-256, sin sustituirlas por archivos de otros juegos.
2. Extraer el título y confirmar tilemaps, compresión, tablas de animación, paletas y consumidor. Identificar también la variante con copyright.
3. Integrar estos PNG/índices mediante operaciones reproducibles, con bytes de precondición y rangos delimitados.
4. Ejecutar en Mesen desde arranque: título estático, cuatro poses, parpadeo, transición al menú y versión con copyright. Comparar capturas nativas.
5. Revisión de legibilidad independiente; BPS acumulativo desde la ROM original y fuentes completas del proyecto integrado.

Ahorro de tokens: no medido. Ningún porcentaje global de traducción se deduce de este trabajo gráfico.
