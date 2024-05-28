""""Utils for routers"""
from datetime import datetime, timedelta
import os
from pathlib import Path
from typing import Annotated
from dotenv import find_dotenv, load_dotenv
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordBearer

from database.db_models import Users


# load environment vars
try:
    env_file = find_dotenv()
    load_dotenv(env_file)
except OSError:
    envp = Path.cwd().parent / ".env"
    load_dotenv(dotenv_path=envp.as_posix())

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# password encrpytion functions
pwd_context = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password, plainpassword):
        return pwd_context.verify(hashed_password, plainpassword)
    
# authentication functions
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


# access token
def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta

    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# get current user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

# authenticate user
def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not Hash.verify(password, user.hashed_password):
        return False
    
    return user

