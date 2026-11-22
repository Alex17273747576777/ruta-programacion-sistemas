"""Motor mínimo de Lógica de Primer Orden: unificación de Robinson (con occurs check) y resolución SLD."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union


@dataclass(frozen=True)
class Var:
    nombre: str


@dataclass(frozen=True)
class Term:
    functor: str
    args: Tuple["Expr", ...] = ()


Expr = Union[Var, Term]
Sustitucion = Dict[str, Expr]


@dataclass(frozen=True)
class Clausula:
    cabeza: Term
    cuerpo: Tuple[Term, ...] = ()


def aplicar_sustitucion(expr: Expr, sust: Sustitucion) -> Expr:
    while isinstance(expr, Var) and expr.nombre in sust:
        expr = sust[expr.nombre]
    if isinstance(expr, Term):
        return Term(expr.functor, tuple(aplicar_sustitucion(a, sust) for a in expr.args))
    return expr


def ocurre_en(var: Var, expr: Expr, sust: Sustitucion) -> bool:
    expr = aplicar_sustitucion(expr, sust)
    if isinstance(expr, Var):
        return expr == var
    return any(ocurre_en(var, a, sust) for a in expr.args)


def unificar(x: Expr, y: Expr, sust: Optional[Sustitucion] = None) -> Optional[Sustitucion]:
    """Algoritmo de unificación de Robinson con occurs check obligatorio."""
    env = dict(sust or {})
    x = aplicar_sustitucion(x, env)
    y = aplicar_sustitucion(y, env)

    if x == y:
        return env
    if isinstance(x, Var):
        if ocurre_en(x, y, env):
            return None
        env[x.nombre] = y
        return env
    if isinstance(y, Var):
        if ocurre_en(y, x, env):
            return None
        env[y.nombre] = x
        return env
    if isinstance(x, Term) and isinstance(y, Term):
        if x.functor != y.functor or len(x.args) != len(y.args):
            return None
        for a, b in zip(x.args, y.args):
            env = unificar(a, b, env)
            if env is None:
                return None
        return env
    return None


def _renombrar_expr(expr: Expr, sufijo: int) -> Expr:
    if isinstance(expr, Var):
        return Var(f"{expr.nombre}__r{sufijo}")
    return Term(expr.functor, tuple(_renombrar_expr(a, sufijo) for a in expr.args))


def renombrar_clausula(clausula: Clausula, sufijo: int) -> Clausula:
    return Clausula(
        cabeza=_renombrar_expr(clausula.cabeza, sufijo),  # type: ignore[arg-type]
        cuerpo=tuple(_renombrar_expr(g, sufijo) for g in clausula.cuerpo),  # type: ignore[arg-type]
    )


def resolver_sld(
    base: Iterable[Clausula],
    metas: Tuple[Term, ...],
    sust: Optional[Sustitucion] = None,
    profundidad: int = 0,
    max_profundidad: int = 32,
) -> Iterator[Sustitucion]:
    """Resolución SLD por backtracking sobre cláusulas de Horn con límite de profundidad."""
    env = dict(sust or {})
    if not metas:
        yield env
        return
    if profundidad >= max_profundidad:
        return

    primera, resto = metas[0], metas[1:]
    lista_base = list(base)
    for idx, clausula in enumerate(lista_base):
        c = renombrar_clausula(clausula, profundidad * 1000 + idx + 1)
        nueva_sust = unificar(primera, c.cabeza, env)
        if nueva_sust is not None:
            nuevas_metas = c.cuerpo + resto
            yield from resolver_sld(lista_base, nuevas_metas, nueva_sust, profundidad + 1, max_profundidad)
