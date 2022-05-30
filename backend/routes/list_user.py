from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import database
from database.models import Users
from database.schema import show_user
from functions import check_role
from functions.oauth import current_user
from typing import List

router = APIRouter(
    tags = ['List Of User']
)

@router.get('/user_list', response_model = List[show_user])
def list_of_user(db: Session = Depends(database.get_db), cur_user: show_user = Depends(current_user)):
    role_id = cur_user.role_id
    role = check_role.check_role(role_id)
    print(role)
    if role == 'Superadmin':
        all_user = db.query(Users).all()
        return all_user
    elif role == 'Admin':
        query = f'select * from users where users.c_id = {cur_user.c_id}'
        res = db.execute(query).fetchall()
        return res
    elif role == 'Supervisor':
        query = f'select * from users where users.c_id = {cur_user.c_id} AND role_id != 1'
        res = db.execute(query).fetchall()
        return res
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)