"""
Unit tests for Persian NLP Command Parser and Normalizer.
"""

import unittest
from command.normalizer import normalize_text, convert_digits
from command.parser import CommandParser
from command.validator import CommandValidator

class TestCommandParser(unittest.TestCase):
    def setUp(self):
        self.parser = CommandParser()
        self.validator = CommandValidator()

    def test_digit_conversion(self):
        self.assertEqual(convert_digits("۱۲۳۴۵۶۷۸۹۰"), "1234567890")
        self.assertEqual(convert_digits("١٢٣٤٥٦٧٨٩٠"), "1234567890")

    def test_normalization(self):
        self.assertEqual(normalize_text("  سلام   دنیا  "), "سلام دنیا")
        self.assertEqual(normalize_text("تست\u200cمی‌کنیم"), "تست می کنیم")

    def test_single_command_run(self):
        result = self.parser.parse("۳۰ ثانیه بدو")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["type"], "run")
        self.assertEqual(result["actions"][0]["duration"], 30.0)

    def test_single_command_situp(self):
        result = self.parser.parse("۱۰ تا دراز و نشست بزن")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["type"], "sit_up")
        self.assertEqual(result["actions"][0]["repetitions"], 10)

    def test_compound_command(self):
        result = self.parser.parse("۳۰ ثانیه بدو، بعد ۱۰ تا درازونشست بزن، بعد بایست")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["actions"]), 3)
        self.assertEqual(result["actions"][0]["type"], "run")
        self.assertEqual(result["actions"][1]["type"], "sit_up")
        self.assertEqual(result["actions"][2]["type"], "stand")

    def test_control_command(self):
        result = self.parser.parse("تمام حرکات را متوقف کن")
        self.assertEqual(result["status"], "control")
        self.assertEqual(result["control_type"], "stop")

    def test_invalid_command(self):
        result = self.parser.parse("متن نامربوط و نامشخص")
        self.assertEqual(result["status"], "error")

if __name__ == "__main__":
    unittest.main()
