from database.database import database
from database.models import Users
from functions import passhash
import datetime

db = database

def new_user(user):
    new_user = Users(c_id = user.c_id,fullname = user.fullname,email = user.email,password = passhash.hash(user.password),contact_no = user.conact_no, working_under = user.working_under, dob = user.dob, isactive = 1 , role_id = user.role_id,created_at = datetime.datetime.now())
    db.add(new_user)
    db.commit()
    db.close()