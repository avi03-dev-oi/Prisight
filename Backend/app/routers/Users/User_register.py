from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.User_model import User
from app.models.auth_models import UserRegisterModel
from werkzeug.security import check_password_hash, generate_password_hash
from app.Services.User_services import UserService
from datetime import datetime
import uuid
router = APIRouter()

@router.post("/register")
async def register_user(user: UserRegisterModel, db: Session = Depends(get_db)):
    return await UserService.register_user(db, user)


    


