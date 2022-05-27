from werkzeug.security import generate_password_hash,check_password_hash

SECRET_KEY = 'b3a94dceab794d6f6d57f711096c7fbd4083d6fcb44209f7be5458e373d9ce79'

def hash(password: str,SECRET_KEY: str):
    hash_pass = generate_password_hash(password,SECRET_KEY)
    return hash_pass

def chech_hash(hpassword: str, cpassword: str):
    return check_password_hash(hpassword,cpassword)