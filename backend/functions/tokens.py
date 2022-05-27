from secrets import token_bytes
from jose import jwt

SECRET_KEY = 'b3a94dceab794d6f6d57f711096c7fbd4083d6fcb44209f7be5458e373d9ce79'

def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode,SECRET_KEY)
    return token

def decode_access_token(token: str):
    return jwt.decode(token,SECRET_KEY)