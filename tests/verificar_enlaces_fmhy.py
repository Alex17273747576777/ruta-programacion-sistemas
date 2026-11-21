#!/usr/bin/env python3
"""Valida formato y presencia de recursos FMHY.net (y opcionalmente conectividad HTTP con --online)."""
from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s)>\"']+")


def extraer_urls() -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []
    archivos = [RAIZ / "recursos" / "fmhy-activos.md"] + sorted((RAIZ / "etapas").glob("*.md")) + sorted((RAIZ / "guias").glob("*.md"))
    vistos: set[str] = set()
    for path in archivos:
        txt = path.read_text(encoding="utf-8")
        for m in URL_RE.finditer(txt):
            url = m.group(0).rstrip(".,;:")
            if url not in vistos:
                vistos.add(url)
                urls.append((str(path.relative_to(RAIZ)), url))
    return urls


def comprobar_http(item: tuple[str, str]) -> tuple[str, str, int, str]:
    origen, url = item
    for metodo in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(
                url,
                method=metodo,
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                return origen, url, r.status, "OK"
        except urllib.error.HTTPError as e:
            if e.code in (403, 405) and metodo == "HEAD":
                continue
            return origen, url, e.code, f"HTTP_{e.code}"
        except Exception as e:
            if metodo == "HEAD":
                continue
            return origen, url, 0, str(e)[:80]
    return origen, url, 0, "ERR"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica los enlaces activos de FMHY y fuentes oficiales")
    parser.add_argument("--online", action="store_true", help="Ejecuta verificación HTTP real contra Internet")
    args = parser.parse_args()

    catalogo = RAIZ / "recursos" / "fmhy-activos.md"
    if not catalogo.is_file():
        print("FALLO: falta recursos/fmhy-activos.md")
        return 1

    urls = extraer_urls()
    if len(urls) < 40:
        print(f"FALLO: se esperaban al menos 40 URLs únicas verificadas, solo hay {len(urls)}")
        return 1

    for origen, url in urls:
        if "fnhy.net" in url.lower():
            print(f"FALLO: URL inválida {url} en {origen} (el dominio real es fmhy.net)")
            return 1

    if not args.online:
        print(f"OK (offline): {len(urls)} URLs únicas válidas en catálogo, etapas y guías (sin dominios rotos).")
        return 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        resultados = list(ex.map(comprobar_http, urls))

    fallos = [r for r in resultados if not (200 <= r[2] < 400)]
    for origen, url, code, msg in fallos:
        print(f"FALLO HTTP ({code} {msg}): {url} [{origen}]")
    if fallos:
        print(f"Total fallos online: {len(fallos)} / {len(resultados)}")
        return 1
    print(f"OK (online): {len(resultados)}/{len(resultados)} URLs activas (2xx/3xx).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
