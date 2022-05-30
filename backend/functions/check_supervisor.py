from database.database import database

db = database

def check_supervisor(user_id: int):
    query = f'select role_id from users where id = {user_id}'
    res = db.execute(query).fetchone()
    res = res[0]
    new_query = f'select role_power from role where role_id = {res}'
    out = db.execute(new_query).fetchone()
    if out[0] == 'Supervisor':
        return True
    else:
        return False