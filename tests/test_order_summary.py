import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from order_summary import summarize_orders, format_summary


class OrderSummaryTests(unittest.TestCase):
    def write_csv(self, rows):
        handle = tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8", delete=False)
        path = Path(handle.name)
        with handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["order_id", "customer", "fabric", "color", "yards", "unit_price"],
            )
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: path.exists() and path.unlink())
        return path

    def test_summarizes_valid_orders_by_customer(self):
        path = self.write_csv([
            {"order_id": "A001", "customer": "Sunrise Apparel", "fabric": "Cotton", "color": "Navy", "yards": "120", "unit_price": "85"},
            {"order_id": "A002", "customer": "Blue Ocean Uniforms", "fabric": "Polyester", "color": "Black", "yards": "80", "unit_price": "60"},
            {"order_id": "A003", "customer": "Sunrise Apparel", "fabric": "Linen", "color": "White", "yards": "50", "unit_price": "120"},
        ])

        summary = summarize_orders(path)

        self.assertEqual(summary["total_orders"], 3)
        self.assertEqual(summary["valid_orders"], 3)
        self.assertEqual(summary["total_yards"], 250)
        self.assertEqual(summary["total_amount"], 21000)
        self.assertEqual(summary["yards_by_customer"], {
            "Sunrise Apparel": 170,
            "Blue Ocean Uniforms": 80,
        })
        self.assertEqual(summary["warnings"], [])

    def test_skips_blank_yards_and_reports_warning(self):
        path = self.write_csv([
            {"order_id": "A001", "customer": "Sunrise Apparel", "fabric": "Cotton", "color": "Navy", "yards": "120", "unit_price": "85"},
            {"order_id": "A004", "customer": "Metro Studio", "fabric": "Cotton Twill", "color": "Gray", "yards": "", "unit_price": "85"},
        ])

        summary = summarize_orders(path)

        self.assertEqual(summary["total_orders"], 2)
        self.assertEqual(summary["valid_orders"], 1)
        self.assertEqual(summary["total_yards"], 120)
        self.assertEqual(summary["total_amount"], 10200)
        self.assertEqual(summary["yards_by_customer"], {"Sunrise Apparel": 120})
        self.assertEqual(summary["warnings"], ["Skipped order A004: yards is blank"])

    def test_format_summary_is_human_readable(self):
        text = format_summary({
            "total_orders": 2,
            "valid_orders": 1,
            "total_yards": 120,
            "total_amount": 10200,
            "yards_by_customer": {"Sunrise Apparel": 120},
            "warnings": ["Skipped order A004: yards is blank"],
        })

        self.assertIn("Total orders: 2", text)
        self.assertIn("Valid orders: 1", text)
        self.assertIn("Total yards: 120", text)
        self.assertIn("Total amount: 10200", text)
        self.assertIn("- Sunrise Apparel: 120 yards", text)
        self.assertIn("Warnings:", text)
        self.assertIn("- Skipped order A004: yards is blank", text)


if __name__ == "__main__":
    unittest.main()
