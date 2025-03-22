# server essentials
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from routers import all_routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(all_routers)

if __name__ == "__main__":
    logger.info('Starting Document service Server on PORT=3210')
    uvicorn.run("main:app", host="0.0.0.0", port=3210, loop='asyncio', reload=True)
