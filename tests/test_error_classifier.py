import unittest
from ghost.error_classifier import classify_error
from ghost.rule_explanations import get_rule_explanation

class TestClassifier(unittest.TestCase):
    def test_cmd_not_found(self):
        c, _ = classify_error(127, "pythno: command not found", "pythno")
        self.assertEqual(c, "command_not_found")
        s, f = get_rule_explanation(c, "not found", "pythno")
        self.assertTrue(f.startswith("Fix:"))
if __name__ == "__main__": unittest.main()
