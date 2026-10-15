# Chocobo English HF13 TEST — QA18/M4

Cuarta iteración de maquetación ejecutada. Cinco recursos corregidos; siete PASS sintéticos acotados. No existe aprobación visual o lingüística global. El caso preset32/F00:I053 sigue sin contexto confirmado.

Lea INFORME_ES.md, docs/issue_register.json y CONTEXTO_CONTINUACION.md. El paquete contiene fuentes acumulativas reconstruidas, BPS directo desde la ROM japonesa CRC32 CCAA4853 y evidencias; no contiene ROM ni BIOS.

```sh
python3 build.py /ruta/original-japonesa.ws --out /ruta/build-hf13
python3 qa18/verify_scope.py --japanese-rom /ruta/original-japonesa.ws --out /ruta/verificacion-qa18.json
python3 -m unittest discover -s tests
```

Aplicar patches/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps sólo a JP limpia. La carpeta patches/historical conserva los parches anteriores. Las verificaciones QA15/16/17 quedan ligadas a sus builds históricos, no al target actual.
