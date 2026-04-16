from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.Services.Elasticity_service import ElasticityService

router = APIRouter(prefix="/elasticity", tags=["Elasticity"])

@router.post("/calculate/{product_id}")
async def calculate(product_id: int, db: AsyncSession = Depends(get_db)):
    return await ElasticityService.calculate_elasticity(db, product_id)
