import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from quiz_cli import cargar_preguntas, evaluar_respuestas  # noqa: E402


class QuizBancoTest(unittest.TestCase):
    def test_banco_completo_y_validacion(self):
        preguntas = cargar_preguntas()
        self.assertGreaterEqual(len(preguntas), 12)
        for p in preguntas:
            self.assertEqual(len(p["opciones"]), 4)
            self.assertIn(p["correcta"], (0, 1, 2, 3))
            self.assertTrue(p["explicacion_feynman"].strip())

        todas_ok = [p["correcta"] for p in preguntas]
        aciertos, total, _ = evaluar_respuestas(preguntas, todas_ok)
        self.assertEqual(aciertos, total)
