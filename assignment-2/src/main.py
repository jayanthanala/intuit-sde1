"""
CLI runner for assignment-2.
"""

from src.load_csv import load_sales_csv
import src.analyzer as analyzer
import src.reporting as reporting
from pathlib import Path
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

DATA_PATH = str(Path(__file__).resolve().parent.parent / "data" / "sales_data.csv")


def run():
    """Run all sales analyses with error handling."""
    try:
        # Validate data file exists
        data_file = Path(DATA_PATH)
        if not data_file.exists():
            raise FileNotFoundError(f"Data file not found: {DATA_PATH}")
        if not data_file.is_file():
            raise ValueError(f"Path is not a file: {DATA_PATH}")
        
        logging.info(f"Loading data from: {DATA_PATH}")
        records = load_sales_csv(DATA_PATH)
        
        # Validate records loaded
        if not records:
            raise ValueError("No records loaded from CSV file")
        
        logging.info(f"Loaded {len(records)} records successfully")

        # 1. Total revenue
        try:
            total_rev = analyzer.total_revenue(records)
            print(f"Total Revenue: {total_rev:.2f}")
        except Exception as e:
            logging.error(f"Error calculating total revenue: {e}")
            raise

        # 2. Revenue by region
        try:
            reporting.print_kv_dict("Revenue by Region", analyzer.revenue_by_region(records))
        except Exception as e:
            logging.error(f"Error analyzing revenue by region: {e}")
            raise

        # 3. Revenue by category
        try:
            reporting.print_kv_dict("Revenue by Category", analyzer.revenue_by_category(records))
        except Exception as e:
            logging.error(f"Error analyzing revenue by category: {e}")
            raise

        # 4. Top 5 products
        try:
            reporting.print_top_products("Top 5 Products", analyzer.top_n_products(records, 5))
        except Exception as e:
            logging.error(f"Error analyzing top products: {e}")
            raise

        # 5. Revenue by month
        try:
            reporting.print_kv_dict("Revenue by Month", analyzer.revenue_by_month(records))
        except Exception as e:
            logging.error(f"Error analyzing revenue by month: {e}")
            raise

        # 6. Salesperson performance
        try:
            perf = analyzer.salesperson_performance(records)
            reporting.print_salesperson_summary(perf, top=5)
        except Exception as e:
            logging.error(f"Error analyzing salesperson performance: {e}")
            raise
            
        logging.info("All analyses completed successfully")
        
    except FileNotFoundError as e:
        logging.critical(f"File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logging.critical(f"Data validation error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run()
