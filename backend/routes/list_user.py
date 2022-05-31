from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import database
from database.models import Users
from database.schema import show_user, update_user
from functions import check_role,addnew_user,check_supervisor
from functions.oauth import current_user
from functions import list_company_id
from typing import List

router = APIRouter(
    tags = ['User Panel']
)

@router.get('/user', response_model = List[show_user])
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

@router.get('/user/{id}',response_model = show_user)
def user_with_id(id: int ,db: Session = Depends(database.get_db) ,cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        res = db.query(Users).get(id)
        if res:
            return res
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    elif role == 'Admin':
        res = db.execute(f'select * from users where id = {id} and role_id != 0 and c_id = {cur_user.c_id}').fetchone()
        if res:
            return res
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    elif role == 'Supervisor':
        query = f'select * from users where id = {id} and c_id = {cur_user.c_id} and role_id != 0 and role_id != 1'
        res = db.execute(query).fetchone()
        if res:
            return res
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)   
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED) 


@router.get('/supervisor',response_model = List[show_user])
def supervisor_check(db: Session = Depends(database.get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        c_id = cur_user.c_id
        cid_list = list_company_id.list_of_cid()
        if c_id in cid_list:
            query = f'select * from users where role_id = 2'
            res = db.execute(query).fetchall()
            if res != []:
                return res
            else:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        else:   
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    elif role in ['Admin','Supervisor']:
        c_id = cur_user.c_id
        cid_list = list_company_id.list_of_cid()
        if c_id in cid_list:
            query = f'select * from users where role_id = 2 and c_id = {cur_user.c_id}'
            res = db.execute(query).fetchall()
            if res != []:
                return res
            else:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        else:   
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

    
@router.put('/user/{id}')
def user_with_id(id: int,user: update_user,db: Session = Depends(database.get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if check_supervisor.check_supervisor(user.working_under):
        if role == 'Superadmin':
            user_toupdate = db.query(Users).get(id)
            if user and cur_user.role_id <= user_toupdate.role_id:
                addnew_user.update_user(user,id)
                return 'User Updated'
            else:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        elif role == 'Admin':
            user_toupdate = db.query(Users).get(id)
            if cur_user.c_id == user_toupdate.c_id:
                if user and cur_user.role_id <= user_toupdate.role_id:
                    if user.role_id in [1,2,3]:
                        addnew_user.update_user(user,id)
                        return 'User Updated'
                    else:
                        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
                else:
                    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
            else:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        elif role == 'Supervisor':
            user_toupdate = db.query(Users).get(id)
            if cur_user.c_id == user_toupdate.c_id:
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
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    else:
        return f'{user.id} is not a SuperVisor'

@router.delete('/user/{id}')
def delete_user(id: int,db: Session = Depends(database.get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        query = 'delete from users where id = {id}'
        db.execute(query)
        db.commit()
        db.close()
        return 'User Deleted'
    elif role in ['Admin','Supervisor']:
        user_todelete = db.query(Users).get(id)
        if user_todelete.c_id == cur_user.c_id:
            query = f'delete from users where id = {id} and c_id = {cur_user.c_id} and role_id != 0 and role_id != 1'
            db.execute(query)
            db.commit()
            db.close()
            return 'User Deleted'
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)