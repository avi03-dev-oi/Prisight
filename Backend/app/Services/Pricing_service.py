from itertools import product
from sqlalchemy import select, func
from fastapi import HTTPException
from datetime import datetime

from app.models.Product_model import Product
from app.models.Productmatch_models import ProductMatch
from app.models.Market_model import MarketPrice
from app.models.PriceRecommendation_model import PriceRecommendation
from app.Services.Elasticity_service import ElasticityService

class PricingService:

    @staticmethod
    async def recommend_price(db, product_id: int):

        # 1️⃣ Fetch product
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        current_price = float(product.current_price)

        # 2️⃣ Market average price
        result = await db.execute(
            select(MarketPrice.price)
            .where(MarketPrice.category == product.category)
        )
        prices = [row[0] for row in result.all()]

        if not prices:
            raise HTTPException(status_code=404, detail="No market price data available")

        market_avg_price = sum(prices) / len(prices)

        # 3️⃣ Demand elasticity (🔥 integrated)
        elasticity = await ElasticityService.get_elasticity_value(db, product_id)

        # 4️⃣ Pricing decision logic
        if elasticity < -1:  # Highly elastic
            if current_price > market_avg_price:
                recommended_price = current_price * 0.95
                reasoning = "High elasticity and overpriced → reduce price"
            else:
                recommended_price = current_price * 1.02
                reasoning = "High elasticity but competitively priced → slight increase"

        elif elasticity > 1:  # Inelastic
            if current_price < market_avg_price:
                recommended_price = current_price * 1.05
                reasoning = "Low elasticity and underpriced → increase price"
            else:
                recommended_price = current_price
                reasoning = "Low elasticity and well priced → hold price"

        else:
            recommended_price = current_price
            reasoning = "Balanced demand → no change"

        recommended_price = round(recommended_price, 2)

        # 5️⃣ Save recommendation
        rec = PriceRecommendation(
                product_id=product_id,
                recommended_price=recommended_price,
                market_avg_price=round(market_avg_price, 2),
                elasticity=round(elasticity, 3),
                reasoning=reasoning
                )

        db.add(rec)
        await db.commit()

        db.add(rec)
        await db.commit()

        return {
            "product_id": product_id,
            "current_price": current_price,  # from Product table
            "market_avg_price": round(market_avg_price, 2),
            "elasticity": round(elasticity, 3),
            "recommended_price": recommended_price,
            "reasoning": reasoning
        }
