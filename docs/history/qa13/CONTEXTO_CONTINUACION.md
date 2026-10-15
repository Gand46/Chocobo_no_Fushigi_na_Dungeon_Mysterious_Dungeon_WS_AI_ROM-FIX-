# Continuación después de HF9 / QA13

Autoridad: manifest.json, docs/issue_register.json y docs/QA13_VALIDATION.json. ROM/BPS idénticos a HF9 QA12; hash final c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284. No crear HF10 sólo por esta revisión.

El usuario autorizó expresamente pruebas sintéticas y PASS_SYNTHETIC para los pendientes antes llamados naturales. Equipamiento, Atla, ascensor/99→30 y guardado tienen aceptación funcional sintética en el alcance documentado. No reabrirlos por falta de adquisición natural. Causas históricas de equipamiento, Atla y reset espontáneo siguen sin reproducirse; no presentarlas como fixes nuevos.

Equipamiento: bolsa nativa18, autoordenada al abrir; resolver ID después del ordenamiento. Seis casos idénticos en HF9/EN/JP regresan al campo0011, cero cruces en cuatro stores/cero escrituras175AC..17F8F. Tabla de fusión117x10 en6D3F; byte0=slot, bytes8/9=propiedades. Tres ciclos guardado/carga fría (equipo D1F1→2, D3F30→31 y32→33), seis copias exactas de2516bytes, commits válidos. No repetir pruebas de escritura parcial HF4 ya cerradas sin un riesgo nuevo.

Atla: bolsa llena de fusionados malditos y HP1, sin editar historia/puntero del rescate. Hitos9A1C/9D07/9E44 y bandera18; JP también alcanza el rescate. HF9: combate asistido→créditos→pueblo→movimiento. No conocemos condiciones exactas de Yahoo; no confundir variante de estrés con reproducción histórica exacta.

Hallazgo principal: llamador nativo de ascensor ROM1998D7 configura E013,1FAE0A,1FB0FE,1FB3=0. Estado05 era un observador incompleto. E0 corresponde al bancoROM00, NO1E. Cadena HF9 fría99→Telep→pueblo→ascensor sintético30 completa; mapa normal0000 y control. JP mismo estado seleccionaA216 (mapa99). Intervenir sólo caché753A..753E al consumidor4D39B corrige JP a0000. Primera lectura: piso29/caché98; el incremento posterior llega30. Fix HF6 ya incluido en HF9 resuelve esta causa. Una escritura de caché al entrar al menú se sobrescribe y NO constituye control causal válido.

JP caminó1800frames por el mapa erróneo y mantuvo guardado intacto; carga fría posterior vuelve99 con2516bytes exactos. No se reproduce el freeze posterior del foro ni borrado. Diferenciar selección de mapa de pérdida de datos.

El menú de escalera puede invocarse sintéticamente por E00A/puntero1950 con1FAE0A y1FB0FF; se pulsan Down/A para Save and go on. No presentar estas entradas como escaleras alcanzadas caminando. Los intentos de reubicar tile031D no abrieron el menú en estos estados y están excluidos. Crear savestates sólo desde callbackCPU, nunca directamente desde endFrame.

Pendientes fuera del alcance funcional aceptado: maquetación/lingüística global; revisión formal independiente de glifos del logo del usuario. No rediseñar el arte, no volver a HF7. Incidente de cartucho físico cerrado por causa eléctrica del usuario. Reproducción portable y estados incluidos en docs/QA13_REPRODUCCION.md y evidence/qa13_fixtures. No repetir inventarios ya cubiertos sin un caso nuevo.
