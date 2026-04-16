import pandas as pd
from sqlalchemy import select
from app.models.Sales_history_model import SalesHistory
from app.models.Market_model import MarketPrice
from app.models.engineered_feature import EngineeredFeature
from fastapi import HTTPException
from datetime import datetime

class FeatureEngineeringService:

    @staticmethod
    async def build_features(db, product_id: int):

        sales = (
            await db.execute(
                select(SalesHistory)
                .where(SalesHistory.product_id == product_id)
                .order_by(SalesHistory.date)
            )
        ).scalars().all()

        if len(sales) < 3:
            raise HTTPException(
                status_code=400,
                detail="At least 3 sales records required for feature engineering"
            )

        market = (
            await db.execute(
                select(MarketPrice)
                .where(MarketPrice.product_name.ilike(f"%"))
            )
        ).scalars().all()

        market_df = pd.DataFrame(
            [{"price": m.price, "date": m.date_collected} for m in market]
        )

        market_avg_price = market_df["price"].mean()

        df = pd.DataFrame([{
            "date": s.date,
            "units_sold": s.units_sold,
            "selling_price": s.selling_price
        } for s in sales])

        df["market_avg_price"] = market_avg_price
        df["discount_percent"] = (
            (df["market_avg_price"] - df["selling_price"])
            / df["market_avg_price"]
        ) * 100

        df["rolling_avg_7"] = df["units_sold"].rolling(window=7, min_periods=1).mean()
        df["rolling_avg_14"] = df["units_sold"].rolling(window=14, min_periods=1).mean()
        df["rolling_avg_30"] = df["units_sold"].rolling(window=30, min_periods=1).mean()

        df["weekday"] = pd.to_datetime(df["date"]).dt.weekday
        df["month"] = pd.to_datetime(df["date"]).dt.month

        df = df.dropna()

        for _, row in df.iterrows():
            feature = EngineeredFeature(
                product_id=product_id,
                date=row["date"],
                units_sold=int(row["units_sold"]),
                selling_price=float(row["selling_price"]),
                market_avg_price=float(row["market_avg_price"]),
                discount_percent=float(row["discount_percent"]),
                rolling_avg_7=float(row["rolling_avg_7"]),
                rolling_avg_14=float(row["rolling_avg_14"]),
                rolling_avg_30=float(row["rolling_avg_30"]),
                weekday=int(row["weekday"]),
                month=int(row["month"])
            )
            db.add(feature)

        await db.commit()

        return {
            "product_id": product_id,
            "rows": len(df),
            "features": list(df.columns)
        }
