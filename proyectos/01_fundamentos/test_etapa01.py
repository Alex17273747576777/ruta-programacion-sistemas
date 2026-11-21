import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agenda import Agenda, ErrorAgenda  # noqa: E402
from calculadora import ErrorCalculadora, calcular, maximo_manual, sumar_manual  # noqa: E402


class Etapa01FundamentosTest(unittest.TestCase):
    def test_calculadora_decimal_exacto_y_errores(self):
        self.assertEqual(calcular("0.1", "+", "0.2"), Decimal("0.3"))
        self.assertEqual(calcular("2", "+", "3"), Decimal("5"))
        with self.assertRaises(ErrorCalculadora):
            calcular("1", "/", "0")
        with self.assertRaises(ErrorCalculadora):
            calcular("2", "**", "3")
        with self.assertRaises(ErrorCalculadora):
            calcular("__import__('os')", "+", "1")

    def test_maximo_y_suma_manual(self):
        self.assertEqual(sumar_manual([]), 0)
        self.assertEqual(sumar_manual([1, -2, 4]), 3)
        self.assertEqual(maximo_manual([-5, -2]), -2)
        with self.assertRaises(ErrorCalculadora):
            maximo_manual([])

    def test_agenda_conserva_ceros_y_protege_corrupcion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "agenda.json"
            ag = Agenda(ruta)
            c1 = ag.agregar("Ana", "00123")
            c2 = ag.agregar("Luis", "00456")
            self.assertEqual(c1.telefono, "00123")

            reabierta = Agenda(ruta)
            self.assertEqual(len(reabierta.listar()), 2)
            self.assertEqual(reabierta.buscar("00123")[0].id, c1.id)
            self.assertTrue(reabierta.eliminar(c2.id))
            self.assertEqual(len(Agenda(ruta).listar()), 1)

            with self.assertRaises(ErrorAgenda):
                ag.agregar("   ", "123")

            ruta.write_text("{json truncado", encoding="utf-8")
            with self.assertRaises(ErrorAgenda):
                Agenda(ruta)
            self.assertEqual(ruta.read_text(encoding="utf-8"), "{json truncado")
