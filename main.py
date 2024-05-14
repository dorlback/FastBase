import models

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests

from database import engine

from domain.question import question_router
from domain.user import user_router
from domain.memo import memo_router
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",    # 또는 "http://localhost:5173"
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://192.168.123.106:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(user_router.router)
app.include_router(memo_router.router)