"""
CLI runner for assignment-2.
"""

from src.load_csv import load_sales_csv
import src.analyzer as analyzer
import src.reporting as reporting
from pathlib import Path

DATA_PATH = str(Path(__file__).resolve().parent.parent / "data" / "sales_data.csv")


def run():
    records = load_sales_csv(DATA_PATH)

    # 1. Total revenue
    print(f"Total Revenue: {analyzer.total_revenue(records):.2f}")

    # 2. Revenue by region
    reporting.print_kv_dict("Revenue by Region", analyzer.revenue_by_region(records))

    # 3. Revenue by category
    reporting.print_kv_dict("Revenue by Category", analyzer.revenue_by_category(records))

    # 4. Top 5 products
    reporting.print_top_products("Top 5 Products", analyzer.top_n_products(records, 5))

    # 5. Revenue by month
    reporting.print_kv_dict("Revenue by Month", analyzer.revenue_by_month(records))

    # 6. Salesperson performance
    perf = analyzer.salesperson_performance(records)
    reporting.print_salesperson_summary(perf, top=5)


if __name__ == "__main__":
    run()
