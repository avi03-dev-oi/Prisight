from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select,update
from app.models.Sales_history_model import SalesHistory
import pandas as pd

class SalesServices:
    @staticmethod
    async def upload_sales_csv(db, file):
        try:
            df=pd.read_csv(file.file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error reading CSV file: {str(e)}"
            )
        required_cols = {"product_id", "date", "units_sold", "selling_price"}
        if not required_cols.issubset(df.columns):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV file must contain product_id, date, units_sold, and selling_price columns."
            )
        # Insert rows
        for _,rows in df.iterrows():
            sales_record = SalesHistory(
                product_id=rows['product_id'],
                date=pd.to_datetime(rows['date']).date(),
                units_sold=rows['units_sold'],
                selling_price=rows['selling_price']
            )
            db.add(sales_record)
            await db.commit()
        return {"message": "Sales records uploaded successfully."}
    @staticmethod
    async def get_product_sales(db, product_id: int):
        stmt = select(SalesHistory).where(SalesHistory.product_id == product_id)
        result = await db.execute(stmt)
        sales_records = result.scalars().all()
        return sales_records