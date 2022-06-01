from datetime import date
from typing import List
import re
from pydantic import BaseModel,EmailStr,validator

def validation(v):
    pattern = re.compile(r'[A-Za-z ]+$')
    if pattern.match(v):
        print(pattern.match(v))
        return v
    else:    
        raise ValueError('Must Only Contain alphanumeric character')

class login_user(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def p_validation(cls,v):
        if len(v) < 8:
            raise ValueError('Length must atleast be 8 characters')

class show_user(BaseModel):
    fullname: str 
    email: EmailStr
    role_id: int
    c_id: int
    working_under: int
    class Config:
        orm_mode = True

    @validator('fullname')
    def f_validation(cls, v):
        validation(v)

class list_user(BaseModel):
    fullname: str 
    email: EmailStr
    role_id: int
    c_id: int
    working_under: int
    class Config:
        orm_mode = True


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
    
    @validator('fullname')
    def name_must_contain_space(cls, v):
        validation(v)

    @validator('contact_no')
    def con_validation(cls,v):
        pattern = re.compile(r'[0-9]')
        if pattern.match(v):
            if len(v) == 10:
                return v
            else:
                raise ValueError('Length Of Conatct Number must be 10 digits')
        else:    
            raise ValueError('Must Only Contain alphanumeric character')

class update_user(BaseModel):
    c_id: int
    fullname: str
    email: EmailStr
    role_id: int
    contact_no : str
    working_under: int
    dob: date

    @validator('fullname')
    def name_must_contain_space(cls, v):
        validation(v)

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
    def cn_validation(cls,v):
        validation(v)

    @validator('country')
    def c_validation(cls,v):
        validation(v)

    @validator('state')
    def s_validation(cls,v):
        validation(v)
    
    @validator('city')
    def validation(cls,v):
        validation(v)
    
    @validator('pincode')
    def p_validation(cls,v):
        pattern = re.compile(r'[0-9]')
        if pattern.match(v):
            return v
        else:    
            raise ValueError('Must Only Contain Number character')

    @validator('department')
    def d_validation(cls,v):
        validation(v)

    @validator('branch')
    def b_validation(cls,v):
        validation(v)

    @validator('address')
    def a_validation(cls,v):
        validation(v)

class list_company(BaseModel):
    company_id: int
    company_name: str
    country: str
    state: str
    city: str
    pincode: str
    department: str
    branch: str
    address: str
    class Config:
        orm_mode = True

class reset_pass(BaseModel):
    email: List[EmailStr]