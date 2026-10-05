from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import Session as SessionLocal
from models import User, UsersRole

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)):
    # Меняя ID здесь, переключается логика всего API
    test_user_id = 1 # 1 - студент, 2 - препод
    return db.execute(select(User).where(User.id == test_user_id)).scalar_one()

def check_teacher_role(current_user: User = Depends(get_current_user)):
    if current_user.role != UsersRole.TEACHER:
        raise HTTPException(status_code=403, detail="Доступ запрещён. Требуются права преподавателя.")
    return current_user

