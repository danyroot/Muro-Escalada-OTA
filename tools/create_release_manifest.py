#!/usr/bin/env python3
"""Assemble and sign immutable ESP32-C6 GitHub Release OTA assets."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys


DEFAULT_REPOSITORY = "danyroot/Muro-Escalada-OTA"
DEFAULT_KEY = Path.home() / ".muro-escalada-ota" / "signing" / "ecdsa_p256_private.pem"


def sha256_and_size(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as binary:
        for chunk in iter(lambda: binary.read(64 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def github_asset_url(repository: str, tag: str, asset: str) -> str:
    return f"https://github.com/{repository}/releases/download/{tag}/{asset}"


def find_openssl() -> str:
    configured = os.environ.get("OPENSSL")
    candidates = [configured] if configured else []
    candidates.extend([
        shutil.which("openssl"),
        r"C:\Program Files\Git\usr\bin\openssl.exe",
        r"C:\Program Files\Git\mingw64\bin\openssl.exe",
    ])
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise RuntimeError("OpenSSL no encontrado. Define OPENSSL con la ruta de openssl.exe.")


def make_manifest(release_version: str, esp_hosted_version: str, driver_led_pixel_version: str,
                  repository: str, integrated_asset: str,
                  integrated_bin: Path, super_mini_asset: str,
                  super_mini_bin: Path) -> bytes:
    tag = f"c6-v{release_version}"
    integrated_hash, integrated_size = sha256_and_size(integrated_bin)
    super_mini_hash, super_mini_size = sha256_and_size(super_mini_bin)
    lines = [
        "format=1",
        f"release={tag}",
        f"esp_hosted.version={esp_hosted_version}",
        f"esp_hosted.url={github_asset_url(repository, tag, integrated_asset)}",
        f"esp_hosted.sha256={integrated_hash}",
        f"esp_hosted.size={integrated_size}",
        f"driver_led_pixel.version={driver_led_pixel_version}",
        f"driver_led_pixel.url={github_asset_url(repository, tag, super_mini_asset)}",
        f"driver_led_pixel.sha256={super_mini_hash}",
        f"driver_led_pixel.size={super_mini_size}",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-version", required=True, help="Version del Release, por ejemplo 2.11.1")
    parser.add_argument("--esp-hosted-version", required=True)
    parser.add_argument("--driver-led-pixel-version", required=True)
    parser.add_argument("--integrated-bin", required=True, type=Path)
    parser.add_argument("--super-mini-bin", required=True, type=Path)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--signing-key", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--output-dir", type=Path, default=Path("release"))
    args = parser.parse_args()

    for image in (args.integrated_bin, args.super_mini_bin):
        if not image.is_file():
            parser.error(f"No existe el binario: {image}")
    if not args.signing_key.is_file():
        parser.error(f"No existe la clave privada: {args.signing_key}")
    for version in (args.release_version, args.esp_hosted_version, args.driver_led_pixel_version):
        if not version or any(ch not in "0123456789.-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for ch in version):
            parser.error("Una version contiene caracteres no permitidos.")

    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    integrated_asset = f"esp-hosted-{args.esp_hosted_version}.bin"
    super_mini_asset = f"DriverLedPixel-{args.driver_led_pixel_version}.bin"
    manifest_asset = f"manifest-c6-{args.release_version}.txt"
    signature_asset = f"manifest-c6-{args.release_version}.sig"

    manifest = make_manifest(args.release_version, args.esp_hosted_version, args.driver_led_pixel_version,
                             args.repository, integrated_asset,
                             args.integrated_bin, super_mini_asset, args.super_mini_bin)
    manifest_path = output / manifest_asset
    signature_path = output / signature_asset
    manifest_path.write_bytes(manifest)
    shutil.copyfile(args.integrated_bin, output / integrated_asset)
    shutil.copyfile(args.super_mini_bin, output / super_mini_asset)

    command = [find_openssl(), "dgst", "-sha256", "-sign", str(args.signing_key),
               "-out", str(signature_path), str(manifest_path)]
    subprocess.run(command, check=True)
    # GitHub resolves /releases/latest/download/<asset> to the asset bearing
    # this stable name in the newest release. Devices fetch these two files.
    shutil.copyfile(manifest_path, output / "manifest-c6-latest.txt")
    shutil.copyfile(signature_path, output / "manifest-c6-latest.sig")

    print("Assets listos para el Release:")
    for asset in (integrated_asset, super_mini_asset, manifest_asset, signature_asset,
                  "manifest-c6-latest.txt", "manifest-c6-latest.sig"):
        print(output / asset)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
