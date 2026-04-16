import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.Market_model import MarketPrice

class MarketService:

    @staticmethod
    async def upload_market_csv(db, file):
        try:
            df = pd.read_csv(file.file)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV file.")

        df.columns = df.columns.str.strip()

        required_cols = {"product_name", "price", "date_collected"}
        if not required_cols.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV file must contain: {', '.join(required_cols)}"
            )
        for _, row in df.iterrows():
            # 🔥 CRITICAL FIX — convert string → datetime.date
            collected_date = pd.to_datetime(row["date_collected"]).date()

            record = MarketPrice(
                product_name=str(row["product_name"]).strip(),
                brand=row.get("brand"),
                category=row.get("category"),
                source=row.get("source"),
                price=float(row["price"]),
                date_collected=collected_date   # ✅ correct type
            )

            db.add(record)

            await db.commit()
        return {"message": "Market price data uploaded successfully."}
    
    @staticmethod
    async def get_market_stats(db, product_name: str):
        result= await db.execute(
            select(MarketPrice).where(MarketPrice.product_name==product_name)
        )
        records=result.scalars().all()
        if not records:
            raise HTTPException(status_code=404, detail="No market data found for the specified product.")
        prices=[r.price for r in records]
        
        return{
            "product_name": product_name,
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "data_points": len(prices)
        }
    