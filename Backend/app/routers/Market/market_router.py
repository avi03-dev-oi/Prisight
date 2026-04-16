from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.Services.Market_services import MarketService

router = APIRouter()
@router.post("/upload")
async def upload_market_data(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await MarketService.upload_market_csv(db, file)
@router.get("/stats/{product_name}")
async def get_market_statistics(
    product_name: str,
    db: AsyncSession = Depends(get_db)
):
    return await MarketService.get_market_stats(db, product_name)