import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from biblioteca import ErrorDominio, Libro, RepositorioMemoria, ServicioBiblioteca  # noqa: E402


class RelojFijo:
    def __init__(self, actual: date) -> None:
        self.actual = actual

    def __call__(self) -> date:
        return self.actual


class Etapa02ModeladoTest(unittest.TestCase):
    def test_no_prestamo_doble_ni_devolucion_doble(self):
        reloj = RelojFijo(date(2026, 11, 1))
        svc = ServicioBiblioteca(RepositorioMemoria(), reloj=reloj)
        svc.registrar_libro("L1", "Sistemas")
        svc.registrar_usuario("U1", "Ana Pérez")
        svc.registrar_usuario("U2", "Ana Pérez")

        p = svc.prestar("L1", "U1", dias=7)
        with self.assertRaises(ErrorDominio):
            svc.prestar("L1", "U2", dias=7)

        reloj.actual = date(2026, 11, 9)
        cerrado, atraso = svc.devolver(p.id)
        self.assertEqual(atraso, 1)
        self.assertFalse(cerrado.activo)

        with self.assertRaises(ErrorDominio):
            svc.devolver(p.id)
        self.assertEqual(len(svc.repo.listar_prestamos()), 1)

    def test_rechaza_usuario_inexistente_e_identidad_por_id(self):
        svc = ServicioBiblioteca(RepositorioMemoria(), reloj=RelojFijo(date(2026, 11, 1)))
        l1 = svc.registrar_libro("L1", "Mismo Título")
        l2 = svc.registrar_libro("L2", "Mismo Título")
        self.assertNotEqual(l1, l2)
        self.assertEqual(l1, Libro("L1", "Mismo Título"))
        with self.assertRaises(ErrorDominio):
            svc.prestar("L1", "NO-EXISTE")
