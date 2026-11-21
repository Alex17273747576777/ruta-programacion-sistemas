#!/usr/bin/env python3
"""Evaluador de quizzes técnicos con retroalimentación Feynman."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BANCO_POR_DEFECTO = Path(__file__).resolve().parent / "banco_preguntas.json"


def cargar_preguntas(ruta: Path = BANCO_POR_DEFECTO, etapa: str | None = None) -> list[dict]:
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if etapa:
        return [p for p in datos if p["etapa"] == etapa]
    return datos


def evaluar_respuestas(preguntas: list[dict], elecciones: list[int]) -> tuple[int, int, list[dict]]:
    """Compara una lista de índices elegidos (0-based) y devuelve puntaje + detalle Feynman."""
    if len(elecciones) != len(preguntas):
        raise ValueError("Número de respuestas distinto al número de preguntas")
    aciertos = 0
    detalle: list[dict] = []
    for p, eleccion in zip(preguntas, elecciones):
        es_ok = eleccion == p["correcta"]
        if es_ok:
            aciertos += 1
        detalle.append(
            {
                "id": p["id"],
                "correcto": es_ok,
                "elegida": eleccion,
                "esperada": p["correcta"],
                "explicacion_feynman": p["explicacion_feynman"],
            }
        )
    return aciertos, len(preguntas), detalle


def main() -> int:
    parser = argparse.ArgumentParser(description="Quiz CLI de Ruta de Programación y Sistemas")
    parser.add_argument("--etapa", help="Filtrar por identificador de etapa o guía")
    parser.add_argument("--listar", action="store_true", help="Mostrar etapas disponibles y total de preguntas")
    args = parser.parse_args()

    todas = cargar_preguntas()
    if args.listar:
        etapas: dict[str, int] = {}
        for p in todas:
            etapas[p["etapa"]] = etapas.get(p["etapa"], 0) + 1
        for k, v in sorted(etapas.items()):
            print(f"- {k}: {v} pregunta(s)")
        print(f"Total: {len(todas)} preguntas")
        return 0

    preguntas = cargar_preguntas(etapa=args.etapa)
    if not preguntas:
        print("No hay preguntas para ese filtro.")
        return 1

    elecciones: list[int] = []
    for idx, p in enumerate(preguntas, 1):
        print(f"\n[{idx}/{len(preguntas)}] ({p['etapa']}) {p['pregunta']}")
        for i, opt in enumerate(p["opciones"], 1):
            print(f"  {i}) {opt}")
        while True:
            raw = input("Tu respuesta (1-4): ").strip()
            if raw in {"1", "2", "3", "4"}:
                elecciones.append(int(raw) - 1)
                break
            print("Ingresa un número entre 1 y 4.")

    aciertos, total, detalle = evaluar_respuestas(preguntas, elecciones)
    print(f"\nResultado: {aciertos}/{total}")
    for d in detalle:
        marca = "OK" if d["correcto"] else f"FALLO (correcta: {d['esperada'] + 1})"
        print(f"- {d['id']}: {marca}\n  Feynman: {d['explicacion_feynman']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
