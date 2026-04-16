from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.Product_model import Product
from app.models.auth_models import ProductCreate, ProductUpdate
from app.Services.Product_services import ProductService

router = APIRouter()

@router.post("/create")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return await ProductService.create_new_product(db, product)

@router.get("/all")
async def get_products(db: Session = Depends(get_db)):
    return await ProductService.get_all_products(db)

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    return await ProductService.get_product_by_id(db, product_id)
    
@router.put("/update/{product_id}")
async def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return await ProductService.update_product(db, product_id, product_data)

@router.delete("/delete/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    return await ProductService.delete_product(db, product_id) 