from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert

from database import init_db, async_session
from models import Purchase
from schema import PurchaseEventSchema

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.get("/")
async def healthcheck():
    return {"status": "ok", "message": "API is running"}


@app.post("/purchase")
async def create_purchase(
    purchase: PurchaseEventSchema, session: AsyncSession = Depends(get_db_session)
):
    try:
        new_purchase = Purchase(**purchase.model_dump())
        session.add(new_purchase)
        await session.commit()
        return {"status": "ok", "message": "Purchase successfully saved to database"}
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving purchase")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")
