from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    cost_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)