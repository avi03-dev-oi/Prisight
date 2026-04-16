from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class PriceRecommendation(Base):
    __tablename__ = "price_recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    recommended_price = Column(Float, nullable=False)
    market_avg_price = Column(Float, nullable=False)
    elasticity = Column(Float, nullable=False)
    reasoning = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
