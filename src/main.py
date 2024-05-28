from fastapi import FastAPI
from database import db_models
from starlette import status
#from routers import auth, todos, admin, users
from routers import auth, todos

app = FastAPI()

app.include_router(auth.router)
# app.include_router(todos.router)