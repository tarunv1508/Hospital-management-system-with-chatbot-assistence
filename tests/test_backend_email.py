import importlib
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


class BackendEmailConfigTests(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.original_cwd = os.getcwd()
        self.original_sys_path = list(sys.path)
        sys.path.insert(0, str(self.project_root))

    def tearDown(self):
        os.chdir(self.original_cwd)
        sys.path[:] = self.original_sys_path
        sys.modules.pop("backend", None)

    def test_env_file_is_loaded_relative_to_project_root(self):
        temp_dir = tempfile.mkdtemp(dir=self.project_root)
        try:
            os.chdir(temp_dir)
            backend = importlib.import_module("backend")
            self.assertTrue(backend.SMTP_CONFIG["user"])
            self.assertTrue(backend.SMTP_CONFIG["password"])
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
