from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    mae = Column(Float, nullable=False)
    rmse = Column(Float, nullable=False)
    mape = Column(Float, nullable=True)

    samples = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
