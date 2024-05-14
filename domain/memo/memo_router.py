import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.memo.memo_crud import create_memo, update_memo, delete_memo
from domain.memo.memo_schema import MemoCreate, MemoIn, CheckDataIn, MemoUpdateIn, MemoShareIn
from models import User, Memo
from datetime import datetime
from starlette import status

from database import get_db, SessionLocal

router = APIRouter(
    prefix="/api/memo",
)

@router.get("/get-memos/{user_email}")
def get_memos_router(user_email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == user_email).first()

    if user:
        return user.memos
    return []

@router.post("/create-memo")
def create_memo_router(memo_in: MemoIn, db: Session =  Depends(get_db)):

    unique_id = uuid.uuid4()

    user = db.query(User).filter(User.email == memo_in.users[0]).first()

    new_memo = MemoCreate(
        unique_id=str(unique_id),
        title="무제",
        content="",
        user_ids=[user.id],
        create_date=datetime.now()
    )
    print(new_memo)
    create_memo(db, new_memo)

    return True

@router.post("/update-memo")
def create_memo_router(memo_update_in: MemoUpdateIn, db: Session =  Depends(get_db)):
    memo_update = db.query(Memo).filter(Memo.unique_id == memo_update_in.unique_id).first()

    memo = update_memo(db, memo_update, memo_update_in)
    return memo

@router.delete("/delete-memo/{unique_id}")
def delete_memo_router(unique_id: str, db: Session = Depends(get_db)):
    deleted_memo = delete_memo(db, unique_id)

    if deleted_memo is None:
        raise HTTPException(status_code=404, detail="Memo not found")
    return deleted_memo

@router.post("/share-memo")
def share_memo_router(memo_share_in: MemoShareIn, db: Session = Depends(get_db)):

    memo = db.query(Memo).filter(Memo.unique_id == memo_share_in.unique_id).first()
    user = db.query(User).filter(User.email == memo_share_in.user_email).first()
    
    memo.users.append(user)
    db.commit()
    
    return True

@router.post("/is-valid-uuid")
def is_valid_uuid_router(check_data_in:CheckDataIn):
    db = SessionLocal()
    memo = db.query(Memo).filter(Memo.unique_id == check_data_in.uuid).first()
    user = db.query(User).filter(User.email == check_data_in.user_email).first()

    # UUID가 유효하지 않은 경우
    if not memo:
        return {"uuid_valid": False, "user_authorized": False, "memo":memo}

    # 사용자가 존재하지 않는 경우
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    is_authorized = user in memo.users
    
    return {"uuid_valid": True, "user_authorized": is_authorized, "memo":memo}