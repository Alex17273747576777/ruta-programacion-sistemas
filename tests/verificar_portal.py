#!/usr/bin/env python3
"""Verifica que docs/index.html está actualizado, autocontenido, sin enlaces ../ rotos y con todos los módulos."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from generar_portal import cargar_modulos, construir_html  # noqa: E402


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
    if 'href="../' in actual:
        print("FALLO: docs/index.html contiene enlaces relativos href=\"../\" rotos para GitHub Pages")
        return 1
    modulos = cargar_modulos()
    if len(modulos) < 28:
        print(f"FALLO: se esperaban al menos 28 módulos embebidos, hay {len(modulos)}")
        return 1
    if 'id="experto"' not in actual or 'runExperto()' not in actual:
        print("FALLO: falta el playground interactivo de Motor Experto en docs/index.html")
        return 1
    if 'id="unificacion"' not in actual or 'runUnificacion()' not in actual or 'runBayes()' not in actual:
        print("FALLO: falta el playground avanzado LPO/Bayes en docs/index.html")
        return 1
    if 'class="skip-link"' not in actual or ':focus-visible' not in actual:
        print("FALLO: faltan controles de accesibilidad básica en docs/index.html")
        return 1
    preguntas = json.loads((RAIZ / "quizzes" / "banco_preguntas.json").read_text(encoding="utf-8"))
    if len(preguntas) < 48:
        print(f"FALLO: se esperaban al menos 48 preguntas en el quiz, hay {len(preguntas)}")
        return 1
    print(
        f"OK: docs/index.html sincronizado, sin 404 relativos, con {len(modulos)} módulos embebidos "
        f"y {len(preguntas)} preguntas del quiz."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
