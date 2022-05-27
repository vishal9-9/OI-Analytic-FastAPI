from fastapi import APIRouter, Depends,HTTPException,status
from database.database import get_db
from database import models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from functions import passhash,tokens

router = APIRouter(
    tags = ['Login']
)

@router.post('/login')
def auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if user:
        if passhash.chech_hash(user.password, request.password):
            access_token = tokens.create_access_token(data = {'sub': user.email})
            db.close()
            return {"access_token" : access_token , "token_type": "bearer"}
        else:
            return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    else:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)    