import models

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from database import engine

from domain.question import question_router

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",    # 또는 "http://localhost:5173"
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)

# 이 아래에 스태틱 파일 작업