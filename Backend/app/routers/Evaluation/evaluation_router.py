from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.ModelEvaluation_service import ModelEvaluationService

router = APIRouter()

@router.post("/evaluate/{product_id}")
async def evaluate_model(product_id: int, db=Depends(get_db)):
    return await ModelEvaluationService.evaluate(db, product_id)
