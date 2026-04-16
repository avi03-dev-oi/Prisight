#app/models/Market_model.py
from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)
    category = Column(String, nullable=True)
    source = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    date_collected = Column(Date, nullable=False)
