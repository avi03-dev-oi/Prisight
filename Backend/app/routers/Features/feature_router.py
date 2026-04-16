from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.Feature_engineering_service import FeatureEngineeringService

router = APIRouter()

@router.post("/build/{product_id}")
async def build_features(product_id: int, db=Depends(get_db)):
    return await FeatureEngineeringService.build_features(db, product_id)
