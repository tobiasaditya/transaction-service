from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from model.model_token import TokenData

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "a92f61642b2561b576d066a20d6459d652977d9eaaa9d4b077b3640487b9468f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    #If timedelta not defined, default 15 menit expiry time token
    else:
        expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token_data(token:str):
    try:
        #'exp' automatically recognize by jwt, if error, then raise HTTPException
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("userId")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(userId = user_id)
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token",headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})