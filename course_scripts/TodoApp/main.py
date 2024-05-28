from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users

from database import SessionLocal


app = FastAPI()

def init_db(engine):
    # Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
    db = SessionLocal
    models.Base.metadata.create_all(bind=engine, checkfirst=True)

    db.commit()

# create db
init_db(engine)
# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)