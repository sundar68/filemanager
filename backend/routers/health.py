import os

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session

health_router = APIRouter()


# @health_router.get("/")
# async def health_check():
#     return {"message": "Welcome to Document Service"}


@health_router.get("/health")
async def health_check():
    return {"status": "success"}


@health_router.get("/test-query")
async def test_query(db: AsyncSession = Depends(get_async_session)):
    """
    Execute a simple query to fetch data from the database.
    """
    try:
        query = text("SELECT 1 as test;")
        result = await db.execute(query)
        result_dict = dict(result.fetchone()._mapping)
        return {"status": "success", "result": result_dict}
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return {"status": "failure", "message": f"Database error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"status": "failure", "message": f"Unexpected error: {str(e)}"}