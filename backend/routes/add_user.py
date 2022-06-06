from fastapi import APIRouter, Depends,HTTPException,status
from database.models import Users
from database.database import get_db
from functions import check_role,addnew_user,list_company_id,check_supervisor
from sqlalchemy.orm import Session
from database.database import get_db
from database.schema import add_user_superadmin, show_user
from functions.oauth import current_user,oauth_scheme

router = APIRouter(
    tags = ['Add User']
)

@router.post('/user')
def add_user(user: add_user_superadmin ,db: Session = Depends(get_db),cur_user : show_user =  Depends(current_user)):
    role_id = cur_user.role_id
    role = check_role.check_role(int(role_id))    
    if role == 'Superadmin':
        check = db.query(Users).filter( Users.email == user.email).first()
        if check:
            raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            new_role = user.role_id 
            id_list = list_company_id.list_of_cid()
            if user.c_id in id_list:
                if new_role in [0,1,2,3]:
                    if new_role == 3:
                        check_bool = check_supervisor.check_supervisor(user.working_under)
                        if check_bool:
                            addnew_user.new_user(user)
                            return 'User Added Successfully'
                        else:
                            return f'{user.working_under} is not a Supervisor'
                    elif new_role == 2:
                        check_bool = check_supervisor.check_admin(user.c_id,user.working_under)
                        if check_bool:
                            addnew_user.new_user(user)
                            return 'User Added Successfully'
                        else:
                            return f'{user.working_under} is not a Admin or Admin Does not belong to Same Company'
                    elif new_role == 1:
                        user.working_under = cur_user.id                       
                        addnew_user.new_user(user)
                        return 'User Added Successfully'
                    else:
                        user.working_under = 0
                        user.c_id = 0
                        addnew_user.new_user(user)
                        return 'User Added Successfully'
                else:
                    return 'GIVEN ROLE ID IS INVALID'
            else:
                return 'Company Id Is Invalid'
    elif role == 'Admin':
        check = db.query(Users).filter( Users.email == user.email).first()
        if check:
            raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            new_role = user.role_id
            if new_role in [2,3]:   
                if new_role == 3:
                    check_bool = check_supervisor.check_supervisor(user.working_under)
                    if check_bool:
                        user.c_id = cur_user.c_id
                        addnew_user.new_user(user)
                        return 'User Added Successfully'
                    else:
                        return f'{user.working_under} is not a Supervisor'
                elif new_role == 2:
                    check_bool = check_supervisor.check_admin(user.c_id,user.working_under)
                    if check_bool:
                        user.c_id = cur_user.c_id
                        addnew_user.new_user(user)
                        return 'User Added Successfully'
                    else:
                        return f'{user.working_under} is not a Admin or Admin Does not belong to Same Company'
                elif new_role == 1:
                    user.working_under = 1
                    user.c_id = cur_user.c_id
                    addnew_user.new_user(user)
                    return 'User Added Successfully'
            else:
                return 'GIVEN ROLE ID IS INVALID'
    elif role == 'Supervisor':
        check = db.query(Users).filter( Users.email == user.email).first()
        if check:
            raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            new_role = user.role_id
            if new_role in [3]:
                if new_role == 3:
                    check_bool = check_supervisor.check_supervisor(user.working_under)
                    if check_bool:
                        user.c_id = cur_user.c_id
                        addnew_user.new_user(user)
                        return 'User Added Successfully'
                    else:
                        return f'{user.working_under} is not a Supervisor'
                else:
                    check_bool = check_supervisor.check_admin(user.c_id,user.working_under)
                    if check_bool:
                        user.c_id = cur_user.c_id
                        addnew_user.new_user(user)
                        return 'User Added Successfully'
                    else:
                        return f'{user.working_under} is not Admin or Admin Does not belong to Same Company'
            else:
                return 'GIVEN ROLE ID IS INVALID'
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)