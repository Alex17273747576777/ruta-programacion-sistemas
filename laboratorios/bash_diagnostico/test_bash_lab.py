import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "verificar_entorno.sh"


class LaboratorioBashTest(unittest.TestCase):
    def test_sintaxis_y_ejecucion_segura(self):
        chk = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(chk.returncode, 0, chk.stderr)
        run = subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("BASH_LAB_OK", run.stdout)
