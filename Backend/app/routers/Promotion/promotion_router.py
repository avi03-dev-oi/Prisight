from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.Promotion_service import PromotionService

router = APIRouter()

@router.post("/recommend/{product_id}")
async def recommend_promotion(
    product_id: int,
    db=Depends(get_db)
):
    return await PromotionService.recommend_promotion(db, product_id)
