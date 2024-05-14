
import datetime

from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import FieldValidationInfo
from typing import List

class CheckDataIn(BaseModel):
    uuid: str
    user_email: str

class MemoIn(BaseModel):
    users: List[str]

class MemoUpdateIn(BaseModel):
    unique_id: str
    title: str
    content: str

class MemoCreate(BaseModel):
    unique_id: str
    title: str
    content: str
    user_ids: List[int] = Field(default=[], description="List of user IDs associated with this memo")
    create_date: datetime.datetime

class MemoShareIn(BaseModel):
    unique_id: str
    user_email: EmailStr

# class Memo(Base):
#     __tablename__ = "memo"

#     id = Column(Integer, primary_key=True)
#     unique_id = Column(String, nullable=False, unique=True) 
#     title = Column(String, nullable=False)     
#     content = Column(String, nullable=False)     
#     users = relationship('User', secondary=user_memo_association, back_populates='memos')
