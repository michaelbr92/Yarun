from enum import Enum
from functools import reduce
from typing import Dict, Union, List, Any

from fastapi import FastAPI, Path, APIRouter, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.datatypes import Bucket
from pydantic import BaseModel
import uvicorn

from routers import bucket, task

app = FastAPI()

router = APIRouter(prefix="/api/v1")
router.include_router(bucket.router)
router.include_router(task.router)
app.include_router(router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
