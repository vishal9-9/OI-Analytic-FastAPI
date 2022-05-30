from database.database import database

def list_of_cid():
    companyid = database.execute('select company_id from company').fetchall()
    id_list = []
    for company_id in companyid:
        id_list.append(company_id[0])
    return id_list