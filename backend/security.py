from bcrypt import hashpw, gensalt, checkpw
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_password_hash(password: str) -> str:
    pass_bytes = password.encode("utf-8")
    pass_hash = hashpw(pass_bytes, salt=gensalt()).decode("utf-8")
    return pass_hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_pass_match = checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    return is_pass_match

def create_access_token(data: dict):
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(minutes=1440)

    to_encode.update({"exp": expiration_time})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
