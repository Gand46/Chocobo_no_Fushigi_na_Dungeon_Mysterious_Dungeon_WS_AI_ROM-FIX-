# Continuación después de HF6 / QA9

Build vigente HF6 TEST. Consultar manifest.json y docs/QA9_REPRODUCTION.md. No repetir las auditorías históricas completas. El fallo físico eléctrico está cerrado.

## Fix nuevo

El opcode34 en14D398 salta a14FDA8..14FDD9. Solo actúa para bancoE1, puntero639C..69FF y dirección753A..753E. Recalcula los dígitos con9000:6E1C desde el piso7303, conserva registros y flags, y vuelve aD39B. El bucle blanco148393 espera4B54;0647=0 impide la aceptación de1EEAFB. No usar la sonda de probabilidad1 como parche: liberaba el bucle sin reconstruir el mapa previsto.

## Control que limita la conclusión

Las fixtures post-ending cambiaban el piso y conservaban la caché61. HF5 con caché98 coherente carga99. El guardado nativo Save and go on desde98 también es coherente y pasa HF5/HF6. La causa natural de reset y el recorrido continuo del ascensor siguen abiertos.

## Telep

Carta0B, acción nativa Use desdeF99 al pueblo. Conserva la caché99. La fixture post_telep99_reentry30 copia ese bloque vivo a un contenedor legacy y cambia D3 y piso/máximo29. HF5 genera A217 en30; HF6 genera0000. Es reproducción sintética basada en datos; no es el recorrido continuo del ascensor. Hay checkpoints y movimiento posterior de ambas variantes.

Los intentos de invocar guiones directamente son incompletos y están excluidos. E0:2873 muestra Go to which floor; usa060E como temporal y7558/7559 para dígitos. El opcode25/20 decrementa7303 en18C83F. Iniciar el guion requiere1FAE=5 y649F=80, pero aún falta reproducir el llamador completo y su retorno al generador de piso. No confundir E0:2D7E con una ruta aprobada del ascensor.

## Fuente/rana

194E8C..4F7E incrementa7514 por Geyser09 y7515 por Frog04. Los umbrales15/30/45 Geyser activan54/55/56; la suma20/40/60 activa57/58/59. En7313 son las máscaras0010..0200. Las variantes coherentes0090 (15+5) y03F0 (45+15) antes del final deD2 terminan E0:ABE2. La completa pasa también enHF6 yJP; los bloques de guion comparados son idénticos. Las hipótesis4D/12 eran ajenas a fuente/rana. No inventar un fix sin reproducir el fallo.

## Pendientes concretos

- Arte inglés del título con identidad nativa; sigue japonés.
- Maquetación global en los consumidores reales.
- Disparador del bloqueo por equipamiento.
- Ascensor continuo y Telep99→30 sin contenedor intermedio.
- Fallo original fuente/rana, no reproducido en variantes coherentes.
- Rescate exacto deAtla; Yahoo sigue inaccesible. No marcar D1F30 como ese rescate.

Próximo paso útil: trazar la entrada auténtica al menú2873 desde el pueblo, incluyendo llamador y modos1FA6/1FAE; capturar los dígitos antes/después de18C83F y comparar selección30/99. Mantener preimágenes. No sustituir el logotipo por tipografía genérica.
