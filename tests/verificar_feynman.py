#!/usr/bin/env python3
"""Verifica que README.md, las 6 etapas, las 4 guías y los 5 cheatsheets
aplican los 4 pasos completos del método Richard Feynman y que sus enlaces locales existen."""
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


def verificar_documentos(directorio: Path, esperados: int, nombre: str, errores: list[str]) -> list[Path]:
    archivos = sorted(directorio.glob("*.md"))
    if len(archivos) != esperados:
        errores.append(f"Se esperaban {esperados} {nombre}, hay {len(archivos)}")
    for doc in archivos:
        txt = doc.read_text(encoding="utf-8")
        if "## Método Richard Feynman (4 pasos obligatorios)" not in txt:
            errores.append(f"{doc.relative_to(RAIZ)}: falta sección '## Método Richard Feynman (4 pasos obligatorios)'")
        for p in PASOS:
            if p not in txt:
                errores.append(f"{doc.relative_to(RAIZ)}: falta paso '{p}'")
        if "analogía" not in txt.lower():
            errores.append(f"{doc.relative_to(RAIZ)}: falta analogía explícita en paso 4")
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", txt):
            href = m.group(1)
            if not href.startswith("http") and not href.startswith("#"):
                destino = (doc.parent / href).resolve()
                if not destino.exists():
                    errores.append(f"{doc.relative_to(RAIZ)}: enlace local roto '{href}'")
    return archivos


def main() -> int:
    errores: list[str] = []
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for p in PASOS:
        if p not in readme:
            errores.append(f"README.md: falta paso Feynman '{p}'")

    for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", readme):
        href = m.group(1)
        if not href.startswith("http") and not href.startswith("#"):
            if not (RAIZ / href).exists():
                errores.append(f"README.md: enlace roto '{href}'")

    etapas = verificar_documentos(RAIZ / "etapas", 6, "etapas", errores)
    guias = verificar_documentos(RAIZ / "guias", 8, "guías", errores)
    cheats = verificar_documentos(RAIZ / "cheatsheets", 7, "cheatsheets", errores)

    if errores:
        for e in errores:
            print("FALLO:", e)
        return 1
    print(
        f"OK: README.md + {len(etapas)} etapas + {len(guias)} guías + {len(cheats)} cheatsheets "
        "cumplen los 4 pasos completos del método Richard Feynman y enlaces locales válidos."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
