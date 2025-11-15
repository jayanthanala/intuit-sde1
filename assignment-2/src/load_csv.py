"""
Functional CSV reader → returns list[SalesRecord]
"""

import csv
from .model import SalesRecord


def _row_to_record():
    """
    Convert a CSV row → SalesRecord instance.

    Functional style: reader → map(row_to_record) → list.
    """
    return lambda r: SalesRecord(
        order_id=r["order_id"],
        date=r["date"],
        customer_id=r["customer_id"],
        product_id=r["product_id"],
        product_name=r["product_name"],
        category=r["category"],
        quantity=int(r["quantity"]),
        unit_price=float(r["unit_price"]),
        discount=float(r["discount"]),
        region=r["region"],
        salesperson=r["salesperson"],
        raw=r,
    )


def load_sales_csv(path: str):
    """
    Load CSV into list of SalesRecord objects using a pure FP pipeline.
    """
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        converter = _row_to_record()
        return list(map(converter, reader))
