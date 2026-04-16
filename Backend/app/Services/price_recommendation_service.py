from sqlalchemy.orm import Session
from app.models.PriceRecommendation_model import PriceRecommendation
from app.models.Product_model import Product

def create_price_recommendation(
    db: Session,
    product_id: int,
    recommended_price: float,
    market_avg_price: float,
    elasticity: float,
    reasoning: str
):
    rec = PriceRecommendation(
        product_id=product_id,
        recommended_price=recommended_price,
        market_avg_price=market_avg_price,
        elasticity=elasticity,
        reasoning=reasoning
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
def calculate_recommended_price(
    market_avg_price: float,
    elasticity: float
) -> float:
    if elasticity < -1:
        return market_avg_price * 0.95   # 5% lower
    elif -1 <= elasticity <= 0:
        return market_avg_price
    else:
        return market_avg_price * 1.05   # 5% premium


def create_price_recommendation(db: Session, payload):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise ValueError("Product not found")

    recommended_price = calculate_recommended_price(
        payload.market_avg_price,
        payload.elasticity
    )

    rec = PriceRecommendation(
        product_id=payload.product_id,
        recommended_price=recommended_price,
        market_avg_price=payload.market_avg_price,
        elasticity=payload.elasticity,
        reasoning=(
            "Price reduced due to high price sensitivity"
            if payload.elasticity < -1 else
            "Price aligned with market average"
            if payload.elasticity <= 0 else
            "Premium pricing due to low price sensitivity"
        )
    )

    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
