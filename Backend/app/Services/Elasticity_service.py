from sqlalchemy import select
from fastapi import HTTPException
from app.models.Sales_history_model import SalesHistory
from app.models.Elasticity_model import Elasticity
import numpy as np

class ElasticityService:

    @staticmethod
    async def calculate_elasticity(db, product_id: int):
        result = await db.execute(
            select(SalesHistory)
            .where(SalesHistory.product_id == product_id)
            .order_by(SalesHistory.date)
        )

        sales = result.scalars().all()

        if len(sales) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least two sales records required"
            )

        prices = np.array([s.selling_price for s in sales])
        quantities = np.array([s.units_sold for s in sales])

        pct_price_change = np.diff(prices) / prices[:-1]
        pct_qty_change = np.diff(quantities) / quantities[:-1]

        # Remove zero or invalid values
        valid = (pct_price_change != 0)
        pct_price_change = pct_price_change[valid]
        pct_qty_change = pct_qty_change[valid]

        if len(pct_price_change) == 0:
            raise HTTPException(status_code=400, detail="Invalid price changes")

        elasticity_value = float(np.mean(pct_qty_change / pct_price_change))

        elasticity = Elasticity(
            product_id=product_id,
            elasticity_value=round(elasticity_value, 3),
            avg_price=float(prices.mean()),
            avg_units_sold=float(quantities.mean())
        )

        db.add(elasticity)
        await db.commit()
        await db.refresh(elasticity)

        return {
            "product_id": product_id,
            "elasticity": elasticity.elasticity_value,
            "interpretation": ElasticityService.interpret(elasticity.elasticity_value)
        }

    @staticmethod
    def interpret(value: float):
        if value < -1:
            return "Highly Elastic (price-sensitive)"
        elif -1 <= value < 0:
            return "Inelastic (price-insensitive)"
        else:
            return "Abnormal / Giffen-like behavior"
    
    @staticmethod
    async def get_elasticity_value(db, product_id: int) -> float:
        """
        Returns numeric price elasticity of demand for a product
        """

        # 1️⃣ Fetch sales history
        result = await db.execute(
            select(
                SalesHistory.selling_price,
                SalesHistory.units_sold
            ).where(SalesHistory.product_id == product_id)
        )

        rows = result.all()

        if len(rows) < 2:
            # Not enough data to compute elasticity
            return 0.0

        prices = np.array([float(r[0]) for r in rows])
        quantities = np.array([float(r[1]) for r in rows])

        # 2️⃣ Remove invalid entries
        mask = (prices > 0) & (quantities > 0)
        prices = prices[mask]
        quantities = quantities[mask]

        if len(prices) < 2:
            return 0.0

        # 3️⃣ Log-log regression
        log_prices = np.log(prices)
        log_quantities = np.log(quantities)

        # slope = elasticity
        elasticity, _ = np.polyfit(log_prices, log_quantities, 1)

        return round(float(elasticity), 3)

    @staticmethod
    def interpret_elasticity(elasticity: float) -> str:
        if elasticity <= -1:
            return "Highly Elastic (price-sensitive)"
        elif -1 < elasticity < 0:
            return "Moderately Elastic"
        elif elasticity == 0:
            return "Perfectly Inelastic"
        else:
            return "Inelastic (price-insensitive)"
