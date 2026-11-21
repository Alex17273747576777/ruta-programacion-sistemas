import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline_async import CacheTTL, PipelineOutbox, calcular_percentiles  # noqa: E402


class RelojMonotonicoFijo:
    def __init__(self, t: float = 0.0) -> None:
        self.t = t

    def __call__(self) -> float:
        return self.t


class Etapa06SistemasTest(unittest.TestCase):
    def test_outbox_con_redelivery_y_caida_inyectada(self):
        with tempfile.TemporaryDirectory() as tmp:
            pipe = PipelineOutbox(Path(tmp) / "sistemas.db")
            pipe.registrar_orden_con_outbox("ORD-1", 250, "evt-1")

            with self.assertRaises(RuntimeError):
                pipe.procesar_pendientes(simular_caida_antes_de_ack=True)

            # Reintento tras caída: el efecto no se duplica y la cola se vacía limpiamente.
            procesados = pipe.procesar_pendientes(simular_caida_antes_de_ack=False)
            self.assertEqual(procesados, 1)
            self.assertEqual(pipe.total_consumido(), 250)
            self.assertEqual(pipe.procesar_pendientes(), 0)

    def test_cache_ttl_invalidacion_y_percentiles(self):
        reloj = RelojMonotonicoFijo(10.0)
        cache = CacheTTL(ttl_segundos=5.0, reloj=reloj)
        cache.guardar("k", "v1")
        self.assertEqual(cache.obtener("k"), "v1")
        reloj.t = 15.0
        self.assertIsNone(cache.obtener("k"))

        cache.guardar("k2", "v2")
        cache.invalidar("k2")
        self.assertIsNone(cache.obtener("k2"))

        p50, p95 = calcular_percentiles([10.0, 20.0, 30.0, 40.0, 100.0])
        self.assertEqual(p50, 30.0)
        self.assertGreaterEqual(p95, 40.0)
