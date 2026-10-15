# Continuidad HF5 TEST / QA8

Último build SHA256 312f688f627f0c5ccf430c35c9632033344fc0397aa25c6f0db9d99a3630f9c8, CRC3887C0CF, checksum06CA. BPS directo desde JP CCAA4853; no encadenar HF4.

Lafoss: modelo faltante corregido1422C5 FFFF→0AF8; daño FE/FF habilitado1EA771 FE00→0001. La rutina14CA16/14CBB3 ya implementaba daño base1000. El menú nativo usa Kick, no un comando llamado Use. Terminal familia0/81 restaurado16E6FA0000→FFFF. Guardado HF4 permanece idéntico.

Prioridad siguiente: fuente/rana antes de concluir D2 y reconstrucción de pisos/ascensor. D2 ya pasó créditos y vuelve al control: evidence/qa8_runs/q8_d2_walk/checkpoint.mss. Estado sintético, jefe HP1 y personaje HP500 durante combate. No llamarlo progresión natural. Para bifurcar antes del final usar q8_d2_event_progress2 (jefe vivo) o q8_d2_boss_assist (postjefe antes de créditos); el segundo requiere demostrar que los flags de fuente se consultan después de ese punto. Rana/Frog Card ID04; Geyser Card ID09; Telep Card ID0B, identificados visualmente. Falta mapear los flags de la misión, no asumir que basta con inyectar las cartas.

D3 con progreso del final: q8_D3_post_ending_to_98 es campo98, q8_D3_post_ending_to_30 es campo30 y99 queda blanco. La fixture mínima anterior usaba730A8000 por error: el bit es0080. D3 requiere730C bit4, pero esos dos bits no reconstruyen toda la historia. Conservar datos exactos y separar corrupción persistente de carga de evento. No reabrir el bloqueo eléctrico del cartucho.

Título: qa8/title_assets tiene411tiles2bpp nativos, ROM155155..156B04, loader154A27. Aún japonés. Mantener estilo; no sustituir por una fuente genérica.

Equipamiento: cuatro nuevos Check +99 con18objetos, IDs65/9D/BF/C0, sin fallo. El intento93/slot9 abrió otro objeto y está excluido. No constituye causa resuelta. Atla tampoco: D1F30 volvió al pueblo, pero no se ha vinculado al rescate preciso.

No repetir matrices de guardado QA7 sin cambio de código. Guardar nativamente y cargar en frío para persistencia; savestates solo validan su ruta. Consultar informe y QA8_REPRODUCTION; los archivos históricos pueden contener conclusiones superadas, expresamente versionadas.
