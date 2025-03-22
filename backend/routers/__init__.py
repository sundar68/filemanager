from fastapi import APIRouter
from .health import health_router
from .file import file_router

all_routers = APIRouter()

all_routers.include_router(health_router)
all_routers.include_router(file_router)
