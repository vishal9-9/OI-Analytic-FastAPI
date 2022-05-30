from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.schema import show_user
from functions import check_role,list_company_id
from functions.oauth import current_user

router = APIRouter(
    tags = ['Soft Delete Company']
)

@router.get('/soft_del_company/{id}')
def soft_delete_company(id: int,db: Session = Depends(get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        cid_list = list_company_id.list_of_cid()
        if id == 0:
            return 'Cannot Delete This Company'
        else:
            if id in cid_list:
                query = f'UPDATE company SET isactive = 0 where company_id = {id}'
                res = db.execute(query)
                db.commit()
                new_query = f'UPDATE users SET isactive = 0 where c_id = {id}'
                db.execute(new_query)
                db.commit()
                return ('done')
            else:
                return 'No Company with Such User Id'
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)