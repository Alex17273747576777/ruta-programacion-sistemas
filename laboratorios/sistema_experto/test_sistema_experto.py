import unittest

from sistema_experto.motor_inferencia import (
    MotorExperto,
    Regla,
    combinar_cf_mycin,
    evaluar_difuso_riego,
)


class LaboratorioSistemaExpertoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reglas = [
            Regla("R1", ("latencia_alta", "perdida_paquetes"), "congestion_red", cf=0.80, prioridad=2),
            Regla("R2", ("cpu_100", "sin_swap"), "saturacion_nodo", cf=0.75, prioridad=1),
            Regla("R3", ("congestion_red",), "alerta_incidente_p1", cf=0.90),
            Regla("R4", ("saturacion_nodo",), "alerta_incidente_p1", cf=0.85),
            # Regla ciclica deliberada para probar refraccion / deteccion de ciclos
            Regla("R_CICLO_A", ("meta_ciclo_b",), "meta_ciclo_a", cf=0.90),
            Regla("R_CICLO_B", ("meta_ciclo_a",), "meta_ciclo_b", cf=0.90),
        ]
        self.motor = MotorExperto(self.reglas)

    def test_combinacion_mycin_converge_sin_exceder_uno(self) -> None:
        self.assertAlmostEqual(combinar_cf_mycin(0.6, 0.7), 0.88, places=4)
        self.assertAlmostEqual(combinar_cf_mycin(-0.5, -0.4), -0.7, places=4)
        self.assertLessEqual(combinar_cf_mycin(0.95, 0.95), 1.0)

    def test_forward_chaining_deriva_y_combina_multiples_ramas(self) -> None:
        hechos = {
            "latencia_alta": 0.9,
            "perdida_paquetes": 1.0,
            "cpu_100": 0.8,
            "sin_swap": 0.9,
        }
        res = self.motor.encadenamiento_adelante(hechos)
        self.assertIn("congestion_red", res.hechos)
        self.assertIn("saturacion_nodo", res.hechos)
        self.assertIn("alerta_incidente_p1", res.hechos)
        # Rama 1: 0.9*0.80*0.90 = 0.648 ; Rama 2: 0.8*0.75*0.85 = 0.51 ; MYCIN = 0.648 + 0.51*(1-0.648) = 0.82752
        self.assertAlmostEqual(res.hechos["alerta_incidente_p1"], 0.82752, places=4)
        self.assertGreaterEqual(len(res.traza), 4)

    def test_backward_chaining_explica_y_evita_ciclos(self) -> None:
        hechos = {"latencia_alta": 0.9, "perdida_paquetes": 1.0}
        ok, cf, explicacion = self.motor.encadenamiento_atras("alerta_incidente_p1", hechos)
        self.assertTrue(ok)
        self.assertAlmostEqual(cf, 0.648, places=4)
        self.assertTrue(any("Regla R3 demostro 'alerta_incidente_p1'" in linea for linea in explicacion))

        ok_ciclo, cf_ciclo, _ = self.motor.encadenamiento_atras("meta_ciclo_a", {})
        self.assertFalse(ok_ciclo)
        self.assertEqual(cf_ciclo, 0.0)

    def test_controlador_difuso_mamdani_diferencia_regimenes(self) -> None:
        apertura_seco_caluroso = evaluar_difuso_riego(humedad_pct=15.0, temp_c=38.0)
        apertura_humedo_frio = evaluar_difuso_riego(humedad_pct=85.0, temp_c=12.0)
        self.assertGreater(apertura_seco_caluroso, 70.0)
        self.assertLess(apertura_humedo_frio, 25.0)


if __name__ == "__main__":
    unittest.main()
