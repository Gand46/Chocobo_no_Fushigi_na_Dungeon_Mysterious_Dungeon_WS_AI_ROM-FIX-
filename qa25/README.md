# QA25 — distribución del texto en HF19

Auditoría de solo lectura, sin cambio de ROM ni BPS. La autoridad binaria sigue
siendo HF19/QA24. `QA25_HF19_Auditoria_Distribucion_Texto.html` contiene las
capturas nativas históricas y la decisión editorial de este ciclo.

## Reproducir

Con `build/Chocobo_EN_v1.1_HF19_TEST.ws` reconstruida desde la JP limpia:

1. `python3 qa25/audit_layout.py --rom build/Chocobo_EN_v1.1_HF19_TEST.ws`
2. `python3 qa25/make_contacts.py` (requiere Pillow para generar hojas PNG)
3. `python3 qa25/candidate_reflows.py`
4. Definir `CONTINUITY_INPUT_JP` y ejecutar `python3 qa25/check_inheritance.py`.
5. `python3 qa25/make_report.py` (requiere Pillow solo al generar contactos).

`results/story_layout.csv` registra los 886 recursos literales, sus celdas
escritas y los motivos de selección. `results/summary.json` conserva los
conteos. `results/balance_evidence_index.json` aporta ruta y SHA256 de 128
capturas históricas. `results/hf18_equivalence.json` comprueba que los 99
flujos story señalados son byte idénticos en HF18/HF19. `results/candidate_reflows.json`
conserva seis ideas no aplicadas, verificadas contra las fuentes editables,
controles y límite de 13 celdas.

## Resultado y límites

- 3.488 story, 886 con texto literal, 2.333 getters y 141 presets censados.
- 640 sin alerta de este filtro, 147 con solo relleno al final y 99 con
  diferencia de seis o más celdas entre líneas. Las 99 alertas no son fallos.
- Dos líneas superan 13 celdas brutas (`G01:M031`, `G06:M022`); solo sus
  ceros de relleno rebasan el límite. Ningún literal visible supera 13.
- Nueve recursos literales con variables requieren valores y consumidores
  reales para medir la composición. Cinco getters nominalmente largos no
  implican recorte sin rastrear su ventana.
- Seis candidatos conservan la misma redacción y caben en los bytes actuales,
  pero no tienen pruebas nativas después de reflujo. Estado:
  `UNAPPLIED_EDITORIAL_REVIEW_CANDIDATE`.

Las capturas QA19–QA22 son evidencias históricas, no ejecuciones nuevas en
HF19. Las imágenes de QA24 ya revisan las 11 reservas anteriores. No afirmar
uniformidad global, alcance natural ni aprobación visual de todos los getters.
