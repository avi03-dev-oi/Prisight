from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class PromotionRecommendation(Base):
    __tablename__ = "promotion_recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    promotion_type = Column(String, nullable=False)
    discount_percent = Column(Float, nullable=True)

    expected_demand = Column(Integer, nullable=False)
    expected_revenue = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
