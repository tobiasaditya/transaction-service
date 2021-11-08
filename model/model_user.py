from pydantic import BaseModel

class RegisterUserInput(BaseModel):
    fullName:str
    email:str
    phoneNumber:str

class VerifyUser(RegisterUserInput):
    otpValue:str
    otpId:str
