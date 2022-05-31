from datetime import date
import pydantic
import re
from pydantic import BaseModel,EmailStr,validator,ValidationError

class login_user(BaseModel):
    email: EmailStr
    password: str

class show_user(BaseModel):
    fullname: str
    email: EmailStr
    role_id: int
    c_id: int
    working_under: int
    class Config:
        orm_mode = True

    # @validator('fullname')
    # def name_must_contain_space(cls, v):
    #     if ' ' not in v:
    #         raise ValueError('must contain a space')
    #     return v


class add_user_superadmin(BaseModel):
    c_id: int
    fullname: str
    email: EmailStr
    password: str
    role_id: int
    contact_no : str
    working_under: int
    dob: date
    class Config:
        orm_mode = True

class update_user(BaseModel):
    c_id: int
    fullname: str
    email: EmailStr
    role_id: int
    contact_no : str
    working_under: int
    dob: date

class add_company(BaseModel):
    company_name: str
    country: str
    state: str
    city: str
    pincode: str
    department: str
    branch: str
    address: str

    @validator('company_name')
    def name_validation(cls,v):
        pattern = '[ a-zA-Z0-9]'
        match = re.match(pattern,v)
        print(match)
        if match is None:
            raise ValueError('Must Only Contain alphanumeric character')
        else:
            return v

class list_company(add_company,BaseModel):
    company_id: int
    class Config:
        orm_mode = True
