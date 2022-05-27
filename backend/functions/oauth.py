from fastapi.security import OAuth2PasswordBearer
from database.database import database
from database import models
from fastapi import Depends, HTTPException,status
from functions import tokens

oauth_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

db = database

def current_user(token: str = Depends(oauth_scheme)):
        payload = tokens.decode_access_token(token)
        email: str = payload.get('sub')
        if email is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        else:
            user = db.query(models.Users).filter( models.Users.email == email ).first()
            if user is None:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
            else:
                return user