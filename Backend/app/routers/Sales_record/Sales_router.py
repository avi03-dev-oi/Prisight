from fastapi import APIRouter, Depends, UploadFile
from app.Services.Sales__services import SalesServices
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
@router.post("/upload_sales_csv")
async def upload_sales_csv(file: UploadFile, db: Session = Depends(get_db)):
    return await SalesServices.upload_sales_csv(db, file)
@router.get("/product_sales/{product_id}")
async def get_product_sales(product_id: int, db: Session = Depends(get_db)):
    return await SalesServices.get_product_sales(db, product_id)
