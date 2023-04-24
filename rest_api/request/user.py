from pydantic import BaseModel

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str or None=None

class User(BaseModel):
    username:str
    email:str or None=None
    full_name:str or None=None
    disabled: bool or None=None

class UserInDb(User):
    hashed_password:str
    