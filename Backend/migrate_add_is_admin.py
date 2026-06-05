"""
One-time migration: adds is_admin column to users table.
Run from the Backend/ directory: python migrate_add_is_admin.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "sqlite+aiosqlite:///./prisight.db"

engine = create_async_engine(DATABASE_URL, echo=False)


async def migrate():
    async with engine.begin() as conn:
        try:
            await conn.execute(
                text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0 NOT NULL")
            )
            print("✅ Migration successful: is_admin column added to users table.")
        except Exception as e:
            print(f"⚠️  Migration skipped (column likely already exists): {e}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate())