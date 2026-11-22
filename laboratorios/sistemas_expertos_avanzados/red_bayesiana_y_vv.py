"""Inferencia Bayesiana exacta por enumeración en DAG y Verificación/Validación (V&V) de reglas."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple


@dataclass(frozen=True)
class NodoBayes:
    nombre: str
    padres: Tuple[str, ...]
    # Mapea tupla de valores booleanos de los padres (ej. (True, False)) -> P(nodo=True | padres)
    cpt: Dict[Tuple[bool, ...], float]

    def prob(self, valor: bool, asignacion: Dict[str, bool]) -> float:
        clave = tuple(asignacion[p] for p in self.padres)
        p_true = self.cpt[clave]
        return p_true if valor else (1.0 - p_true)


class RedBayesiana:
    def __init__(self, nodos: List[NodoBayes]) -> None:
        self.nodos = nodos
        self.por_nombre = {n.nombre: n for n in nodos}
        self._validar_dag()

    def _validar_dag(self) -> None:
        vistos: Set[str] = set()
        for nodo in self.nodos:
            for p in nodo.padres:
                if p not in vistos:
                    raise ValueError(f"Orden topológico inválido o ciclo: padre '{p}' antes de '{nodo.nombre}'")
            vistos.add(nodo.nombre)

    def _enumerar_todo(self, variables: List[str], evidencia: Dict[str, bool]) -> float:
        if not variables:
            return 1.0
        primera, resto = variables[0], variables[1:]
        nodo = self.por_nombre[primera]
        if primera in evidencia:
            val = evidencia[primera]
            return nodo.prob(val, evidencia) * self._enumerar_todo(resto, evidencia)

        total = 0.0
        for val in (True, False):
            ext = dict(evidencia)
            ext[primera] = val
            total += nodo.prob(val, ext) * self._enumerar_todo(resto, ext)
        return total

    def consultar(self, consulta: str, evidencia: Dict[str, bool]) -> Dict[bool, float]:
        """Calcula la distribución exacta P(consulta | evidencia) normalizada."""
        orden = [n.nombre for n in self.nodos]
        p_true = self._enumerar_todo(orden, {**evidencia, consulta: True})
        p_false = self._enumerar_todo(orden, {**evidencia, consulta: False})
        z = p_true + p_false
        if z <= 0.0:
            raise ValueError("Evidencia imposible (probabilidad conjunta 0)")
        return {True: p_true / z, False: p_false / z}


@dataclass(frozen=True)
class ReglaLogica:
    rid: str
    premisas: frozenset[str]
    conclusion: Tuple[str, str]  # (atributo, valor)


def verificar_base_reglas(reglas: Iterable[ReglaLogica], observables: Set[str]) -> Dict[str, List[str]]:
    """Auditoría estática V&V: detecta conflictos, subsunción/redundancia, ciclos e inalcanzables."""
    lista = list(reglas)
    conflictos: List[str] = []
    redundancias: List[str] = []
    inalcanzables: List[str] = []
    ciclos: List[str] = []

    for i, r1 in enumerate(lista):
        for r2 in lista[i + 1 :]:
            if r1.premisas == r2.premisas and r1.conclusion[0] == r2.conclusion[0] and r1.conclusion[1] != r2.conclusion[1]:
                conflictos.append(f"{r1.rid} vs {r2.rid}: conflicto en '{r1.conclusion[0]}'")
            if r1.conclusion == r2.conclusion:
                if r1.premisas.issubset(r2.premisas):
                    redundancias.append(f"{r2.rid} subsumida por {r1.rid}")
                elif r2.premisas.issubset(r1.premisas):
                    redundancias.append(f"{r1.rid} subsumida por {r2.rid}")

    concluidos = {f"{r.conclusion[0]}={r.conclusion[1]}" for r in lista}
    disponibles = set(observables) | concluidos
    for r in lista:
        faltantes = sorted(r.premisas - disponibles)
        if faltantes:
            inalcanzables.append(f"{r.rid}: premisas sin origen {faltantes}")

    # Grafo dirigido de dependencias para detectar ciclos
    aristas: Dict[str, Set[str]] = {}
    for r in lista:
        dest = f"{r.conclusion[0]}={r.conclusion[1]}"
        for p in r.premisas:
            aristas.setdefault(p, set()).add(dest)

    visitado: Set[str] = set()
    en_pila: Set[str] = set()

    def dfs(nodo: str) -> None:
        visitado.add(nodo)
        en_pila.add(nodo)
        for nxt in sorted(aristas.get(nodo, ())):
            if nxt in en_pila:
                ciclos.append(f"{nodo} -> {nxt}")
            elif nxt not in visitado:
                dfs(nxt)
        en_pila.remove(nodo)

    for n in sorted(aristas):
        if n not in visitado:
            dfs(n)

    return {
        "conflictos": conflictos,
        "redundancias": redundancias,
        "inalcanzables": inalcanzables,
        "ciclos": ciclos,
    }
