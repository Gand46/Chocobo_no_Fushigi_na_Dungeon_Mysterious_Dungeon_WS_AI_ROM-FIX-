# Integración del logo aportado — QA11

## Base y procedencia

HF7 fue verificada por SHA-256 antes de continuar. La ROM HF8 reconstruida desde JP es byte-idéntica a la candidata usada en todas las pruebas QA11. Los nombres de ruta en run.json conservan la candidata `private_roms/qa11_title.ws`; su hash es el de la entrega final. La base y el archivo gráfico constan en manifest.json.

El ZIP de arte se conserva como fuentes expandidas en assets/title/user_v01. Sus documentos describen su estado previo offline, no el estado de integración HF8. Se mantiene autoría/procedencia y sus advertencias originales. La paleta RGB de su GIF no es una lectura de hardware; se usan sus índices con los cuatro colores del juego. La primera imagen offline no incluye copyright: el juego sí lo muestra y QA11 lo comprobó.

## Operación binaria

- Recurso nativo: ROM155155..156B04,411tiles 2bpp; consumidor154A27..154A43, destino WRAM2000.
- Reserva para arte: tiles61..194 y215..327 (247 disponibles); se usan139. Tiles328..391 de animación intactos;392..410 del japonés anterior vacíos.
- Mapa0 en150034..1501B6:247bytes comprimidos y padding FF. Paleta transparente4 conservada.
- Mapa1: puntero150032 a15FD58;625bytes, termina15FFC8 inclusive. Se respeta el código anterior en15FD00..15FD57.
- Formato nativo de mapas,1024words, compresión LZ del juego. Recompresión/decodificación exacta; preimágenes y presupuesto de tiles/mapa verificados.
- El arte usa filas56..120; la animación nativa sigue superpuesta en su ventana. La prueba de fidelidad del rótulo cubre64..120 inclusive. Copyright y PUSH BUTTON siguen siendo controlados por el juego.
- Checksum actualizado. No cambia la fuente compartida, la lógica de eventos, el guardado ni la lógica de equipamiento.

## Recorrido y evidencia

Comando reproducible, usando un Mesen2.1.1 privado:

`python3 qa11/run.py HF8.ws - qa11/title_animation.lua runs/title --timeout 35 --mesen /ruta/Mesen`

Planes title_menu.lua (2000frames), title_animation.lua (1400frames, capturas300..1300) y start_game.lua (4000frames). El estado de walk procede de start_game y utiliza post_ending_walk.lua,480frames; el nombre histórico del plan no convierte esta prueba en un ending. No se hacen pokes ni cambios de registros. Accesos SCRIPTED_NATURAL y SAVESTATE con botones.

Comparación: qa11/compare_animation.py y animation_validation.json. Los mapas registrados en1000 correspondían a BG1 y contienen la nueva ilustración fija: su desigualdad es esperada. No se usa ese registro como prueba de igualdad del mapa animado. Las pruebas válidas son igualdad de píxeles superiores/pie, estabilidad del logo, tiles de animación byte-idénticos y ausencia de cambios en el código nativo.

Los16estados superiores RGB incluyen cuatro poses estables y transiciones de la representación LCD del emulador; no se afirma que existan16poses. El GIF de entrega es una previsualización muestreada de capturas reales, no reemplaza los registros por cuadro ni controla el juego.

## Límites

No se transfiere la aprobación de36glifos de HF7 al diseño diferente de HF8. Lectura directa revisada; reconocimiento independiente sin contexto pendiente. Los estados previos QA1–QA10 mantienen su hash/procedencia y no se presentan como nuevas ejecuciones de HF8. Su vigencia se limita a código/recursos no modificados; los pendientes anteriores permanecen explícitos.
