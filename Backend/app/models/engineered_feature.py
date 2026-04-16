from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from app.database import Base

class EngineeredFeature(Base):
    __tablename__ = "engineered_features"

    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    date = Column(Date, nullable=False)

    units_sold = Column(Integer, nullable=False)
    selling_price = Column(Float, nullable=False)
    market_avg_price = Column(Float, nullable=False)
    discount_percent = Column(Float, nullable=False)

    rolling_avg_7 = Column(Float)
    rolling_avg_14 = Column(Float)
    rolling_avg_30 = Column(Float)

    weekday = Column(Integer)  # 0=Monday
    month = Column(Integer)    # 1–12
