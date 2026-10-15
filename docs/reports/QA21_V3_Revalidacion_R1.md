# Chocobo English HF16 — revisión V3 (3 de 5), R1

**Dictamen:** V3 ejecutada y revalidada con alcance sintético. De 207 referencias, 205 tienen aprobación visual y lingüística acotada; dos requieren contexto. La aprobación global del juego permanece abierta.

| Ámbito | Resultado |
|---|---|
| Texto narrativo | 207 referencias, 64 diálogos corregidos; 60.714 cuadros finales y 284 lecturas visuales archivadas. |
| Inventario y equipo | Cuatro escenarios de inventario/estado y seis configuraciones fusionadas, cinco sesiones HF16 y cinco JP; 13.641 cuadros HF16 y 100 lecturas bilingües. Dos propiedades corregidas. |
| Integración | ROM HF16 y BPS reproducidos sin cambio binario; 3.365 comprobaciones de alcance y 952 de evidencias complementarias; 13 pruebas unitarias. |
| Reservas V3 | G06:M100: consumidor de depuración. G11:M011: número de plantas y ventana compuesta. |
| Pendiente | V4: 194 referencias G09. V5: 154 G14 más revisión transversal y reservas heredadas. |

La lectura directa del inglés final y la comparación con japonés están documentadas en QA21_V3_Informe.html y en `qa21/linguistic_review.json`, `qa21/visual_readings.json` y `qa21/supplemental_visual_readings.json`. La corrección del crecimiento del pueblo (`G07:M000`) y la frase de Item File (`G06:M081`) se mantienen legibles en el motor. La propiedad de equipo describe eficacia contra enemigos venenosos, no resistencia al veneno.

La revalidación R1 corrige el verificador complementario para leer las sesiones archivadas, comprueba los bytes y píxeles de las lecturas finales sin reescribirlas, actualiza la matriz de aprobación que aún describía HF9 y documenta la reconstrucción reproducible. También reduce el espacio temporal necesario para comprobar dos compilaciones independientes desde el ZIP. **No cambia la ROM ni el BPS.**

El BPS `patches/Chocobo_EN_v1.1_HF16_TEST_JP_CCAA4853.bps` se aplica sobre una ROM JP limpia CRC32 CCAA4853; no sobre HF15. SHA-256 JP `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`; HF16 `14abf199753631e907e80092ce50f4e48d7eb139f31964cdc8897b9d6bf51c00`; BPS `5f1c59ee00a6e564ff007518aa86e46b40eb9f94dc0f410fd702df0db8a6e78a`. El ZIP incluye fuentes acumulativas editables, historial y evidencias; no incluye la ROM comercial.

Las seis reservas V2 (`G00:M252–255` y `G04:M033–034`) y las de `G16:M073`, preset32/F00:I053 y consumidores G16:M000/M003/M004 siguen abiertas. Las selecciones sintéticas no demuestran el recorrido natural completo. No consta validación en hardware, un segundo emulador ni una segunda revisión independiente.
