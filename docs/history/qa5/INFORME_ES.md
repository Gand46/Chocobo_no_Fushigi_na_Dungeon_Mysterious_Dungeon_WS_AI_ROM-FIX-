# Chocobo HF3 TEST — QA5: guardado y reportes originales
Fecha: 13 de octubre de 2026. ROM y BPS sin cambios respecto a HF3. Auditoría adicional, no HF4.

## Conclusión
Se localizaron y validaron condiciones que hacen desaparecer o alteran una partida reconocible. No se ha demostrado todavía que esas condiciones sean provocadas por el menú de equipo, por la traducción ni por los eventos concretos de los foros. No se incorpora un parche especulativo al sistema de guardado.

## Hallazgos demostrados

1. La rutina normal copia 2516 bytes desde SRAM6BD8..75AB a75B6..7F89 y escribe la firma ASCII n_c1 en75B0..75B3. Está en ROM190367. Otra rutina19038C escribe el mismo bloque y una firma A_C1 en75AC..75AF. Esas rutinas usan un único destino de datos; las dos firmas no demuestran dos copias recuperables de la partida.
2. La comprobación1903B8 reconstruye bits de validez en75B4 comparando ambas firmas de cuatro bytes. Al alterar sólo75B0 de6E a00, Load deja de reconocer la partida, conservando intactos los2516 bytes del contenido. Esto reproduce una causa concreta de aparente pérdida, bajo modificación artificial; no identifica quién destruiría ese byte durante juego normal.
3. Al cambiar sólo el byte del nivel guardado765B de1 a2, la partida carga comoLv2. Esa ruta no rechaza la alteración del contenido. El análisis del cargador observado no muestra un checksum del bloque; el resultado experimental demuestra al menos que ese cambio no queda detectado. Una firma válida no certifica coherencia de mapa o eventos.
4. Guardado normal y carga en frío no borran la firma normal en las pruebas. Existe una rutina explícita de borrado/inicialización en18C813 que pone a cero75B0..75B3; no se observó ejecutarse en la carga normal. No se atribuye la pérdida a una supuesta eliminación automática al cargar.
5. El bloqueo Lafoss en JP y EN, y su protección en HF3, se probaron con una copia del bloque de guardado nativo ya existente. En los tres casos75AC..7F89 se conserva byte por byte; después se carga la partida en un proceso nuevo. Lafoss no explica por sí solo el reset del guardado en estas condiciones.
6. El código190333..190401 y18C760..18C8FF examinado es idéntico entre japonesa e inglesa. La inglesa del foroCRC AC2E344C se obtiene exactamente de nuestra inglesa normalizada6E8CA148 sustituyendo únicamente el checksum final13E3 por3321. Esta diferencia no identifica un fallo de SRAM. Sigue abierta la posibilidad de daños indirectos desde otras rutinas.

## Pruebas de pisos y límites

Se construyeron guardados sintéticos partiendo del contenido de una mazmorra temprana y del guardado nativo. Son pruebas de acceso, no recorridos naturales ni certificaciones de las rutas del foro.

- Primera mazmorra: carga al piso2 y acceso a la escena del jefe en30. No se observa pérdida del bloque guardado.
- Tercera mazmorra, piso33: tras incorporar las banderas de progreso correspondientes, el cargador mantiene identificador3, llega al piso33 y responde a las entradas. Esto valida ese acceso sintético; no valida el ascensor ni todos los pisos especiales.
- Los primeros intentos rotulados segunda/tercera mazmorra se reducen internamente a identificador1: quedan descalificados como prueba de progreso tardío. Se conservan para trazabilidad.
- El intento de segunda mazmorra/piso60 muestra pantalla blanca persistente. La traza encuentra4000:8393–83A0 repitiendo6CC0; el filtroE000:EAFB/EB00 devuelve cero con el umbralSRAM0647=0 y4B54 no aumenta. El bloque guardado permanece. Pero el script4000:D34E cambia el identificador2→1, incluso en la variante de banderas ensayada. Por ello es un bloqueo demostrado de un estado sintético incoherente, todavía NO una reproducción acreditada deJP01 oJP02. No se repara alterando arbitrariamente el bucle.

## Causas evaluadas

| Hipótesis | Estado |
|---|---|
| Firma destruida: partida no reconocida aunque quedan datos | Demostrada mediante un cambio artificial de un byte. Disparador natural pendiente. |
| Datos alterados aceptados por el cargador | Demostrado para el byte del nivel; integridad global no garantizada por la firma. |
| Cargar normalmente elimina el guardado | No observado en la ruta probada; firma y contenido guardado conservados. |
| Lafoss destruye automáticamente el guardado existente | No reproducido: bloque intacto y carga posterior correcta enJP/EN/HF3. |
| Traducción cambia directamente la rutina de guardado | Descartado para los rangos examinados; daños indirectos siguen sin demostrar. |
| Menú de equipo corrompe SRAM | Testimonio conservado; no reproducido por la matriz previa ni atribuido a un byte concreto. |
| Carga de eventos/ascensor deja el mapa incoherente | Pista vigente deWazap; acceso sintético parcial, ruta exacta pendiente. |
| Batería/contactos causan datos absurdos | Hipótesis en otro testimonio; no validada aquí. El fallo físico del usuario ya tiene causa eléctrica y queda fuera de ROM. |

## Contraste del chat y los foros

El servicio de recuperación devolvió que el contexto personal no está disponible. No se presenta esta auditoría como lectura íntegra del chat «Analizar bloqueo de Chocobo». Se contrastaron el PDF aportado, sus enlaces y el fragmento disponible de ese chat. La cobertura documental incluye las diez incidencias del PDF; no se puede excluir una mención adicional que sólo exista en la parte del chat no accesible.

RetroAchievements relaciona consultar equipo con bloqueo/pérdida y advierte sobre guardados. Wazap describe carga de pisos de evento y ascensor, además del salto99→30. El segundo artículo describe la combinación fuente/rana y final de segunda mazmorra. Son testimonios, no causas de código confirmadas. La fuente deAtla no pudo reabrirse y conserva su estatus previo. El nuevo relato del piso20000 se conserva como pista de datos alterados, con acceso limitado a resultados de búsqueda. URLs exactas en docs/qa5_sources.json.

## Pendientes y continuación

Prioridad inmediata: seguir la escritura del identificador de mazmorra desde4000:D34E con banco de script649B y puntero64A1; completar una fixture coherente de segunda mazmorra; comparar entrada ordinaria, carga y ascensor en las mismas condiciones. Después contrastar las ramas fuente/rana paraJP02 y las transiciones99→30/Atla. Mantener los accesos sintéticos explícitamente identificados.

Lafoss completo, título japonés, revisión global del texto y los reportesEN01/EN03 siguen con sus límites anteriores. El silbato permanece corregido. No hay cambios de ROM: se conserva el BPS acumulativo HF3 original→302765E7, SHA85a8be61fdac2feb777ed1726235b46b36f8950265a1788e7d7c9a0bc90f4b11. No se anuncia RC ni reparación total del guardado.

## Herramienta y reproducción

Incluye tools/inspect_chocobo_save.py, de sólo lectura, para identificar firmas, hashes y diferencias de marcadores/contenido. No repara ni sobrescribe el archivo. Ejemplo:
python3 tools/inspect_chocobo_save.py partida.sav --compare copia_anterior.sav

Repetición: copiar una fixture.sav a Saves/Chocobo_EN_v1.1_HF3_TEST.sav del perfil portátil y lanzar qa5/run.py con ROM HF3, estado '-' yqa5/cold_trace.lua. Las copias de prueba están enqa5/save_fixtures con metadatos. Hacerlo en un perfil aislado. El arnés termina cada ejecución y registra hashes/estado de finalización. Los timeouts se conservan separados y no cuentan como resultados de juego. Restauraciones de savestate no sustituyen la carga en frío.
