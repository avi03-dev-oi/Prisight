from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.Services.Pricing_service import PricingService

router = APIRouter()

@router.post("/recommend/{product_id}")
async def recommend_price(product_id: int, db: AsyncSession = Depends(get_db)):
    return await PricingService.recommend_price(db, product_id)
