from typing import Optional
from sqlmodel import Field, SQLModel
import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    cost: float  # Price from supplier
    quantity: int # Stock level
    description: Optional[str] = None

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    # total_amount is removed, will be calculated from SaleItems

class SaleItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_id: Optional[int] = Field(default=None, foreign_key="sale.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    quantity: int
    price_at_sale: float # The price of the product at the time of sale
    cost_at_sale: float # The cost of the product at the time of sale
