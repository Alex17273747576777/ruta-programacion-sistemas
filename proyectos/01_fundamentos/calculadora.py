"""Etapa 1 · Calculadora CLI segura y exacta con Decimal."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation


class ErrorCalculadora(ValueError):
    """Error controlado para entradas u operaciones inválidas."""


def calcular(izquierda: str, operador: str, derecha: str) -> Decimal:
    """Evalúa una operación aritmética básica sin usar eval().

    Usa Decimal para evitar imprecisiones binarias de punto flotante (p. ej. 0.1 + 0.2).
    """
    try:
        a = Decimal(izquierda.strip())
        b = Decimal(derecha.strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ErrorCalculadora("Entrada numérica inválida") from exc

    if not a.is_finite() or not b.is_finite():
        raise ErrorCalculadora("Solo se aceptan números finitos")

    if operador == "+":
        return a + b
    if operador == "-":
        return a - b
    if operador == "*":
        return a * b
    if operador == "/":
        if b == 0:
            raise ErrorCalculadora("División por cero no permitida")
        return a / b
    raise ErrorCalculadora(f"Operación desconocida: {operador!r}")


def maximo_manual(valores: list[int | float | Decimal]) -> int | float | Decimal:
    """Devuelve el máximo sin inicializar en 0 (soporta negativos)."""
    if not valores:
        raise ErrorCalculadora("La lista está vacía")
    mayor = valores[0]
    for v in valores[1:]:
        if v > mayor:
            mayor = v
    return mayor


def sumar_manual(valores: list[int | float | Decimal]) -> int | float | Decimal:
    """Suma iterativa sin usar la función incorporada sum()."""
    total: int | float | Decimal = 0
    for v in valores:
        total += v
    return total
