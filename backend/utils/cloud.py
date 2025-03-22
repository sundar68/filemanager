import logging
import uuid
from abc import ABC, abstractmethod
from io import StringIO
from typing import Dict

import aioboto3
import httpx
# import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, UploadFile
from tenacity import retry, stop_after_attempt, wait_fixed

from db.settings import get_settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config = get_settings()

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "txt", "json"}


def allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(filename: str) -> str:
    """
    Generate a unique filename using UUID while preserving the original file extension.
    """
    extension = filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4().hex}.{extension}"


class CloudStorage(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> Dict[str, str]:
        """
        Upload a file to the cloud.

        Args:
            file: A FastAPI UploadFile.
            folder: The folder (or prefix) to store the file.

        Returns:
            A dictionary containing the file URL and the unique filename.
        """
        pass


# ==============================================================================
# MinIO
# ==============================================================================

class MinioStorage(CloudStorage):
    def __init__(self):
        self.endpoint_url = config.cloud.minio_endpoint_url
        self.bucket_name = config.cloud.minio_bucket_name
        self.access_key = config.cloud.minio_access_key_id
        self.secret_key = config.cloud.minio_secret_access_key

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        before=lambda retry_state: logger.info("Retrying upload to MinIO: attempt %d", retry_state.attempt_number),
        after=lambda retry_state: logger.info("Finished attempt %d", retry_state.attempt_number),
    )
    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> Dict[str, str]:
        """Upload a file to MinIO storage."""
        if not allowed_file(file.filename):
            logger.error("Disallowed file extension: %s", file.filename)
            raise HTTPException(status_code=400, detail="File type not allowed")

        unique_filename = generate_unique_filename(file.filename)
        file_path = f"{folder}/{unique_filename}"
        session = aioboto3.Session()

        try:
            async with session.client(
                    "s3",
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
            ) as client:
                await client.upload_fileobj(file.file, self.bucket_name, file_path)
            logger.info("File uploaded to MinIO: %s", file_path)
        except NoCredentialsError:
            logger.exception("MinIO credentials not found.")
            raise HTTPException(status_code=500, detail="MinIO credentials not found")
        except ClientError as e:
            logger.exception("Error uploading file to MinIO: %s", e)
            raise HTTPException(status_code=500, detail="Could not upload file to MinIO")
        except Exception as e:
            logger.exception("Unexpected error during file upload: %s", e)
            raise HTTPException(status_code=500, detail=str(e))

        file_url = f"{self.endpoint_url}/{self.bucket_name}/{file_path}"
        return {"file_url": file_url, "filename": unique_filename}


# ==============================================================================
# AWS S3 
# ==============================================================================

class AWSS3Storage(CloudStorage):
    def __init__(self):
        self.region = config.cloud.aws_region
        self.bucket_name = config.cloud.aws_bucket_name
        self.access_key = config.cloud.aws_access_key
        self.secret_key = config.cloud.aws_secret_key

    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> Dict[str, str]:
        """Upload a file to AWS S3."""
        if not allowed_file(file.filename):
            logger.error("Disallowed file extension: %s", file.filename)
            raise HTTPException(status_code=400, detail="File type not allowed")

        unique_filename = generate_unique_filename(file.filename)
        file_path = f"{folder}/{unique_filename}"
        session = aioboto3.Session()

        try:
            async with session.client(
                    "s3",
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region,
            ) as client:
                await client.upload_fileobj(file.file, self.bucket_name, file_path)
            logger.info("File uploaded to AWS S3: %s", file_path)
        except ClientError as e:
            logger.exception("Error uploading file to AWS S3: %s", e)
            raise HTTPException(status_code=500, detail="Could not upload file to AWS S3")
        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            raise HTTPException(status_code=500, detail=str(e))

        file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_path}"
        return {"file_url": file_url, "filename": unique_filename}



def get_cloud_storage() -> CloudStorage:
    """
    Return an instance of CloudStorage based on an environment/config variable.
    """
    provider = config.cloud.cloud_provider.lower()

    if provider == "aws":
        return AWSS3Storage()
    elif provider == "minio":
        return MinioStorage()
    else:
        raise ValueError(f"Unsupported cloud provider: {provider}")


async def upload_file(file: UploadFile):
    return await get_cloud_storage().upload_file(file)
