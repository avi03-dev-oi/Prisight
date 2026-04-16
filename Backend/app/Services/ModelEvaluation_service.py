import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sqlalchemy import select
from app.models.engineered_feature import EngineeredFeature
from app.models.ModelEvaluation import ModelEvaluation
from fastapi import HTTPException
import math

class ModelEvaluationService:

    @staticmethod
    async def evaluate(db, product_id: int):
        result = await db.execute(
            select(EngineeredFeature)
            .where(EngineeredFeature.product_id == product_id)
            .order_by(EngineeredFeature.date)
        )
        rows = result.scalars().all()

        if len(rows) < 10:
            raise HTTPException(
                status_code=400,
                detail="Not enough data to evaluate model"
            )

        y_true = np.array([r.units_sold for r in rows])
        y_pred = np.full_like(y_true, y_true.mean())

        mae = mean_absolute_error(y_true, y_pred)
        rmse = math.sqrt(mean_squared_error(y_true, y_pred))
        mape = float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)

        record = ModelEvaluation(
            product_id=product_id,
            mae=round(mae, 2),
            rmse=round(rmse, 2),
            mape=round(mape, 2),
            samples=len(y_true)
        )

        db.add(record)
        await db.commit()

        return {
            "product_id": product_id,
            "samples": len(y_true),
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "MAPE (%)": round(mape, 2)
        }
