# Revisión independiente de las reservas HF18

Autoridad leída: ZIP HF18 QA23 V5 con SHA256 6607e0a5398c35f9deaae5053e6f1d3acab155acb242541867faf0968c578e26. Revisión contra ROM JP SHA256 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728 y HF18 SHA256 6b7b0d79c4d60e6a6bbb5ae062b4255e75eda716f83bfbbd972cad65f3e05c24. Se leyeron AGENTS.md, PROJECT_CONTEXT.md y .continuity/RESUME.md; el coordinador verificó la autoridad. No se ha modificado src/corrections.json, manifest.json ni el builder canónico.

## Defecto confirmado: G00:M253 selecciona el número equivocado

Payload HF18 1B30F5..1B3107: `c1000a027802f4ff0001c5007a00f2ffffff`.
Payload JP en la misma dirección: `010010000200f4ff010081007a00f2ffffff`.
El argumento de FFF4 ocupa 1B30FD..1B30FF: HF18 `00 01` = 0100; JP `01 00` = 0001.

La ROM prueba que no son equivalentes:

- ROM151066 llama al lector113B; ROM151069 aplica AND AL,0F.
- Tabla ROM15106E: words1074,1083,1074.
- Rama0 ROM151074: lee SRAM67C6, limpia word1FEF y va a145A (formato16bit/cinco dígitos).
- Rama1 ROM151083: lee low-word72FD y high-word72FF, y va a146A (formateador siete dígitos).
- 0100 conserva nibble bajo0, por tanto lee67C6, igual que G00:M252.

Corrección mínima inequívoca: restaurar argumento0001. Caso diferencial sugerido:67C6=37; dinero72FD/72FF=123456. Debe mostrarse123456, no37. Valor0 y9.999.999 prueban extremos del formateador. NO usar4294967295 como máximo válido:146A produce siete posiciones y comienza por divisor1.000.000; fuera del dominiodecimal el primer cociente excede9 y genera un glifo incorrecto. No se demostró el máximo alcanzable naturalmente de dinero. La UI principal usa otro formateador de ocho dígitos185390.

## Consumidores y contexto exacto de los mensajes de depuración

G00:M252 JP <FFF4:0000>レベル; HF18 <FFF4:0000>Level. La captura release_G00_M252/page_01.png muestra `0 Level`. La etiqueta inglesa más clara sería `Level [n]`, conservando selector0000.

G00:M253 JP あたい<FFF4:0001>ギル. Value o Cost son traducciones defendibles. `Value [n] Gil` evita inventar un contexto de vendedor.

G00:M254 JP <FFF8:0000> アイテム. HF18 muestra `ID Card Items` en release_G00_M254/page_01.png. Selector0 lee itemIndex byte64CB, coloca en1FEB y llama135F para copiar nombre F03 al buffer6440. Etiqueta preferible: `Item: [nombre]`, sin perder argumento0000.

G00:M255 JP 名前は<FFF8:0001>です. FFF8:0001 no prepara un nombre: la tabla1510C6 elige10D6, que es RET. Luego el motor consume el buffer6440 que debe estar preparado antes. La captura histórica release_G00_M255/f02400.png está vacía; no acredita esta ruta. Los planes qa17/plans/dyn_G00_M255_min.lua y max.lua contienen fixtures de palabras exactas F03, adecuados para una prueba del consumidor nativo con preparación sintética explícita. `Name: [buffer]` es fiel como etiqueta.

G06:M100 JP デバッグモード！ / ここから交換へいく！！, con FFFA:0006 al comienzo y FFFA:0005 al final. HF18 normaliza paleta final a0000 como otras traducciones del proyecto y muestra `DebugMode! / Let's start to exchange!`. Recomendación: `Debug mode! / Start item trading!`. No añade una mecánica nueva; la frase japonesa dice que desde aquí se entra al intercambio.

Búsqueda acotada de llamadas: los opcodes de script28 y2F llaman literalmente a(group,message); la tabla14D1AD los despacha aD2DC yD2FA. El opcode29 es indirecto y NO tiene formato(group,message). No se encontró llamada literal válida de28/2F a los cuatro G00 de depuración ni G06:M100 en las búsquedas de patrones realizadas. Varias coincidencias brutas caen en glifos, gráficos o datos. Tampoco apareció un inicio de esos recursos fuera de las sesiones sintéticas conocidas entre los2843 story.csv examinados. Esto NO demuestra ausencia, inaccesibilidad ni autoriza un cierre N/A. El cierre defendible es estático+runtime sintético con valores/estado documentados.

## Nombres de habilidades y coherencia transversal

### Wither Hit

La lectura exacta primaria es **ウィザーヒット**, con vocal largaー; varios documentos heredados omitían ese signo. G14:M007 JP palabras0054,009A,0085,0051,006C,009E,0065. `Wither Hit` reproduce correctamente el préstamo y es semánticamente adecuado para una habilidad de árboles que marchita/debilita.

La misma secuenciaJP aparece en F17:I007, ROM19C15E. EnHF18 esa etiqueta YA codifica `Wither Hit` exactamente:00D5,014B,011C,0238,00C6,014B. El glifo0238 incluye `r `; una decodificación ingenua que elimine espacios de digrafos produce falsamente WitherHit. No se requiere corrección. G14 agrega un0000 final de relleno, sin diferencia textual.

Consumidor confirmado estáticamente: el bestiario utiliza F17:I007 para monsterIndex32 木人/Treant y53 マモン/Mamon. Registros de habilidades ROM18696A=`03 3B 08 07`, ROM1869B1=`03 3B 4C 07`. Esto constituye contexto primario del juego, además de la lectura aislada.

### Ruin Cannon y Wave Cannon

G14:M067 contiene **破動砲**, palabras0127,01FB,0221. G14:M152 contiene **波動砲**, palabras0203,01FB,0221. La diferencia破/波 está en laROM y es visible, no un error OCR. `Ruin Cannon` es una localización defendible que retiene el matiz de破 (romper/destruir), mientras `Wave Cannon` traduce波 (onda).

No se debe afirmar que son habilidades mecánicamente distintas: no se ha demostrado. El bestiario de monsterIndex63 オメガ/Omega usaI152, noI067; registroROM1869D5=`03 45 03 98`. I067 no figura en las82 listas de habilidades de esa tabla. Podría ser una variante histórica de nombre o un texto de otro consumidor. Conservar dos rótulos es una decisión de traducción fiel a la distinción gráfica, no una afirmación de nomenclatura inglesa oficial.

Los getters hermanosF17:I067 eI152 conservaban `Guns` y `Aura`, pese a compartir exactamente las secuenciasJP deG14. Para coherencia se prepararon dos correcciones a `Ruin Cannon` y `Wave Cannon`. El scriptqa24/rebuild_getter_edits.py produce4edits independientes deHF18 (2payloads+2punteros) y no modifica fuentes canónicas. Nuevos payloads19FF00..19FF20; banco19 tiene colaFF desde19FBA9. TablaF17=19BFC4, entradasI067=19C04A eI152=19C0F4. Cada etiqueta ocupa7celdas/112px y cabe nominalmente en el consumidor128px. Esto todavía requiere runtime visual final.

## Consumidor nativo F17: bestiario preset81

- Preset81=129: interior128px, seis filas; initializer1864B9; row_consumer1899E3.
- El initializer lee SRAM2000 como monsterIndex y2001 como parámetro auxiliar.
- Compone buffer de índices629A: nombreF12, etiquetaF05:I073, elementoF10, tipoF11 y listaF17.
- Tabla de listas18685D con82entradas word; cada registro es count+IDs.
- Row consumer1899E3 calcula64C4+6299; para filas>=4 usa rama189A82, fija family17, luego llama7ABE/7AD3.
- Wither yWave son la tercera habilidad de sus monstruos y requieren desplazamiento para la séptima fila. Se puede seleccionar preset81 y monster32/53/63 mediante fixture, dejando intacto el initializer y consumidor.
- I067 requiere índice de fila sintético porque no está en las82listas; no llamarlo recorrido natural.

## Reservas que coordina el agente principal

G11:M011 yG16:M073 tienen idéntico textoJP 階くらいあとで e idéntica traducciónHF18. Significado completo: `in about N floors` / `N floors later`. La fraseHF18 `N floors or so` pierdeあとで si es una opción autónoma. G11:M012 habla de adelantarse para abrir tienda, que apoya el matiz futuro. Modificar sólo con la composición del consumidor verificada.

G04:M033 tiene dos alternativas `Are these 2 OK?` y `Are these 3 OK?`; G04:M034 precios1000/500Gil. Son variantes concatenadas, y leer ambas seguidas no prueba el consumidor de selección. El coordinador investiga la selección/ventana.

## Lecturas visuales realizadas

Se inspeccionaron directamente las láminasJP/EN qa20/audit_08.png, qa20/audit_20.png, qa21/audit_12.png, qa21/audit_22.png, qa19/audit_07.png, qa23/audit_01.png, qa23/audit_11.png, qa23/audit_25.png; también las capturas runtime históricas enumeradas y qa23 verified_G14_M007/end_text.png y verified_G14_M067/end_text.png. Estas últimas muestran completos `Wither Hit` y `Ruin Cannon` dentro de una ventana nativa. La revisión no equivale a PASS de nuevasROM ni a recorrido natural universal.

Artefactos de análisis: reservation_bytes.json (bytes y punterosJP/HF18), ability_consumers.json, monster_labels.png (render de glifos exactos para comparación, NO captura runtime), getter_build/getter_edits.json ygetter_allocations.json. Los .bin de desensamblado ygetter_candidate.ws son temporales privados; no deben añadirse a una entrega de fuentes.

## Adenda runtime de la candidata QA24

Candidata SHA256 f27e69f65e134b161c1f3ce263c3ed78a8ae247997c95d7383c43c4a78c8962f.
Se realizaron y leyeron tres sesiones nuevas del consumidor nativo preset81,600cuadros cada una, usando un perfilMesen separado. F17:I007, I152 e I067 aparecen completos, como `Wither Hit`, `Wave Cannon` y `Ruin Cannon`, respectivamente. Todos registran family17/window129, retorno7AEA y terminadorFFFF; cero row_overflow para el objetivo. Capturas exactas f00120.png de bestiary_treant_scroll, bestiary_omega ybestiary_ruin_fixture.

El acceso es sintético: preset81,monsterIndex yscroll64C4=1. ParaI067 se sustituye explícitamente la última entrada de la lista SRAM62A6 tras el initializer nativo; no se acredita que Omega utilice esa etiqueta naturalmente. El primer bestiary_treant sinscroll es diagnóstico y no acreditaI007.

También se leyó independientemente el contacto nativo20story qa24/native_review_contact.png. La cifraM253 es123456 con nivel37 en su fixture diferencial y9999999 en su extremo de siete dígitos. Debug mode!/Start item trading! aparece completo, en paleta gris heredada. Los sufijosG11/G16 muestranfloors or so later, completos; la frase anfitriona/selección natural sigue fuera de este alcance.

Transcripciones,hashes y límites en qa24/astra_visual_review.json. La aprobación resultante es lingüística y visual de recursos/consumidores con acceso sintético declarado; no FINAL_APPROVED ni recorrido universal.
