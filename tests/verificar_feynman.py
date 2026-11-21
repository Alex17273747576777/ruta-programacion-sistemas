#!/usr/bin/env python3
"""Verifica que README.md y las 6 etapas aplican de forma completa los 4 pasos
del método Richard Feynman y que sus enlaces locales existen."""
from pathlib import Path
import re
import sys

RAIZ = Path(__file__).resolve().parents[1]

PASOS = [
    "1. **Seleccionar y estudiar el concepto:**",
    "2. **Enseñarlo",
    "3. **Identificar lagunas y volver a la fuente original:**",
    "4. **Simplificar y revisar con analogías",
]

def main() -> int:
    errores: list[str] = []
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for p in PASOS:
        if p not in readme:
            errores.append(f"README.md: falta paso Feynman '{p}'")

    etapas = sorted((RAIZ / "etapas").glob("*.md"))
    if len(etapas) != 6:
        errores.append(f"Se esperaban 6 etapas, hay {len(etapas)}")

    for etapa in etapas:
        txt = etapa.read_text(encoding="utf-8")
        if "## Método Richard Feynman (4 pasos obligatorios)" not in txt:
            errores.append(f"{etapa.name}: falta sección '## Método Richard Feynman (4 pasos obligatorios)'")
        for p in PASOS:
            if p not in txt:
                errores.append(f"{etapa.name}: falta paso '{p}'")
        if "Analogía" not in txt:
            errores.append(f"{etapa.name}: falta analogía explícita en paso 4")

    # Verificar enlaces locales de README.md
    for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", readme):
        href = m.group(1)
        if not href.startswith("http") and not href.startswith("#"):
            if not (RAIZ / href).exists():
                errores.append(f"README.md: enlace roto '{href}'")

    if errores:
        for e in errores:
            print("FALLO:", e)
        return 1
    print(f"OK: README.md + {len(etapas)} etapas cumplen los 4 pasos completos del método Richard Feynman.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
