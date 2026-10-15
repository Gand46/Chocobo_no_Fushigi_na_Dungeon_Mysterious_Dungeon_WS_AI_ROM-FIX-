"""Self-contained illustrated QA19–QA23 synthesis; retained historical capture provenance."""
from pathlib import Path
from html import escape as h
import base64,json,hashlib
R=Path(__file__).resolve().parents[1];read=lambda p:json.loads((R/p).read_text())
reviews={v:read(f'qa{v}/linguistic_review.json') for v in range(19,24)}
manifest=read('manifest.json');verify={v:read(f'qa{v}/verification.json') for v in range(19,24)}
style=(R/'QA21_V3_Informe.html').read_text().split('<style>')[1].split('</style>')[0]
style+='''nav{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}nav a{padding:5px 10px;border:1px solid #ccc;border-radius:6px;background:white;color:#284840}.r{color:#7a4420}.ok{color:#22583b}figure.audit{width:min(100%,1000px)}.audit img{max-width:100%}.small{font-size:13px}.pill{background:#eff3e9;border-radius:9px;padding:2px 7px}.phase{border-left:5px solid #947235}.gallery{display:flex;flex-wrap:wrap;gap:16px}caption{text-align:left;font-weight:bold} .toc a{color:#28554c}details img{width:224px} @media print{details{display:block}}'''
def image(path,caption,width=None,klass=''):
 p=R/path;assert p.is_file(),p
 src=base64.b64encode(p.read_bytes()).decode('ascii');attrs=f' width="{width}"' if width else ''
 return f'<figure class="{klass}"><img loading="lazy"{attrs} src="data:image/png;base64,{src}" alt="{h(caption)}"><figcaption>{h(caption)}</figcaption></figure>'
def native(v,id,baseline=False):
 slug=id.replace(':','_');folder=R/f'evidence/qa{v}_runs'
 if v==19:
  p=folder/(('candidate_' if baseline else 'release2_')+slug)/'end_text.png'
 elif v==23:
  p=folder/(('baseline_' if baseline else 'verified_')+slug)/'end_text.png'
 else:
  p=folder/(('baseline_' if baseline else ('release_' if v==20 else 'verified_'))+slug)
  imgs=sorted(p.glob('page_*.png'))
  if not imgs:imgs=sorted(p.glob('end_text.png')) or sorted(p.glob('f*.png'))
  assert imgs,p;p=imgs[0]
 return p.relative_to(R)
def phase_label(v):return {19:'V1 · HF14',20:'V2 · HF15',21:'V3 · HF16',22:'V4 · HF17',23:'V5 · HF18'}[v]
def status(v,x):return x.get('linguistic_status',x.get('status'))
def reason(v,x):return x.get('reason',x.get('correction_reason')) or x.get('source_meaning_es') or 'Revisada contra el original japonés y la captura nativa.'
def final_image(v,x):
 if v==19:return native(19,x['id'])
 if v in (20,21):return Path(x['final_images'][0])
 if v==22:return Path(f'evidence/qa22_runs/{x["final_run"]}/{x["final_page"]}')
 return Path(x['final_image'])
html=['<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chocobo · consolidado V1–V5 · HF18 TEST</title><style>',style,'</style></head><body><main>']
def add(s):html.append(s)
add('''<header><div class="eyebrow">CHOCOBO WONDER SWAN · INGLÉS · QA19–QA23</div><h1>Aprobación visual y lingüística<br>Consolidado de las validaciones 1 a 5</h1><p>Informe ilustrado de la partición prevista de 886 referencias literales. La quinta validación se ejecutó en HF18 TEST. Las capturas de V1–V4 documentan sus respectivas versiones históricas; V5 y las dos correcciones de nombre corresponden a HF18.</p></header>''')
add('''<div class="badges"><div class="badge"><b>886</b>referencias literales revisadas</div><div class="badge"><b>875</b>PASS lingüísticos acotados tras reconciliar nombres</div><div class="badge"><b>11</b>reservas de contexto o término</div><div class="badge"><b>5/5</b>lotes ejecutados; aprobación global abierta</div></div>''')
add('''<div class="callout"><strong>Dictamen: NO APROBADO GLOBALMENTE.</strong> Se completaron los cinco lotes planeados, pero 11 referencias aún requieren contexto o confirmación léxica. Tampoco hay recorrido natural universal, revisión independiente, segundo emulador ni prueba en hardware. Una captura sintética demuestra legibilidad en esa ventana y escena; no acredita todos los consumidores ni toda la terminología del juego.</div>''')
add('<nav class="toc">'+''.join(f'<a href="#v{i}">Validación {i}</a>' for i in range(1,6))+'<a href="#reservas">Reservas</a><a href="#registro">Registro visual</a><a href="#integridad">Integridad</a></nav>')
add('''<h2>Resultados comparables</h2><table><tr><th>Lote</th><th>Referencias</th><th>Textos cambiados</th><th>PASS lingüístico acotado al cierre</th><th>Reservas vigentes</th><th>Versión de las capturas</th></tr>''')
for v,n,changes,passed,pending in [(19,83,36,82,1),(20,248,74,242,6),(21,207,64,205,2),(22,194,43,194,0),(23,154,65,152,2)]:
 add(f'<tr><td><a href="#v{v-18}">{phase_label(v)}</a></td><td>{n}</td><td>{changes}</td><td>{passed}</td><td>{pending}</td><td>{phase_label(v).split("· ")[1]}</td></tr>')
add('''</table><p class="muted">V4 registró originalmente dos reservas «Doru» (192/194). V5 comprobó el mismo ドル君 en G08/G11, cuyo nombre establecido es «Chip», y corrigió G09:M086/M089: el balance consolidado actual computa 194/194 en V4. No se altera el informe histórico de V4.</p>''')
examples={19:[('G16:M000','Nuevo juego: lámina bilingüe y pantalla final')],20:[('G00:M005','Consulta por el marido')],21:[('G06:M019','Respuesta sobre los libros')],22:[('G09:M002','Sorpresa ante el chocobo')],23:[('G14:M019','Ice Claw: garra helada'),('G14:M119','Six Nether Blasts: se conserva el numeral seis')]}
summary={19:'83 cadenas de menú y mensajes breves. Se mantiene la reserva G16:M073 y la comprobación de los consumidores compuestos de G16.',20:'248 referencias de G00–G05. Se conservan seis casos que dependen de variables, depuración o composición de precios y preguntas.',21:'207 referencias de G06–G08/G10/G11; quedan G06:M100 (depuración) y G11:M011 (número de planta y ventana).',22:'194 referencias G09. Sus dos nombres provisionales fueron reconciliados con Chip en HF18.',23:'154 referencias G14 de habilidades, elementos y tipos. Se cambiaron 65 textos y quedaron dos matices léxicos por confirmar.'}
for v in range(19,24):
 i=v-18;add(f'<section class="phase" id="v{i}"><article><h2>Validación {i} · {phase_label(v).split("· ")[1]}</h2><p>{h(summary[v])}</p>')
 for id,why in examples[v]:
  add(f'<h3>{h(id)} · {h(why)}</h3><div class="comparison"><div><h4>{"Original japonés y base HF13" if v==19 else "Antes · "+{20:"HF14",21:"HF15",22:"HF16",23:"HF17"}[v]}</h4><div class="screens">')
  if v==19:add(image('qa19/audit_00.png','Lámina bilingüe JP / base de V1',klass='audit'))
  else:add(image(native(v,id,True),id+' · versión anterior'))
  add('</div></div><div><h4>Después · '+phase_label(v).split('· ')[1]+'</h4><div class="screens">'+image(native(v,id),id+' · lectura nativa final')+'</div></div></div>')
 add('</article></section>')
add('''<h2>Corrección transversal: Chip</h2><p>Las secuencias japonesas ドル君 de G09:M086 y M089 coinciden con el mismo personaje nombrado «Chip» en G08 y G11. La grafía «Doru» del lote V4 era provisional. HF18 reemplaza tres celdas de nombre por tres celdas de «Chip» en cada recurso, sin cambiar controles de color ni paginación.</p><div class="comparison"><div><h3>G09:M086</h3><div class="screens">''')
add(image(native(22,'G09:M086'),'HF17 · Doru')+image(native(23,'G09:M086'),'HF18 · Chip')+'</div></div><div><h3>G09:M089</h3><div class="screens">')
add(image(native(22,'G09:M089'),'HF17 · Doru')+image('evidence/qa23_runs/verified_G09_M089/page_01.png','HF18 · Chip, primera página')+'</div></div></div>')
add('''<h2>Título, créditos y muestra japonesa de V5</h2><p>Los 1.001 cuadros del título en HF18 son idénticos píxel a píxel a la referencia histórica QA14. Las 14 páginas de créditos también son idénticas a QA17. La inspección de los 26 pliegos japoneses de G14 documenta las 154 etiquetas, incluidos los nombres conservados.</p><div class="screens">''')
add(image('evidence/qa23_runs/final_title/anim01000.png','Título HF18 · cuadro 1000')+image('qa23/credits_final_contact.png','Créditos HF18 · 14 páginas',klass='audit')+'</div>')
add('<details><summary>26 láminas de comparación japonés/HF17 para G14</summary><p class="muted">Cada pliego reúne seis referencias. La versión final HF18 se ve en el registro visual inferior.</p>')
for j in range(26):add(image(f'qa23/audit_{j:02d}.png',f'Lámina {j+1:02d}/26 · JP / HF17',klass='audit'))
add('</details>')
add('''<h2 id="reservas">Reservas que impiden el cierre global</h2><table><tr><th>Origen</th><th>Referencias</th><th>Qué falta</th></tr><tr><td>V1</td><td>G16:M073</td><td>Frase anfitriona para sufijo temporal de número/piso.</td></tr><tr><td>V2</td><td>G00:M252–255; G04:M033–034</td><td>Variables, consumidor de depuración y preguntas/precios de forja compuestos.</td></tr><tr><td>V3</td><td>G06:M100; G11:M011</td><td>Consumidor de depuración; número de planta y ventana compuesta.</td></tr><tr><td>V5</td><td>G14:M007; G14:M067</td><td>Confirmar el término «Wither Hit» y el matiz «Ruin Cannon» frente a «Wave Cannon» en contexto natural.</td></tr></table><p>Además: preset32/F00:I053 y los consumidores reales G16:M000/M003/M004 no están validados universalmente. Los 2.333 getters, gráficos y composición de todas las rutas no forman parte de un censo lingüístico/visual exhaustivo; la inspección de título y créditos es específica.</p>''')
add('<h2 id="registro">Registro visual completo · 886 referencias</h2><p>Una captura por referencia con lectura y decisión. Las capturas V1–V4 pertenecen al parche de su validación, mientras las 154 de V5 pertenecen a HF18. Pulse cada referencia para abrir su imagen. G00:M255 sólo conserva una captura diagnóstica y sigue pendiente.</p>')
counts={}
for v,rs in reviews.items():
 add(f'<h3>{phase_label(v)} · {len(rs)} referencias</h3>')
 for x in rs:
  id=x['id'];st=status(v,x);pending=st in ('CONTEXT_PENDING','NEEDS_CONTEXT','NEEDS_NAME_CONFIRMATION','NEEDS_TERM_CONFIRMATION')
  if v==22 and id in ('G09:M086','G09:M089'):pending=False;st='PASS_RECONCILED_IN_V5'
  counts[st]=counts.get(st,0)+1
  img=final_image(v,x);is_diag=(v==20 and id=='G00:M255');label='RESERVA' if pending else 'PASS acotado';label+=' · imagen diagnóstica' if is_diag else ''
  add(f'<details id="{id.replace(":","-")}-{v}"><summary>{h(id)} · {h(label)}'+(' · corregida' if x.get('changed',x.get('action')=='CORRECTED') else '')+'</summary>')
  add('<p>'+h(reason(v,x))+'</p>')
  if v==22 and id in ('G09:M086','G09:M089'):add('<p>Reconciliado en HF18 como Chip. La imagen siguiente es la captura histórica HF17; la captura nueva aparece en la sección transversal.</p>')
  if x.get('reservation'):add('<p class="r">'+h(x['reservation'])+'</p>')
  add('<div class="screens">'+image(img,f'{id} · {phase_label(v)} · {img.name}')+'</div><p class="muted small">Fuente: '+h(str(img))+'</p></details>')
assert sum(counts.values())==886 and sum(n for k,n in counts.items() if k.startswith('PASS'))==875,counts
add('''<h2 id="integridad">Integridad, reconstrucción y límites</h2><table><tr><th>Control</th><th>Resultado</th></tr>''')
for k,val in [('Inventario literal','886 referencias en cinco particiones disjuntas; 3.488 entradas de historia y 2.333 getters en el análisis estático.'),('V5 nativo',f"154 etiquetas G14 + 2 nombres G09; {verify[23]['native_frames']:,} cuadros, 156 terminadores, cero glifos no blancos descartados."),('Byte y punteros','65 recursos G14, 2 nombres G09 y 54 punteros asignados; 931 bytes distintos frente a HF17. Fuente de glifos sin cambios.'),('Repetibilidad',f"{verify[23]['checks']:,} controles de V5; builder editable reproduce exactamente ROM y ediciones; BPS desde JP limpia reproduce el objetivo; 13 pruebas de unidad."),('Gráficos específicos','1.001/1.001 cuadros del título y 14/14 páginas de créditos coinciden exactamente con referencias históricas.'),('Límites','Sin ruta natural universal, hardware, segundo emulador ni segundo revisor; no declarar FINAL_APPROVED.')]:add(f'<tr><td>{h(k)}</td><td>{h(val)}</td></tr>')
add('</table><p>La ROM japonesa limpia requerida tiene CRC32 <strong>CCAA4853</strong>. El BPS acumulativo HF18 se aplica directamente a esa base. El paquete contiene fuentes, scripts, matrices y capturas; no incluye ROM comercial, BIOS ni emulador.</p>')
add('<p class="muted">SHA-256 ROM HF18 <code>'+manifest['target']['sha256']+'</code><br>SHA-256 BPS <code>'+manifest['bps_sha256']+'</code><br>SHA-256 JP limpia <code>'+manifest['original']['sha256']+'</code></p>')
add('<footer>QA23 · HF18 TEST · Consolidado V1–V5. Dictamen global pendiente; aprobación sintética acotada sólo para los casos indicados.</footer></main></body></html>')
p=R/'QA23_V1-V5_Informe_Consolidado.html';p.write_text(''.join(html))
print(json.dumps({'report':str(p),'bytes':p.stat().st_size,'embedded_images':''.join(html).count('data:image/png;base64,'),'details':''.join(html).count('<details'),'status_counts':counts},ensure_ascii=False))
