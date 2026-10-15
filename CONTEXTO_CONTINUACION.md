# Continuación — HF16 / QA21 V3

Objetivo: aprobación visual/lingüística global en cinco validaciones. V3 ejecutada con 207 referencias,64 diálogos corregidos,205 PASS sintéticos acotados y dos reservas. Dos propiedades getter corregidas. Global abierto; siguiente V4:194 referencias de G09 de qa19/five_validation_plan.json. V5:154 de G14 más transversal/reservas. No añadir otra fase automáticamente.

Autoridad de partida HF15/QA20: ZIP82f9bbe4007a56c93f223b84a39acc163f223d72bc1c04d61a9a4c8a23d9913b; snapshot481fcb1bcd729cc7c4d5908e10aa3e9055c65dcae393487104aa8af3e6ca115b. Se verificaron65488 archivos antes de editar. Partir ahora de este paquete HF16 y comprobar .continuity antes de nuevos cambios.

ROM final 14abf199753631e907e80092ce50f4e48d7eb139f31964cdc8897b9d6bf51c00; CRC20FF7B24; checksum6555. Builder canónico src/corrections.json; regenerador qa21/rebuild_translation_edits.py parte del snapshot HF15 incorporado. QA20 histórico se fija a su BPS y recetas originales.

Evidencia final del lote: evidence/qa21_runs/verified_G*. Prefijos baseline_,final_,pregetter_,release_,rejected_,repair_ son diagnósticos o fases previas; no asumir versión por nombre. El manifiesto de cada sesión debe coincidir con el SHA final. visual_readings.json enlaza capturas finales con lectura directa o igualdad exacta de píxeles. No usar exit0 ni una carpeta existente como PASS. Dos últimas propiedades tienen lecturas en fused_HF16V3; inventario/estado en ui_HF16V3_*. JP sólo comparativo.

Reservas V3:G06:M100 depuración;G11:M011 frase de número de plantas. V2:G00:M252–255,G04:M033–034. Heredadas:G16:M073,preset32/F00:I053,consumidores G16:M000/M003/M004. La muestra getter no es un censo lingüístico completo. No hardware,segundo emulador,segundo revisor ni ruta natural universal.

Nueva región06:E588–06:F708 exclusivo,4480bytes; siguiente inicio posible06:F708 sólo tras verificar de nuevo. El inicio rechazado06:E586 contenía el terminador FFFF de G06:M099: nunca inferir espacio libre sólo por FF; comprobar extents heredados. Banco1B conserva ocupación QA20 hasta1B:EE88. G07 tabla066F40 y G16 tabla06CB86 tienen256 entradas fijas porque sus primeros recursos se relocalizaron.

F06:I019/I022 se corrigieron in situ. PROPERTY_UNDEAD_TEXT de la receta previa se fusionó conservando su preimagen original; QA21 edits registra la transición real HF15→HF16. Fuente compartida y código iguales. El codec es parcial: leer cada nuevo texto en el motor. Camilla's Dad conserva secuencia nativa especial. Professor se usa para先生 de Faukes en este lote; comprobar coherencia transversal enV5.

Checkpoints incluidos: evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss para diálogos y evidence/qa3/q3_dungeon/checkpoint.mss para inventario. Una instancia de Mesen a la vez. Límite de emergencia40min/turno; guardar checkpoint antes de cortar. Entrega siempre fuentes completas+BPS directoJP+evidencia sin ROM.

Empaquetado: conservar el arreglo de tools/continuity.py que elimina cada extracción verificada tras preservar logs/artefactos. El paquete ya mide más de4GB y mantener todas las extracciones simultáneas agotó el disco; ver qa21/PACKAGING_RESOURCE_FIX.md.

R1 revalidó HF16 sin cambios de ROM/BPS; matriz vigente en docs/approval_matrix.json, verificador reproducible qa21/revalidate_delivery.py y dictamen QA21_V3_Revalidacion_R1.md. Dos reservas V3 y global pendiente.
