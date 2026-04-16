from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False)
    units_sold = Column(Integer, nullable=False)
    selling_price = Column(Float, nullable=False)

    product = relationship("Product")
