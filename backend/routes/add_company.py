from fastapi import APIRouter, Depends, HTTPException, status
from database.schema import add_company, show_user
from database.database import get_db
from database.models import Company
from functions.oauth import current_user
from sqlalchemy.orm import Session
from functions import check_role
from functions.addnew_company import new_company

router = APIRouter(
    tags = ['Add Company']
)

@router.post('/company_add')
def add_company(company: add_company,db: Session = Depends(get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    if role == 'Superadmin':
        check = db.query(Company).filter(Company.company_name == company.company_name).first()
        if check:
            raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            new_company(company)
            return '{Success : Added Company}'
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)