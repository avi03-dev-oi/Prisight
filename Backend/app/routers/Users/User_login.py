from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.User_model import User
from app.models.auth_models import UserLoginModel
from app.Services.User_services import UserService

router = APIRouter()
@router.post("/login")
async def login_user(user: UserLoginModel, db: Session = Depends(get_db)):
    return await UserService.user_login(db, user)