from models import User, Memo
from domain.memo.memo_schema import MemoCreate, MemoUpdateIn
from sqlalchemy.orm import Session


def create_memo(db: Session, memo_data: MemoCreate):

    
    memo = Memo(unique_id=memo_data.unique_id, 
                title=memo_data.title, 
                content=memo_data.content,
                create_date=memo_data.create_date
                )
    db.add(memo)
    
    # user_ids에 해당하는 User 객체들을 찾아 Memo의 users 관계에 추가
    users = db.query(User).filter(User.id.in_(memo_data.user_ids)).all()
    memo.users = users

    db.commit()

def update_memo(db: Session, memo, memo_data):

    memo.title = memo_data.title
    memo.content = memo_data.content

    db.add(memo)
    db.commit()

    return memo

def delete_memo(db: Session, unique_id: int):
    # 메모를 찾아서
    memo = db.query(Memo).filter(Memo.unique_id == unique_id).first()
    if memo is None:
        return None  # 해당 ID를 가진 메모가 없는 경우 None 반환
    
    # 메모를 데이터베이스에서 삭제
    db.delete(memo)
    
    # 변경 사항 커밋
    db.commit()
    