import unittest
import subprocess
import os
import sys

class TestScripts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure src is in PYTHONPATH before running tests."""
        src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
        sys.path.insert(0, src_path)  # Add src/ to Python path

    def test_script_runs(self):
        """Run the script and check for expected behavior."""
        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../src/annotator_module/annotator_workflow/incisionDataFolderCreation.py")
        )

        result = subprocess.run(
            ["python", script_path, "--batch", "4",
             "--output", "annotationDatas/annotationData4", "--project", "Endometriosis_WS2",
             "--annotator", "nicolas.bourdel"],
            capture_output=True, text=True, env=os.environ.copy()
        )
        self.assertEqual(result.returncode, 0)  # Expect success

if __name__ == "__main__":
    unittest.main()
