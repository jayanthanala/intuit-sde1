"""
Data model for sales records.
Defines the SalesRecord structure with type validation.
"""
from dataclasses import dataclass


@dataclass
class SalesRecord:
    order_id: str
    date: str
    customer_id: str
    product_id: str
    product_name: str
    category: str
    quantity: int
    unit_price: float
    discount: float
    region: str
    salesperson: str
    raw: dict # just in case

    @property
    def amount(self) -> float:
        """Revenue after discount."""
        return self.quantity * self.unit_price * (1 - self.discount)

    @property
    def full_price_revenue(self) -> float:
        """Revenue without discount."""
        return self.quantity * self.unit_price

    @property
    def discount_amount(self) -> float:
        """Total discount applied."""
        return self.quantity * self.unit_price * self.discount
