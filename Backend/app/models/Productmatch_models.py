from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class ProductMatch(Base):
    __tablename__ = "product_matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    market_name = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    confirmed = Column(Integer, default=0)  # 0 = auto, 1 = user-confirmed
