from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.NLP.explanation_service import NLPExplanationService

router = APIRouter()

@router.post("/explain/pricing/{product_id}")
async def pricing_explanation(product_id: int, db=Depends(get_db)):
    return await NLPExplanationService.pricing_explanation(db, product_id)

@router.post("/explain/forecast/{product_id}")
async def forecast_explanation(product_id: int, db=Depends(get_db)):
    return await NLPExplanationService.forecast_explanation(db, product_id)

@router.post("/explain/promotion/{product_id}")
async def promotion_explanation(product_id: int, db=Depends(get_db)):
    return await NLPExplanationService.promotion_explanation(db, product_id)
