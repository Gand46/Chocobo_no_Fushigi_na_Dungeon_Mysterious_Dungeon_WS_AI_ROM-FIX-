CHOCOBO — HF8 TEST / QA11 — 14 de octubre de 2026

Resultado
Se integró el logo inglés entregado en Chocobo_WS_Logo_EN_v0.1_Fuentes_y_Animacion.zip. Se respetaron sus letras, proporciones, composición y píxeles nativos. El diseño reemplaza al rótulo provisional de HF7; utiliza la paleta real del juego.

La integración usa 139 patrones de 8×8 dentro del recurso nativo de 411 tiles. Se conservan los 64 tiles de animación de Chocobo y el código que controla poses, tiempos, copyright y PUSH BUTTON. Se recompusieron dos mapas; sus tamaños comprimidos son 247 y 625 bytes. No se introdujo un reproductor de GIF.

Validación realizada
• 1.001 cuadros comparados: filas 0–55 y 121–143 idénticas a HF7; cero discrepancias.
• En esos mismos cuadros, las filas 64–120 del nuevo rótulo/subtítulo coinciden píxel a píxel con el diseño aportado, usando los cuatro colores de la paleta nativa.
• Cuatro poses estables y transiciones visibles; copyright, parpadeo, menú, partida nueva y llegada al pueblo verificados desde arranque mediante botones. Movimiento posterior verificado desde el estado generado por ese recorrido.
• Reconstrucción desde los assets editables idéntica a los cambios incluidos; build desde JP y aplicación BPS independiente idénticos.
• 11 pruebas de infraestructura correctas. Cambios respecto a HF7: 2368 bytes, incluidos los dos bytes de checksum. Cero cambios fuera de recursos exclusivos del título y checksum; fixes de juego y guardado byte-idénticos.

Alcance de calidad
La lectura directa en pantalla fue revisada con conocimiento del texto. No se presenta como reconocimiento ciego ni se hereda el PASS de los 36 glifos del diseño anterior de HF7. La aprobación formal independiente de glifos del arte aportado queda pendiente; su fidelidad de integración está comprobada. No se redibujó el diseño del usuario.

HF8 sigue siendo TEST. Maquetación global, disparador del bloqueo por equipamiento y variante histórica del bloqueo de Atla conservan sus pendientes; esta fase no altera ni vuelve a certificar esas rutas. Tampoco se ejecutaron hardware real ni segundo emulador.

Identidad
JP SHA-256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF8 SHA-256: 831d5778ba5887941235365a4065d8cc090c1a871fbdfc00f398c2b5c0ebc89c
HF8 CRC32: A4D202FA; checksum WS: E459.
BPS SHA-256: 59c6d3447528774a57a43dad862ea5a8792da4377d56f41954b7eaff08265c66
Archivo gráfico aportado SHA-256: 5cc1543cb62cd506ad3822043e074af3cd27169bd47dc3e72a5e862f670d834b
Entorno: Linux x86_64, Mesen 2.1.1. Fuentes completas acumulativas, evidencias, estados y BPS directo desde JP. No se incluyen ROM, BIOS ni emulador.
