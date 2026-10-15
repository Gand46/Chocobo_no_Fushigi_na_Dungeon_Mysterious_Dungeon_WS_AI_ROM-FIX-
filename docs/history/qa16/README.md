# Chocobo English HF11 TEST · QA16 M2

La ROM HF11 y su BPS no cambian. Esta entrega amplía las pruebas y las fuentes acumulativas de maquetación: 16 escenarios sintéticos acotados aprobados y un candidato nuevo pendiente de contexto. La maquetación global, la revisión lingüística, el hardware y el segundo emulador siguen sin aprobación global.

Aplicar `patches/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps` directamente a la ROM japonesa con CRC32 `CCAA4853`. No requiere parches intermedios. No se distribuyen ROM, BIOS ni emulador.

```sh
python3 build.py /ruta/JP.ws --out /ruta/privada
python3 qa16/verify_scope.py --japanese-rom /ruta/JP.ws --out /ruta/QA16_VERIFICATION.json
```

Resultados actuales: `docs/QA16_VALIDATION.json`, `docs/QA16_RUN_INDEX.json` y `qa16/visual_readings.json`. Informe legible: `qa16/Chocobo_QA16_M2_Informe.html`. Reproducción: `docs/QA16_REPRODUCCION.md`.

M3 atenderá diálogos, eventos, créditos y las 13 alertas heredadas; M4 integrará los resultados y resolverá los contextos restantes, incluido M2-C01. Consultar `CONTEXTO_CONTINUACION.md` antes de continuar. Dos iteraciones base restantes son una estimación, no una garantía de cierre total.
