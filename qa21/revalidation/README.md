# HF16 V3: revalidación desde fuentes completas

Desde la raíz del ZIP extraído, con Python 3 y Pillow:

```bash
python3 qa21/revalidate_delivery.py --japanese-rom /ruta/Chocobo_JP.ws --out /ruta/qa21_revalidation
```

La entrada es la ROM JP limpia SHA-256 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728. El comando reconstruye ROM y BPS, compara la regeneración editable, repite 3365 verificaciones del lote, comprueba los consumidores y enlaces de píxeles archivados, y ejecuta las pruebas unitarias. Los resultados se escriben fuera de las fuentes para conservar el snapshot. Una selección sintética no acredita una ruta natural del juego.
