from fastapi import APIRouter
from model.model_otp import OtpBase
from model.model_response import DefaultResponseContent

from model.model_user import RegisterUserInput, VerifyUser
from config.config import user_collection, otp_collection
from service.service_email import email
from util.util_datetime import datetime_jakarta
from datetime import datetime, timedelta
from bson import ObjectId
import random
router_auth = APIRouter()

@router_auth.post("/register",response_model=DefaultResponseContent)
async def register(data_register:RegisterUserInput):
    #Check for duplicate phone
    found_duplicate = await user_collection.find_one({"phoneNumber":data_register.phoneNumber})

    if not found_duplicate:
       return {
        "request_time":str(datetime_jakarta()),
        "status_code":400,
        "message":"Phone number has been used"}
    
    #Generate an OTP 6 digit value
    otp = OtpBase()
    otp.otpValue = str(random.randint(100000,999999))
    otp.otpExpired = datetime.now()+timedelta(minutes=2)
    otp.otpReceiver = data_register.email

    inserted_otp = await otp_collection.insert_one(otp.dict())
    content = {
        "otpId":str(inserted_otp.inserted_id)
    }
    email(data_register.email,otp)

    return {
        "request_time":str(datetime_jakarta()),
        "status_code":200,
        "message":"OTP send to email",
        "content":content}
    
@router_auth.post("/verify")
async def verify(data_verify:VerifyUser):
    #Cari OTP
    found_otp = await otp_collection.find_one({
        "_id":ObjectId(data_verify.otpId),
        "otpValue":data_verify.otpValue,
        "otpReceiver":data_verify.email,
        "otpVerifed":False
    })

    if not found_otp:
        return {
            "request_time":str(datetime_jakarta()),
            "status_code":404,
            "message":"OTP invalid"
        }
    
    



