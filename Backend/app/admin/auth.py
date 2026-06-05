from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.User_model import User


async def require_admin(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Simple session-cookie-based admin guard.
    Since the project has no JWT yet, we check a custom header
    X-Admin-Token that the frontend sends after admin login.
    """
    admin_token = request.headers.get("X-Admin-Token")
    if not admin_token or admin_token != "prisight-admin-secret":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )
    return True