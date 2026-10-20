import unittest
import tempfile
import os
import sys
import subprocess
from decimal import Decimal

class TestCSVStats(unittest.TestCase):
    def run_tool(self, csv_content):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            f.flush()
            result = subprocess.run([
                sys.executable, 'csv_stats.py', f.name
            ], capture_output=True, text=True)
            os.unlink(f.name)
        return result

    def test_normal_case(self):
        csv_content = '''category,amount\n食品,100.00\n交通,100.25\n食品,50.00'''
        result = self.run_tool(csv_content)
        self.assertEqual(result.returncode, 0)
        expected = {
            'total_count': 3,
            'total_amount': '250.25',
            'category_stats': {
                '食品': {'count': 2, 'amount': '150.00'},
                '交通': {'count': 1, 'amount': '100.25'}
            }
        }
        self.assertEqual(eval(result.stdout.strip()), expected)

    def test_negative_amount(self):
        csv_content = '''category,amount\n食品,-50.00\n交通,100.25'''
        result = self.run_tool(csv_content)
        self.assertEqual(result.returncode, 0)
        expected = {
            'total_count': 2,
            'total_amount': '50.25',
            'category_stats': {
                '食品': {'count': 1, 'amount': '-50.00'},
                '交通': {'count': 1, 'amount': '100.25'}
            }
        }
        self.assertEqual(eval(result.stdout.strip()), expected)

    def test_only_header(self):
        csv_content = '''category,amount'''
        result = self.run_tool(csv_content)
        self.assertEqual(result.returncode, 0)
        expected = {
            'total_count': 0,
            'total_amount': '0.00',
            'category_stats': {}
        }
        self.assertEqual(eval(result.stdout.strip()), expected)

    def test_missing_field(self):
        csv_content = '''category\n食品'''
        result = self.run_tool(csv_content)
        self.assertEqual(result.returncode, 1)
        self.assertIn("錯誤：CSV 檔案缺少必要欄位。", result.stderr)

    def test_empty_category(self):
        csv_content = '''category,amount\n食品,100.00\n,50.00'''
        result = self.run_tool(csv_content)
        self.assertEqual(result.returncode, 0)
        expected = {
            'total_count': 2,
            'total_amount': '150.00',
            'category_stats': {
                '食品': {'count': 1, 'amount': '100.00'},
                'UNKNOWN': {'count': 1, 'amount': '50.00'}
            }
        }
        self.assertEqual(eval(result.stdout.strip()), expected)

    def test_invalid_amount(self):
        csv_content = '''category,amount\n食品,abc'''
        result = self.run_tool(csv_content)
        self.assertEqual(result.returncode, 1)
        self.assertIn("錯誤：金額格式無效。", result.stderr)

if __name__ == '__main__':
    unittest.main()
