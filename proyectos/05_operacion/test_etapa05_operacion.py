import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "03_datos"))

from inventario import InventarioDB  # noqa: E402
from operacion import (  # noqa: E402
    comprobar_liveness,
    comprobar_readiness,
    log_estructurado,
    respaldar_sqlite,
    restaurar_y_verificar,
)


class Etapa05OperacionTest(unittest.TestCase):
    def test_liveness_readiness_y_logs_sin_secretos(self):
        vivo, _ = comprobar_liveness()
        self.assertTrue(vivo)

        with tempfile.TemporaryDirectory() as tmp:
            inexistente = Path(tmp) / "no-existe.db"
            listo, motivo = comprobar_readiness(inexistente)
            self.assertFalse(listo)
            self.assertEqual(motivo, "db_missing")

            db_path = Path(tmp) / "prod.db"
            InventarioDB(db_path).crear_producto("S-OP", "Switch", 5)
            listo2, motivo2 = comprobar_readiness(db_path)
            self.assertTrue(listo2)
            self.assertEqual(motivo2, "ready")

        linea = json.loads(log_estructurado("peticion", usuario="ana", token="secreto-123"))
        self.assertEqual(linea["token"], "[REDACTADO]")
        self.assertEqual(linea["usuario"], "ana")

    def test_respaldo_y_restauracion_ensayada(self):
        with tempfile.TemporaryDirectory() as tmp:
            origen = Path(tmp) / "origen.db"
            bkp = Path(tmp) / "backup.db"
            restaurada = Path(tmp) / "restaurada.db"

            db = InventarioDB(origen)
            pid = db.crear_producto("SKU-BKP", "Router", 10)
            sha = respaldar_sqlite(origen, bkp)
            origen.unlink()

            ok = restaurar_y_verificar(bkp, sha, restaurada)
            self.assertTrue(ok)
            db_restaurada = InventarioDB(restaurada)
            self.assertEqual(db_restaurada.obtener_producto(pid)["cantidad"], 10)
