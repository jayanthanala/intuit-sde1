"""Test functional programming operations (filter, map, sort) on sales records."""

from src.model import SalesRecord

#filter->map->sort
def test_pipeline():
    """Verify functional pipeline: filter by amount > 70, extract names, sort alphabetically."""
    records = [
        SalesRecord("1", "2024-01-01", "C1", "P1", "Laptop",
                    "Electronics", 1, 1000.0, 0.0, "US", "S1", {}),
        SalesRecord("2", "2024-01-02", "C2", "P2", "Mouse",
                    "Electronics", 2, 25.0, 0.0, "US", "S1", {}),
        SalesRecord("3", "2024-01-03", "C3", "P3", "Keyboard",
                    "Electronics", 1, 80.0, 0.0, "EU", "S2", {}),
    ]

    # Filter records > $70, map to product names, sort alphabetically
    names = sorted(
        map(
            lambda r: r.product_name,
            filter(lambda r: r.amount > 70.0, records),
        )
    )

    # Should include Keyboard ($80) and Laptop ($1000), excluding Mouse ($50)
    assert names == ["Keyboard", "Laptop"]
