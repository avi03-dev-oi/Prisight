from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.PriceRecommendation_model import PriceRecommendation
from app.models.Elasticity_model import Elasticity
from app.models.PromotionRecommendation_model import PromotionRecommendation
from app.models.DemandForecast_model import DemandForecast
from app.models.nlp_insight_model import NLPInsight
from app.Services.Inventory_service import InventoryService


class NLPExplanationService:

    # ---------------- PRICING EXPLANATION ----------------
    @staticmethod
    async def pricing_explanation(db: AsyncSession, product_id: int):
        result = await db.execute(
            select(PriceRecommendation)
            .where(PriceRecommendation.product_id == product_id)
            .order_by(PriceRecommendation.created_at.desc())
        )
        pricing = result.scalars().first()

        if not pricing:
            return {"detail": "No pricing data available"}

        elasticity = pricing.elasticity
        price_gap = pricing.market_avg_price - pricing.recommended_price

        if elasticity < -1 and price_gap > 0:
            explanation = (
                "The product shows high price sensitivity and is priced above "
                "the market average. Reducing the price is expected to improve demand."
            )
        elif elasticity < -1:
            explanation = (
                "Demand is highly price sensitive. Small pricing changes can "
                "cause large fluctuations in sales volume."
            )
        else:
            explanation = (
                "Demand appears stable with respect to price. Current pricing "
                "is unlikely to significantly affect demand."
            )

        insight = NLPInsight(
            product_id=product_id,
            insight_type="pricing",
            content=explanation,
            created_at=datetime.utcnow()
        )
        db.add(insight)
        await db.commit()

        return {"product_id": product_id, "explanation": explanation}


    # ---------------- FORECAST EXPLANATION ----------------
    @staticmethod
    async def forecast_explanation(db: AsyncSession, product_id: int):
        """
        Explain forecast & inventory outlook using Inventory Engine output
        """

        # 1️⃣ Get inventory + demand intelligence
        inventory_data = await InventoryService.recommend_reorder(
            db, product_id
        )

        avg_daily_demand = inventory_data["avg_daily_demand"]
        reorder_now = inventory_data["reorder_now"]

        # 2️⃣ NLP logic
        if avg_daily_demand > 10:
            explanation = (
                "Strong demand is forecasted in the coming period. "
                "Sales velocity is high and inventory levels should be reviewed frequently."
            )
        elif avg_daily_demand < 5:
            explanation = (
                "Demand is expected to remain low. "
                "Excess inventory risk exists, and promotions may help stimulate sales."
            )
        else:
            explanation = (
                "Demand is projected to remain stable. "
                "Current inventory and pricing strategies appear sufficient."
            )

        if reorder_now:
            explanation += " Immediate replenishment is recommended to prevent stockouts."

        # 3️⃣ Store NLP insight
        insight = NLPInsight(
            product_id=product_id,
            insight_type="forecast",
            content=explanation,
            created_at=datetime.utcnow()
        )
        db.add(insight)
        await db.commit()

        return {
            "product_id": product_id,
            "avg_daily_demand": avg_daily_demand,
            "reorder_now": reorder_now,
            "explanation": explanation
        }


    # ---------------- PROMOTION EXPLANATION ----------------
    @staticmethod
    async def promotion_explanation(db: AsyncSession, product_id: int):
        result = await db.execute(
            select(PromotionRecommendation)
            .where(PromotionRecommendation.product_id == product_id)
            .order_by(PromotionRecommendation.created_at.desc())
        )
        promo = result.scalars().first()

        if not promo:
            return {"detail": "No promotion recommendation available"}

        if promo.discount_percent >= 25:
            explanation = (
                "A high-discount promotion is recommended due to weak baseline demand. "
                "This strategy aims to maximize volume despite reduced margins."
            )
        elif promo.discount_percent >= 10:
            explanation = (
                "A moderate discount balances revenue and demand growth, "
                "making it suitable for stable market conditions."
            )
        else:
            explanation = (
                "No significant promotion is required. "
                "The product is performing well without heavy discounts."
            )

        insight = NLPInsight(
            product_id=product_id,
            insight_type="promotion",
            content=explanation,
            created_at=datetime.utcnow()
        )
        db.add(insight)
        await db.commit()

        return {
            "product_id": product_id,
            "promotion_type": promo.promotion_type,
            "discount_percent": promo.discount_percent,
            "explanation": explanation
        }
