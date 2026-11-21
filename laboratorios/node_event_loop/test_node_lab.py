import shutil
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "event_loop_orden.mjs"


class LaboratorioNodeEventLoopTest(unittest.TestCase):
    def test_orden_estricto_sync_microtarea_macrotarea(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Se requiere node para el laboratorio de Event Loop")
        run = subprocess.run([node, str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            "EVENT_LOOP=1:sync-inicio,2:sync-fin,3:microtarea-promise,4:macrotarea-timeout",
            run.stdout,
        )
