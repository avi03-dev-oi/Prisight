from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.LSTMTraining_service import LSTMTrainingService
from app.Services.LSTMForecast_service import LSTMForecastService

router = APIRouter()

@router.post("/train/{product_id}")
async def train_lstm(product_id: int, db=Depends(get_db)):
    return await LSTMTrainingService.train_product_model(db, product_id)

@router.post("/predict/{product_id}")
async def predict_lstm(product_id: int, days: int = 7, db=Depends(get_db)):
    return await LSTMForecastService.forecast(db, product_id, days)
