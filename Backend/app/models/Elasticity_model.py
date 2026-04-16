from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Elasticity(Base):
    __tablename__ = "elasticities"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    elasticity_value = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    avg_units_sold = Column(Float, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", backref="elasticities")
