from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    user_name: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/users", status_code=status.HTTP_200_OK)
async def new_users(db: db_dependency, user_request: CreateUserRequest):
    try:
        new_user = Users(
            user_name=user_request.user_name,
            hashed_password=bcrypt_context.hash(user_request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error {e}") from e

    return {"User": new_user}


@router.post("/token", response_model=TokenResponse)
async def login_by_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user!"
        )
    token = create_token(user.user_name, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        user_id: int = payload.get("id")

        if user_name is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valid user!"
            )

        return {"id": user_id, "user_name": user_name}
    except JWTError as e:
        raise ValueError(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valid user!"
        ) from e


def authenticate_user(user_name: str, password: str, db):
    user = db.query(Users).filter(Users.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_token(user_name: str, user_id: int, expires_delta: timedelta):
    expires = datetime.utcnow() + expires_delta
    encode_jwt = {"sub": user_name, "id": user_id, "exp": expires}

    return jwt.encode(encode_jwt, SECRET_KEY, algorithm=ALGORITHM)
