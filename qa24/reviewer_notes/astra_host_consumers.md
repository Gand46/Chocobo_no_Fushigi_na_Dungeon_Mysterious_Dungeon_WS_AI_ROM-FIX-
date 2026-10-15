# HF18 — revisión acotada de G04:M033/M034 y G11:M011/G16:M073

Investigación estática y lectura de evidencia histórica; no nueva ejecución runtime. Fuente canónica leída sin cambios. ROM HF18 SHA256 6b7b0d79c4d60e6a6bbb5ae062b4255e75eda716f83bfbbd972cad65f3e05c24.

## Dictamen lingüístico

- G04:M033: JP この２つでいいかい？ / この３つでいいかい？. EN Are these 2 OK? / Are these 3 OK? conserva ambas preguntas y sus cantidades. Las dos frases son literales; no hay sustitución dinámica. Lectura directa de evidencia/qa20_runs/release_G04_M033/page_01.png: ambas líneas completas y legibles.
- G04:M034: JP １０００ギル / 必要だけどいいかな？ ５００ギル / 必要だけどいいかな？. EN 1000 Gil, OK? / 500 Gil, OK? expresa correctamente la confirmación de cada coste literal. Lectura directa de evidencia/qa20_runs/release_G04_M034/page_01.png: ambas líneas completas y legibles. El espaciado heredado de cifras es amplio, no recorte. No requiere cambio de texto.
- G11:M011 y G16:M073: JP idéntico 階くらいあとで; traducción fiel como sufijo es “floors or so later”. EN heredado “floors or so” omite el componente temporal あとで. Se puede corregir semántica del fragmento sin conocer su anfitrión. No se puede deducir del fragmento la cantidad máxima, si será singular, dónde se inserta, ni su ventana real. Un ensayo con 1/2 dígitos será un fixture limitado, no prueba del dominio natural.

## Motor y búsquedas

Motor story arranca en CPU 5000:0E6F (ROM150E6F) y recibe mensaje AL y grupo SRAM648F. Guarda ID en648E, obtiene banco desde150ED3+grupo, consulta tabla raíz del banco y tabla de punteros del grupo. La carga final del puntero ocurre CPU50EAB/50EAE. Sólo tres llamadas far a 5000:0E6F existen en la ROM HF18: ROM14D2F3,14D311,14D335.

- op28 (handler14D2DC) lee grupo byte, mensaje byte y llama story.
- op2F (handler14D2FA) lee grupo byte, mensaje byte y llama story; luego pone cursores6490/6492 a0.
- op29 (handler14D322) lee UNA dirección word de SRAM; usa el byte en esa dirección como mensaje y conserva el grupo648F existente. NO interpretar la forma `29 04 xx` como grupo4.

Búsqueda exacta en ROM completa no encuentra ninguna firma `28 04 21`, `2F 04 21`, `28 04 22`, `2F 04 22`, `28 0B 0B`, `2F 0B 0B`, `2F 10 49`. Las tres coincidencias `28 10 49` (ROM0925D1,0E664C,0EEC2C) tienen contexto gráfico, no guion demostrado. Ninguno de los 2333 getters apunta a los cuatro recursos.

Esto NO demuestra exhaustivamente ausencia de consumidor: op29 es indirecto, puede haber entradas que no se han trazado o referencias a subcadenas. No clasificar N/A universal ni declarar inaccesible.

## Referencias vecinas y forja real

- G04:M032 (ID20h) tiene llamada literal E0:F302. G04:M033/034/035 (IDs21h/22h/23h) no tienen llamadas literales op28/op2F. ID24h ya aparece en E0:D26B.
- Guion de forja E0:F17A contiene selección de dos/tres mediante ventanas2A/52; E0:F201 muestra G04:M075 (ID4Bh), E0:F243..F251 llama subguion0772, E0:F253..F266 llama0A02.
- Subguion E0:0772 abre ventanas3C/3D y otras41/42/43/44/45; E0:0A02 abre46/47/49. Sus confirmaciones se basan en consumidores UI/getter; no se puede atribuirles G04:M033/M034 sólo por semejanza textual.
- G11:M008/009/010/012 se usan en bloques E1:979E..9DCC; se omite literalmente M011. Ejemplos: E1:979E=28 0B 08, E1:987A=28 0B 09, E1:9959=28 0B 0A, E1:9A35=28 0B 0C.
- G16:M072 (ID48h) aparece E1:4EB4=28 10 48; no consumidor literal confirmado para M073.

## Alcance de cierre defendible

Es defendible dar aprobación lingüística a las cuatro referencias tras la corrección temporal; para G04, además, la lectura sintética histórica del recurso completo es legible. Se requiere revalidar la compilación actual o justificar herencia por bytes/hash de la evidencia. Sigue NOT_VALIDATED el consumidor compuesto/forja, su llegada natural, rango numérico y contexto de la frase anfitriona. Un cierre de las 11 referencias como textos revisados no debe presentarse como aprobación universal de consumidores ni FINAL_APPROVED del proyecto.

## Corrección técnica verificada sobre HF19

La versión inicial de estas notas rotuló erróneamente el handler D2FA como opcode2D. La tabla ROM14D1AD + 2*opcode confirma: 28→D2DC, 29→D322, 2D→DF2F, 2F→D2FA. Se ha corregido el texto y repetido la búsqueda usando **2F** para los cuatro targets en HF18 y HF19. No aparece ninguna firma 2F para ellos. Tampoco aparece 28 para G04:M033/M034 ni G11:M011. Las tres firmas28 10 49 siguen en0925D1/0E664C/0EEC2C con contexto gráfico; no son consumidores de guion confirmados. No cambia la conclusión sobre consumidores ni su alcance NOT_VALIDATED.

ROM HF19 comprobada: build/Chocobo_EN_v1.1_HF19_TEST.ws, SHA256 f27e69f65e134b161c1f3ce263c3ed78a8ae247997c95d7383c43c4a78c8962f. Esta revisión corrige la investigación estática; no añade ejecución runtime.
