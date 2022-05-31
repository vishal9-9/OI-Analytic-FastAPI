from fastapi import APIRouter, Depends,HTTPException,status
from database.database import get_db
from database.models import Users
from database.schema import login_user
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from functions import passhash,tokens

router = APIRouter(
    tags = ['Login']
)

@router.post('/login')
def auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == request.username).first()
    if not user.isactive == 1:
        raise HTTPException(status_code = 404,detail = "User Deleted")
    if not user:
        raise HTTPException(status_code = 404,detail = "Email Incorrect")
    password = passhash.chech_hash(user.password, request.password)
    if not password:
        raise HTTPException(status_code = 404,detail = "Password Incorrect")
    access_token = tokens.create_access_token(data = {'sub': user.email})
    return {"access_token" : access_token , "token_type": "bearer"}