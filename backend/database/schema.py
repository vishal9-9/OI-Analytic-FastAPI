from typing import Optional
from pydantic import BaseModel

class login_user(BaseModel):
    email: str
    password: str

class show_user(BaseModel):
    id : int
    name: str
    email: str
    class Config:
        orm_mode = True