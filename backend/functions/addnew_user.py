from database.database import database
from database.models import Users
from functions import passhash
import datetime

db = database

def new_user(user_schema):
    new_user = Users(c_id = user_schema.c_id,fullname = user_schema.fullname,email = user_schema.email,password = passhash.hash(user_schema.password),contact_no = user_schema.conact_no, working_under = user_schema.working_under, dob = user_schema.dob, isactive = 1 , role_id = user_schema.role_id,created_at = datetime.datetime.now())
    db.add(new_user)
    db.commit()
    db.close()

def update_user(user_schema,id: int):
    query = f'UPDATE users SET c_id = {user_schema.c_id}, fullname = "{user_schema.fullname}", email = "{user_schema.email}", contact_no = "{user_schema.contact_no}", working_under = {user_schema.working_under}, dob = "{user_schema.dob}" ,role_id = {user_schema.role_id} where id = {id}'
    res = db.execute(query)
    db.commit()