"""
Functional CSV reader → returns list[SalesRecord]
"""

import csv
from .model import SalesRecord
from pathlib import Path


def _row_to_record():
    """
    Convert a CSV row → SalesRecord instance.

    Functional style: reader → map(row_to_record) → list.
    
    Returns:
        Lambda function that converts dict row to SalesRecord
        
    Raises:
        ValueError: If required fields are missing or invalid
        TypeError: If type conversion fails
    """
    def converter(r):
        try:
            # Validate required fields
            required_fields = [
                "order_id", "date", "customer_id", "product_id", "product_name",
                "category", "quantity", "unit_price", "discount", "region", "salesperson"
            ]
            missing = [f for f in required_fields if f not in r]
            if missing:
                raise ValueError(f"Missing required fields: {missing}")
            
            # Convert with type validation
            try:
                quantity = int(r["quantity"])
                unit_price = float(r["unit_price"])
                discount = float(r["discount"])
            except ValueError as e:
                raise ValueError(f"Type conversion error in row {r.get('order_id', 'unknown')}: {e}")
            
            # Validate ranges
            if quantity < 0:
                raise ValueError(f"Quantity cannot be negative: {quantity}")
            if unit_price < 0:
                raise ValueError(f"Unit price cannot be negative: {unit_price}")
            if not (0 <= discount <= 1):
                raise ValueError(f"Discount must be between 0 and 1: {discount}")
            
            return SalesRecord(
                order_id=r["order_id"],
                date=r["date"],
                customer_id=r["customer_id"],
                product_id=r["product_id"],
                product_name=r["product_name"],
                category=r["category"],
                quantity=quantity,
                unit_price=unit_price,
                discount=discount,
                region=r["region"],
                salesperson=r["salesperson"],
                raw=r,
            )
        except (ValueError, TypeError, KeyError) as e:
            raise ValueError(f"Error parsing CSV row {r.get('order_id', 'unknown')}: {e}")
    
    return converter


def load_sales_csv(path: str):
    """
    Load CSV into list of SalesRecord objects using a pure FP pipeline.
    
    Args:
        path: Path to CSV file
        
    Returns:
        List of SalesRecord objects
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        PermissionError: If file cannot be read
        ValueError: If CSV is malformed or contains invalid data
    """
    # Validate path
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    if not csv_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            # Validate CSV has headers
            if not reader.fieldnames:
                raise ValueError("CSV file has no headers")
            
            converter = _row_to_record()
            records = list(map(converter, reader))
            
            if not records:
                raise ValueError("CSV file contains no data rows")
            
            return records
            
    except PermissionError as e:
        raise PermissionError(f"Cannot read file {path}: {e}")
    except csv.Error as e:
        raise ValueError(f"CSV parsing error in {path}: {e}")
    except UnicodeDecodeError as e:
        raise ValueError(f"File encoding error in {path}: {e}")
    except Exception as e:
        raise ValueError(f"Error loading CSV from {path}: {e}")
