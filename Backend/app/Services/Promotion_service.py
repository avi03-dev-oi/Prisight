from sqlalchemy import select
from fastapi import HTTPException
from app.models.Product_model import Product
from app.models.Sales_history_model import SalesHistory
from app.models.PromotionRecommendation_model import PromotionRecommendation
import math

class PromotionService:

    @staticmethod
    async def recommend_promotion(db, product_id: int):

        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # ---- Average daily demand ----
        result = await db.execute(
            select(SalesHistory.units_sold)
            .where(SalesHistory.product_id == product_id)
        )
        sales = result.scalars().all()

        avg_demand = max(1, math.ceil(sum(sales) / len(sales))) if sales else 5

        base_price = product.current_price
        scenarios = []

        # ---- Promotion scenarios ----
        promotion_cases = [
            ("No Promotion", 0, 1.0),
            ("5% Discount", 5, 1.1),
            ("10% Discount", 10, 1.25),
            ("15% Discount", 15, 1.4),
            ("20% Discount", 20, 1.6),
            ("BOGO", 50, 2.0),
            ("Flash Sale", 25, 1.8)
        ]

        for name, discount, demand_multiplier in promotion_cases:
            discounted_price = base_price * (1 - discount / 100)
            expected_units = math.ceil(avg_demand * demand_multiplier)
            revenue = discounted_price * expected_units

            scenarios.append({
                "promotion": name,
                "discount": discount,
                "expected_units": expected_units,
                "revenue": revenue
            })

        # ---- Pick best promotion ----
        best = max(scenarios, key=lambda x: x["revenue"])

        record = PromotionRecommendation(
            product_id=product_id,
            promotion_type=best["promotion"],
            discount_percent=best["discount"],
            expected_demand=best["expected_units"],
            expected_revenue=best["revenue"]
        )

        db.add(record)
        await db.commit()

        return {
            "product_id": product_id,
            "best_promotion": best["promotion"],
            "discount_percent": best["discount"],
            "expected_units_sold": best["expected_units"],
            "expected_revenue": round(best["revenue"], 2),
            "all_simulations": scenarios
        }
