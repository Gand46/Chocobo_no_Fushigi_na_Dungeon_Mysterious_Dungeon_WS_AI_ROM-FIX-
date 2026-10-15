#!/usr/bin/env python3
"""Produce portable, self-contained HF19 QA25 read-only layout audit report."""
import base64
import csv
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa25/results"
report = ROOT / "QA25_HF19_Auditoria_Distribucion_Texto.html"
summary = json.loads((OUT / "summary.json").read_text())
index = json.loads((OUT / "balance_evidence_index.json").read_text())
proposals = json.loads((OUT / "candidate_reflows.json").read_text())
assert len(index) == 99 and len(proposals) == 6
inheritance = json.loads((OUT / "hf18_equivalence.json").read_text())
assert inheritance["status"] == "PASS_EXACT_STREAM_EQUIVALENCE_HF18_TO_HF19"
assert {x["id"] for x in index} == set(inheritance["identical_story_streams"])
proposed_ids = {x["id"] for x in proposals}


def h(v):
    return html.escape(str(v), quote=True)


def figure(entry, n):
    path = ROOT / entry["path"]
    image = path.read_bytes()
    assert hashlib.sha256(image).hexdigest() == entry["sha256"]
    encoded = base64.b64encode(image).decode("ascii")
    return (f'<figure><img width="224" src="data:image/png;base64,{encoded}" '
            f'alt="Captura nativa histórica, página {n}"><figcaption>Página {n}. '
            f'<code>{h(entry["path"])}</code></figcaption></figure>')


style = '''*{box-sizing:border-box}body{font:16px/1.5 system-ui,sans-serif;color:#1b2926;background:#f1f2ee;margin:0}main{max-width:1200px;margin:auto;padding:28px}h1{font-size:32px;line-height:1.2}h2{margin-top:36px;border-bottom:2px solid #87a5a0;padding-bottom:6px}p{max-width:980px}table{border-collapse:collapse;background:white;width:100%}th,td{border-bottom:1px solid #d4dcd7;padding:8px;text-align:left;vertical-align:top}code{overflow-wrap:anywhere}nav a{margin-right:12px}article,details{background:white;border:1px solid #d9dfda;border-radius:8px;margin:10px 0;padding:14px}details[open]{border-color:#599281}summary{cursor:pointer;font-weight:650}.grid{display:flex;flex-wrap:wrap;gap:8px}figure{margin:4px;width:224px}img{display:block;image-rendering:pixelated;max-width:100%}figcaption{font-size:11px;overflow-wrap:anywhere}.tag{color:#77511d}.ok{color:#266545}.small{font-size:13px;color:#55645f}.proposed{border-left:5px solid #3c8a75}.risk{border-left:5px solid #b88332}@media(max-width:650px){main{padding:14px}table{font-size:13px}}'''
content = ['<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
           '<title>Chocobo HF19 · QA25 distribución de texto</title><style>', style,
           '</style><main><h1>HF19 · QA25: distribución del texto</h1>',
           '<p class="tag"><strong>Auditoría de solo lectura.</strong> La ROM y el BPS HF19 no cambiaron. '
           'Las capturas de la galería son pruebas nativas históricas de fases QA19–QA22; no se les atribuye una ejecución nueva en HF19.</p>',
           '<nav><a href="#metodo">Método</a><a href="#propuestas">Propuestas</a><a href="#galeria">99 alertas</a><a href="#limites">Alcance</a></nav>',
           '<h2 id="metodo">Censo y método</h2>',
           '<p>Se leyó la ROM HF19 exacta (SHA-256 <code>', h(summary['rom_sha256']), '</code>). '
           'Se recorrieron 3.488 recursos story, de los cuales 886 contienen texto literal; también se inventariaron '
           '2.333 getters y 141 presets. El límite nominal del diálogo común es 13 celdas de 16 píxeles. '
           'Las variables dinámicas y los consumidores de getters no se juzgan por esa regla general.</p>',
           '<table><tr><th>Resultado estático</th><th>Recursos</th><th>Interpretación</th></tr>',
           f'<tr><td>Sin alerta de este filtro</td><td>{summary["risk_counts"]["NONE"]}</td><td>No equivale a aprobación visual universal.</td></tr>',
           f'<tr><td>Relleno al final</td><td>{summary["risk_counts"]["PADDING_ONLY"]}</td><td>Espacios vacíos; no se recorta texto visible por sí mismo.</td></tr>',
           f'<tr><td>Diferencia entre líneas ≥6 celdas</td><td>{summary["risk_counts"]["BALANCE_REVIEW"]}</td><td>Cola de lectura editorial, no defectos confirmados.</td></tr>',
           f'<tr><td>Literal visible &gt;13 celdas</td><td>{len(summary["visible_over_13"])}</td><td>Los dos casos brutos de 14/15 son relleno 0000 y ya estaban documentados.</td></tr></table>',
           '<p>Se inspeccionaron directamente 128 imágenes, distribuidas en siete hojas principales y dos de páginas adicionales, '
           'para los 99 recursos señalados. Sus secuencias story son idénticas entre HF18 y HF19. '
           'Las pausas, los nombres y la intención dramática explican muchas líneas cortas; no se corrigen automáticamente.</p>',
           '<h2 id="propuestas">Seis redistribuciones candidatas</h2>',
           '<p>Se conserva exactamente la redacción, los controles FFFE/FFF2 y el número máximo de 13 celdas. '
           'Cada candidato cabe en el tamaño actual del flujo, pero <strong>ninguno se ha escrito ni probado como cambio</strong>. '
           'La siguiente iteración requiere ROM de trabajo, captura nativa comparada y prueba de regresión.</p>',
           '<table><tr><th>Recurso</th><th>Antes</th><th>Posible reparto</th><th>Bytes de texto</th></tr>']
for p in proposals:
    content.append(f'<tr><td>{h(p["id"])}</td><td>{h(p["before_cells"])}</td>'
                   f'<td>{h(p["proposed_lines"][0])}<br>{h(p["proposed_lines"][1])} '
                   f'<span class="small">{h(p["proposed_cells"])}</span></td>'
                   f'<td>{p["encoded_byte_delta"]:+d}</td></tr>')
content.extend(['</table><h2 id="galeria">Galería de las 99 alertas</h2>',
                '<p>Las imágenes permiten comprobar la composición existente y sus pausas. '
                'Cada ficha conserva fase, ruta y SHA-256 en el índice JSON; una imagen histórica no demuestra el consumidor natural de HF19.</p>'])
for x in index:
    cls = 'proposed' if x['id'] in proposed_ids else 'risk'
    status = 'Candidato de reparto' if x['id'] in proposed_ids else 'Revisión visual, sin cambio propuesto'
    content.append(f'<details class="{cls}"><summary>{h(x["id"])} · diferencia {x["imbalance_cells"]} celdas '
                   f'· QA{x["evidence_phase"]} · {h(status)}</summary><p>Segmentos literales: '
                   f'<code>{h(x["visible_segments"])}</code>. Captura histórica de consumidor sintético; '
                   'el recurso es byte idéntico entre HF18 y HF19.</p><div class="grid">')
    for n, entry in enumerate(x['images'], 1):
        content.append(figure(entry, n))
    content.append('</div></details>')
content.extend(['<h2 id="limites">Alcance pendiente</h2>',
                '<p>Las nueve referencias con sustituciones dinámicas necesitan extremos reales del valor y su anfitrión. '
                'Cinco getters superan 208 píxeles de ancho nominal si se copian como una sola fila '
                '(F00:I075, F00:I076, F13:I210/I236/I260); sin la vinculación a ventana y sus controles esto no demuestra desborde. '
                'Quedan fuera las rutas naturales aún no localizadas, todos los consumidores de getters y la revisión global de gráficos. '
                'FINAL_APPROVED permanece false.</p>',
                '<p class="small">Archivos reproducibles: qa25/audit_layout.py, qa25/make_contacts.py, '
                'qa25/candidate_reflows.py, qa25/results/story_layout.csv, summary.json, '
                'balance_evidence_index.json y candidate_reflows.json. Versión de la ROM intacta.</p></main></html>'])
report.write_text(''.join(content), encoding='utf-8')
result = {"status": "PASS_STATIC_SCOPED_EDITORIAL_REVIEW", "rom_sha256": summary['rom_sha256'],
          "story_literal_resources": 886, "balance_flags": len(index), "historical_images_read": sum(len(x['images']) for x in index),
          "candidates_unapplied": len(proposals), "current_rom_edited": False,
          "html": report.name, "html_sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
          "global_visual_approved": False}
(OUT / "report_validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
