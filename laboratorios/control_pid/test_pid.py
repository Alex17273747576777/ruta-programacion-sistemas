import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from simulador_pid import simular_pid  # noqa: E402


class LaboratorioPIDTest(unittest.TestCase):
    def test_lazo_cerrado_converge_al_setpoint(self):
        traza = simular_pid(setpoint=50.0, kp=2.4, ki=1.2, kd=0.15, pasos=100, dt=0.1)
        self.assertEqual(len(traza), 100)
        self.assertLess(abs(traza[-1] - 50.0), 0.5)
        self.assertLess(max(traza), 65.0)
