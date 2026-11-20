# Formato de manifiesto OTA C6 v1

Cada GitHub Release de C6 contiene un manifiesto de texto UTF-8 y su firma
ECDSA P-256/SHA-256 DER separada. El manifiesto usa saltos de línea `LF` y
termina con un `LF`; esos bytes exactos son los que se firman.

```text
format=1
release=c6-v1.0.0
esp_hosted.version=1.0.0
esp_hosted.url=https://github.com/danyroot/Muro-Escalada-OTA/releases/download/c6-v1.0.0/esp-hosted-1.0.0.bin
esp_hosted.sha256=<64 hex SHA-256>
esp_hosted.size=<bytes>
driver_led_pixel.version=1.0.0
driver_led_pixel.url=https://github.com/danyroot/Muro-Escalada-OTA/releases/download/c6-v1.0.0/DriverLedPixel-1.0.0.bin
driver_led_pixel.sha256=<64 hex SHA-256>
driver_led_pixel.size=<bytes>
```

Los assets del Release son:

- `esp-hosted-<version>.bin`
- `DriverLedPixel-<version>.bin`
- `manifest-c6-<version>.txt`
- `manifest-c6-<version>.sig`
- `manifest-c6-latest.txt`
- `manifest-c6-latest.sig`

Los dos assets `latest` contienen exactamente los mismos bytes que el
manifest y la firma versionados del Release. Permiten que los dispositivos
consulten el Release más reciente mediante la URL estable de GitHub.

El firmware rechaza un manifiesto si falla la firma, el destino, el tamaño,
la URL HTTPS o el SHA-256. La firma autentica el manifiesto; el SHA-256
vincula exactamente el binario descargado con ese manifiesto.

La clave privada no forma parte de este repositorio ni de los dispositivos.
