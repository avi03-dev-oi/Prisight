#app/models/auth_models.py
from typing import Optional,List,Union
from pydantic import BaseModel,EmailStr
from datetime import datetime, date

class UserRegisterModel(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str
class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str | None = None
    brand: str | None = None
    cost_price: float
    current_price: float | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    brand: str | None = None
    cost_price: float | None = None
    current_price: float | None = None
class SalesRecord(BaseModel):
    product_id: int
    date: date
    units_sold: int
    selling_price: float
class MarketPriceRecord(BaseModel):
    product_name: str
    brand: str | None = None
    category: str | None = None
    source: str | None = None
    price: float
    date_collected: date
class PriceRecommendationCreate(BaseModel):
    product_id: int
    recommended_price: float
    market_avg_price: float
    elasticity: float
    reasoning: str

class PriceRecommendationOut(PriceRecommendationCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True