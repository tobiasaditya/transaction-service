from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from service.service_jwt_token import get_token_data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(created_token = Depends(oauth2_scheme)):
    user = get_token_data(created_token)
    return user