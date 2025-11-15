"""
Functional analysis utilities for SalesRecord data.
Uses: reduce, sorted, groupby, lambda transforms.
"""

from functools import reduce
from itertools import groupby
from datetime import datetime


# ---------------------------------------------------------
# Helper: Extract YYYY-MM from ISO date
# ---------------------------------------------------------
def extract_month(date_str: str) -> str:
    """Parse ISO date string and return YYYY-MM format for monthly grouping."""
    try:
        return datetime.fromisoformat(date_str).strftime("%Y-%m")
    except Exception:
        return "unknown"


# =========================================================
# 1. TOTAL REVENUE  (after discount)
# =========================================================
def total_revenue(records):
    """Sum all record amounts using reduce: accumulator + current record amount."""
    return reduce(lambda acc, r: acc + r.amount, records, 0.0)


# =========================================================
# 2. REVENUE BY REGION
# =========================================================
def revenue_by_region(records):
    """Group records by region, sum amounts per group """
    recs = sorted(records, key=lambda r: r.region)  # Sort by region (required for groupby)
    return {
        region: sum(r.amount for r in group)  # Sum amounts for each region group
        for region, group in groupby(recs, key=lambda r: r.region)
    }


# =========================================================
# 3. REVENUE BY CATEGORY
# =========================================================
def revenue_by_category(records):
    """Group records by category, sum amounts per group"""
    recs = sorted(records, key=lambda r: r.category)  # Sort by category (required for groupby)
    return {
        category: sum(r.amount for r in group)  # Sum amounts for each category group
        for category, group in groupby(recs, key=lambda r: r.category)
    }


# =========================================================
# 4. TOP-N PRODUCTS BY REVENUE
# =========================================================
def top_n_products(records, n=5):
    """Aggregate revenue per product using reduce, then sort descending and take top N."""
    # Use reduce to build dict: {product_name: total_revenue}
    totals = reduce(
        lambda acc, r: {**acc, r.product_name: acc.get(r.product_name, 0.0) + r.amount},  # Merge dicts, accumulate revenue
        records,
        {}  # Start with empty dict
    )
    # Sort by revenue (descending), slice top N
    return sorted(totals.items(), key=lambda x: x[1], reverse=True)[:n]


# =========================================================
# 5. REVENUE BY MONTH (YYYY-MM)
# =========================================================
def revenue_by_month(records):
    """Group records by month (YYYY-MM), sum amounts per group"""
    recs = sorted(records, key=lambda r: extract_month(r.date))  # Sort by extracted month (required for groupby)
    return {
        month: sum(r.amount for r in group)  # Sum amounts for each month group
        for month, group in groupby(recs, key=lambda r: extract_month(r.date))
    }


# =========================================================
# 6. SALESPERSON PERFORMANCE (ADVANCED)
# ---------------------------------------------------------
# For each salesperson:
#   - total_revenue
#   - orders (number of order lines)
#   - customers served
#   - regions covered
#   - effective_discount (total discount ÷ full_price_revenue)
# =========================================================
def salesperson_performance(records):
    """Calculate comprehensive performance metrics for each salesperson."""
    recs = sorted(records, key=lambda r: r.salesperson)  # Sort by salesperson (required for groupby)
    perf = {}

    for sp, group in groupby(recs, key=lambda r: r.salesperson):
        lst = list(group)  # Materialize group iterator for multiple passes

        # Aggregate metrics for this salesperson
        total_rev = sum(r.amount for r in lst)  # Total revenue after discount
        orders = len(lst)  # Number of orders
        customers = len(set(r.customer_id for r in lst))  # Unique customers
        regions = len(set(r.region for r in lst))  # Unique regions
        total_disc_amt = sum(r.discount_amount for r in lst)  # Total $ discounted
        total_full = sum(r.full_price_revenue for r in lst)  # Total $ before discount
        effective_discount = (total_disc_amt / total_full) if total_full else 0.0  # Average discount rate

        perf[sp] = {
            "total_revenue": total_rev,
            "orders": orders,
            "customers": customers,
            "regions": regions,
            "effective_discount": effective_discount,
        }

    return perf
