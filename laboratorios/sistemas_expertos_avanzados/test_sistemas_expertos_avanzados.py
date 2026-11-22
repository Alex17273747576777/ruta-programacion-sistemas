import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from red_bayesiana_y_vv import NodoBayes, RedBayesiana, ReglaLogica, verificar_base_reglas  # noqa: E402
from unificador_prolog import Clausula, Term, Var, aplicar_sustitucion, resolver_sld, unificar  # noqa: E402


class SistemasExpertosAvanzadosTest(unittest.TestCase):
    def test_unificacion_robinson_y_occurs_check(self):
        t1 = Term("depende", (Var("S"), Term("bd_1")))
        t2 = Term("depende", (Term("api_pagos"), Var("N")))
        sust = unificar(t1, t2)
        self.assertIsNotNone(sust)
        assert sust is not None
        self.assertEqual(aplicar_sustitucion(Var("S"), sust), Term("api_pagos"))
        self.assertEqual(aplicar_sustitucion(Var("N"), sust), Term("bd_1"))

        # Occurs check obligatorio: X = lista(X) debe fallar
        ciclico = unificar(Var("X"), Term("lista", (Var("X"),)))
        self.assertIsNone(ciclico)

    def test_resolucion_sld_transitiva_y_backtracking(self):
        base = [
            Clausula(Term("depende", (Term("checkout"), Term("api")))),
            Clausula(Term("depende", (Term("api"), Term("postgres")))),
            Clausula(Term("caido", (Term("postgres"),))),
            Clausula(
                Term("afectado", (Var("S"),)),
                (Term("depende", (Var("S"), Var("D"))), Term("caido", (Var("D"),))),
            ),
            Clausula(
                Term("afectado", (Var("S"),)),
                (Term("depende", (Var("S"), Var("M"))), Term("afectado", (Var("M"),))),
            ),
        ]
        soluciones = list(resolver_sld(base, (Term("afectado", (Var("Quien"),)),)))
        afectados = {
            aplicar_sustitucion(Var("Quien"), s).functor  # type: ignore[union-attr]
            for s in soluciones
        }
        self.assertEqual(afectados, {"api", "checkout"})

    def test_red_bayesiana_y_explaining_away(self):
        red = RedBayesiana(
            [
                NodoBayes("FallaDisco", (), {(): 0.02}),
                NodoBayes("PicoRed", (), {(): 0.05}),
                NodoBayes(
                    "LatenciaAlta",
                    ("FallaDisco", "PicoRed"),
                    {
                        (True, True): 0.98,
                        (True, False): 0.85,
                        (False, True): 0.80,
                        (False, False): 0.01,
                    },
                ),
            ]
        )
        sin_pico = red.consultar("FallaDisco", {"LatenciaAlta": True})[True]
        con_pico = red.consultar("FallaDisco", {"LatenciaAlta": True, "PicoRed": True})[True]
        self.assertGreater(sin_pico, 0.20)
        # Explaining away: al confirmar PicoRed=True, baja la probabilidad posterior de FallaDisco
        self.assertLess(con_pico, sin_pico)

    def test_vv_detecta_conflicto_subsunion_ciclo_e_inalcanzable(self):
        reglas = [
            ReglaLogica("R1", frozenset({"cpu_alta", "sin_swap"}), ("estado", "critico")),
            ReglaLogica("R2", frozenset({"cpu_alta", "sin_swap"}), ("estado", "normal")),
            ReglaLogica("R3", frozenset({"cpu_alta"}), ("alerta", "si")),
            ReglaLogica("R4", frozenset({"cpu_alta", "disco_lleno"}), ("alerta", "si")),
            ReglaLogica("R5", frozenset({"sensor_fantasma=1"}), ("alerta", "manual")),
            ReglaLogica("R6", frozenset({"a=1"}), ("b", "1")),
            ReglaLogica("R7", frozenset({"b=1"}), ("a", "1")),
        ]
        reporte = verificar_base_reglas(reglas, {"cpu_alta", "sin_swap", "disco_lleno"})
        self.assertTrue(reporte["conflictos"])
        self.assertTrue(reporte["redundancias"])
        self.assertTrue(reporte["inalcanzables"])
        self.assertTrue(reporte["ciclos"])
