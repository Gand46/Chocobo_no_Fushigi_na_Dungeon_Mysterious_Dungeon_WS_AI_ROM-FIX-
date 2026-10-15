"""Build a self-contained Spanish before/after report from reviewed native images."""
from pathlib import Path
import base64,html,json
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def image(p):return 'data:image/png;base64,'+base64.b64encode((ROOT/p).read_bytes()).decode()
review=load('qa26/layout_review.json');pairs=load('qa26/native_pairs.json');v=load('qa26/verification.json');m=load('manifest.json')
parts=['''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chocobo HF20 · Distribución estética QA26</title><style>
body{font:17px/1.55 system-ui,sans-serif;background:#f1f3ee;color:#263129;max-width:1080px;margin:auto;padding:32px}h1,h2{line-height:1.15}h1{font-size:36px}section{background:white;border-radius:12px;padding:24px;margin:20px 0}.badge{background:#d8ead7;padding:6px 12px;border-radius:20px;display:inline-block}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}img{width:100%;image-rendering:pixelated}figcaption{font-weight:600;margin-bottom:10px}table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}code{overflow-wrap:anywhere;font-size:13px}.note{color:#4c5a4f} @media(max-width:650px){body{padding:16px}.pair{grid-template-columns:1fr}h1{font-size:28px}} @media print{section{break-inside:avoid}body{background:white;padding:0}}</style>
<p>CHOCOBO WONDER SWAN · HF20 TEST · QA26 · 15 OCT 2026</p><h1>Una distribución más uniforme</h1>
<p>Corrección aplicada sobre HF19: <strong>14 textos, seis redistribuciones de líneas y doce huecos excesivos reducidos.</strong> La validación se centra en el aspecto estético del texto en su espacio disponible.</p>
<p class="badge">Mejora visual confirmada por el coordinador y Astra · alcance limitado</p>
<section><h2>Qué se corrigió</h2><p>Se retiraron doce celdas vacías de 16 píxeles que, sumadas al margen interno de los glifos contiguos, producían huecos de 24–31 píxeles. La separación restante es de 8–15 píxeles. Seis frases se repartieron de forma más equilibrada entre las dos líneas, conservando exactamente sus palabras.</p>
<p>Un primer ensayo con un mínimo de cuatro píxeles se rechazó porque algunas palabras parecían unidas. Las capturas finales corresponden al segundo ensayo. No se alteran la fuente, el tamaño de letra, el motor, los colores ni la geometría de las ventanas.</p></section>
<section><h2>Verificación y límites</h2><p>28 sesiones nuevas de Mesen, 8.311 cuadros y 18 páginas comparadas: todos los textos llegaron a su terminador, sin caracteres ni espacios descartados. 231 comprobaciones de alcance y 13 pruebas del proyecto aprobadas. Reconstrucción semántica exacta y aplicación independiente del BPS verificadas.</p>
<p>La diferencia frente a HF19 es de 352 bytes, limitada a los catorce bloques de texto y el campo de checksum autorizado. Los 3.488 punteros story, los 2.333 getters y las 141 ventanas mantienen sus datos; código, fuente y gráficos se conservan. El checksum coincide con el anterior porque se han redistribuido bytes y retirado celdas nulas; los SHA-256 sí distinguen ambas ROM.</p>
<p class="note">Acceso sintético: se selecciona cada recurso en una ventana nativa desde un estado controlado. No acredita todos sus contextos de partida. Astra revisó las 18 comparativas y la receta; no ejecutó las pruebas. Persisten irregularidades previas, como el espacio visual antes del punto en «guy .» y antes de la coma en «Poulet ,». La revisión global de espaciados, getters y gráficos continúa pendiente; HF20 conserva el estado TEST.</p></section>
<section><h2>Detalle de las correcciones</h2><table><thead><tr><th>Recurso</th><th>Celdas por línea antes → después</th><th>Ajuste</th></tr></thead><tbody>''']
for r in review:
    action=[]
    if r['reflow']:action.append('Reparto: '+' / '.join(r['proposed_lines']))
    if r['spacing_events']:action.append('Huecos: '+', '.join(f"{x['before_gap_px']}→{x['after_gap_px']} px" for x in r['spacing_events']))
    parts.append('<tr><td>'+r['id']+'</td><td>'+str(r['original_lines'])+' → '+str(r['new_lines'])+'</td><td>'+html.escape('; '.join(action))+'</td></tr>')
parts.append('</tbody></table></section><h2>Antes y después · todas las páginas</h2><p>Capturas completas de 224 × 157 píxeles, ampliadas sin suavizado. Las páginas sin cambios visibles se conservan para mostrar el contexto completo del recurso.</p>')
for p in pairs:
    parts.append(f'<section><h2>{p["id"]} · página {p["page"]}</h2><div class="pair">')
    for key,label in [('before','Antes · HF19'),('after','Después · HF20')]:parts.append(f'<figure><figcaption>{label}</figcaption><img alt="{label} {p["id"]} página {p["page"]}" src="{image(p[key])}"></figure>')
    parts.append('</div></section>')
parts.append('<section><h2>Aplicación y trazabilidad</h2><p>Aplicar el BPS acumulativo directamente a la ROM japonesa limpia, CRC32 CCAA4853. El paquete de fuentes incluye el historial completo, las recetas editables y la evidencia nativa. No incluye ROM, BIOS ni emulador.</p><p>ROM HF20 SHA-256:<br><code>'+m['target']['sha256']+'</code></p><p>BPS SHA-256:<br><code>'+m['bps_sha256']+'</code></p><p>Fuentes de evidencia: qa26/verification.json, qa26/native_pairs.json, qa26/layout_review.json y qa26/astra_visual_review.json. La auditoría QA25 permanece como antecedente, no como validación del parche nuevo.</p></section></html>')
p=ROOT/'QA26_HF20_Correccion_Estetica.html';p.write_text('\n'.join(parts),encoding='utf-8')
assert p.read_text().count('<img ')==36
print(p)
