from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from uvicorn import Config, Server
from passlib.context import CryptContext
from jose import JWSError,jwt
from rest_api.request.user import UserInDb,User,TokenData,Token
from datetime import datetime ,timedelta
from config import SECREAT_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

# SECREAT_KEY="secreatekey"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=30

router=APIRouter()
db={
    "gopal":{
        "username":"gopal",
        "full_name":"Gopal Goyal",
        "email":"gopalgoyal612002@gmail.com",
        "hashed_password":"$2b$12$9KfJDo9LHyB4l10psH7EL.GvosyuqcBwW.mFKljACSEVbvgU2W3Eu",
        "disabled":False
    }
}


paw_context=CryptContext(schemes=['bcrypt'],deprecated="auto")
oath_2_scheme=OAuth2PasswordBearer(tokenUrl='token')

def varify_password(plain_password,hashed_password):
    # print(plain_password)
    return paw_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return paw_context.hash(password)

# print(get_password_hash("1234"))

def get_user(db,username:str):
    if(username in db):
        user_data=db[username]
        return UserInDb(**user_data)

def authenticate_user(db,username:str,password):
    # print(username,password)
    user=get_user(db,username)
    if not user:
        return False
    if not varify_password(password,user.hashed_password):
        return False

    return user

# print(authenticate_user(db,"gopal","1234"))

def create_access_token(data:dict,expires_delta:timedelta or None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECREAT_KEY,algorithm=ALGORITHM)
    return encoded_jwt


async def get_curr_user(token : str = Depends(oath_2_scheme)):
    credential_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="counld not validate credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
    try:
        payload= jwt.decode(token,SECREAT_KEY,algorithms=[ALGORITHM])
        username:str= payload.get('sub')
        if username is None:
            raise credential_exception
        token_data=TokenData(username=username)

    except JWSError:
        raise credential_exception
    
    user=get_user(db,username=token_data.username)
    if(user is None):
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: UserInDb = Depends(get_curr_user)):
    # print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive User")
    return current_user


@router.post("/token",response_model=Token)
async def login_from_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    # print(form_data)
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED
                            ,detail="incorrect username and password",
                           headers={"WWW-Authenticate":"Bearer"})
    
    access_token_expire=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username},expires_delta=access_token_expire)
    return {"access_token":access_token,"token_type":"bearer"}