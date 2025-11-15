"""Test CSV loading and parsing into SalesRecord objects."""

import tempfile
import textwrap

from src.load_csv import load_sales_csv


def test_load_csv():
    """Verify CSV is parsed correctly with proper type conversions and field mapping."""
    csv_content = textwrap.dedent("""\
    order_id,date,customer_id,product_id,product_name,category,quantity,unit_price,discount,region,salesperson
    1,2024-01-01,C1,P1,Laptop,Electronics,1,1000,0.0,US,S1
    2,2024-01-02,C2,P2,Mouse,Electronics,2,25,0.0,US,S2
    """)

    # Create temporary CSV file for testing
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=True) as tmp:
        tmp.write(csv_content)
        tmp.flush()

        records = load_sales_csv(tmp.name)

    # Validate record count and field values
    assert len(records) == 2
    assert records[0].product_name == "Laptop"
    assert records[0].amount == 1000.0
    assert records[1].quantity == 2
    assert records[1].salesperson == "S2"
