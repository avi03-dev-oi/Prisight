from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class NLPInsight(Base):
    __tablename__ = "nlp_insights"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    insight_type = Column(String, nullable=False)  # pricing, forecast, promo, inventory
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
