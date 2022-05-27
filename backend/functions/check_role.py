from database import database

db = database.database

def check_role(user_role_id: int):
    query = f'select role_power from role where role_id = {user_role_id}'
    res = db.execute(query)
    roles = res.fetchall()
    if roles != []:
        for x in roles:
            return x[0]
    else:
        return 'No User With Such Role'
