# Continuar desde HF11 TEST / QA16 M2

M2 de4 ejecutada con16 PASS_SYNTHETIC acotados; maquetación global y fidelidad lingüística siguen abiertas. No hay cambios de ROM ni BPS frente aHF11/QA15. No crearHF12 a partir de esta revisión.

Autoridad actual: manifest.json, docs/QA16_VALIDATION.json, QA16_RUN_INDEX.json, QA16_PLAN_MAQUETACION.json, issue_register.json. Siguiente M3: diálogos/tutoriales/eventos/créditos,13 alertas heredadas,9 recursos dinámicos. M4 integra y reconcilia los contextos pendientes. Dos iteraciones base restantes son estimación, no promesa de cierre total.

Estado y equipamiento: ingresar los registros de inventario en6C9F, no sólo6BF5, porque la inicialización reconstruye el equipo. Flags18h equipan e identifican. Campo nivel99/+99 y157/-99. Nombre largoF03:I136+modificador termina en208px, dentro del área. Cantidad visible99 en Fire/Teleport Box; F14:I087/I093 son los dos nombres no identificados más anchos144px.

Comercio: el checkpoint qa3/shop_dialog está afuera de la tienda. qa16 shop_enter alcanza el interior. Las primeras rutas sólo leen diálogo de historia. Rama op71: banco0 bits en7309+2*(id//16). La prueba útil cambia, una vez en CPU4D160 antes de seleccionar bancoC2, 649B=E0 y64A1=0D0E desdeE1:1DA2. No entrar en0D0D: esRET de guion. Activar bit26h en730D (40h) habilitaBuy. Buy/Sell son ventanas11..16. NO marcar como natural. El script conserva el bucle nativo de lista, precio y compra/venta. Compra:99,999,999→99,999,899, nuevaPotionID73. VentaID136+99:2898Gil; ID157-99:1Gil. Confirmar selección real: el inventario se ordena y las primeras pruebas llamadasplus/minus elegíanFire oel+99, noel-99.

CandidatoM2-C01: preset32, initializer1860AF, row188F2C, F00:I053. Primera páginaStore1..5; forzar64C4=5 muestra pregunta de pisos recortada antes deStore7..10. La tabla prevé10filas pero no se encontró caller nativo válido que llegue aesa página. Es candidata de contexto, NO defecto alcanzable demostrado. El recursoJP también ocupa la misma posición; no cambiarlo porStore6 sin revisar todos los consumidores. Los intentos window49 y shop_default NOson fallos deROM: contexto incompatible / timeout.

Reproducción: qa16/run.py ROM checkpoint plan out --mesen Mesen --timeout15; LAYOUT_OBSERVER=qa16/layout_observer.lua (v3) oelobserver.lua archivado con cada ejecución. Metadatos ystate_path están enprovenance.json. v2 no registra stores/initializers/script. TagWRAM_POKE se conserva por convención del proyecto; las escrituras físicas de fixtures van awsCartRam/SRAM. Pruebas de magia conbytes255 son stress de entrada, noafirmación de límites alcanzables. Cero guardas comunes noevalúa todas las escrituras ni todas las rutinas numéricas.

QA10/12,QA13funcional yQA14logo se heredan por identidad exacta delROM; no repetir barridos255/96,logo orecorridos naturales sin riesgo nuevo. Paquete no incluyeROM,BIOS,emulador. El BPS es acumulativo desdeJPCCAA4853.

QA16 final: `magic_display99` sustituye al ensayo `magic_boundaries` en la lista de PASS. Los valores 99 se muestran completos (Lv.99, ATB99 y NEXT99P). El ensayo anterior con 255 se conserva como diagnóstico excluido porque supera el formato de dos cifras. No demuestra un defecto alcanzable de la ROM.
