from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from starlette import status

from google.oauth2 import credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth

from database import get_db, SessionLocal

import  models

from . import user_schema
from . import user_crud

router = APIRouter(
    prefix="/api/user",
)

def get_existing_user(db: Session, user_create: user_crud.UserCreate):
    return db.query(models.User).filter(
        (models.User.username == user_create.username) |
        (models.User.email == user_create.email)
    ).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

@router.get("/get-user/{user_email}")
def get_user( user_email: str, ):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()

@router.post("/is-user")
def is_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)
    if user:
        return True
    else:
        user_crud.create_user(db, user_in)
        return True