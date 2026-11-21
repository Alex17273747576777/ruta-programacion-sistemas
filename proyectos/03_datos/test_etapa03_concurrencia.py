import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inventario import ConflictoIdempotencia, InventarioDB, StockInsuficiente  # noqa: E402


class Etapa03DatosConcurrenciaTest(unittest.TestCase):
    def test_salidas_concurrentes_con_barrera(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = InventarioDB(Path(tmp) / "inv.db")
            pid = db.crear_producto("SKU-1", "Teclado", cantidad_inicial=3)

            barrera = threading.Barrier(2)
            resultados: list[str] = []
            lock = threading.Lock()

            def worker(clave: str) -> None:
                barrera.wait()
                try:
                    db.aplicar_movimiento(pid, -2, clave)
                    estado = "ok"
                except StockInsuficiente:
                    estado = "sin_stock"
                with lock:
                    resultados.append(estado)

            t1 = threading.Thread(target=worker, args=("op-1",))
            t2 = threading.Thread(target=worker, args=("op-2",))
            t1.start()
            t2.start()
            t1.join()
            t2.join()

            self.assertEqual(sorted(resultados), ["ok", "sin_stock"])
            self.assertEqual(db.obtener_producto(pid)["cantidad"], 1)
            self.assertEqual(len(db.listar_movimientos(pid)), 1)

    def test_idempotencia_y_conflicto(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = InventarioDB(Path(tmp) / "inv.db")
            pid = db.crear_producto("SKU-2", "Mouse", cantidad_inicial=5)

            r1 = db.aplicar_movimiento(pid, -2, "req-100")
            r2 = db.aplicar_movimiento(pid, -2, "req-100")
            self.assertFalse(r1.reutilizado)
            self.assertTrue(r2.reutilizado)
            self.assertEqual(db.obtener_producto(pid)["cantidad"], 3)

            with self.assertRaises(ConflictoIdempotencia):
                db.aplicar_movimiento(pid, -1, "req-100")
