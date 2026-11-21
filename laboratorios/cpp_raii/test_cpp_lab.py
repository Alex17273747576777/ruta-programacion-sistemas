import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SRC_CPP = Path(__file__).resolve().parent / "raii_pool.cpp"


class LaboratorioCppRAIITest(unittest.TestCase):
    def test_raii_libera_recurso_incluso_con_excepcion(self):
        gpp = shutil.which("g++")
        self.assertIsNotNone(gpp, "Se requiere g++ para el laboratorio C++20")
        with tempfile.TemporaryDirectory() as tmp:
            bin_path = Path(tmp) / "raii_pool"
            comp = subprocess.run(
                [gpp, "-std=c++20", "-Wall", "-Wextra", "-Werror", str(SRC_CPP), "-o", str(bin_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(comp.returncode, 0, comp.stderr)
            run = subprocess.run([str(bin_path)], capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("CPP_RAII_OK vivos=0", run.stdout)
