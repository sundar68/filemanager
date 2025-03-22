import logging
from typing import Optional, List
from utils.file import create_file, fetch_files
from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from utils.cloud import upload_file

from schemas.file import FileRead, FileCreate, FileUploadBody
from db import get_async_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_router = APIRouter(tags=["FILES"])


@file_router.get("/files", summary="Get all files")
async def get_notebook_by_id(
        request: Request,
        db: AsyncSession = Depends(get_async_session)
):
    # files = [{
    #     "id": "1",
    #     "name": "file1",
    #     "type": "text",
    #     "size": 100,
    #     "url": "",
    #     "storage_type": "local",
    #     "upload_date": datetime.utcnow()
    # }]
    files = await fetch_files(db)
    return {"files": files}


@file_router.post("/files/upload", response_model=FileRead)
async def upload_to_cloud(info: FileUploadBody = Depends(), file: UploadFile = File(...), db: AsyncSession = Depends(get_async_session)) -> str:
    try:
        result = await upload_file(file)
        print(result)
        new_file= FileCreate(
            name=info.name,
            type=info.type,
            size=info.size,
            url=result['file_url'],
            storage_type='minio'
        )
        data = await create_file(new_file, db)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
