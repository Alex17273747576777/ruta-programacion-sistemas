#!/usr/bin/env python3
"""Verifica que docs/index.html está actualizado, autocontenido y libre de URLs inválidas."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from generar_portal import construir_html  # noqa: E402


def main() -> int:
    portal = RAIZ / "docs" / "index.html"
    if not portal.is_file():
        print("FALLO: falta docs/index.html")
        return 1
    actual = portal.read_text(encoding="utf-8")
    esperado = construir_html()
    if actual != esperado:
        print("FALLO: docs/index.html está desactualizado respecto a scripts/generar_portal.py")
        return 1
    if "fnhy.net" in actual.lower():
        print("FALLO: dominio inválido fnhy.net encontrado en docs/index.html")
        return 1
    preguntas = json.loads((RAIZ / "quizzes" / "banco_preguntas.json").read_text(encoding="utf-8"))
    if len(preguntas) < 26:
        print(f"FALLO: se esperaban al menos 26 preguntas en el quiz, hay {len(preguntas)}")
        return 1
    print(f"OK: docs/index.html sincronizado, autocontenido y con {len(preguntas)} preguntas del quiz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
