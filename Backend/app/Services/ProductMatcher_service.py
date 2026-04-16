from fastapi import APIRouter, Depends,HTTPException, UploadFile
from app.Services.Sales__services import SalesServices
from app.database import get_db
from sqlalchemy.orm import Session
from fuzzywuzzy import fuzz
from sqlalchemy import select
from app.models.Productmatch_models import Product
from app.models.Market_model import MarketPrice
from app.utils.normalizer import normalize_text

class ProductMatcher:
    async def auto_match_product(db,product_id:int):
        #fetch products
        product=await db.get(Product,product_id)
        if not product:
            raise HTTPException(status_code=404,detail="Product not found")
        normalized_product_name=normalize_text(product.name)
        #fetch all products from market
        result=await db.execute(select(MarketPrice))
        market_products=result.scalars().all()



