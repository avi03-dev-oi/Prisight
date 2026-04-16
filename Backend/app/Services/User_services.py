from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.User_model import User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import uuid

class UserService:
    @staticmethod
    async def register_user(db, usermodel):
        # Checking if existing user
        result = await db.execute(
            select(User).where(
                (User.email == usermodel.email) |
                (User.phone_number == usermodel.phone_number)
            )
        )
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email or phone number already exists."
            )

        # Creating hashed password
        hashed_password = generate_password_hash(usermodel.password)

        # Creating new user
        new_user = User(
            uid=str(uuid.uuid4()),
            username=usermodel.name,
            email=usermodel.email,
            phone_number=usermodel.phone_number,
            password=hashed_password,
            created_at=datetime.utcnow()
        )

        db.add(new_user)

        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating user. {str(e)}")

        # Return a proper dictionary response, not HTTPException
        return {"status": "success", "message": "User registered successfully."}
    
    @staticmethod
    async def user_login(db, usermodel):
        #Match User email and password which is hashed
        result = await db.execute(
            select(User).where(User.email == usermodel.email)
        )
        user = result.scalars().first()
        if not user or not check_password_hash(user.password, usermodel.password):
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        
        # Return a proper dictionary response, not HTTPException
        return {"status": "success", "message": "Login successful.", "user": {"email": user.email, "username": user.username}}