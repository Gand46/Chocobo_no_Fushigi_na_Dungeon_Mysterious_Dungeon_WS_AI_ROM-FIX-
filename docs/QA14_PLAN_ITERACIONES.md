# Dos tareas globales separadas

Estimación provisional: **6 iteraciones coordinadas**, con rango de planificación **6–8**, revisable tras la primera. No hay un límite máximo garantizado. El logo ya está cerrado en el alcance QA14.

| Iteración | Maquetación | Lingüística | Resultado requerido |
|---|---|---|---|
| 1 | Censo de recursos y contextos | Original JP, texto EN y glosario | Universo trazable y estimación ajustada |
| 2 | UI, inventario y propiedades pendientes | Nombres, descripciones y terminología | Lote revisado en ambas dimensiones |
| 3 | Diálogos, tiendas, tutoriales, eventos y créditos | — | Cobertura de ventanas, variables y paginación |
| 4 | — | Diálogos principales y relato | Fidelidad y naturalidad por entrada |
| 5 | — | Ramas tardías, variantes, ayudas y créditos | Coherencia de todo el glosario |
| 6 | Regresión de textos modificados y cobertura | Conciliación final de correcciones | Cierre de ambos registros dentro del universo definido |

Maquetación participa en **4** iteraciones; lingüística en **5**. Se comparten **3**: 4+5−3=6. Las reservas 7/8 se activan sólo con recursos o defectos concretos que lo justifiquen.

El censo de 2333 entradas/19 familias (1970 no vacías según estructura) no demuestra cobertura de todos los diálogos. Los 255 IDs de objetos y 96 descriptores ya revisados son unidades diferentes; no se restan de ese total. La primera iteración debe definir qué entradas son texto visible, localizar los scripts externos al getter y registrar exclusiones.

Detalle reproducible: `QA14_PLAN_ITERACIONES.json`; inventario base: `../qa14/text_family_inventory.json`.
