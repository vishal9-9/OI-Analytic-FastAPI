from database.database import database
from database.models import Company
import datetime

db = database

def new_company(company_schema):
    new_company = Company(company_name = company_schema.company_name,country = company_schema.country, state = company_schema.state, city = company_schema.city, pincode = company_schema.pincode, department = company_schema.department, branch = company_schema.branch, address = company_schema.address, created_at = datetime.datetime.now(),isactive = 1)
    database.add(new_company)
    database.commit()
    database.close()

def update_company(company_schema):
    pass