from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.inventory_model import Inventory
from app.Services.Demand_forecast_service import DemandForecastService

class InventoryService:

    @staticmethod
    async def recommend_reorder(db, product_id: int):
        result = await db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        inventory = result.scalar_one_or_none()

        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")

        forecast = await DemandForecastService.forecast_demand(
            db, product_id, inventory.lead_time_days
        )

        avg_daily_demand = forecast["total_predicted_units"] / inventory.lead_time_days

        safety_stock = avg_daily_demand * inventory.lead_time_days * 0.25
        reorder_point = (avg_daily_demand * inventory.lead_time_days) + safety_stock

        reorder_now = inventory.current_stock <= reorder_point
        reorder_qty = max(0, int(reorder_point - inventory.current_stock))

        return {
            "product_id": product_id,
            "current_stock": inventory.current_stock,
            "avg_daily_demand": round(avg_daily_demand, 2),
            "lead_time_days": inventory.lead_time_days,
            "reorder_point": round(reorder_point, 2),
            "reorder_now": reorder_now,
            "recommended_reorder_quantity": reorder_qty
        }
