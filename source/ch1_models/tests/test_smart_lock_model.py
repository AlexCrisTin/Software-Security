import unittest

from source.buggy.build_lock_kripke import build_lock_model


class SmartLockKripkeTests(unittest.TestCase):
    def test_safe_labels_match_report_properties(self):
        model = build_lock_model(insecure=False)
        self.assertIn("authenticated", model.labels["UNLOCKED"])
        self.assertIn("locked", model.labels["ALARM"])
        self.assertNotIn("unlocked", model.labels["ALARM"])
        self.assertIn("ALARM", model.transitions["ALARM"])

    def test_buggy_model_marks_unauthenticated_unlock(self):
        model = build_lock_model(insecure=True)
        self.assertIn("unauthenticated", model.labels["UNLOCKED"])
        self.assertEqual(model.find_path("UNLOCKED"), ["LOCKED", "UNLOCKING", "UNLOCKED"])


if __name__ == "__main__":
    unittest.main()
