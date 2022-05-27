from fastapi import APIRouter, Depends,HTTPException,status
from database.models import Users
from database.database import get_db
from functions import check_role,addnew_user
from sqlalchemy.orm import Session
from database.database import get_db
from database.schema import show_user,add_user
from functions.oauth import current_user,oauth_scheme

router = APIRouter(
    tags = ['Add User']
)

@router.post('/user_add')
def add_user(user: add_user ,db: Session = Depends(get_db),cur_user : show_user =  Depends(current_user)):
    print(cur_user.role_id)
    role_id = cur_user.role_id
    role = check_role.check_role(int(role_id))
    if role == 'Superadmin':
        check = db.query(Users).filter( Users.email == user.email).first()
        if check:
            return HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            new_role = user.role_id 
            if new_role in [0,1,2,3]:
                addnew_user.new_user(user)
                return 'User Added Successfully'
            else:
                return 'GIVEN ROLE ID IS INVALID'
    elif role == 'Admin':
        return 'Can Add User Supervisor,User'
    elif role == 'Supervisor':
        return 'Can Add only User'
    else:
        return 'You Can Add No one'