import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "03_datos"))

from api_inventario import InventarioHTTPServer  # noqa: E402
from inventario import InventarioDB  # noqa: E402


def _req(url: str, method: str = "GET", token: str | None = None, body: dict | None = None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read().decode("utf-8"))


class Etapa04RedesAPITest(unittest.TestCase):
    def test_contrato_http_autorizacion_e_idempotencia(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = InventarioDB(Path(tmp) / "api.db")
            srv = InventarioHTTPServer(
                ("127.0.0.1", 0),
                db=db,
                tokens={"tok-alice": "alice", "tok-bob": "bob"},
            )
            th = threading.Thread(target=srv.serve_forever, daemon=True)
            th.start()
            base = f"http://127.0.0.1:{srv.server_port}"
            try:
                st, _ = _req(f"{base}/products/1", "GET")
                self.assertEqual(st, 401)

                st, prod = _req(
                    f"{base}/products",
                    "POST",
                    token="tok-alice",
                    body={"sku": "S-1", "nombre": "Sensor", "cantidad": 4},
                )
                self.assertEqual(st, 201)
                pid = prod["id"]

                st_bob, _ = _req(f"{base}/products/{pid}", "GET", token="tok-bob")
                self.assertEqual(st_bob, 403)

                st_m1, m1 = _req(
                    f"{base}/products/{pid}/movements",
                    "POST",
                    token="tok-alice",
                    body={"delta": -2, "clave_operacion": "k-1"},
                )
                st_m2, m2 = _req(
                    f"{base}/products/{pid}/movements",
                    "POST",
                    token="tok-alice",
                    body={"delta": -2, "clave_operacion": "k-1"},
                )
                self.assertEqual(st_m1, 200)
                self.assertEqual(st_m2, 200)
                self.assertEqual(m1["cantidad"], 2)
                self.assertTrue(m2["reutilizado"])

                st_404, _ = _req(f"{base}/products/999", "GET", token="tok-alice")
                self.assertEqual(st_404, 404)
            finally:
                srv.shutdown()
                srv.server_close()
