from datetime import datetime
from pydantic import BaseModel

class RegisterUserInput(BaseModel):
    fullName:str
    email:str
    phoneNumber:str
    password:str

class VerifyUser(RegisterUserInput):
    otpValue:str = None
    otpId:str = None

class DataUserDb(RegisterUserInput):
    token:str = None
    createTime:datetime = None

class LoginUser(BaseModel):
    username:str
    password:str
