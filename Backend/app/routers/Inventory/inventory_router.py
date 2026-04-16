from fastapi import APIRouter, Depends
from app.database import get_db
from app.Services.Inventory_service import InventoryService

router = APIRouter()

@router.post("/reorder/{product_id}")
async def reorder_recommendation(
    product_id: int,
    db=Depends(get_db)
):
    return await InventoryService.recommend_reorder(db, product_id)
