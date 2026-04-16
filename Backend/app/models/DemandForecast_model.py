from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from datetime import date
from app.database import Base

class DemandForecast(Base):
    __tablename__ = "demand_forecasts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    forecast_date = Column(Date, nullable=False)
    predicted_units = Column(Float, nullable=False)
