# Reintentos y límites QA24

- Copia local previa incompleta por mantenimiento: HF18 recuperado íntegro (112893 archivos).
- libarchive no logró extraer el archivo7z; py7zr1.1.4 extrajo JP y su SHA256 coincide. No se declaró corrupción del insumo.
- Mesen sin settings.json abrió wizard y no pudo iniciar pruebas; perfil portable con settings.json={} resolvió el arranque headless. Los intentos probe_forge/money_candidate/money_valid carecen decompleted y no cuentan como evidencia. No se necesita Xvfb.
- bestiary_treant sin scroll mostró el monstruo pero no la tercera habilidad; bestiary_treant_scroll usa el mismo consumidor con scroll explícito y sí demuestra I007.
- Revisión cruzada corrigió opcode2D a2F en notas de consumers y repitió búsqueda; no aparecieron consumidores nuevos.
- No confundir formateador32bit con máximo4294967295: este motor dibuja siete posiciones y se ensayó hasta9999999 como extremo sintético, sin afirmar límite natural.
