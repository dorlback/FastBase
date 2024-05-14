from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")

user_memo_association = Table(
    'user_memo',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'),  primary_key=True),
    Column('memo_id', Integer, ForeignKey('memo.id'),  primary_key=True)
)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)   
    username = Column(String, nullable=False)
    memos = relationship('Memo', secondary="user_memo", back_populates='users')
    
class Memo(Base):
    __tablename__ = "memo"

    id = Column(Integer, primary_key=True)
    unique_id = Column(String, nullable=False, unique=True) 
    title = Column(String, nullable=False)     
    content = Column(String, nullable=False)     
    users = relationship('User', secondary="user_memo", back_populates='memos')
    create_date = Column(DateTime, nullable=False)