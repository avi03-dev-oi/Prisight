# app/routers/price_recommendation_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.auth_models import (
    PriceRecommendationCreate,
    PriceRecommendationOut
)
from app.Services.price_recommendation_service import (
    create_price_recommendation
)

router = APIRouter()

@router.post("/", response_model=PriceRecommendationOut)
def create_rec(
    payload: PriceRecommendationCreate,
    db: Session = Depends(get_db)
):
    return create_price_recommendation(db, **payload.dict())
