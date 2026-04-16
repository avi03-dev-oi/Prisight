import pandas as pd
import numpy as np
from sqlalchemy import select
from app.models.engineered_feature import EngineeredFeature
from app.ML.dataset_builder import create_lstm_dataset
from app.ML.lstm_model import build_lstm_model
from sklearn.preprocessing import MinMaxScaler
from fastapi import HTTPException
import os

class LSTMTrainingService:

    @staticmethod
    async def train_product_model(db, product_id: int):

        result = await db.execute(
            select(EngineeredFeature)
            .where(EngineeredFeature.product_id == product_id)
            .order_by(EngineeredFeature.date)
        )
        rows = result.scalars().all()

        if len(rows) < 15:
            raise HTTPException(
                status_code=400,
                detail="Not enough data to train LSTM model"
            )

        df = pd.DataFrame([{
            "units_sold": r.units_sold,
            "selling_price": r.selling_price,
            "market_avg_price": r.market_avg_price,
            "discount_percent": r.discount_percent,
            "rolling_avg_7": r.rolling_avg_7,
            "rolling_avg_14": r.rolling_avg_14,
            "rolling_avg_30": r.rolling_avg_30,
            "weekday": r.weekday,
            "month": r.month
        } for r in rows])

        feature_cols = [
            "selling_price",
            "market_avg_price",
            "discount_percent",
            "rolling_avg_7",
            "rolling_avg_14",
            "rolling_avg_30",
            "weekday",
            "month"
        ]

        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])

        X, y = create_lstm_dataset(
            df,
            feature_cols=feature_cols,
            target_col="units_sold",
            window_size=7
        )

        model = build_lstm_model(
            input_shape=(X.shape[1], X.shape[2])
        )

        model.fit(
            X,
            y,
            epochs=30,
            batch_size=8,
            verbose=0
        )

        os.makedirs("models", exist_ok=True)
        model.save(f"models/lstm_product_{product_id}.h5")

        return {
            "product_id": product_id,
            "samples": len(X),
            "status": "LSTM model trained successfully"
        }
