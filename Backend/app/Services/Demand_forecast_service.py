import pandas as pd
import numpy as np
from sqlalchemy import select
from fastapi import HTTPException
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta

from app.models.Sales_history_model import SalesHistory


class DemandForecastService:

    @staticmethod
    async def forecast_demand(db, product_id: int, days: int = 7):
        """
        Forecast product demand using ARIMA time-series model
        """

        # 1️⃣ Fetch sales history
        result = await db.execute(
            select(
                SalesHistory.date,
                SalesHistory.units_sold
            )
            .where(SalesHistory.product_id == product_id)
            .order_by(SalesHistory.date)
        )

        rows = result.all()

        if len(rows) < 5:
            raise HTTPException(
                status_code=400,
                detail="Not enough data for forecasting (minimum 5 records required)"
            )

        # 2️⃣ Convert to DataFrame
        df = pd.DataFrame(rows, columns=["date", "units_sold"])
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        # 3️⃣ Create continuous daily series
        ts = (
            df["units_sold"]
            .resample("D")
            .sum()
            .fillna(0)  # assume no sales on missing days
        )

        # 4️⃣ Fit ARIMA model (safe defaults)
        try:
            model = ARIMA(ts, order=(1, 1, 1))
            model_fit = model.fit()
            forecast_values = model_fit.forecast(steps=days)

        except Exception:
            # Fallback: rolling average if ARIMA fails
            avg_demand = ts.rolling(7).mean().iloc[-1]
            forecast_values = pd.Series(
                [avg_demand] * days,
                index=pd.date_range(
                    start=ts.index[-1] + timedelta(days=1),
                    periods=days,
                    freq="D"
                )
            )

        # 5️⃣ Clean forecast
        forecast_values = forecast_values.clip(lower=0)

        # 6️⃣ Build response
        forecast_dates = pd.date_range(
            start=ts.index[-1] + timedelta(days=1),
            periods=days,
            freq="D"
        )

        daily_forecast = [
            {
                "date": str(forecast_dates[i].date()),
                "predicted_units": int(round(forecast_values.iloc[i]))
            }
            for i in range(days)
        ]

        return {
            "product_id": product_id,
            "forecast_days": days,
            "daily_forecast": daily_forecast,
            "total_predicted_units": int(round(forecast_values.sum()))
        }
