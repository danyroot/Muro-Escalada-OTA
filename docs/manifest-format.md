# Formato de manifiesto OTA C6 v1

Cada GitHub Release de C6 contiene un manifiesto de texto UTF-8 y su firma
ECDSA P-256/SHA-256 DER separada. El manifiesto usa saltos de línea `LF` y
termina con un `LF`; esos bytes exactos son los que se firman.

```text
format=1
release=c6-v1.0.0
integrated_c6.version=1.0.0
integrated_c6.url=https://github.com/danyroot/Muro-Escalada-OTA/releases/download/c6-v1.0.0/integrated-c6-1.0.0.bin
integrated_c6.sha256=<64 hex SHA-256>
integrated_c6.size=<bytes>
super_mini_c6.version=1.0.0
super_mini_c6.url=https://github.com/danyroot/Muro-Escalada-OTA/releases/download/c6-v1.0.0/super-mini-c6-1.0.0.bin
super_mini_c6.sha256=<64 hex SHA-256>
super_mini_c6.size=<bytes>
```

Los assets del Release son:

- `integrated-c6-<version>.bin`
- `super-mini-c6-<version>.bin`
- `manifest-c6-<version>.txt`
- `manifest-c6-<version>.sig`

El firmware rechaza un manifiesto si falla la firma, el destino, el tamaño,
la URL HTTPS o el SHA-256. La firma autentica el manifiesto; el SHA-256
vincula exactamente el binario descargado con ese manifiesto.

La clave privada no forma parte de este repositorio ni de los dispositivos.
