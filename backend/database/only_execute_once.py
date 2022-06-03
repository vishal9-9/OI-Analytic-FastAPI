import datetime
from database.database import database
from database.models import Company
from functions.passhash import hash


def initial_setup():
    password = hash('12345678')
    to_execute = database.query(Company).get(0)
    if not to_execute:
        c_query = f"insert into company (company_id, company_name, country, state, city, pincode, department, branch, address, isactive,created_at) values (0, 'SAdmin', 'SAdmin', 'SAdmin', 'SAdmin', '12345', 'SAdmin', 'SAdmin', 'SAdmin',1,'{datetime.datetime.now()}')"
        database.execute(c_query)
        database.commit()
        database.execute(f'update company set company_id = 0 where company_id = 1')
        database.commit()
        database.execute("insert into role (role_id,role_power) values (0,'Superadmin')")
        database.commit()
        database.execute("update role set role_id = 0 where role_id = 1")
        database.commit()
        database.execute("insert into role (role_id,role_power) values (1,'Admin'),(2,'Supervisor'),(3,'User')")
        database.commit()
        query = f"insert into users(c_id,fullname,email,password,contact_no,working_under,dob,isactive,role_id,created_at) values(0,'SuperAdmin','super@admin.com','{password}','1234567890',0,'2017-06-15',1,0,'{datetime.datetime.now()}')"
        database.execute(query)
        database.commit()
    else:
        print('initial setup not done')