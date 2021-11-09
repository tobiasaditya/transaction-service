from fastapi import APIRouter
from model.model_otp import OtpBase
from model.model_response import DefaultResponseContent
from model.model_token import TokenData

from model.model_user import DataUserDb, LoginUser, RegisterUserInput, VerifyUser
from config.config import user_collection, otp_collection
from service.service_email import email
from service.service_jwt_token import create_access_token, get_token_data
from util.util_datetime import datetime_jakarta
from datetime import datetime, timedelta
from bson import ObjectId
import random
import logging
logger = logging.getLogger(__name__)

router_auth = APIRouter()

@router_auth.post("/register",response_model=DefaultResponseContent)
async def register(data_register:RegisterUserInput):
    #Check for duplicate phone
    found_duplicate = await user_collection.find_one({"phoneNumber":data_register.phoneNumber})

    if found_duplicate:
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
    email(data_register.email,otp.otpValue)

    return {
        "request_time":str(datetime_jakarta()),
        "status_code":200,
        "message":"OTP send to email",
        "content":content}
    
@router_auth.post("/verify",response_model=DefaultResponseContent)
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
    
    #If data OTP oke
    data_user = DataUserDb.parse_obj(data_verify)
    data_user.createTime = datetime_jakarta()
    data_user.token = None
    inserted_user = await user_collection.insert_one(data_user.dict())


    data_token = TokenData(userId = str(inserted_user.inserted_id))
    created_token = create_access_token(data_token.dict())

    logger.debug(f"Token | {created_token}")
    logger.debug(f"Try decode | {get_token_data(created_token)}")

    await user_collection.update_one({
        "_id":ObjectId(inserted_user.inserted_id)
        },{
            "$set":{
                "token":created_token
            }
        })
    
    return {
            "request_time":str(datetime_jakarta()),
            "status_code":200,
            "message":"Registration success"
        }

@router_auth.post("/login")
async def login(data_login:LoginUser):
    found_user = await user_collection.find_one({"phoneNumber":data_login.phoneNumber})

    if not found_user:
        return {
            "request_time":str(datetime_jakarta()),
            "status_code":404,
            "message":"User not found"
        }
    
    access_token = found_user['token']

    #Verify token (if expired)
    verify_token = get_token_data()




