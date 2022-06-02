# checks if leaving the parameter user id email no user with same email is in database
from database.database import database

db = database

emai_list = []

def email_check(id: int):
    query = f'select email from users where id != {id}'
    already_exist_email = db.execute(query).fetchall()
    for email in already_exist_email:
        emai_list.append(email[0])
    return emai_list