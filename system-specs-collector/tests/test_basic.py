import unittest
from system_specs_collector.cli import get_cpu_info

class TestCPUInfo(unittest.TestCase):
    def test_cpu_cores(self):
        info = get_cpu_info()
        self.assertIn("Physical cores", info)
        self.assertIsInstance(info["Physical cores"], int)
        self.assertGreater(info["Physical cores"], 0)  # optional: sanity check

if __name__ == "__main__":
    unittest.main()
