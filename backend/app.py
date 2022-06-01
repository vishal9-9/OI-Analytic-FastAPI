from fastapi import FastAPI
from database import models
from routes import list_user, login, add_company, add_user, list_company, soft_del_company, reset_password
from database.database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(login.router)
app.include_router(add_user.router)
app.include_router(list_user.router)
app.include_router(add_company.router)
app.include_router(list_company.router)
app.include_router(soft_del_company.router)
app.include_router(reset_password.router)

#routes are done
