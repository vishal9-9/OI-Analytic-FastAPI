from fastapi import APIRouter, Depends,HTTPException,status
from functions import check_role
from sqlalchemy.orm import Session
from database.database import get_db
from database.schema import show_user
from functions.oauth import current_user,oauth_scheme

router = APIRouter(
    tags = ['Add User']
)

@router.get('/user_add')
def add_user(db: Session = Depends(get_db),cur_user : show_user =  Depends(current_user)):
    role_id = cur_user.role_id
    role = check_role.check_role(role_id)
    return role
