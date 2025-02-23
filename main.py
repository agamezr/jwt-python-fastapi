from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import auth
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dpendency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/users", status_code=status.HTTP_200_OK)
async def users(user_logged: user_dependency, db: db_dpendency):
    if user_logged is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return db.query(models.Users).all()
