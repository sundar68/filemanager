import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from schemas.file import FileCreate, FileRead
from models.file import File
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

async def create_file( file: FileCreate, db: AsyncSession):
    try:
        # file["storage_type"] = file["storage_type"].lower()
        new_file = File(**file.model_dump())
        db.add(new_file)
        await db.commit()
        await db.refresh(new_file)
        return FileRead.model_validate(new_file.__dict__).model_dump()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error adding file {str(e)}")
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

async def fetch_files(db: AsyncSession):
    try:
         db_files = await db.execute(select(File))
         files = db_files.scalars().all()
         return [FileRead.model_validate(file) for file in files]
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error fetching files {str(e)}")
        raise HTTPException(status_code=500, detail="Database error: " + str(e))