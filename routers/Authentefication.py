from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from db.models import User
from db.database import get_session
import secrets
import string
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlmodel import Session, select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Token(BaseModel):
    token_type: str
    access_type: str = "Bearer"

router = APIRouter()

def generate_secret_key(length=64):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

SECRET_KEY = generate_secret_key()
ALGORITHM = "HS256"
ACCESS_EXPIRE_TIME = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.now() + timedelta(minutes=ACCESS_EXPIRE_TIME)
    to_encode.update({"exp": expires})
    decoded = jwt.encode(to_encode, SECRET_KEY, algorithms=ALGORITHM)
    return decoded

@router.post("/authentefication")
def auth(user: User, session: Session = Depends(get_session)):
    right_name = session.exec(select(User).where(User.name == user.name)).first()
    if right_name:
        raise HTTPException(status_code=401, detail="name is using")
    session.add(user)
    session.commit()
    session.refresh(user)

@router.post("/login")
def login(user: User, session: Session = Depends(get_session)):
    right_login = session.exec(select(User).where((User.name == user.name) & (User.password == user.password))).first()
    if not right_login:
        raise HTTPException(status_code=400, detail="incorrect")
    token = create_access_token(data={"sub": user.name})
    return {"token_type": token, "access_type": "Bearer"}

def current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="no name given")
        user = session.exec(select(User).where(User.name == username)).first()
        if user is None:
            raise HTTPException(status_code=400, detail="wrong token")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.get("/me")
def all_my_information(session: Session = Depends(get_session)):
    pass