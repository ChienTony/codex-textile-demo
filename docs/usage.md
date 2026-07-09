# Usage Guide

Run the summary script from the repo root:

```bash
python3 src/order_summary.py sample_data/orders.csv
```

Expected behavior:

- Count all rows in the CSV as orders.
- Skip rows with blank or invalid numeric fields when calculating totals.
- Print a warning for skipped rows.
- Show total valid yards, total amount, and yards grouped by customer.

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Teaching note: this repo is intentionally small. Do not turn it into a full order-management system during the course.
