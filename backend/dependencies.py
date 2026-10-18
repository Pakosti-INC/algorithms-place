from fastapi import Depends,HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import Session as SessionLocal
from schemas import CurrentUser
from models import User, UsersRole
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorigth=ALGORITHM)
        user_id: str = payload.get("sub")
        group_id: int | None = payload.get("group")
        role: str = payload.get("role")

        if user_id is None or role is None:
            raise credentials_exception

        return CurrentUser(user_id=int(user_id), group_id=group_id, role=role)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истёк",
            headers={"WWW-Authenticate": "bearer"}
        )

    except jwt.PyJWTError:
        raise credentials_exception

def check_teacher_role(data: CurrentUser = Depends(get_current_user)):
    if data.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Доступ запрещён. Требуются права преподавателя.")
    return data

