

<!-- project-continuity:start -->
## Continuidad verificable
Antes de editar, leer .continuity/RESUME.md y PROJECT_CONTEXT.md si existe;
ejecutar python3 tools/continuity.py verify . y contrastar el snapshot esperado.
Usar las fuentes activas verificadas. No elegir una base solo por fecha/nombre,
ni retroceder a una compilacion antigua porque falten fuentes recientes.
Conservar fuentes, recursos, herramientas, tablas, licencias y dependencias
heredadas. Registrar movimientos/retiros justificados en CONTINUITY_MIGRATIONS.json.
Guardar avances con checkpoint; entregar fuentes formales con release.
Un checkpoint conserva trabajo y no certifica compilacion, jugabilidad o calidad.
Probar release desde el ZIP extraido; no usar salidas de compilacion anteriores.
Guardar el ZIP en un destino duradero autorizado y registrar su id/hash antes
de cerrar. Un archivo local o un enlace sandbox no confirma guardado duradero.
Ante un faltante, preservar el WIP y recuperar solo el objeto identificado.
No pedir al usuario archivos que ya pueden recuperarse en los recursos conectados.
<!-- project-continuity:end -->
