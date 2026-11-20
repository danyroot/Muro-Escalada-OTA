# Muro-Escalada-OTA

Assets OTA para el ESP32-C6 integrado ESP-Hosted y el ESP32-C6 Super Mini
DriverLedPixel. El ESP32-P4 conserva RainMaker como su mecanismo OTA.

## Seguridad

Cada Release contiene un manifiesto con firma ECDSA P-256/SHA-256 y hashes
SHA-256 de los binarios. La clave privada de firma no se guarda en este
repositorio. Consulta [`docs/manifest-format.md`](docs/manifest-format.md).

## Preparar un Release

Compila ambos C6 y ejecuta localmente:

```powershell
python tools/create_release_manifest.py `
  --version 1.0.0 `
  --integrated-bin ..\UpdateEsp32c6_2.11.0_Esp-Now\build\network_adapter.bin `
  --super-mini-bin ..\DriverLedPixel-Esp-Now\build\DriverLedPixel.bin
```

El comando genera en `release/` los cuatro assets que deben cargarse en un
GitHub Release con tag `c6-v1.0.0`. Antes de publicar, comprueba que la
versión y los hashes correspondan con los binarios que se van a distribuir.
