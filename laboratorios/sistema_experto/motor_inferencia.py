"""Motor de inferencia simbolico y controlador difuso Mamdani.

Implementa:
- Encadenamiento hacia adelante (Forward Chaining) con control de refraccion.
- Encadenamiento hacia atras (Backward Chaining) con deteccion de ciclos y traza explicable.
- Combinacion de Factores de Certeza (MYCIN, Shortliffe 1975).
- Controlador difuso triangular Mamdani con defusificacion por centroide.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Regla:
    id: str
    antecedentes: tuple[str, ...]
    consecuente: str
    cf: float = 1.0
    prioridad: int = 0

    def __post_init__(self) -> None:
        if not self.antecedentes:
            raise ValueError(f"La regla {self.id} debe tener al menos un antecedente")
        if not (-1.0 <= self.cf <= 1.0):
            raise ValueError(f"El factor de certeza de {self.id} debe estar en [-1, 1]")


def combinar_cf_mycin(cf1: float, cf2: float) -> float:
    """Combina dos factores de certeza independientes segun Shortliffe (MYCIN)."""
    if cf1 > 0 and cf2 > 0:
        return round(cf1 + cf2 * (1.0 - cf1), 6)
    if cf1 < 0 and cf2 < 0:
        return round(cf1 + cf2 * (1.0 + cf1), 6)
    denom = 1.0 - min(abs(cf1), abs(cf2))
    if denom == 0:
        return 0.0
    return round((cf1 + cf2) / denom, 6)


@dataclass
class ResultadoInferencia:
    hechos: dict[str, float]
    reglas_disparadas: list[str] = field(default_factory=list)
    traza: list[str] = field(default_factory=list)


class MotorExperto:
    def __init__(self, reglas: list[Regla]) -> None:
        # Orden estable: mayor prioridad y mayor especificidad (mas antecedentes) primero
        self.reglas = sorted(
            reglas,
            key=lambda r: (r.prioridad, len(r.antecedentes), r.id),
            reverse=True,
        )

    def encadenamiento_adelante(self, hechos_iniciales: dict[str, float]) -> ResultadoInferencia:
        memoria = dict(hechos_iniciales)
        disparadas: set[str] = set()
        orden_reglas: list[str] = []
        traza: list[str] = []

        cambio = True
        while cambio:
            cambio = False
            for regla in self.reglas:
                if regla.id in disparadas:
                    continue
                if all(memoria.get(a, 0.0) > 0.0 for a in regla.antecedentes):
                    cf_ant = min(memoria[a] for a in regla.antecedentes)
                    cf_nuevo = round(cf_ant * regla.cf, 6)
                    disparadas.add(regla.id)
                    orden_reglas.append(regla.id)

                    if regla.consecuente in memoria:
                        combinado = combinar_cf_mycin(memoria[regla.consecuente], cf_nuevo)
                        if combinado != memoria[regla.consecuente]:
                            memoria[regla.consecuente] = combinado
                            cambio = True
                    else:
                        memoria[regla.consecuente] = cf_nuevo
                        cambio = True

                    traza.append(
                        f"{regla.id}: SI {' Y '.join(regla.antecedentes)} -> {regla.consecuente} "
                        f"(CF regla={regla.cf:.2f}, CF aporte={cf_nuevo:.4f}, CF acumulado={memoria[regla.consecuente]:.4f})"
                    )
        return ResultadoInferencia(hechos=memoria, reglas_disparadas=orden_reglas, traza=traza)

    def encadenamiento_atras(
        self,
        meta: str,
        hechos_iniciales: dict[str, float],
        visitados: frozenset[str] | None = None,
    ) -> tuple[bool, float, list[str]]:
        if visitados is None:
            visitados = frozenset()
        if meta in visitados:
            return False, 0.0, [f"Ciclo evitado al intentar probar '{meta}'"]

        if hechos_iniciales.get(meta, 0.0) > 0.0:
            cf = hechos_iniciales[meta]
            return True, cf, [f"Hecho observado: {meta} (CF={cf:.4f})"]

        nuevos_visitados = visitados | {meta}
        candidatas = [r for r in self.reglas if r.consecuente == meta]
        cf_acumulado: float | None = None
        explicacion: list[str] = []

        for regla in candidatas:
            sub_cfs: list[float] = []
            sub_trazas: list[str] = []
            ok = True
            for ant in regla.antecedentes:
                probado, cf_a, traza_a = self.encadenamiento_atras(ant, hechos_iniciales, nuevos_visitados)
                if not probado or cf_a <= 0.0:
                    ok = False
                    break
                sub_cfs.append(cf_a)
                sub_trazas.extend(traza_a)

            if ok:
                cf_regla = round(min(sub_cfs) * regla.cf, 6)
                cf_acumulado = cf_regla if cf_acumulado is None else combinar_cf_mycin(cf_acumulado, cf_regla)
                explicacion.extend(sub_trazas)
                explicacion.append(
                    f"Regla {regla.id} demostro '{meta}' (CF={cf_regla:.4f}, acumulado={cf_acumulado:.4f})"
                )

        if cf_acumulado is not None and cf_acumulado > 0.0:
            return True, cf_acumulado, explicacion
        return False, 0.0, [f"No se pudo demostrar '{meta}'"]


def membresia_triangular(x: float, a: float, b: float, c: float) -> float:
    """Funcion de pertenencia triangular en [0, 1]."""
    if x <= a or x >= c:
        if x == b and (a == b or b == c):
            return 1.0
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


def evaluar_difuso_riego(humedad_pct: float, temp_c: float) -> float:
    """Controlador difuso Mamdani que devuelve apertura de valvula en [0, 100]%."""
    humedad_pct = max(0.0, min(100.0, humedad_pct))
    temp_c = max(0.0, min(50.0, temp_c))

    # Fusificacion
    h_seca = membresia_triangular(humedad_pct, 0.0, 0.0, 45.0)
    h_media = membresia_triangular(humedad_pct, 25.0, 50.0, 75.0)
    h_humeda = membresia_triangular(humedad_pct, 55.0, 100.0, 100.0)

    t_fria = membresia_triangular(temp_c, 0.0, 0.0, 20.0)
    t_templada = membresia_triangular(temp_c, 15.0, 25.0, 35.0)
    t_calurosa = membresia_triangular(temp_c, 28.0, 50.0, 50.0)

    # Reglas difusas Mamdani (MIN para AND, MAX para agregacion)
    riego_bajo = max(h_humeda, min(h_media, t_fria))
    riego_medio = max(min(h_media, t_templada), min(h_seca, t_fria))
    riego_alto = max(min(h_seca, t_calurosa), min(h_seca, t_templada), min(h_media, t_calurosa))

    # Defusificacion por centroide discreto en [0..100]
    numerador = 0.0
    denominador = 0.0
    for z in range(0, 101):
        mu_bajo = min(riego_bajo, membresia_triangular(float(z), 0.0, 0.0, 40.0))
        mu_medio = min(riego_medio, membresia_triangular(float(z), 25.0, 50.0, 75.0))
        mu_alto = min(riego_alto, membresia_triangular(float(z), 60.0, 100.0, 100.0))
        mu = max(mu_bajo, mu_medio, mu_alto)
        numerador += z * mu
        denominador += mu

    if denominador == 0.0:
        return 0.0
    return round(numerador / denominador, 2)
