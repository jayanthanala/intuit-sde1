"""Test all sales analysis functions with sample data."""

from src.model import SalesRecord
from src import analyzer


def sample_records():
    """Create test dataset: 4 records across 2 regions, 2 categories, 2 months, 3 salespeople."""
    return [
        SalesRecord("1", "2024-01-01", "C1", "P1", "Laptop",
                    "Electronics", 1, 1000.0, 0.0, "US", "S1", {}),
        SalesRecord("2", "2024-01-05", "C1", "P2", "Mouse",
                    "Electronics", 2, 25.0, 0.0, "US", "S1", {}),
        SalesRecord("3", "2024-02-10", "C2", "P3", "Shirt",
                    "Clothing", 3, 20.0, 0.1, "EU", "S2", {}),
        SalesRecord("4", "2024-02-14", "C3", "P4", "Shoes",
                    "Clothing", 1, 80.0, 0.2, "EU", "S3", {}),
    ]


def test_total_revenue():
    """Verify sum of all revenue after discounts: 1000 + 50 + 54 + 64 = 1168."""
    records = sample_records()
    assert analyzer.total_revenue(records) == 1168.0


def test_revenue_by_region():
    """Verify revenue grouped by region: US vs EU breakdown."""
    records = sample_records()
    out = analyzer.revenue_by_region(records)
    assert out["US"] == 1050.0
    assert out["EU"] == 118.0


def test_revenue_by_category():
    """Verify revenue grouped by category: Electronics vs Clothing."""
    records = sample_records()
    out = analyzer.revenue_by_category(records)
    assert out["Electronics"] == 1050.0
    assert out["Clothing"] == 118.0


def test_top_n_products():
    """Verify top 2 products by revenue: Laptop (1000), Shoes (64)."""
    records = sample_records()
    top = analyzer.top_n_products(records, n=2)
    assert top[0][0] == "Laptop"
    assert top[1][0] == "Shoes"


def test_revenue_by_month():
    """Verify revenue grouped by month: January vs February."""
    records = sample_records()
    out = analyzer.revenue_by_month(records)
    assert out["2024-01"] == 1050.0
    assert out["2024-02"] == 118.0


def test_salesperson_performance():
    """Verify salesperson metrics: order count, unique customers, total revenue."""
    records = sample_records()
    perf = analyzer.salesperson_performance(records)

    # S1 sold Laptop + Mouse to same customer C1
    assert "S1" in perf
    assert perf["S1"]["orders"] == 2
    assert perf["S1"]["customers"] == 1
    assert perf["S1"]["total_revenue"] == 1050.0
