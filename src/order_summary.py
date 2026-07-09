import csv
import sys
from pathlib import Path


def summarize_orders(csv_path):
    summary = {
        "total_orders": 0,
        "valid_orders": 0,
        "total_yards": 0,
        "total_amount": 0,
        "yards_by_customer": {},
        "warnings": [],
    }

    with Path(csv_path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            summary["total_orders"] += 1
            order_id = row.get("order_id") or f"row {summary['total_orders']}"
            customer = row.get("customer", "Unknown")
            yards_text = (row.get("yards") or "").strip()
            unit_price_text = (row.get("unit_price") or "").strip()

            if not yards_text:
                summary["warnings"].append(f"Skipped order {order_id}: yards is blank")
                continue

            try:
                yards = int(yards_text)
                unit_price = int(unit_price_text)
            except ValueError:
                summary["warnings"].append(f"Skipped order {order_id}: numeric field is invalid")
                continue

            summary["valid_orders"] += 1
            summary["total_yards"] += yards
            summary["total_amount"] += yards * unit_price
            summary["yards_by_customer"][customer] = summary["yards_by_customer"].get(customer, 0) + yards

    return summary


def format_summary(summary):
    lines = [
        f"Total orders: {summary['total_orders']}",
        f"Valid orders: {summary['valid_orders']}",
        f"Total yards: {summary['total_yards']}",
        f"Total amount: {summary['total_amount']}",
        "",
        "By customer:",
    ]

    for customer, yards in summary["yards_by_customer"].items():
        lines.append(f"- {customer}: {yards} yards")

    if summary["warnings"]:
        lines.extend(["", "Warnings:"])
        lines.extend(f"- {warning}" for warning in summary["warnings"])

    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 src/order_summary.py sample_data/orders.csv")
        return 2

    print(format_summary(summarize_orders(argv[1])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
