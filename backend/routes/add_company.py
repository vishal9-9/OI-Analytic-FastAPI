from fastapi import APIRouter, Depends, HTTPException, status
from database.schema import show_user, add_company
from database.database import get_db
from database.models import Company
from functions.oauth import current_user
from sqlalchemy.orm import Session
from functions import check_role,addnew_company
from functions.addnew_company import new_company

router = APIRouter(
    tags = ['Add Company']
)

@router.post('/company')
def addcompany(company: add_company,db: Session = Depends(get_db),cur_user: show_user = Depends(current_user)):
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

@router.put('/company/{id}')
def updatecompany(id: int,company: add_company,db: Session = Depends(get_db),cur_user: show_user = Depends(current_user)):
    role = check_role.check_role(cur_user.role_id)
    do_exist = db.query(Company).get(id)
    if role == 'Superadmin':
        if do_exist:
            query = f'select company_name from company where company_id != {id} and company_id != 0'
            res = db.execute(query).fetchall()
            cname_list = []
            for cname in res:
                cname_list.append(cname[0])
            if company.company_name in cname_list:
                raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                addnew_company.update_company(company,id)
                return 'Company Updated Successfully'
        else:
            return 'No Company with such id'    
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)