import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SRC_C = Path(__file__).resolve().parent / "buffer_seguro.c"


class LaboratorioCMemoriaTest(unittest.TestCase):
    def test_compila_sin_warnings_y_detecta_overflow_y_truncado(self):
        gcc = shutil.which("gcc")
        self.assertIsNotNone(gcc, "Se requiere gcc para compilar el laboratorio C")
        with tempfile.TemporaryDirectory() as tmp:
            bin_path = Path(tmp) / "buffer_seguro"
            comp = subprocess.run(
                [gcc, "-std=c99", "-Wall", "-Wextra", "-Werror", str(SRC_C), "-o", str(bin_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(comp.returncode, 0, comp.stderr)
            run = subprocess.run([str(bin_path)], capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("C_OK res=42 buf=ok-c", run.stdout)
