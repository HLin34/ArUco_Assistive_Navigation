"""Run with: python -m unittest discover -s tests -v"""
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / "DISTANCE-ESTIMATION-master" / "navigation_logic.py"
spec = importlib.util.spec_from_file_location("navigation_logic", MODULE)
logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic)


class NavigationLogicTests(unittest.TestCase):
    def test_direction_thresholds(self):
        self.assertEqual(logic.direction_for_offset(11), "left")
        self.assertEqual(logic.direction_for_offset(-11), "right")
        self.assertIsNone(logic.direction_for_offset(10))
        self.assertIsNone(logic.direction_for_offset(-10))

    def test_cooldown(self):
        self.assertFalse(logic.should_announce("left", "left", 10, 12))
        self.assertTrue(logic.should_announce("left", "left", 10, 15))
        self.assertTrue(logic.should_announce("right", "left", 10, 11))

    def test_id_based_lookup(self):
        records = [
            {"id": 42, "output": "traffic"},
            {"id": 3, "name": "Stadium", "output": "stadium"},
            {"id": 1, "name": "Library", "output": "library"},
        ]
        self.assertEqual(logic.marker_message(1, records), ("library", "zh-TW"))
        self.assertEqual(logic.marker_message(42, records), ("traffic", "zh-TW"))
        self.assertEqual(logic.marker_message(0, records), ("Stadium, Library", "en"))
        self.assertEqual(logic.marker_message(99, records), ("", "zh-TW"))


if __name__ == "__main__":
    unittest.main()
