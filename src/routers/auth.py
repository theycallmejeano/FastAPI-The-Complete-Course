from typing import Annotated
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm.session import Session
from sqlalchemy import text
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# local imports
from app.app_models import CreateUserRequest, Token
from routers.utils import authenticate_user, create_access_token, pwd_context, Hash
from database.db_models import Users
from database.utils import get_db

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/auth/")
def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=Hash.bcrypt(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()

@router.get("/auth/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(Users).all()


@router.get("/test-db")
def read_root(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * from users"))
    return {"result": result.fetchone()}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed authentication'

    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}



