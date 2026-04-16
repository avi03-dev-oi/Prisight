import numpy as np
import pandas as pd
from sqlalchemy import select
from app.models.engineered_feature import EngineeredFeature
from tensorflow.keras.models import load_model
from fastapi import HTTPException
from sklearn.preprocessing import MinMaxScaler

class LSTMForecastService:

    @staticmethod
    async def forecast(db, product_id: int, days: int = 7):

        result = await db.execute(
            select(EngineeredFeature)
            .where(EngineeredFeature.product_id == product_id)
            .order_by(EngineeredFeature.date)
        )
        rows = result.scalars().all()

        if len(rows) < 7:
            raise HTTPException(
                status_code=400,
                detail="Not enough data for LSTM inference"
            )

        model = load_model(
            f"models/lstm_product_{product_id}.h5",
            compile=False
        )


        df = pd.DataFrame([{
            "selling_price": r.selling_price,
            "market_avg_price": r.market_avg_price,
            "discount_percent": r.discount_percent,
            "rolling_avg_7": r.rolling_avg_7,
            "rolling_avg_14": r.rolling_avg_14,
            "rolling_avg_30": r.rolling_avg_30,
            "weekday": r.weekday,
            "month": r.month
        } for r in rows])

        feature_cols = df.columns.tolist()
        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])

        window = df.iloc[-7:].values
        window = window.reshape(1, window.shape[0], window.shape[1])

        predictions = []

        for _ in range(days):
            pred = model.predict(window, verbose=0)[0][0]
            predictions.append(round(float(pred), 2))

        return {
            "product_id": product_id,
            "forecast_days": days,
            "predicted_units": predictions
        }
