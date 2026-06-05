from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.User_model import User
from app.models.auth_models import UserLoginModel
from app.Services.User_services import UserService

router = APIRouter()


@router.post("/login")
async def login_user(user: UserLoginModel, db: AsyncSession = Depends(get_db)):
    return await UserService.user_login(db, user)


# ── Admin login ───────────────────────────────────────────────────────────────
ADMIN_EMAIL = "admin@prisight.com"
ADMIN_PASSWORD = "admin123"


@router.post("/admin-login")
async def admin_login(credentials: UserLoginModel, db: AsyncSession = Depends(get_db)):
    if credentials.email != ADMIN_EMAIL or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials.")

    # Find or create admin user row in DB
    result = await db.execute(select(User).where(User.email == ADMIN_EMAIL))
    admin_user = result.scalars().first()

    if not admin_user:
        import uuid
        from datetime import datetime
        from werkzeug.security import generate_password_hash

        admin_user = User(
            uid=str(uuid.uuid4()),
            username="Admin",
            email=ADMIN_EMAIL,
            phone_number="admin",
            password=generate_password_hash(ADMIN_PASSWORD),
            is_admin=True,
            created_at=datetime.utcnow(),
        )
        db.add(admin_user)
        await db.commit()
        await db.refresh(admin_user)

    return {
        "status": "success",
        "message": "Admin login successful.",
        "user": {
            "email": admin_user.email,
            "username": admin_user.username,
            "is_admin": True,
        },
        "is_admin": True,
    }