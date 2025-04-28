from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from database import init_db, async_session
from models import Purchase
from schema import PurchaseEventSchema


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def healthcheck():
    return {"status": "ok", "message": "API is running"}


@app.post("/purchase")
async def create_purchase(
    purchase: PurchaseEventSchema, session: AsyncSession = Depends(get_db_session)
):
    try:
        query = insert(Purchase).values(purchase.model_dump()).returning(Purchase)
        await session.execute(query)
        await session.commit()
        return {"status": "ok", "msg": "purchase saved"}
    except Exception as e:
        print(f"Something went wrong\n{str(e)}")
        raise HTTPException(status_code=500, detail="Error saving purchase")
