from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    current_stock = Column(Integer, nullable=False)
    daily_holding_cost = Column(Float, default=0.0)
    lead_time_days = Column(Integer, default=7)
