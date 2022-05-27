from fastapi import FastAPI
from database import models
from routes import list_user, login
from database.database import engine
from routes import add_user

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(login.router)
app.include_router(add_user.router)
app.include_router(list_user.router)