from fastapi import APIRouter,HTTPException,status,Depends
from database.schema import list_company, show_user
from sqlalchemy.orm import Session
from database.database import get_db
from functions import check_role
from typing import List
from functions.oauth import current_user

router = APIRouter(
    tags = ['List Company']
)

@router.get('/company_list',response_model = List[list_company])
def list_of_company(db: Session = Depends(get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        company_list = db.execute('select * from company').fetchall()
        return company_list
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
