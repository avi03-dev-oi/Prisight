from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.routers.Users import User_register, User_login
from app.routers.Products import Product_router
from app.routers.Sales_record import Sales_router
from app.routers.Market import market_router
from app.routers.Elasticity import elasticity_router
from app.routers.Products import Product_router
from app.routers.Pricing import pricing_router
from app.routers.Forecast import forecast_router
from app.routers.Inventory import inventory_router
from app.routers.Promotion import promotion_router
from app.routers.Features import feature_router
from app.routers.LSTM import lstm_router
from app.routers.Evaluation import evaluation_router
from app.routers.NLP import nlp_router



app = FastAPI()
# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(User_register.router, prefix="/users", tags=["Users"])
app.include_router(User_login.router, prefix="/users", tags=["Users"])
app.include_router(Product_router.router, prefix="/products", tags=["Products"])
app.include_router(Sales_router.router, prefix="/sales", tags=["Sales"])
app.include_router(market_router.router, prefix="/market", tags=["Market"])
app.include_router(elasticity_router.router, prefix="/elasticity", tags=["Elasticity"])
app.include_router(Product_router.router, prefix="/products", tags=["Products"])
app.include_router(pricing_router.router, prefix="/pricing", tags=["Pricing Engine"])
#app.include_router(pricing_router.router, prefix="/price-recommendations", tags=["Price Recommendation"])
app.include_router(forecast_router.router, prefix="/forecast", tags=["Forecast Stocks"])
app.include_router(inventory_router.router,prefix="/inventory",tags=["Inventory"])
app.include_router(promotion_router.router, prefix="/promotions", tags=["Promotions"])
app.include_router(feature_router.router,prefix="/features",tags=["Feature Engineering"])
app.include_router(lstm_router.router, prefix="/lstm", tags=["LSTM Forecast"])
app.include_router(evaluation_router.router, prefix="/evaluation", tags=["Model Evaluation"])
app.include_router(nlp_router.router, prefix="/nlp", tags=["NLP Insights"])







@app.get("/")
def root():
    return {"message": "Backend running successfully 🚀"}
