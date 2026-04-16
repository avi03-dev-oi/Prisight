from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.Demand_forecast_service import DemandForecastService

router = APIRouter()

@router.post("/predict/{product_id}")
async def forecast_demand(
    product_id: int,
    days: int = 7,
    db=Depends(get_db)
):
    return await DemandForecastService.forecast_demand(db, product_id, days)
