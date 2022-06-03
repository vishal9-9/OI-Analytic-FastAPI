from datetime import date
from typing import List
import re
from pydantic import BaseModel,EmailStr,validator

def validation(v: str):
    pattern = re.compile(r"[A-Za-z ]+$")
    if pattern.match(v):
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
        else:
            return v

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
    def name_validation(cls, v):
        return validation(v)

    @validator('password')
    def p_validation(cls,v):
        if len(v) < 8:
            raise ValueError('Length must atleast be 8 characters')
        else:
            return v

    @validator('contact_no')
    def validation(cls,v1: str):
        patt = re.compile(r'^[0-9]*$')
        if patt.match(v1):
            if len(v1) == 10:
                return v1
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
    def name_validation(cls, v):
        return validation(v)
    
    @validator('contact_no')
    def validation(cls,v1: str):
        patt = re.compile(r'^[0-9]*$')
        if patt.match(v1):
            if len(v1) == 10:
                return v1
            else:
                raise ValueError('Length Of Conatct Number must be 10 digits')
        else:    
            raise ValueError('Must Only Contain alphanumeric character')

class add_company(BaseModel):
    company_name: str
    country: str
    state: str
    city: str
    pincode: str
    department: str
    branch: str
    address: str

    @validator('company_name',allow_reuse = True)
    def validation(cls,v):
        return validation(v)

    @validator('country')
    def c_validation(cls,v1):
        return validation(v1)

    @validator('state')
    def s_validation(cls,v2):
        return validation(v2)
    
    @validator('city')
    def validation(cls,v3):
        return validation(v3)
    
    @validator('pincode')
    def p_validation(cls,v4):
        pattern = re.compile(r'[0-9]')
        if pattern.match(v4):
            return v4
        else:    
            raise ValueError('Must Only Contain Number character')

    @validator('department')
    def d_validation(cls,v5):
        return validation(v5)

    @validator('branch')
    def b_validation(cls,v6):
        return validation(v6)

    @validator('address')
    def a_validation(cls,v7):
        return validation(v7)

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