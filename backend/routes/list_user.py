from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import database
from database.models import Users
from database.schema import show_user, update_user
from functions import check_role,addnew_user
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

@router.post('/user/{id}')
def user_with_id(id: int,user: update_user,db: Session = Depends(database.get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        user_toupdate = db.query(Users).get(id)
        if user and cur_user.role_id <= user_toupdate.role_id:
            addnew_user.update_user(user,id)
            return 'User Updated'
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    elif role == 'Admin':
        user_toupdate = db.query(Users).get(id)
        if user and cur_user.role_id <= user_toupdate.role_id:
            if user.role_id in [1,2,3]:
                addnew_user.update_user(user,id)
                return 'User Updated'
            else:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    elif role == 'Supervisor':
        user_toupdate = db.query(Users).get(id)
        if user:
            if user.role_id in [2,3] and cur_user.role_id <= user_toupdate.role_id:
                addnew_user.update_user(user,id)
                return 'User Updated'
            else:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)